#include "device_api_client.h"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <inttypes.h>
#include <new>
#include <string>

#include <cJSON.h>
#include <esp_app_format.h>
#include <esp_http_client.h>
#include <esp_log.h>
#include <esp_ota_ops.h>
#include <esp_timer.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#define TAG "SelfDeviceApi"

namespace {
constexpr int kHeartbeatHttpTimeoutMs = 10000;
constexpr int kConfigInitialDelayMs = 3000;
constexpr int kHeartbeatAfterConfigDelayMs = 7000;
constexpr size_t kConversationQueueDepth = 16;
constexpr char kConversationContentSource[] = "xiaozhi_official_device_log";
constexpr char kConversationSessionSource[] = "xiaozhi_official";
constexpr char kDeviceTimezoneOffset[] = "+08:00";
constexpr double kEarthRadiusMeters = 6371000.0;
constexpr double kPi = 3.14159265358979323846;

esp_err_t CollectResponseData(esp_http_client_event_t* event) {
    if (event->event_id == HTTP_EVENT_ON_DATA && event->user_data != nullptr && event->data_len > 0) {
        auto* response = static_cast<std::string*>(event->user_data);
        response->append(static_cast<const char*>(event->data), event->data_len);
    }
    return ESP_OK;
}

bool IsSuccessfulResponse(const cJSON* root) {
    const cJSON* success = cJSON_GetObjectItem(root, "success");
    return cJSON_IsTrue(success);
}

const char* JsonStringOr(const cJSON* object, const char* name, const char* fallback) {
    const cJSON* item = cJSON_GetObjectItem(object, name);
    return cJSON_IsString(item) ? item->valuestring : fallback;
}

uint32_t Fnv1a(const std::string& value) {
    uint32_t hash = 2166136261u;
    for (const unsigned char byte : value) {
        hash ^= byte;
        hash *= 16777619u;
    }
    return hash;
}

double DegreesToRadians(double degrees) {
    return degrees * kPi / 180.0;
}

double DistanceMeters(double lat1, double lon1, double lat2, double lon2) {
    const double dlat = DegreesToRadians(lat2 - lat1);
    const double dlon = DegreesToRadians(lon2 - lon1);
    const double a = std::sin(dlat / 2) * std::sin(dlat / 2) +
        std::cos(DegreesToRadians(lat1)) * std::cos(DegreesToRadians(lat2)) *
        std::sin(dlon / 2) * std::sin(dlon / 2);
    return kEarthRadiusMeters * 2 * std::atan2(std::sqrt(a), std::sqrt(1 - a));
}

std::string SerializeJson(cJSON* object) {
    char* serialized = cJSON_PrintUnformatted(object);
    if (serialized == nullptr) {
        return {};
    }
    std::string result(serialized);
    cJSON_free(serialized);
    return result;
}

std::string FormatConversationCreatedAt() {
    const std::time_t now = std::time(nullptr);
    if (now < 1704067200) {
        return {};
    }
    // Xiaozhi OTA currently applies the server timezone offset before calling
    // settimeofday(), so gmtime_r() yields the device's configured local time.
    // This Phase-1 deployment is fixed to Asia/Shanghai (+08:00).
    std::tm device_local = {};
    gmtime_r(&now, &device_local);
    char local_time[24] = {};
    if (std::strftime(
            local_time, sizeof(local_time), "%Y-%m-%dT%H:%M:%S",
            &device_local) == 0) {
        return {};
    }
    return std::string(local_time) + kDeviceTimezoneOffset;
}
}

DeviceApiClient& DeviceApiClient::GetInstance() {
    static DeviceApiClient instance;
    return instance;
}

DeviceApiClient::~DeviceApiClient() {
    Stop();
}

