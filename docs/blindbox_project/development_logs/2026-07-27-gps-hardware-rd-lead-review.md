# 研发日志：GPS 硬件接入复核与当前上报阻塞

| 字段 | 内容 |
| --- | --- |
| 日期 | 2026-07-27 |
| 责任角色 | 研发主管 |
| 协作角色 | 硬件/固件工程师、联调工程师 |
| 状态 | GPS 接线/NMEA 部分通过；当前平台实时上报阻塞 |

## 1. 背景

用户指出硬件工程师已接上 GPS，但部分研发主管文档仍保留“GPS 未验收 / 待接入”的旧状态。研发主管因此重新复核文档、固件配置、后端数据库和串口日志。

## 2. 复核证据

固件配置：

```text
CONFIG_BLINDBOX_GPS_ENABLED=y
CONFIG_BLINDBOX_GPS_UART_PORT=1
CONFIG_BLINDBOX_GPS_UART_RX_GPIO=17
CONFIG_BLINDBOX_GPS_UART_BAUD_RATE=9600
```

接线口径：

```text
GPS VCC -> ESP32 3V3
GPS GND -> ESP32 GND
GPS TX  -> ESP32 GPIO17
GPS RX  -> 悬空
GPIO18  -> 禁止用于 GPS
```

串口复核：

```text
BlindboxGps: NMEA GGA: fix=false satellites=0 hdop=0.0
```

当前阻塞日志：

```text
SelfDeviceApi: Heartbeat request failed: ESP_ERR_HTTP_CONNECT
```

后端数据库复核：

```text
device_id=device_001
online_status=online
last_seen_at=2026-07-26 22:11:57.794396+00:00
firmware=blindbox-2.2.6
gps=no_fix
last_location_at=2026-07-26 22:11:57.758201+00:00
quality={'fix': False, 'hdop': 0, 'satellites': 0}
```

## 3. 研发主管判定

- GPS 已物理接入。
- GPS UART/NMEA 已通过当前无 fix 验收。
- 室内 `fix=false satellites=0` 不能说明 GPS 坏，只说明当前无卫星定位。
- 当前自研平台没有收到今天的新 GPS 事件，原因是设备 API 访问失败，不是 GPS 线本身失败。
- 后续必须把设备 API 地址做成运行期配置，或至少重新烧录为当前启动脚本打印的新后端地址。

## 4. 文档同步

本次已同步更新：

- `phase1_acceptance_handoff.md`
- `testing_and_quality.md`
- `phase1_hardware_wiring_manual.md`
- `development_logs/README.md`

## 5. 下一步

1. 保持 GPS `TX -> GPIO17` 接线，不要改回 `GPIO18`。
2. 更新 ESP32 设备 API 地址，复验 `device-config`、`device-heartbeats`、`location-events`。
3. 到室外或开阔窗边冷启动 5-15 分钟，复验 `fix=true`、卫星数大于 0、经纬度非零。
4. 完成后再更新 ACC-07 总验收状态。
