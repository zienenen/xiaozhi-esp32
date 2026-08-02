# 硬件/固件实机测试记录（2026-07-26）

## 测试对象

- 主控：DZQJ ESP32-S3 N16R8（实机识别为 ESP32-S3 rev v0.2、16 MB Flash、8 MB PSRAM）
- 板型配置：`bread-compact-wifi`
- 已接模块：INMP441 麦克风、MAX98357A 功放与扬声器、带自有陶瓷天线的 GPS
- 当前没有/未接模块：PN532 NFC、电池、OLED
- 固件版本：Xiaozhi `2.2.6`
- 固件文件：`build_hwpm_gps/xiaozhi.bin`
- 当前已刷 GPS/实时对话上报固件 SHA-256：`B9201141E7F004F6C58FFD7D633CAE04E62FFB933365CED1953722190B33208D`

## 本轮实机接线

- INMP441：VDD→3V3，GND→GND，SCK→GPIO5，WS→GPIO4，SD→GPIO6，L/R→GND
- MAX98357A：VIN→5V/VBUS，GND→GND，BCLK→GPIO15，LRC→GPIO16，DIN→GPIO7，SD/EN→GPIO21
- GPS：VCC→3V3，GND→GND，TX→GPIO17；GPS RX 悬空
- GPIO18 保留给灯，不用于 GPS

## 实测结果

| 测试项 | 结果 | 证据摘要 |
| --- | --- | --- |
| 固件编译 | 通过 | ESP-IDF 5.5.2 完整编译成功，应用分区剩余 35% |
| 芯片连接及刷写 | 通过 | COM4 识别成功；写入后所有分区 Hash 校验通过 |
| 功放使能 | 通过 | 启动日志：`MAX98357A enabled on GPIO21` |
| 麦克风采集/语音识别 | 通过 | 两次准确识别用户询问时间的语音 |
| 官方小智会话 | 通过 | 官方 MQTT session `a4681f38`；用户及助手消息均生成 `CONVERSATION_EVIDENCE` |
| 实时对话入库 | 通过 | user/assistant 每句保留 `CONVERSATION_EVIDENCE` 并异步 POST；真实 session `d0d109c0` 共 9 条消息已按句入库 |
| 扬声器播放 | 通过（有已知杂音） | 用户确认喇叭有正常语音回应；存在杂音，本轮不处理，不阻塞当前联调 |
| GPS 串口/NMEA | 通过 | `GPS UART ready: port=1 rx_gpio=17 baud=9600`；持续收到校验有效的 GGA |
| GPS 卫星定位 | 待室外验证 | 当前室内 `fix=false, satellites=0`，说明已收数但尚未获得卫星定位 |
| 定位事件上报 | 通过 | `/location-events` 周期上报返回 HTTP 200 |
| GPS/心跳状态一致性 | 通过 | 合并为单一设备客户端后，数据库持续显示 `last_gps_status=no_fix`，不再被心跳覆盖为 `not_connected` |
| 事件时间 | 通过 | 固件不再发送上游本地化后的伪 UTC；数据库使用平台接收时间，位置时间与后端 UTC 一致 |
| 设备配置拉取 | 通过 | 配置加载成功，spots=1、nfc_tags=1 |
| 心跳上报 | 通过 | 周期心跳返回 HTTP 200 |
| PN532/NFC | 待定 | 当前没有 PN532 模块，收到模块后再安排实机验收 |
| PN532 启用编译 | 通过 | 独立配置启用 I2C1/GPIO8/GPIO9 后完整编译成功；未刷入当前 GPS 装配 |

## 已知问题与后续项