void DeviceApiClient::Start() {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (CONFIG_BLINDBOX_DEVICE_API_URL[0] == '\0' || CONFIG_BLINDBOX_DEVICE_API_TOKEN[0] == '\0') {
        ESP_LOGE(TAG, "Device API enabled but URL or token is empty");
        return;
    }

    started_.store(true);
    configuration_loaded_.store(false);
    if (heartbeat_task_handle_ == nullptr &&
        xTaskCreate(HeartbeatLoopTask, "device_heartbeat", 6144, this, 3,
            &heartbeat_task_handle_) != pdPASS) {
        heartbeat_task_handle_ = nullptr;
        started_.store(false);
        ESP_LOGE(TAG, "Failed to create heartbeat loop task");
        return;
    }
    EnsureConversationWorker();
    ESP_LOGI(TAG, "Device API enabled: device=%s heartbeat_interval=%ds; config fetch scheduled",
        CONFIG_BLINDBOX_DEVICE_ID, CONFIG_BLINDBOX_HEARTBEAT_INTERVAL_SECONDS);
#endif
}

void DeviceApiClient::Stop() {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    started_.store(false);
    configuration_loaded_.store(false);
#endif
}

void DeviceApiClient::HeartbeatLoopTask(void* arg) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    auto* self = static_cast<DeviceApiClient*>(arg);
    const TickType_t interval = pdMS_TO_TICKS(
        CONFIG_BLINDBOX_HEARTBEAT_INTERVAL_SECONDS * 1000);
    vTaskDelay(pdMS_TO_TICKS(kConfigInitialDelayMs));
    while (true) {
        if (self->started_.load()) {
            if (!self->configuration_loaded_.load()) {
                self->FetchDeviceConfig();
                vTaskDelay(pdMS_TO_TICKS(kHeartbeatAfterConfigDelayMs));
            }
            ESP_LOGI(TAG, "Sending heartbeat");
            self->SendHeartbeat();
        }
        vTaskDelay(interval);
    }
#endif
}

void DeviceApiClient::EnsureConversationWorker() {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (conversation_queue_ == nullptr) {
        conversation_queue_ = xQueueCreate(
            kConversationQueueDepth, sizeof(ConversationPost*));
        if (conversation_queue_ == nullptr) {
            ESP_LOGE(TAG,
                "Conversation event queue unavailable; serial evidence remains enabled");
            return;
        }
    }
    if (conversation_task_handle_ == nullptr &&
        xTaskCreate(ConversationLoopTask, "device_conversation", 6144, this, 3,
            &conversation_task_handle_) != pdPASS) {
        conversation_task_handle_ = nullptr;
        ESP_LOGE(TAG,
            "Conversation event worker unavailable; serial evidence remains enabled");
    }
#endif
}

void DeviceApiClient::ConversationLoopTask(void* arg) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    auto* self = static_cast<DeviceApiClient*>(arg);
    while (true) {
        ConversationPost* event = nullptr;
        if (xQueueReceive(
                self->conversation_queue_, &event, portMAX_DELAY) != pdTRUE ||
            event == nullptr) {
            continue;
        }
        if (!self->started_.load()) {
            ESP_LOGW(TAG,
                "Conversation event skipped while device API is offline: "
                "session=%s role=%s; serial evidence retained",
                event->session_id.c_str(), event->role.c_str());
        } else if (!self->PostJson(
                       self->GetSiblingApiUrl("/device-conversation-events"),
                       event->body, "Conversation event")) {
            ESP_LOGW(TAG,
                "Conversation event post failed: session=%s role=%s; "
                "serial evidence retained",
                event->session_id.c_str(), event->role.c_str());
        }
        delete event;
    }
#endif
}

void DeviceApiClient::EnqueueConversationEvent(
    const std::string& body, const std::string& session_id, const std::string& role) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (conversation_queue_ == nullptr) {
        ESP_LOGW(TAG,
            "Conversation event queue unavailable: session=%s role=%s; "
            "serial evidence retained",
            session_id.c_str(), role.c_str());
        return;
    }
    auto* event = new (std::nothrow) ConversationPost{body, session_id, role};
    if (event == nullptr) {
        ESP_LOGW(TAG,
            "Conversation event allocation failed: session=%s role=%s; "
            "serial evidence retained",
            session_id.c_str(), role.c_str());
        return;
    }
    if (xQueueSend(conversation_queue_, &event, 0) != pdTRUE) {
        ESP_LOGW(TAG,
            "Conversation event queue full: session=%s role=%s; "
            "serial evidence retained",
            session_id.c_str(), role.c_str());
        delete event;
    }
