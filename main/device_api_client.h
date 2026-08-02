#ifndef _DEVICE_API_CLIENT_H_
#define _DEVICE_API_CLIENT_H_

#include <atomic>
#include <mutex>
#include <string>
#include <vector>

#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
#include <freertos/task.h>

class DeviceApiClient {
public:
    struct GpsReading {
        bool fix = false;
        double latitude = 0;
        double longitude = 0;
        int satellites = 0;
        double hdop = 0;
    };

    static DeviceApiClient& GetInstance();

    void Start();
    void Stop();
    void ReportGps(const GpsReading& reading);
    void ReportNfcTag(const std::string& tag_id);
    void LogConversationEvidence(const char* session_id, const char* role, const char* content);

    DeviceApiClient(const DeviceApiClient&) = delete;
    DeviceApiClient& operator=(const DeviceApiClient&) = delete;

private:
    DeviceApiClient() = default;
    ~DeviceApiClient();

    static void HeartbeatLoopTask(void* arg);
    static void ConversationLoopTask(void* arg);
    void FetchDeviceConfig();
    void SendHeartbeat();
    void EnsureConversationWorker();
    void EnqueueConversationEvent(
        const std::string& body, const std::string& session_id, const std::string& role);
    std::string GetDeviceConfigUrl() const;
    std::string GetSiblingApiUrl(const char* endpoint) const;
    bool PostJson(const std::string& url, const std::string& body, const char* operation);

    struct SpotConfig {
        std::string spot_id;
        double latitude = 0;
        double longitude = 0;
        double radius_meters = 0;
    };

    struct TagConfig {
        std::string tag_id;
        std::string spot_id;
    };

    struct ConversationPost {
        std::string body;
        std::string session_id;
        std::string role;
    };

    std::atomic<bool> started_{false};
    std::atomic<bool> configuration_loaded_{false};
    TaskHandle_t heartbeat_task_handle_ = nullptr;
    TaskHandle_t conversation_task_handle_ = nullptr;
    QueueHandle_t conversation_queue_ = nullptr;
    std::mutex state_mutex_;
    std::vector<SpotConfig> spots_;
    std::vector<TagConfig> tags_;
    GpsReading latest_gps_;
    bool has_gps_reading_ = false;
};

#endif  // _DEVICE_API_CLIENT_H_
