# ESP-IDF 构建、烧录与硬件联调手册

文档状态：partially_confirmed（主控、联网、INMP441、MAX98357A、GPS NMEA/上报和官方对话实时入库已验证；喇叭杂音待优化；NFC 当前无模块、待定）
主责角色：硬件/固件研发，研发主管验收
更新时间：2026-07-26

## 1. 当前定位

本文记录一期 ESP32-S3 真实硬件的可复现烧录、接线、串口判断和分模块验收方法。

当前已确认：

- 主控为 DZQJ ESP32-S3 N16R8，实测为 ESP32-S3 rev 0.2、16MB Flash、8MB PSRAM。
- 首轮验证使用小智上游正式版 `v2.3.0_bread-compact-wifi`；2026-07-18 为接入自研平台，已切换为仓库 `2.2.6` 源码编译的 `bread-compact-wifi` 心跳版。
- 自研心跳版已完成编译、烧录哈希校验、Wi-Fi 连接和 `/api/v1/device-heartbeats` HTTP 200 验证；已获得云端回复，MAX98357A 在 `SD/EN` 拉高后完成实体播放。
- INMP441 已完成真实语音输入验证：唤醒、VAD、音频上传、ASR 文本和 AI 回复链路均通过。
- MAX98357A 驱动已启动且设备进入过 `speaking`；将 `SD/EN` 显式拉高后，用户确认 3W 喇叭发声，但杂音较大，当前只能标记功能通过、音质待优化。
- 真实设备的 device-config、心跳、GPS 无 fix 位置摘要和小智官方 user/assistant 对话事件均已进入自研 `/api/v1`。
- GPS 使用 UART1、ESP RX=GPIO17、9600 baud，持续收到校验有效的 GGA；室内当前为明确 `no_fix`，室外真坐标待复验。
- PN532/NFC 当前没有实物模块，按用户确认标记为待定。

开发阶段全部使用 USB 供电。每次只接一个模块，杜邦线版本通过后再规划洞洞板焊接。

## 2. 2026-07-18 硬件任务状态

| 任务 | 当前状态 | 证据/说明 |
| --- | --- | --- |
| HW-01 ESP32-S3 板型 | 已通过 | `esptool flash-id` 识别 ESP32-S3、16MB Flash、8MB PSRAM；上游 2.3.0 和自研心跳版 2.2.6 均可启动 |
| HW-02 麦克风和功放 | 部分通过 | INMP441 识别真实讲话；MAX98357A `SD/EN` 拉高后实体发声，但杂音较大，音质待优化 |
| HW-03 GPS | 已通过当前无 fix 验收 | UART1/GPIO17/9600 持续收到校验有效 GGA；自带陶瓷天线，室内明确无 fix |
| HW-04 PN532 NFC | 待定 | 当前没有 PN532 模块，固件启用配置已编译通过 |
| HW-05 GPS 约 10 秒上报 | 已通过 | `/api/v1/location-events` 连续 HTTP 200；数据库和前端显示 GPS 无 fix |
| HW-06 NFC 打卡调用 | 待定 | 等收到 PN532 后读取真实 UID 并验收 `/api/v1/checkins` |
| HW-07 保留小智语音链路 | 已通过 | 短按 BOOT 进入监听，真实讲话被识别并收到云端回复，真实喇叭可播放 |
| HW-08 串口日志可诊断 | 已通过当前已接模块 | 启动、Wi-Fi、激活、音频、device-config、心跳、GPS、对话入库成功/失败均有脱敏日志 |
| HW-09 电池供电 | 未开始 | 继续 USB 供电，最后执行电池压测 |

## 3. 当前硬件连接原则

1. 接线或改线前必须拔掉 USB，灯完全熄灭后再操作。
2. 一次只接一个模块，接好后拍照核对，再通电测试。
3. 所有模块必须与 ESP32 共地。
4. INMP441 只能接 `3V3`，禁止接 `5V`。
5. 喇叭只能接 MAX98357A 输出端，禁止直接接 ESP32 GPIO。
6. GPS、NFC、功放和电池不得在对应单模块验收前同时接入。
7. 开发阶段不焊死主控板；杜邦线版本完整通过后再规划洞洞板。

## 4. 已验证的 INMP441 接线

当前正式固件启用了 Simplex I2S，实际引脚以 `main/boards/bread-compact-wifi/config.h` 为准：

| INMP441 | ESP32-S3 | 说明 |
| --- | --- | --- |
| `VDD` / `VCC` | `3V3` | 禁止接 5V |
| `GND` | `GND` | 共地 |
| `SCK` / `BCLK` | `GPIO5` | 麦克风位时钟 |
| `WS` / `LRCL` | `GPIO4` | 左右声道时钟 |
| `SD` / `DOUT` | `GPIO6` | 麦克风数据输出 |
| `L/R` | `GND` | 选择当前固件读取的声道 |