#endif
}

std::string DeviceApiClient::GetDeviceConfigUrl() const {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
#ifdef CONFIG_BLINDBOX_DEVICE_CONFIG_URL
    if (CONFIG_BLINDBOX_DEVICE_CONFIG_URL[0] != '\0') {
        return CONFIG_BLINDBOX_DEVICE_CONFIG_URL;
    }
#endif
    std::string url = CONFIG_BLINDBOX_DEVICE_API_URL;
    const std::string heartbeat_path = "/device-heartbeats";
    const size_t position = url.rfind(heartbeat_path);
    if (position == std::string::npos) {
        return {};
    }
    url.replace(position, heartbeat_path.size(), "/device-config?device_id=");
    url += CONFIG_BLINDBOX_DEVICE_ID;
    return url;
#else
    return {};
#endif
}

void DeviceApiClient::FetchDeviceConfig() {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    const std::string url = GetDeviceConfigUrl();
    if (url.empty()) {
        ESP_LOGE(TAG, "Cannot derive device-config URL from heartbeat URL");
        return;
    }

    std::string response;
    esp_http_client_config_t config = {};
    config.url = url.c_str();
    config.timeout_ms = kHeartbeatHttpTimeoutMs;
    config.event_handler = CollectResponseData;
    config.user_data = &response;
    esp_http_client_handle_t http = esp_http_client_init(&config);
    if (http == nullptr) {
        ESP_LOGE(TAG, "Device config client initialization failed");
        return;
    }
    esp_http_client_set_method(http, HTTP_METHOD_GET);
    esp_http_client_set_header(http, "X-Device-Id", CONFIG_BLINDBOX_DEVICE_ID);
    esp_http_client_set_header(http, "X-Device-Token", CONFIG_BLINDBOX_DEVICE_API_TOKEN);
    const esp_err_t error = esp_http_client_perform(http);
    const int status = esp_http_client_get_status_code(http);
    esp_http_client_cleanup(http);
    if (error != ESP_OK) {
        ESP_LOGW(TAG, "Device config request failed: %s", esp_err_to_name(error));
        return;
    }
    if (status < 200 || status >= 300) {
        ESP_LOGW(TAG, "Device config rejected: HTTP %d", status);
        return;
    }

    cJSON* root = cJSON_ParseWithLength(response.data(), response.size());
    const cJSON* data = root == nullptr ? nullptr : cJSON_GetObjectItem(root, "data");
    const cJSON* agent = cJSON_IsObject(data) ? cJSON_GetObjectItem(data, "agent") : nullptr;
    const cJSON* spots = cJSON_IsObject(data) ? cJSON_GetObjectItem(data, "spots") : nullptr;
    const cJSON* tags = cJSON_IsObject(data) ? cJSON_GetObjectItem(data, "nfc_tags") : nullptr;
    if (root == nullptr || !IsSuccessfulResponse(root) || !cJSON_IsObject(agent) ||
        !cJSON_IsArray(spots) || !cJSON_IsArray(tags)) {
        ESP_LOGW(TAG, "Device config response schema invalid: HTTP %d", status);
        cJSON_Delete(root);
        return;
    }

    std::vector<SpotConfig> new_spots;
    cJSON* spot = nullptr;
    cJSON_ArrayForEach(spot, spots) {
        const cJSON* spot_id = cJSON_GetObjectItem(spot, "spot_id");
        const cJSON* latitude = cJSON_GetObjectItem(spot, "latitude");
        const cJSON* longitude = cJSON_GetObjectItem(spot, "longitude");
        const cJSON* radius = cJSON_GetObjectItem(spot, "gps_radius_meters");
        if (cJSON_IsString(spot_id) && cJSON_IsNumber(latitude) &&
            cJSON_IsNumber(longitude) && cJSON_IsNumber(radius)) {
            new_spots.push_back({
                spot_id->valuestring, latitude->valuedouble,
                longitude->valuedouble, radius->valuedouble});
        }
    }
    std::vector<TagConfig> new_tags;
    cJSON* tag = nullptr;
    cJSON_ArrayForEach(tag, tags) {
        const cJSON* tag_id = cJSON_GetObjectItem(tag, "tag_id");
        const cJSON* spot_id = cJSON_GetObjectItem(tag, "spot_id");
        if (cJSON_IsString(tag_id) && cJSON_IsString(spot_id)) {
            new_tags.push_back({tag_id->valuestring, spot_id->valuestring});
        }
    }
    {
        std::lock_guard<std::mutex> lock(state_mutex_);
        spots_ = std::move(new_spots);
        tags_ = std::move(new_tags);
    }
    const uint32_t payload_hash = Fnv1a(response);
    ESP_LOGI(TAG,
        "Device config accepted: device=%s agent=%s version=%s payload_hash=%08" PRIx32
        " spots=%d nfc_tags=%d dataset=%s",
        CONFIG_BLINDBOX_DEVICE_ID,
        JsonStringOr(agent, "agent_id", "unknown"),
        JsonStringOr(agent, "prompt_version", "unavailable"),
        payload_hash,
        cJSON_GetArraySize(spots),
        cJSON_GetArraySize(tags),
        JsonStringOr(agent, "dataset_id", "none"));
    configuration_loaded_.store(true);
    cJSON_Delete(root);
#endif
}

