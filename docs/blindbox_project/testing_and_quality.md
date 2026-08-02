# 一期测试与质量门

文档状态：pending_user_confirmation  
主责角色：研发主管  
更新时间：2026-07-12

## 1. 目的

本文定义一期工程的最低测试要求、质量门和验收路径。目标是先用软件闭环降低硬件不确定性，再接真实 ESP32、GPS、NFC。

## 2. 测试范围

| 范围 | 当前测试重点 |
| --- | --- |
| `backend/` | Django 配置、API、数据模型、幂等、权限草案 |
| `frontend/` | 构建、页面渲染、三端响应式、API 错误展示 |
| `tools/device_simulator/` | 设备配置拉取、心跳、GPS 接近、NFC 打卡 |
| `main/` | 后续 GPS/NFC 硬件接入、串口日志、供电稳定 |
| `deploy/` | Nginx/Gunicorn 示例配置可读、环境变量完整 |

## 3. 阶段质量门

### QG-1：工程框架质量门

必须通过：

```powershell
cd backend
python manage.py check
```

```powershell
cd frontend
npm run build
```

检查项：

- `.venv/` 未被 Git 跟踪。
- `node_modules/` 未被 Git 跟踪。
- `dist/` 未被 Git 跟踪。
- `__pycache__/` 未被 Git 跟踪。
- `.env` 未被 Git 跟踪。
- `.env.example` 存在。

### QG-2：后端 API 质量门

最低要求：

- `/api/v1/device-config` 可返回演示设备配置。
- `/api/v1/device-heartbeats` 可接收心跳。
- `/api/v1/location-events` 可接收约 10 秒一次的 GPS 位置信息和定位质量。
- `/api/v1/checkins` 可处理 NFC 打卡。
- `/api/v1/demo/simulate-checkin` 可生成模拟记录。
- `/api/v1/demo/overview` 可聚合演示状态。

必须覆盖的结果：

| 场景 | 期望 |
| --- | --- |
| 合法设备 + 合法标签 | `success` |
| 重复打卡 | `duplicate` |
| 未登记标签 | `tag_unknown` |
| 停用标签 | `tag_disabled` |
| 设备未绑定角色 | `device_not_bound` |
| 模拟打卡 | `source=simulation` |

### QG-3：前端质量门

最低页面：

- 演示总览页
- 设备页
- 角色页
- 点位页
- NFC 标签页
- 数据集页
- 打卡记录页
- 手动模拟打卡页

检查项：

- PC/平板/手机核心信息不遮挡。
- 设备离线、GPS 无信号、NFC 无效、后端错误有明确状态。
- 模拟打卡记录有明确标记。
- 普通查看页面不暴露设备 token。

### QG-4：模拟器软件闭环质量门

`tools/device_simulator/` 至少支持：

1. 拉取配置。
2. 上报心跳。
3. 上报约 10 秒一次的 GPS 位置信息和接近事件。
4. 上报 NFC 打卡事件。
5. 重复打卡验证。
6. 非法标签验证。

通过标准：

- 后端产生对应记录。
- 前端演示页显示状态变化。
- 打卡记录可区分真实/模拟。

### QG-5：真实硬件质量门

硬件到位后执行。

| 模块 | 检查 |
| --- | --- |
| ESP32-S3 | 可烧录、可串口观察 |
| 麦克风/喇叭 | 小智语音问答可用 |
| GPS | 有 NMEA 输出，有效 fix 可读取 |
| NFC | 能读取指定标签 UID/tag_id |
| 电池 | 可完成一轮演示，无异常重启 |
| 后端连接 | 设备能访问 `/api/v1` |

#### 2026-07-18 至 2026-07-25 部分执行记录

| 模块 | 当前结论 | 证据/剩余项 |
| --- | --- | --- |
| ESP32-S3 | 通过 | DZQJ ESP32-S3 N16R8；16MB Flash、8MB PSRAM；小智 2.3.0 烧录、启动、串口观察通过 |
| 麦克风 | 通过 | INMP441 完成真实讲话输入、VAD、音频上传和 ASR；2026-07-25 短按 BOOT 后串口出现 `idle -> connecting -> listening` 和真实 `Application: >>` 识别记录 |
| 喇叭 | 功能通过、音质待优化 | MAX98357A `SD/EN` 显式拉高后，3W 喇叭可实际播放官方链路返回语音；当前杂音较大，尚未关闭音质问题 |
| 小智官网连接 | 通过 | 串口完成 `MQTT: Connected`、`Activation done`、`listening -> speaking`；用户于 2026-07-25 现场确认小智官网后台出现对应真实记录 |
| GPS | 未验收 | 尚无 UART NMEA；上游固件的 `GPIO18/LAMP_GPIO` 与早期 GPS RX 规划冲突，解决前保持断开 |
| NFC | 未验收 | 等 PN532 实物接口确认和 `tag_id` 读取 |
| 电池 | 未验收 | 当前仅 USB 供电，电池和升压压测后置 |
| 后端连接 | 心跳通过 | 真实 ESP32 串口连续两次 `Heartbeat accepted: HTTP 200`；Django 连续两次 POST 200；数据库 `device_001=online`、`firmware_version=blindbox-2.2.6` |