注意：早期交接表曾写成 `SCK -> GPIO4`、`WS -> GPIO5`，与当前实际固件相反。真实验证使用的是 `SCK -> GPIO5`、`WS -> GPIO4`。

## 5. 功能通过、音质待优化的 MAX98357A 接线

以下映射来自当前固件配置；2026-07-25 将模块 `SD/EN` 显式拉高后已确认实体喇叭发声：

| MAX98357A | ESP32-S3 | 状态 |
| --- | --- | --- |
| `VIN` | `5V` | 接线口径已确认，电压待测 |
| `GND` | `GND` | 接线口径已确认 |
| `BCLK` | `GPIO15` | 固件映射已确认 |
| `LRC` / `LRCLK` | `GPIO16` | 固件映射已确认 |
| `DIN` | `GPIO7` | 固件映射已确认 |
| 喇叭 `+/-` | MAX98357A 输出端 | 禁止接 ESP32 |

验收证据：设备短按 BOOT 后串口依次出现 `idle -> connecting -> listening`，真实讲话产生 `Application: >>` 识别记录，随后进入 `listening -> speaking`；模块 `SD/EN` 显式拉高后，用户确认 3W 喇叭实际发声。当前杂音较大，后续需降低软件音量、缩短信号线、优化共地和电源去耦后再关闭音质问题。

## 6. GPS 安全引脚与当前验收结果

上游 `bread-compact-wifi` 把 `GPIO18` 定义为 `LAMP_GPIO` 输出，因此 GPS TX 永久禁止接 GPIO18。当前已选择未占用的 GPIO17：

| GPS | ESP32-S3 |
| --- | --- |
| VCC | 3V3 |
| GND | GND |
| TX | GPIO17（ESP UART1 RX） |
| RX | 不接 |

固件参数为 UART1、9600 baud。实机已通过 NMEA 解析自检并持续收到 GGA，约 10 秒调用一次 `/api/v1/location-events`；后端与前端显示 `no_fix`，没有用 Wi-Fi 状态冒充 GPS。模块自带陶瓷天线；最终真坐标复验时陶瓷面朝上放到室外或开阔窗边，远离功放、ESP32 和金属遮挡，冷启动静置 5～15 分钟。

## 7. 固件下载与校验

本次使用小智上游 GitHub Release：

```text
版本：v2.3.0
文件：v2.3.0_bread-compact-wifi.zip
SHA-256：4f385496d75e0431fa4538be263ac1f30fbc224f75d19c890b99c189785d2525
解压文件：merged-binary.bin
```

PowerShell 示例：

```powershell
curl.exe -L --fail --retry 4 `
  -o v2.3.0_bread-compact-wifi.zip `
  https://github.com/78/xiaozhi-esp32/releases/download/v2.3.0/v2.3.0_bread-compact-wifi.zip

Get-FileHash -Algorithm SHA256 .\v2.3.0_bread-compact-wifi.zip
Expand-Archive .\v2.3.0_bread-compact-wifi.zip -DestinationPath .\firmware
```

固件包和临时烧录工具保存在本机 `tmp/firmware/`，不提交 Git。

## 8. 烧录工具与命令

本次实测使用 `esptool 5.1.0`。先识别芯片：

```powershell
python -m pip install esptool==5.1.0
python -m esptool --port COM4 flash-id
```

本机实测串口为 `COM4`，其他电脑必须按设备管理器实际端口替换。识别通过后烧录：

```powershell
python -m esptool `
  --chip esp32s3 `
  --port COM4 `
  --baud 460800 `
  --before default-reset `
  --after hard-reset `
  write-flash `
  --flash-mode dio `
  --flash-freq 80m `
  --flash-size 16MB `
  0x0 .\firmware\merged-binary.bin
```

通过标准：

- 写入结束显示 `Hash of data verified`。
- 自动复位后串口出现 `Project name: xiaozhi` 和 `App version: 2.3.0`。
- 串口波特率为 `115200`。

本次曾尝试全量读取 16MB 原示例固件作为备份，但 FTDI 链路在高速长时间读取中出现数据校验错误，未生成有效备份。原固件仅为无业务数据的通用日志示例；正式固件烧录成功后，以重新烧录已校验的官方包作为当前恢复路径。

## 9. 配网与激活

首次启动没有保存 Wi-Fi 时，设备会创建类似 `Xiaozhi-XXXX` 的热点：

