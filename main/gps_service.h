#ifndef _GPS_SERVICE_H_
#define _GPS_SERVICE_H_

#include "device_api_client.h"

#include <atomic>
#include <string>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

class NmeaParser {
public:
    bool ParseLine(const std::string& line, DeviceApiClient::GpsReading& reading) const;
};

class GpsService {
public:
    static GpsService& GetInstance();
    void Start();
    void Stop();

    GpsService(const GpsService&) = delete;
    GpsService& operator=(const GpsService&) = delete;

private:
    GpsService() = default;
    ~GpsService();
    static void TaskEntry(void* arg);
    void Run();

    std::atomic<bool> started_{false};
    TaskHandle_t task_handle_ = nullptr;
};

#endif  // _GPS_SERVICE_H_