1. 扬声器有杂音：已记录为非阻塞问题，后续单独排查供电、地线、走线和数字增益。
2. GPS 尚无卫星 fix：模块自带陶瓷天线，不需要另接外置天线。把陶瓷面朝上移到室外或窗边，远离 ESP32、功放和金属遮挡，冷启动静置 5–15 分钟，验收 `fix=true`、卫星数大于 0 和非零经纬度。
3. PN532/NFC 待定：当前没有模块；收到模块并具备免焊接线条件后，再验证 UID 读取及 `/checkins`。
4. OLED 未连接，因此启动时 SSD1306 I2C 初始化失败属于当前装配状态的预期现象。
5. 日志出现一次 MQTT 音频序号跳号警告，但会话和播放均继续完成；暂不作为阻塞问题。
6. 实时对话 API 已接通；历史手工证据 `evidence/conversation_a4681f38.json` 继续保留作离线兜底，不再作为当前落库主链路。

## 平台数据库复核

修正版刷机后的只读复核结果：

- `online_status=online`
- `firmware_version=blindbox-2.2.6`
- `last_gps_status=no_fix`
- `last_location_quality={"fix": false, "hdop": 0, "satellites": 0}`
- `last_location_at=2026-07-26T10:26:08.676357+00:00`
- 同次复核后端当前时间：`2026-07-26T10:26:26.029681+00:00`

这证明设备在线、GPS 无定位状态与位置事件均已进入自研平台，且事件时间没有继续产生未来 8 小时的偏移。

## HW-PM-01～07 验收矩阵

| 编号 | 当前结论 | 权威证据 / 缺口 |
| --- | --- | --- |
| HW-PM-01 | 通过 | 官方 MQTT 会话建立；真实收音、STT、助手回复和喇叭播放均复现；用户确认喇叭有回应 |
| HW-PM-02 | 通过 | 设备使用 `192.168.1.9` 局域网地址；`device-config` 返回成功，日志不输出 token |
| HW-PM-03 | 通过 | 心跳 HTTP 200；数据库 `online_status=online`；前端设备页显示“在线” |
| HW-PM-04 | 通过 | 真实 session `d0d109c0` 已通过设备鉴权实时入库，同一会话聚合 9 条 user/assistant 消息；串口证据继续保留 |
| HW-PM-05 | 通过当前无 fix 验收 | GPIO17 收到有效 NMEA，约 10 秒上报；数据库与前端显示“GPS 无 fix”，没有用 Wi-Fi 冒充定位 |
| HW-PM-06 | 待定 | 当前没有 PN532 模块；固件启用构建已通过，待收到模块后验证检测、真实 UID 和 `/checkins` |
| HW-PM-07 | 通过 | 先稳定音频，再单独接 GPS；PN532 仅做独立编译未刷写；电池保持后置 |

前端只读核对时，设备页显示：

- 设备：`ESP32-S3-HW-TEST` / `ESP32S3-N16R8-HW-001`
- 状态：在线
- 唯一绑定角色：`agent_alo`
- GPS：GPS 无 fix

实时对话记录已形成后端权威数据：设备 `device_001`、绑定角色 `agent_alo`、来源 `device_log`、官方 session `d0d109c0`，user/assistant 顺序和带时区时间均可追溯。

## HW-RT-01～05 实机验收

| 编号 | 结论 | 实机证据 |
| --- | --- | --- |
| HW-RT-01 | 通过 | 每个 user/assistant 句子继续打印完整 `CONVERSATION_EVIDENCE` |
| HW-RT-02 | 通过 | 首句 POST 返回 HTTP 201，后续 8 句返回 HTTP 200 |
| HW-RT-03 | 通过 | 使用 `X-Device-Id` / `X-Device-Token` 鉴权；串口未输出 token |
| HW-RT-04 | 通过 | 上报 official_session_id、role、content、content/session 来源和 `+08:00` ISO 8601 时间 |
| HW-RT-05 | 通过 | POST 运行在独立队列/HTTP 任务；用户确认喇叭正常回应，官方语音链路未受影响；失败分支保留串口证据 |

数据库只读复核：

- `official_session_id=d0d109c0`
- `device_id=device_001`
- `agent_id=agent_alo`
- `source=device_log`
- `message_count=9`
- 第一条为 user，后续 user/assistant 消息按 `created_at` 顺序保存
