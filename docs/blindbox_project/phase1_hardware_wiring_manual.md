# 一期演示机器人硬件接线说明书

文档状态：partially_confirmed（INMP441、MAX98357A、GPS UART/NMEA 与平台上报已验证；喇叭杂音待优化；PN532 当前无模块、状态待定；电池待验收）  
主责角色：硬件/固件研发  
最后更新：2026-07-26

本说明适用于 DZQJ ESP32-S3 N16R8、INMP441、MAX98357A、3W 喇叭、NEO-6M/7M 类 GPS、PN532、TP4056 和 18650。GPIO 以当前 `bread-compact-wifi` 的 `main/boards/bread-compact-wifi/config.h` 为准；数字指开发板排针旁的丝印，不是排针顺序。

## 安全规则

1. 插拔线前拔掉 ESP32 USB；一次只新增一个模块，拍照确认后再通电。
2. 所有模块共地。INMP441 只能接 3V3。
3. 喇叭只接 MAX98357A 的 SPK+、SPK-；SPK- 不是 GND。
4. 开发阶段只用 USB，电池最后做；先跑通杜邦线，再焊洞洞板。

## 当前 GPIO 总表

| 功能 | ESP32 引脚 | 状态 |
| --- | --- | --- |
| 麦克风 WS / SCK / SD | GPIO4 / GPIO5 / GPIO6 | 已验证 |
| 功放 DIN / BCLK / LRC | GPIO7 / GPIO15 / GPIO16 | 实体播放已通过，杂音待优化 |
| 功放 SD/EN | GPIO21 | 固件启动后拉高，已验证 |
| GPS TX → ESP RX | GPIO17 | 已收到有效 GGA；室内明确无 fix |
| PN532 SDA / SCL | GPIO8 / GPIO9 | 仅暂定，待实物确认 |
| 灯控制 | GPIO18 | 固件已占用，禁止接 GPS TX |
| OLED SDA / SCL | GPIO41 / GPIO42 | 固件预留 |

## INMP441（已验证）

| INMP441 | ESP32 |
| --- | --- |
| VDD/VCC | 3V3 |
| GND | GND |
| SCK/BCLK | GPIO5 |
| WS/LRCL | GPIO4 |
| SD/DOUT | GPIO6 |
| L/R | GND |

一期只接一个麦克风。以上接线无松动、VCC 确认是 3V3 时可以 USB 通电。

## MAX98357A + 3W 喇叭（现在接这个）

| MAX98357A | 接到 |
| --- | --- |
| VIN | ESP32 5V/VBUS（先看清丝印，不能接 3V3） |
| GND | ESP32 GND |
| BCLK | ESP32 GPIO15 |
| LRC/LRCLK/WS | ESP32 GPIO16 |
| DIN | ESP32 GPIO7 |
| SPK+ | 喇叭正极 |
| SPK- | 喇叭负极，不能接 GND |
| SD/EN | ESP32 GPIO21，由固件拉高 |
| GAIN | 暂不接，使用模块默认增益 |

操作顺序：拔 USB；保留麦克风；先接 GND、三根 I2S、最后接 VIN；喇叭接 SPK+、SPK-；拍一张能看清两块板全部丝印和连线的照片，确认后再通电。首次音量约 20%～30%。

通电判断：七项必接线都能辨认、无裸线相碰、VIN 确认接 5V/VBUS 时才可以通电。丝印不同则停止并拍照。

## GPS（UART/NMEA 与平台上报已验证）

| GPS | ESP32 |
| --- | --- |
| VCC | 3V3；不要同时插 GPS 自身 Type-C |
| GND | GND |
| TX | ESP32 GPIO17；禁止接 GPIO18 |
| RX | 暂不接 |

当前 GPS 模块已确认自带陶瓷天线，不需要另接外置天线。固件配置为 UART1、9600 baud、ESP RX=GPIO17，已持续收到校验有效的 GGA 并约每 10 秒上报。室内实测 `fix=false, satellites=0` 属于明确无 fix，不等于损坏；最终真坐标验收需把陶瓷面朝上放到室外或窗边，远离 ESP32、功放和金属遮挡，冷启动静置 5～15 分钟。

## 3V3 与 GND 免焊分配

ESP32 不需要为每个模块提供独立 3V3 针脚。使用面包板电源轨：

1. ESP32 任意一个 `3V3` → 面包板红色正电源轨。
2. ESP32 任意一个 `GND` → 面包板蓝色负电源轨。
3. INMP441、GPS，后续确认后的 PN532，其 VCC 分别插到同一条 3V3 正电源轨。
4. 所有模块 GND 分别插到同一条负电源轨；MAX98357A 的 VIN 仍接 ESP32 5V/VBUS，不接这条 3V3 轨。

不要把多根杜邦线的裸端拧在一起，不要让 5V 与 3V3 电源轨短接。通电前先确认电源轨中间是否断开；有断点的长面包板需要用一根杜邦线跨接同色两段。

## PN532（当前无模块，待定）

若实物明确有 VCC/GND/SDA/SCL 且已设置为 I2C，暂定 VCC→3V3、GND→GND、SDA→GPIO8、SCL→GPIO9。接口、电压和模式开关未确认前不可通电。只有 USB/APP 的门禁成品不能直接接 ESP32。