1. 手机连接该热点。
2. 浏览器打开 `http://192.168.4.1`。
3. 选择 2.4GHz Wi-Fi，输入密码并提交。
4. 串口出现 `Save SSID`、`Got IP` 和 `Network connected` 才算保存成功。
5. 固件连接官方服务后会输出临时激活码；登录 `xiaozhi.me` 完成设备激活。

禁止在文档、Git、截图或日志交接中记录 Wi-Fi 密码、激活码或明文 token。

## 10. 串口日志判断标准

### 10.1 主控与固件通过

```text
Project name: xiaozhi
App version: 2.3.0
Board: ... SKU=bread-compact-wifi
Found 8MB PSRAM device
```

### 10.2 无 OLED 的预期降级

当前硬件没有 SSD1306 OLED，因此会出现：

```text
Failed to initialize display
```

随后固件使用 `NoDisplay` 继续运行。只要没有崩溃重启，该错误在当前一期无屏方案中不阻塞语音验收。

### 10.3 Wi-Fi 和官方服务通过

```text
Got IP
Application: Network connected
Ota: Current is the latest version
```

### 10.4 INMP441 真实语音输入通过

```text
AFE: Input PCM Config: total 1 channels(1 microphone, 0 playback)
AudioCodec: Set input enable to true
Application: Wake word detected
StateMachine: State: connecting -> listening
Application: >> <识别到的用户文本>
Application: << <服务器回复文本>
```

2026-07-18 实测两轮均成功识别唤醒词和用户语音，并收到 AI 回复。验证层级为 `hardware_verified`（仅主控、联网和真实麦克风输入链路）。

## 11. 后续验收顺序

当前已完成：小智官网语音链路、INMP441 真实输入、MAX98357A + 3W 喇叭实体发声、device-config、心跳、GPS NMEA/无 fix 上报、官方 user/assistant 对话实时入库。后续顺序更新如下：

1. 音频小优化：在不阻塞主线的前提下，降低软件音量/增益、缩短功放信号线、检查共地和电源去耦；杂音问题记录为“音质待优化”，不作为 GPS/NFC 前置阻塞。
2. GPS 室外真 fix 复验：保持 GPIO17 接线不动，在开阔环境确认 `fix=true`、卫星数大于 0 和非零经纬度。
3. PN532/NFC：当前无模块、状态待定；收到模块后先确认 I2C 模式和 3.3V，再按 GPIO8/GPIO9 独立验收真实 UID。
4. NFC 打卡：后端用真实 UID 替换占位标签后，由 ESP32 调用 `/api/v1/checkins`，验证真实 `source=device` 打卡记录。
5. 语音回归：每次后续固件修改后，回归短按 BOOT、真实讲话、官网 session、实时对话入库和喇叭播放。
6. 电池压测：最后接 TP4056、升压模块和 18650，完成一轮短时演示；此前全部 USB 供电。

如果后续需要修改固件，必须先列出将改动的 `main/` 文件并同步研发主管确认。自定义板型不得直接覆盖上游 `bread-compact-wifi` 配置。

## 12.1 自研平台真实心跳接入记录

2026-07-18 修改范围：

```text
main/application.cc
main/CMakeLists.txt
main/Kconfig.projbuild
main/device_api_client.h
main/device_api_client.cc
```

本机使用 ESP-IDF 5.5.2 构建，设备联网后立即发送心跳，随后每 30 秒发送一次。设备 token 仅保存在 Git 忽略的本机 `sdkconfig`，串口日志不输出 token。

本轮网络事实：

| 项 | 值 |
| --- | --- |
| ESP32 地址 | `192.168.101.10` |
| 后端电脑 WLAN 地址 | `192.168.101.119` |
| 心跳接口 | `http://192.168.101.119:8000/api/v1/device-heartbeats` |
| 串口结果 | 连续两次 `Heartbeat accepted: HTTP 200` |
| 后端结果 | `device_001=online`，`firmware_version=blindbox-2.2.6` |

故障判断：早期使用 `192.168.168.155` 和 `192.168.168.134` 时串口返回连接错误 `0x71`，原因是 ESP32 与电脑不在同一网段；切换到相同 WLAN 后，Django 又因 `ALLOWED_HOSTS` 未包含当天 WLAN IP 而拒绝请求。将当天 IP 加入本地 `.env` 并重启服务后通过。局域网 IP 不是固定配置，每次演示前必须用 `ipconfig`/`Get-NetIPAddress` 重新确认。

### 12.2 2026-07-19 家庭网络与心跳可靠性复验

