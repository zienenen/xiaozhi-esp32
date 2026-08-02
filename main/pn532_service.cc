#include "pn532_service.h"

#include "device_api_client.h"

#include <cstdio>
#include <string>
#include <vector>

#include <driver/i2c.h>
#include <esp_log.h>

#define TAG "BlindboxPn532"

namespace {
constexpr uint8_t kAddress = 0x24;
constexpr uint8_t kHostToPn532 = 0xD4;
constexpr uint8_t kPn532ToHost = 0xD5;

std::vector<uint8_t> BuildFrame(uint8_t command, const std::vector<uint8_t>& data) {
    const uint8_t length = static_cast<uint8_t>(data.size() + 2);
    uint8_t checksum = static_cast<uint8_t>(kHostToPn532 + command);
    std::vector<uint8_t> frame = {
        0x00, 0x00, 0xFF, length, static_cast<uint8_t>(0 - length),
        kHostToPn532, command};
    for (const uint8_t value : data) {
        frame.push_back(value);
        checksum = static_cast<uint8_t>(checksum + value);
    }
    frame.push_back(static_cast<uint8_t>(0 - checksum));
    frame.push_back(0x00);
    return frame;
}

bool ReadResponse(i2c_port_t port, uint8_t command, std::vector<uint8_t>& payload) {
    uint8_t buffer[64] = {};
    for (int attempt = 0; attempt < 40; ++attempt) {
        vTaskDelay(pdMS_TO_TICKS(25));
        if (i2c_master_read_from_device(
                port, kAddress, buffer, sizeof(buffer), pdMS_TO_TICKS(500)) != ESP_OK ||
            buffer[0] != 0x01) {
            continue;
        }
        size_t offset = 1;
        while (offset + 7 < sizeof(buffer) &&
               !(buffer[offset] == 0x00 && buffer[offset + 1] == 0x00 &&
                 buffer[offset + 2] == 0xFF)) {
            ++offset;
        }
        if (offset + 6 >= sizeof(buffer)) return false;
        const uint8_t length = buffer[offset + 3];
        if (length == 0 && buffer[offset + 4] == 0xFF) {
            continue;  // ACK frame; the command response follows.
        }
        if (length < 2 || offset + 5 + length >= sizeof(buffer) ||
            static_cast<uint8_t>(length + buffer[offset + 4]) != 0 ||
            buffer[offset + 5] != kPn532ToHost ||
            buffer[offset + 6] != static_cast<uint8_t>(command + 1)) {
            return false;
        }
        uint8_t checksum = 0;
        for (size_t index = offset + 5; index < offset + 5 + length; ++index) {
            checksum = static_cast<uint8_t>(checksum + buffer[index]);
        }
        if (static_cast<uint8_t>(checksum + buffer[offset + 5 + length]) != 0) {
            return false;
        }
        payload.assign(buffer + offset + 7, buffer + offset + 5 + length);
        return true;
    }
    return false;
}

bool Execute(
    i2c_port_t port, uint8_t command, const std::vector<uint8_t>& data,
    std::vector<uint8_t>& response) {
    const std::vector<uint8_t> frame = BuildFrame(command, data);
    return i2c_master_write_to_device(
               port, kAddress, frame.data(), frame.size(), pdMS_TO_TICKS(500)) == ESP_OK &&
        ReadResponse(port, command, response);
}

std::string FormatUid(const uint8_t* uid, size_t length) {
    std::string result;
    result.reserve(length * 2);
    char byte[3] = {};
    for (size_t index = 0; index < length; ++index) {
        std::snprintf(byte, sizeof(byte), "%02X", uid[index]);
        result += byte;
    }
    return result;
}
}

Pn532Service& Pn532Service::GetInstance() {
    static Pn532Service instance;
    return instance;
}

Pn532Service::~Pn532Service() {
    Stop();
}

