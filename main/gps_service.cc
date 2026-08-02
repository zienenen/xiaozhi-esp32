#include "gps_service.h"

#include <cmath>
#include <cstdlib>
#include <vector>

#include <driver/uart.h>
#include <esp_log.h>
#include <esp_timer.h>

#define TAG "BlindboxGps"

namespace {
constexpr size_t kMaxLineLength = 160;
constexpr int64_t kReportIntervalUs = 10LL * 1000 * 1000;

std::vector<std::string> Split(const std::string& value) {
    std::vector<std::string> fields;
    size_t start = 0;
    while (true) {
        const size_t end = value.find(',', start);
        fields.emplace_back(value.substr(start, end - start));
        if (end == std::string::npos) {
            return fields;
        }
        start = end + 1;
    }
}

int HexDigit(char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'A' && value <= 'F') return value - 'A' + 10;
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    return -1;
}

bool ParseCoordinate(
    const std::string& value, const std::string& hemisphere, double& coordinate) {
    if (value.empty() || hemisphere.size() != 1) return false;
    char* end = nullptr;
    const double raw = std::strtod(value.c_str(), &end);
    if (end == value.c_str() || *end != '\0') return false;
    const int degrees = static_cast<int>(raw / 100);
    const double minutes = raw - degrees * 100;
    if (minutes < 0 || minutes >= 60) return false;
    coordinate = degrees + minutes / 60.0;
    if (hemisphere == "S" || hemisphere == "W") {
        coordinate = -coordinate;
    } else if (hemisphere != "N" && hemisphere != "E") {
        return false;
    }
    return true;
}
}

bool NmeaParser::ParseLine(
    const std::string& line, DeviceApiClient::GpsReading& reading) const {
    const size_t star = line.find('*');
    if (line.size() < 7 || line.front() != '$' || star == std::string::npos ||
        star + 2 >= line.size()) {
        return false;
    }
    uint8_t checksum = 0;
    for (size_t index = 1; index < star; ++index) {
        checksum ^= static_cast<uint8_t>(line[index]);
    }
    const int high = HexDigit(line[star + 1]);
    const int low = HexDigit(line[star + 2]);
    if (high < 0 || low < 0 || checksum != static_cast<uint8_t>((high << 4) | low)) {
        return false;
    }
    const std::vector<std::string> fields = Split(line.substr(1, star - 1));
    if (fields.size() < 9 || (fields[0] != "GPGGA" && fields[0] != "GNGGA")) {
        return false;
    }
    char* end = nullptr;
    const long fix_quality = std::strtol(fields[6].c_str(), &end, 10);
    if (end == fields[6].c_str() || *end != '\0') return false;
    reading = {};
    reading.fix = fix_quality > 0;
    reading.satellites = static_cast<int>(std::strtol(fields[7].c_str(), nullptr, 10));
    reading.hdop = std::strtod(fields[8].c_str(), nullptr);
    return !reading.fix ||
        (ParseCoordinate(fields[2], fields[3], reading.latitude) &&
         ParseCoordinate(fields[4], fields[5], reading.longitude));
}

GpsService& GpsService::GetInstance() {
    static GpsService instance;
    return instance;
}

GpsService::~GpsService() {
    Stop();
}

void GpsService::Start() {
#if CONFIG_BLINDBOX_GPS_ENABLED
    if (CONFIG_BLINDBOX_GPS_UART_RX_GPIO == 18) {
        ESP_LOGE(TAG, "GPS disabled: GPIO18 conflicts with LAMP_GPIO");
        return;
    }
    NmeaParser parser;
    DeviceApiClient::GpsReading fixed;
    DeviceApiClient::GpsReading no_fix;
    if (!parser.ParseLine(
            "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
            fixed) ||
        !fixed.fix || std::fabs(fixed.latitude - 48.1173) > 0.000001 ||
        !parser.ParseLine("$GPGGA,123520,,,,,0,00,99.9,,,,,,*76", no_fix) ||
        no_fix.fix ||
        parser.ParseLine(
            "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*00",
            no_fix)) {
        ESP_LOGE(TAG, "GPS disabled: NMEA parser self-test failed");
        return;
    }
    ESP_LOGI(TAG, "NMEA parser self-test passed");
    bool expected = false;
    if (!started_.compare_exchange_strong(expected, true)) return;
    if (xTaskCreate(TaskEntry, "blindbox_gps", 4096, this, 2, &task_handle_) != pdPASS) {
        task_handle_ = nullptr;
        started_.store(false);
        ESP_LOGE(TAG, "Failed to create GPS task");
    }
#endif
}

void GpsService::Stop() {
#if CONFIG_BLINDBOX_GPS_ENABLED
    started_.store(false);
#endif
}

void GpsService::TaskEntry(void* arg) {
#if CONFIG_BLINDBOX_GPS_ENABLED
    static_cast<GpsService*>(arg)->Run();
#endif
    vTaskDelete(nullptr);
}

void GpsService::Run() {
#if CONFIG_BLINDBOX_GPS_ENABLED
    const uart_port_t port = static_cast<uart_port_t>(CONFIG_BLINDBOX_GPS_UART_PORT);
    const uart_config_t config = {
        .baud_rate = CONFIG_BLINDBOX_GPS_UART_BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    esp_err_t error = uart_param_config(port, &config);
    if (error == ESP_OK) {
        error = uart_set_pin(port, UART_PIN_NO_CHANGE, CONFIG_BLINDBOX_GPS_UART_RX_GPIO,
            UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    }
    if (error == ESP_OK) error = uart_driver_install(port, 2048, 0, 0, nullptr, 0);
    if (error != ESP_OK) {
        ESP_LOGE(TAG, "GPS UART initialization failed: %s", esp_err_to_name(error));
        started_.store(false);
        task_handle_ = nullptr;
        return;
    }
    ESP_LOGI(TAG, "GPS UART ready: port=%d rx_gpio=%d baud=%d (GPIO18 forbidden)",
        CONFIG_BLINDBOX_GPS_UART_PORT, CONFIG_BLINDBOX_GPS_UART_RX_GPIO,
        CONFIG_BLINDBOX_GPS_UART_BAUD_RATE);

    NmeaParser parser;
    std::string line;
    DeviceApiClient::GpsReading latest;
    bool has_reading = false;
    int64_t last_report = esp_timer_get_time() - kReportIntervalUs;
    uint8_t buffer[128];
    while (started_.load()) {
        const int count = uart_read_bytes(
            port, buffer, sizeof(buffer), pdMS_TO_TICKS(250));
        for (int index = 0; index < count; ++index) {
            const char value = static_cast<char>(buffer[index]);
            if (value == '\n') {
                if (parser.ParseLine(line, latest)) has_reading = true;
                line.clear();
            } else if (value != '\r') {
                if (line.size() < kMaxLineLength) line.push_back(value);
                else {
                    line.clear();
                    ESP_LOGW(TAG, "Discarded oversized NMEA sentence");
                }
            }
        }
        const int64_t now = esp_timer_get_time();
        if (now - last_report >= kReportIntervalUs) {
            last_report = now;
            if (has_reading) {
                ESP_LOGI(TAG, "NMEA GGA: fix=%s satellites=%d hdop=%.1f",
                    latest.fix ? "true" : "false", latest.satellites, latest.hdop);
                DeviceApiClient::GetInstance().ReportGps(latest);
            } else {
                ESP_LOGW(TAG, "No valid GGA sentence received in reporting window");
            }
        }
    }
    uart_driver_delete(port);
    task_handle_ = nullptr;
#endif
}