void DeviceApiClient::SendHeartbeat() {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    const auto* app_desc = esp_app_get_description();
    const char* gps_status = "not_connected";
    {
        std::lock_guard<std::mutex> lock(state_mutex_);
        if (has_gps_reading_) {
            gps_status = latest_gps_.fix ? "fixed" : "no_fix";
        }
    }
    std::string body = std::string("{\"device_id\":\"") + CONFIG_BLINDBOX_DEVICE_ID +
        "\",\"firmware_version\":\"blindbox-" + app_desc->version +
        "\",\"gps_status\":\"" + gps_status + "\"}";

    esp_http_client_config_t config = {};
    config.url = CONFIG_BLINDBOX_DEVICE_API_URL;
    config.timeout_ms = kHeartbeatHttpTimeoutMs;
    esp_http_client_handle_t http = esp_http_client_init(&config);
    if (http == nullptr) {
        ESP_LOGE(TAG, "Heartbeat client initialization failed");
        return;
    }

    esp_http_client_set_method(http, HTTP_METHOD_POST);
    esp_http_client_set_header(http, "Content-Type", "application/json");
    esp_http_client_set_header(http, "X-Device-Id", CONFIG_BLINDBOX_DEVICE_ID);
    esp_http_client_set_header(http, "X-Device-Token", CONFIG_BLINDBOX_DEVICE_API_TOKEN);
    esp_http_client_set_post_field(http, body.data(), body.size());

    const esp_err_t error = esp_http_client_perform(http);
    const int status = esp_http_client_get_status_code(http);
    esp_http_client_cleanup(http);
    if (error != ESP_OK) {
        ESP_LOGW(TAG, "Heartbeat request failed: %s", esp_err_to_name(error));
        return;
    }
    if (status >= 200 && status < 300) {
        ESP_LOGI(TAG, "Heartbeat accepted: HTTP %d", status);
    } else {
        ESP_LOGW(TAG, "Heartbeat rejected: HTTP %d", status);
    }
#endif
}

std::string DeviceApiClient::GetSiblingApiUrl(const char* endpoint) const {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (endpoint == nullptr || endpoint[0] == '\0') {
        return {};
    }
    std::string url = CONFIG_BLINDBOX_DEVICE_API_URL;
    const std::string heartbeat_path = "/device-heartbeats";
    const size_t position = url.rfind(heartbeat_path);
    if (position == std::string::npos) {
        return {};
    }
    url.replace(position, heartbeat_path.size(), endpoint);
    return url;
#else
    return {};
#endif
}