### PN532 免焊实机验收顺序

当前板内是 GPS 固件，不能直接把 PN532 插上就测试。按以下顺序隔离变量：

1. 拔掉 ESP32 USB；保留已通过的麦克风和功放，暂时拔掉 GPS 的 VCC、GND、TX 三根线。
2. 拍清楚 PN532 正反面、模式开关/拨码和引脚丝印。只有确认模块处于 **I2C 模式** 后才能继续；不同版本拨码方向不一致，不能仅凭开关位置猜测。
3. 用面包板和杜邦线免焊连接：PN532 VCC→3V3 电源轨、GND→地线轨、SDA→GPIO8、SCL→GPIO9。
4. 刷入 PN532 启用、GPS 禁用的独立固件。预期启动日志依次包含：
   - `PN532 I2C ready: port=1 sda=8 scl=9`
   - `PN532 detected: ...`
   - 放上 NTAG 后出现 `PN532 UID: <真实UID>`
5. 第一次真实 UID 尚不在 `device-config` 时，日志会明确显示标签未配置。记下 UID（大写十六进制，不含空格），在项目根目录执行：

   ```powershell
   .\backend\.venv\Scripts\python.exe .\backend\manage.py set_hw_nfc_tag <真实UID>
   ```

6. 重启 ESP32 让它重新拉取 `device-config`，再次放同一标签。预期日志为 `NFC checkin accepted: HTTP 200`，平台打卡记录的 `source` 必须是 `device`。
7. 验收后再决定恢复 GPS 固件或进行下一项；不得在同一轮同时改 PN532、电池和音频接线。

## TP4056、18650（最后做）

TP4056 只负责充电/保护，不能输出稳定 5V，必须另有 5V 升压模块：

`18650 B+/B- → TP4056 B+/B- → TP4056 OUT+/OUT- → 5V 升压 IN+/IN- → 5V/GND → ESP32 5V/VBUS/GND`

接 ESP32 前用万用表把升压输出调到约 5.00V。当前未确认升压模块和测量结果，电池不可接 ESP32。USB 与外部 5V 一次只选一种。

## 杜邦线、洞洞板和验收状态

- 两边都是公针时用母对母杜邦线；无排针的模块先焊排针。
- 洞洞板给 ESP32 焊排母，使主控可插拔，不焊死。
- 焊后测量 5V-GND、3V3-GND 无短路，再通电。

| 项目 | 状态/证据 |
| --- | --- |
| ESP32、串口、Wi-Fi、自研心跳 | 已通过 |
| INMP441 | 已通过真实讲话验证 |
| MAX98357A + 喇叭 | 功能通过：`SD/EN` 拉高后实体喇叭发声；当前杂音较大，音质门待优化 |
| GPS | UART1/GPIO17/9600 已收到 GGA；`location-events` 已进平台，室外真 fix 待验收 |
| PN532 | 当前没有模块，待收到后确认接口并验证 tag_id |
| 电池、洞洞板 | 前述模块通过后再做 |

2026-07-25 已确认完整语音功能链路：短按 BOOT 后设备进入 `listening`，真实讲话被识别，云端回复使设备进入 `speaking`；将 MAX98357A `SD/EN` 显式拉高后，用户确认实体喇叭发声。当前杂音较大，因此只标记“功能通过、音质待优化”。后续仍不要同时接 GPS、PN532 或电池，应继续逐模块验收。

## 给硬件工程师的下一步任务

硬件工程师不要把 Wi-Fi 当定位能力。Wi-Fi 只证明设备联网、能访问小智官网和自研后端；一期 GPS 验收仍必须来自 GPS 模块 NMEA/fix 或明确 no fix 日志。

执行顺序：

1. 保持当前已通过的麦克风、功放和小智官网链路不动，只做必要的喇叭杂音优化。
2. 先做 ESP32 设备侧 `device-config` 拉取，不接新模块也能验收。
3. GPS 保持 TX→GPIO17；禁止使用 GPIO18。到室外完成 `fix=true` 真坐标验收。
4. PN532 先确认实物接口、电压和模式开关；未确认前不可通电。
5. GPS/NFC 都能独立工作后，再接入自研 `/api/v1/location-events` 和 `/api/v1/checkins`。
6. 最后才做 TP4056、升压模块、18650 和洞洞板焊接。

交付时必须给研发主管：

- 接线照片。
- 串口关键日志。
- 修改过的 `main/` 文件列表。
- 后端接口或前端页面证据。
- 哪些是真实硬件触发，哪些只是手工/API smoke test。
## 2026-07-27 研发主管复核补充

当前实机仍能从串口看到 GPS NMEA 输入：

```text
BlindboxGps: NMEA GGA: fix=false satellites=0 hdop=0.0
```

因此 GPS 物理接线与 UART 输入继续判定为“已接入 / 当前无 fix 验收通过”。但同一轮串口也持续出现：

```text
SelfDeviceApi: Heartbeat request failed: ESP_ERR_HTTP_CONNECT
```

这说明当前局域网下设备 API 地址未打通，后端数据库没有收到今天的新 GPS 事件。硬件工程师下一步不要改 GPS 线，优先配合固件/联调把设备 API 地址更新为当前启动脚本输出的 `ESP32 device API base URL`，再复验 `device-config`、`device-heartbeats` 和 `location-events`。