void Pn532Service::Start() {
#if CONFIG_BLINDBOX_PN532_ENABLED
    if (CONFIG_BLINDBOX_PN532_SDA_GPIO == 18 || CONFIG_BLINDBOX_PN532_SCL_GPIO == 18) {
        ESP_LOGE(TAG, "PN532 disabled: GPIO18 conflicts with LAMP_GPIO");
        return;
    }
    bool expected = false;
    if (!started_.compare_exchange_strong(expected, true)) return;
    if (xTaskCreate(TaskEntry, "blindbox_pn532", 4096, this, 2, &task_handle_) != pdPASS) {
        task_handle_ = nullptr;
        started_.store(false);
        ESP_LOGE(TAG, "Failed to create PN532 task");
    }
#endif
}

void Pn532Service::Stop() {
#if CONFIG_BLINDBOX_PN532_ENABLED
    started_.store(false);
#endif
}

void Pn532Service::TaskEntry(void* arg) {
#if CONFIG_BLINDBOX_PN532_ENABLED
    static_cast<Pn532Service*>(arg)->Run();
#endif
    vTaskDelete(nullptr);
}

void Pn532Service::Run() {
#if CONFIG_BLINDBOX_PN532_ENABLED
    const i2c_port_t port = static_cast<i2c_port_t>(CONFIG_BLINDBOX_PN532_I2C_PORT);
    const i2c_config_t config = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = static_cast<gpio_num_t>(CONFIG_BLINDBOX_PN532_SDA_GPIO),
        .scl_io_num = static_cast<gpio_num_t>(CONFIG_BLINDBOX_PN532_SCL_GPIO),
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master = {.clk_speed = CONFIG_BLINDBOX_PN532_I2C_FREQUENCY},
        .clk_flags = 0,
    };
    esp_err_t error = i2c_param_config(port, &config);
    if (error == ESP_OK) error = i2c_driver_install(port, I2C_MODE_MASTER, 0, 0, 0);
    if (error != ESP_OK) {
        ESP_LOGE(TAG, "PN532 I2C initialization failed: %s", esp_err_to_name(error));
        started_.store(false);
        task_handle_ = nullptr;
        return;
    }
    ESP_LOGI(TAG, "PN532 I2C ready: port=%d sda=%d scl=%d",
        CONFIG_BLINDBOX_PN532_I2C_PORT, CONFIG_BLINDBOX_PN532_SDA_GPIO,
        CONFIG_BLINDBOX_PN532_SCL_GPIO);

    std::vector<uint8_t> response;
    if (!Execute(port, 0x02, {}, response) || response.size() < 4) {
        ESP_LOGE(TAG, "PN532 firmware query failed; verify I2C mode, 3.3V and wiring");
        i2c_driver_delete(port);
        started_.store(false);
        task_handle_ = nullptr;
        return;
    }
    ESP_LOGI(TAG, "PN532 detected: IC=0x%02X firmware=%u.%u support=0x%02X",
        response[0], response[1], response[2], response[3]);
    response.clear();
    if (!Execute(port, 0x14, {0x01, 0x14, 0x01}, response)) {
        ESP_LOGE(TAG, "PN532 SAMConfiguration failed");
        i2c_driver_delete(port);
        started_.store(false);
        task_handle_ = nullptr;
        return;
    }

    std::string last_uid;
    TickType_t last_seen = 0;
    while (started_.load()) {
        response.clear();
        if (Execute(port, 0x4A, {0x01, 0x00}, response) &&
            response.size() >= 7 && response[0] > 0) {
            const size_t uid_length = response[5];
            if ((uid_length == 4 || uid_length == 7 || uid_length == 10) &&
                response.size() >= 6 + uid_length) {
                const std::string uid = FormatUid(response.data() + 6, uid_length);
                const TickType_t now = xTaskGetTickCount();
                if (uid != last_uid || now - last_seen >= pdMS_TO_TICKS(5000)) {
                    ESP_LOGI(TAG, "PN532 UID: %s", uid.c_str());
                    DeviceApiClient::GetInstance().ReportNfcTag(uid);
                    last_uid = uid;
                    last_seen = now;
                }
            }
        }
        vTaskDelay(pdMS_TO_TICKS(750));
    }
    i2c_driver_delete(port);
    task_handle_ = nullptr;
#endif
}