bool DeviceApiClient::PostJson(
    const std::string& url, const std::string& body, const char* operation) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (url.empty()) {
        ESP_LOGE(TAG, "%s URL cannot be derived from heartbeat URL", operation);
        return false;
    }
    std::string response;
    esp_http_client_config_t config = {};
    config.url = url.c_str();
    config.timeout_ms = kHeartbeatHttpTimeoutMs;
    config.event_handler = CollectResponseData;
    config.user_data = &response;
    esp_http_client_handle_t http = esp_http_client_init(&config);
    if (http == nullptr) {
        ESP_LOGE(TAG, "%s client initialization failed", operation);
        return false;
    }
    esp_http_client_set_method(http, HTTP_METHOD_POST);
    esp_http_client_set_header(http, "Content-Type", "application/json");
    esp_http_client_set_header(http, "X-Device-Id", CONFIG_BLINDBOX_DEVICE_ID);
    esp_http_client_set_header(http, "X-Device-Token", CONFIG_BLINDBOX_DEVICE_API_TOKEN);
    esp_http_client_set_post_field(http, body.data(), body.size());
    const esp_err_t error = esp_http_client_perform(http);
    const int status = esp_http_client_get_status_code(http);
    esp_http_client_cleanup(http);
    if (error != ESP_OK) {
        ESP_LOGW(TAG, "%s request failed: %s", operation, esp_err_to_name(error));
        return false;
    }
    if (status < 200 || status >= 300) {
        ESP_LOGW(TAG, "%s rejected: HTTP %d", operation, status);
        return false;
    }
    cJSON* root = cJSON_ParseWithLength(response.data(), response.size());
    const bool success = root != nullptr && IsSuccessfulResponse(root);
    cJSON_Delete(root);
    if (!success) {
        ESP_LOGW(TAG, "%s response schema invalid: HTTP %d", operation, status);
        return false;
    }
    ESP_LOGI(TAG, "%s accepted: HTTP %d", operation, status);
    return true;
#else
    return false;
#endif
}

void DeviceApiClient::ReportGps(const GpsReading& reading) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    SpotConfig spot;
    {
        std::lock_guard<std::mutex> lock(state_mutex_);
        latest_gps_ = reading;
        has_gps_reading_ = true;
        if (spots_.empty()) {
            ESP_LOGW(TAG, "GPS report deferred: device config has no spot");
            return;
        }
        spot = spots_.front();
    }

    const double distance = reading.fix
        ? DistanceMeters(reading.latitude, reading.longitude, spot.latitude, spot.longitude)
        : 0;
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "device_id", CONFIG_BLINDBOX_DEVICE_ID);
    cJSON_AddStringToObject(root, "spot_id", spot.spot_id.c_str());
    cJSON_AddStringToObject(
        root, "event_type",
        reading.fix && distance <= spot.radius_meters ? "near_spot" : "position_update");
    if (reading.fix) {
        cJSON_AddNumberToObject(root, "latitude", reading.latitude);
        cJSON_AddNumberToObject(root, "longitude", reading.longitude);
        cJSON_AddNumberToObject(root, "distance_meters", distance);
    } else {
        cJSON_AddNullToObject(root, "latitude");
        cJSON_AddNullToObject(root, "longitude");
    }
    cJSON* quality = cJSON_AddObjectToObject(root, "location_quality");
    cJSON_AddBoolToObject(quality, "fix", reading.fix);
    cJSON_AddNumberToObject(quality, "satellites", reading.satellites);
    cJSON_AddNumberToObject(quality, "hdop", reading.hdop);
    // Xiaozhi's OTA path stores server time after applying the local timezone
    // offset. It is therefore not a true UTC epoch. Omit event_time and let the
    // platform use its authenticated receive time instead of creating a future
    // location record.
    const std::string body = SerializeJson(root);
    cJSON_Delete(root);
    if (!body.empty() && PostJson(GetSiblingApiUrl("/location-events"), body, "GPS location")) {
        ESP_LOGI(TAG, "GPS summary: fix=%s satellites=%d hdop=%.1f",
            reading.fix ? "true" : "false", reading.satellites, reading.hdop);
    }
#endif
}