- 家庭 Wi-Fi：`CMCC-22NX`；ESP32 地址 `192.168.1.10`；电脑 WLAN 地址 `192.168.1.6`。
- 配网成功后 `Xiaozhi-XXXX` 热点自动关闭，手机看不到该热点属于正常结果。
- 本地忽略配置中的 API 地址更新为 `http://192.168.1.6:8000/api/v1/device-heartbeats`；地址随局域网变化，不提交 Git。
- 首次后台启动失败不是数据库结构问题，而是项目本地 PostgreSQL 未运行；使用 `pg_ctl` 启动后，`pg_isready` 和 Django system check 均通过。
- 原心跳实现通过仓库通用 `EspTcp::Connect()` 发起连接；该调用没有连接超时，局域网抖动时可能永久阻塞。现改为专用 FreeRTOS 心跳任务和 ESP-IDF `esp_http_client`，HTTP 超时 10 秒，失败后下一周期重试。
- 最终构建镜像 `0x28a0b0` 字节，app 分区剩余 36%；烧录哈希校验通过。
- 串口连续两轮出现 `Sending heartbeat` 和 `Heartbeat accepted: HTTP 200`。关闭 COM4 后，PostgreSQL 的 `last_seen_at` 仍在约 31 秒内从 `2026-07-19T05:17:35.145252+00:00` 更新到 `2026-07-19T05:18:06.892342+00:00`，证明心跳不依赖串口监视器。

本轮实际修改的 `main/` 文件：

```text
main/application.cc
main/CMakeLists.txt
main/Kconfig.projbuild
main/device_api_client.h
main/device_api_client.cc
```

数据库迁移和数据库架构均未修改。

### 12.3 2026-07-26 小智官方对话实时入库验收

目标：保留小智官方语音链路，同时把固件捕获的每条 user 文本和 assistant 回复实时写入自研平台。

本轮固件修改：

```text
main/device_api_client.h
main/device_api_client.cc
```

`main/application.cc` 中既有两个捕获点保持不变：

- 官方 STT 文本：`role=user`
- 官方 TTS `sentence_start`：`role=assistant`

实现原则：

1. 回调先打印完整 `CONVERSATION_EVIDENCE`。
2. 使用深度 16 的 FreeRTOS 指针队列零等待入队，不在官方语音回调中执行 HTTP。
3. 独立 `device_conversation` 任务调用 `POST /api/v1/device-conversation-events`，HTTP 超时 10 秒。
4. 请求头使用 `X-Device-Id` / `X-Device-Token`；token 仅在 Git 忽略的本机 `sdkconfig` 中保存。
5. 请求体包含 `official_session_id`、`role`、`content`、`content_source`、`session_source`、`created_at`。
6. 中国区一期时间使用带 `+08:00` 的 ISO 8601；后端保存后可规范化为 UTC。
7. HTTP 失败、设备 API 离线、队列不可用/已满或内存分配失败时，只打印脱敏告警并保留串口证据，不中断对话。
8. 当前接口未定义设备事件幂等键，因此失败后不盲目自动重试，避免重复消息。

成功日志判断：

```text
Application: >> <用户文本>
CONVERSATION_EVIDENCE {..."role":"user"...}
Conversation event accepted: HTTP 201
Application: << <助手回复>
CONVERSATION_EVIDENCE {..."role":"assistant"...}
Conversation event accepted: HTTP 200
```

失败降级日志判断：

```text
Conversation event post failed: session=<session> role=<role>; serial evidence retained
Conversation event queue full: session=<session> role=<role>; serial evidence retained
Conversation event not queued because device time is unavailable: ...; serial evidence retained
```

真实硬件结果：

| 项 | 结果 |
| --- | --- |
| 固件 SHA-256 | `B9201141E7F004F6C58FFD7D633CAE04E62FFB933365CED1953722190B33208D` |
| 固件大小 | `0x2913b0`，app 分区剩余 35% |
| 官方 session | `d0d109c0` |
| 后端 session | `session_1162ee462f6d48c8ad7fd8f86060096b` |
| 设备 / 绑定角色 | `device_001` / `agent_alo` |
| 入库消息 | 9 条，user/assistant 按带时区时间顺序保存 |
| HTTP | 首句 201；后续 8 句 200 |
| 语音回归 | 用户确认喇叭正常回应 |
| 其他链路 | 同轮心跳和 GPS 上报继续 HTTP 200 |

后端只读复核显示 `source=device_log`，第一条为 user，后续 user/assistant 消息全部归属同一 `official_session_id`。串口、文档和代码扫描均未发现明文 device token。

## 12. 关联资料

- [development_task_ownership.md](development_task_ownership.md)
- [phase1_single_robot_budget.md](phase1_single_robot_budget.md)
- [web_api_contract.md](web_api_contract.md)
- [testing_and_quality.md](testing_and_quality.md)
- [release_operations_runbook.md](release_operations_runbook.md)
- [phase1_acceptance_handoff.md](phase1_acceptance_handoff.md)