当前 QG-5 结论：**部分通过，不得作为真实硬件整门通过记录**。已达到的最高验证层级为 `hardware_verified`：主控、Wi-Fi、INMP441 真实语音输入、自研平台真实设备心跳、小智官网连接以及 MAX98357A/3W 喇叭实体播放功能已验证。喇叭杂音仍待优化，GPS、NFC 和电池仍未验收。

## 4. 风险测试

必须测试：

- GPS 无 fix。
- NFC 标签不存在。
- NFC 标签停用。
- 重复打卡。
- 后端不可用。
- 设备未绑定角色。
- 数据集状态失败。
- 模拟打卡被误用于正式统计。

## 5. 数据与安全检查

发布前必须确认：

- 日志不输出明文 device token。
- 前端不展示 device token。
- `.env` 不提交。
- GPS 按约 10 秒一次上报位置；后端保存最近位置和签到时定位点，不保存长期连续轨迹。
- 模拟记录有 `source=simulation`。
- API 错误使用稳定 `code`。

## 6. 测试记录格式

每次阶段验收记录：

```text
日期：
提交：
范围：
命令：
结果：
失败项：
是否阻塞：
下一步：
```

## 7. 当前最低验收顺序

1. backend `manage.py check`
2. frontend `npm run build`
3. device_simulator 拉配置
4. device_simulator 心跳
5. device_simulator GPS 接近
6. device_simulator NFC 打卡
7. 前端演示页查看状态
8. 前端打卡记录页查看记录
9. 确认模拟数据标记
10. 提交并推送 GitHub

## 8. 当前状态

| 项 | 状态 |
| --- | --- |
| backend `manage.py check` | 2026-07-13 研发主管复核通过 |
| frontend `npm run build` | 2026-07-13 研发主管复核通过；存在 chunk 体积警告，不阻塞一期 |
| PostgreSQL migrate / seed | 2026-07-13 本机项目内 PostgreSQL 17.10 验证通过 |
| device_simulator 软件闭环 | 2026-07-13 HTTP flow 验证通过 |
| 后端 API 契约测试 | 2026-07-13 后端 15 个自动化测试通过，模拟器 3 个测试通过 |
| 前端 P0 页面验证 | 2026-07-13 PC / 平板 / 手机登录后核心页面通过 Chrome 自动化冒烟 |
| 真实 ESP32 硬件验证 | 2026-07-25 部分通过：主控、Wi-Fi、INMP441、自研 `/device-heartbeats`、小智官网连接和 MAX98357A/3W 喇叭实体播放功能通过；喇叭杂音、GPS、NFC、电池和设备配置拉取待验收 |
| 小智官网语音链路 | 2026-07-25 真实硬件通过：官网后台有真实记录，串口完成 MQTT/激活/听说状态转换；小智工具/MCP 的业务工具调用仍按后续用例验收 |

## 8.1 真实硬件联调数据判定补充

从 2026-07-18 起，真实硬件联调必须采用“清场后再验收”的数据口径：

- 真实硬件验收前必须清空模拟/手工打卡记录。
- 前端总览页的设备在线状态，只有真实 ESP32 调用 `/api/v1/device-heartbeats` 后才可作为 ACC-07 证据。
- 手工 curl、Postman、device_simulator 只能作为接口 smoke test 或软件闭环证据，不可冒充真实硬件验收。
- GPS 验收必须有真实 UART NMEA/fix 或串口日志证据；没有真实定位输出时，不得仅用后台坐标变化判定通过。
- NFC 验收必须有 PN532 实物读到的 `tag_id`，并能在后端/前端对应到合法标签或明确失败原因。

## 9. 阻塞规则

- 后端 check 不通过，不进入 API 实现合并。
- 前端 build 不通过，不进入页面合并。
- 模拟打卡不能区分 `source=simulation`，不允许作为演示验收记录。
- 任何日志输出明文 token，必须阻塞发布。
- 保存长期连续 GPS 轨迹或做轨迹回放，必须重新走产品和安全确认。
## 10. 2026-07-27 真实硬件质量门补充

本节用于修正早期“GPS 未验收”的旧状态。当前以 2026-07-27 研发主管复核为准：

| 质量项 | 当前状态 | 判定 |
| --- | --- | --- |
| GPS 接线 | GPS `VCC -> 3V3`、`GND -> GND`、`TX -> GPIO17`，GPS `RX` 悬空 | 通过 |
| GPIO 风险 | `GPIO18` 已明确保留给灯控制，禁止接 GPS TX | 通过 |
| GPS NMEA 输入 | 串口出现 `BlindboxGps: NMEA GGA: fix=false satellites=0 hdop=0.0` | 通过当前无 fix 验收 |
| GPS 真定位 | 室内无卫星 fix，尚未验证真实经纬度 | 待室外复验 |
| GPS 上报到当前自研平台 | 当前串口存在 `ESP_ERR_HTTP_CONNECT`，数据库未收到今天的新位置事件 | 阻塞 |

质量门口径：

- GPS 硬件接入和 UART/NMEA 已通过，不再按“未接 GPS”处理。
- GPS 真坐标定位仍未通过，必须室外复验 `fix=true`。
- 当前局域网下的 `/api/v1/location-events` 未形成新证据，原因是设备 API 地址仍需更新；该问题归入固件配置/联调问题，不否定 GPS 硬件接线。