void DeviceApiClient::ReportNfcTag(const std::string& tag_id) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    TagConfig tag;
    GpsReading gps;
    bool has_gps = false;
    {
        std::lock_guard<std::mutex> lock(state_mutex_);
        const auto found = std::find_if(tags_.begin(), tags_.end(),
            [&tag_id](const TagConfig& item) { return item.tag_id == tag_id; });
        if (found == tags_.end()) {
            ESP_LOGW(TAG, "NFC tag not present in device config: tag_id=%s", tag_id.c_str());
            return;
        }
        tag = *found;
        gps = latest_gps_;
        has_gps = has_gps_reading_;
    }
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "device_id", CONFIG_BLINDBOX_DEVICE_ID);
    cJSON_AddStringToObject(root, "spot_id", tag.spot_id.c_str());
    cJSON_AddStringToObject(root, "tag_id", tag.tag_id.c_str());
    cJSON_AddStringToObject(root, "method", "gps_nearby_nfc_confirmed");
    cJSON_AddStringToObject(root, "source", "device");
    cJSON* quality = cJSON_AddObjectToObject(root, "location_quality");
    cJSON_AddBoolToObject(quality, "fix", has_gps && gps.fix);
    cJSON_AddNumberToObject(quality, "satellites", has_gps ? gps.satellites : 0);
    cJSON_AddNumberToObject(quality, "hdop", has_gps ? gps.hdop : 0);
    // See ReportGps(): the platform receive time is the authoritative check-in
    // time until the upstream clock is changed to a true UTC epoch.
    const std::string body = SerializeJson(root);
    cJSON_Delete(root);
    if (!body.empty()) {
        PostJson(GetSiblingApiUrl("/checkins"), body, "NFC checkin");
    }
#endif
}

void DeviceApiClient::LogConversationEvidence(
    const char* session_id, const char* role, const char* content) {
#if CONFIG_BLINDBOX_DEVICE_API_ENABLED
    if (role == nullptr || content == nullptr || content[0] == '\0') {
        return;
    }
    const std::string official_session_id =
        session_id != nullptr && session_id[0] != '\0' ? session_id : "unavailable";
    const std::string created_at = FormatConversationCreatedAt();

    cJSON* evidence = cJSON_CreateObject();
    cJSON_AddStringToObject(evidence, "event_type", "conversation_message_import");
    cJSON_AddStringToObject(evidence, "device_id", CONFIG_BLINDBOX_DEVICE_ID);
    cJSON_AddStringToObject(
        evidence, "official_session_id", official_session_id.c_str());
    cJSON_AddStringToObject(evidence, "role", role);
    cJSON_AddStringToObject(evidence, "content", content);
    cJSON_AddStringToObject(evidence, "content_source", kConversationContentSource);
    cJSON_AddStringToObject(evidence, "session_source", kConversationSessionSource);
    cJSON_AddBoolToObject(evidence, "hardware_verified", true);
    cJSON_AddNumberToObject(evidence, "uptime_ms", esp_timer_get_time() / 1000);
    if (!created_at.empty()) {
        cJSON_AddStringToObject(evidence, "created_at", created_at.c_str());
    } else {
        cJSON_AddStringToObject(evidence, "created_at", "unavailable");
    }
    const std::string serialized_evidence = SerializeJson(evidence);
    cJSON_Delete(evidence);
    if (!serialized_evidence.empty()) {
        ESP_LOGI(TAG, "CONVERSATION_EVIDENCE %s", serialized_evidence.c_str());
    }

    if (created_at.empty()) {
        ESP_LOGW(TAG,
            "Conversation event not queued because device time is unavailable: "
            "session=%s role=%s; serial evidence retained",
            official_session_id.c_str(), role);
        return;
    }
    cJSON* request = cJSON_CreateObject();
    cJSON_AddStringToObject(
        request, "official_session_id", official_session_id.c_str());
    cJSON_AddStringToObject(request, "role", role);
    cJSON_AddStringToObject(request, "content", content);
    cJSON_AddStringToObject(request, "content_source", kConversationContentSource);
    cJSON_AddStringToObject(request, "session_source", kConversationSessionSource);
    cJSON_AddStringToObject(request, "created_at", created_at.c_str());
    const std::string request_body = SerializeJson(request);
    cJSON_Delete(request);
    if (request_body.empty()) {
        ESP_LOGW(TAG,
            "Conversation event serialization failed: session=%s role=%s; "
            "serial evidence retained",
            official_session_id.c_str(), role);
        return;
    }
    EnqueueConversationEvent(
        request_body, official_session_id, role);
#endif
}
