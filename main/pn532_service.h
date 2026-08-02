#ifndef _PN532_SERVICE_H_
#define _PN532_SERVICE_H_

#include <atomic>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

class Pn532Service {
public:
    static Pn532Service& GetInstance();
    void Start();
    void Stop();

    Pn532Service(const Pn532Service&) = delete;
    Pn532Service& operator=(const Pn532Service&) = delete;

private:
    Pn532Service() = default;
    ~Pn532Service();
    static void TaskEntry(void* arg);
    void Run();

    std::atomic<bool> started_{false};
    TaskHandle_t task_handle_ = nullptr;
};

#endif  // _PN532_SERVICE_H_
