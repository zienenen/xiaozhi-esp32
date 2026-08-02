# 一期验收与交接记录

文档状态：software_local_accepted_with_external_blockers  
主责角色：研发主管 / 验收 agent  
验收日期：2026-07-13（2026-07-18 补充真实硬件部分记录）

## 1. 本次验收范围

依据 [development_task_ownership.md](development_task_ownership.md) 第 9、10、11、12 章，以及验收/QA 必读文档：

- [testing_and_quality.md](testing_and_quality.md)
- [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、10、11 节
- [release_operations_runbook.md](release_operations_runbook.md)

按需核对：

- [web_api_contract.md](web_api_contract.md)
- [security_and_data_governance.md](security_and_data_governance.md)

## 2. ACC 验收结论

| 编号 | 验收项 | 当前结论 | 证据 |
| --- | --- | --- | --- |
| ACC-01 | 后端检查 | 通过 | `backend/.venv/Scripts/python.exe manage.py check`：0 issues |
| ACC-02 | 前端构建 | 通过 | `frontend/npm run build` 通过；仍有 Vite chunk > 500 kB 警告，不阻塞一期演示 |
| ACC-03 | 数据库 | 通过 | 本机项目内 PostgreSQL 17.10，`migrate --noinput`、`migrate --check --noinput` 通过 |
| ACC-04 | 演示数据 | 通过 | `python manage.py seed_demo`：1 device、2 agents、1 spot、1 NFC tag、1 dataset |
| ACC-05 | 模拟器闭环 | 通过 | `simulate_device.py flow` 完成配置拉取、心跳、GPS、near_spot、NFC 模拟打卡，返回 `source=simulation` |
| ACC-06 | 前端三端 | 通过 | Chrome 自动化验收 PC 1440×900、平板 834×1112、手机 390×844；登录后核心页面 API 200、无横向溢出 |
| ACC-07 | 真实硬件 | 部分通过 | 2026-07-18 完成 ESP32-S3、Wi-Fi、INMP441 首轮真实语音输入及真实 ESP32 心跳进入自研后端；功放/喇叭、GPS/NFC、设备配置拉取和心跳版完整语音回归仍未验收 |
| ACC-08 | 公网环境 | 未验收 | 本地后端、前端、模拟器已通；公网域名/IP、HTTPS/CORS、服务器 PostgreSQL 未配置 |
| ACC-09 | 小智工具 | 部分通过 | 本地 `X-Tool-Token` 调用 `/agents/{agent_id}/context`、`/knowledge/search` 成功；小智官网/MCP 公网调用未验收 |
| ACC-10 | 安全边界 | 通过本地检查 | `.env`、`tmp/`、`.venv/`、`node_modules/`、`dist/`、`__pycache__/` 未被 Git 跟踪；未发现用户 GitHub 密码写入仓库 |
| ACC-11 | GitHub 节点 | 待本次提交后完成 | 本文档和验收修复提交后推送 `main` |

## 3. 本次验收发现并处理的问题

| 问题 | 处理结果 |
| --- | --- |
| 本机缺 PostgreSQL，无法执行真实迁移验收 | 已使用项目内免安装 PostgreSQL 17.10 运行在 `127.0.0.1:5432`，并完成 migrate / seed |
| 前端生产预览没有本地 API 地址 | 已补本地 `frontend/.env`，并确认 `.env` 不提交 |
| 前端登录页使用 Ant Design `App.useApp()`，但根组件未包 provider | 已在 `frontend/src/main.tsx` 增加 `<AntdApp>` provider |
| Vite preview 端口 `4173` 未在 CORS 示例中放行 | 已更新 `backend/.env.example`，本地 `.env` 同步放行 `4173` |

## 4. 当前可演示能力

- 本地 PostgreSQL 数据库可承载演示数据。
- 后端 API 可完成设备配置、心跳、GPS 上报、NFC/模拟打卡、数据集、演示总览和小智工具上下文查询。
- 设备模拟器可在无硬件时跑通软件闭环。
- 前端响应式 Web 可在 PC / 平板 / 手机查看核心页面。
- 打卡记录能明确显示模拟数据，不与真实硬件验收混淆。

## 5. 仍需用户或外部条件确认/处理

| 编号 | 问题 | 是否阻塞最终验收 | 责任建议 |
| --- | --- | --- | --- |
| Q-A01 | 真实 ESP32、GPS、NFC、电池到货并接线烧录后，是否由硬件研发按 [espidf_runbook.md](espidf_runbook.md) 接入 | 部分完成，仍阻塞 ACC-07 完整通过：主控和麦克风已验证；功放/喇叭、GPS、NFC、电池待验收 | 硬件/固件研发执行，研发主管验收 |
| Q-A02 | 公网服务器、域名或公网 IP、HTTPS 方案何时提供 | 是，阻塞 ACC-08 和小智公网调用 | 部署研发执行，研发主管验收 |
| Q-A03 | 小智官网/MCP 工具调用公网 HTTPS 后端是否可配置并稳定返回 | 是，阻塞 ACC-09 最终验收 | 小智工具/MCP 验证人员执行，研发主管验收 |
| Q-A04 | Vite chunk 体积警告是否本期处理 | 否 | 一期可暂不处理，后续做路由级拆包 |

## 6. 模块交接记录

```text
模块：一期软件本地闭环验收
负责人：研发主管 / 验收 agent
提交 commit：本文件随验收修复提交
涉及目录：backend/、frontend/、tools/device_simulator/、docs/blindbox_project/
完成任务：PostgreSQL 迁移验收、演示数据初始化、模拟器 HTTP 闭环、前端三端页面验收、小智工具本地接口验证、安全边界检查
运行命令：manage.py check / migrate / seed_demo / test；npm run build；simulate_device.py flow；Chrome 响应式自动化验收；Git 安全边界检查
验证结果：软件本地闭环通过；真实硬件、公网、小智官网/MCP 公网调用未验收
遗留问题：ACC-07、ACC-08、ACC-09 公网侧
是否阻塞：阻塞最终演示验收，不阻塞后端/前端/模拟器继续开发
下一步：部署公网环境；接入真实硬件；配置并验证小智工具公网调用
```

## 7. 2026-07-18 硬件/固件阶段交接补充

```text
模块：一期真实硬件主控与麦克风输入链路
负责人：硬件/固件研发；研发主管待验收
固件：小智上游 v2.3.0_bread-compact-wifi
完成任务：HW-01；HW-02 麦克风部分；HW-07 语音输入/对话部分；HW-08 启动、网络和音频日志部分
验证结果：ESP32-S3 16MB Flash / 8MB PSRAM 识别通过；固件写入哈希通过；Wi-Fi 配网、xiaozhi.me 激活、官方服务连接通过；INMP441 两轮真实唤醒、ASR 和 AI 回复通过
未完成：MAX98357A/喇叭播放、GPS NMEA、PN532 tag_id、真实 GPS/NFC 进入自研后端、前端真实设备状态、电池演示
验证层级：hardware_verified（仅限主控、联网和真实麦克风输入链路）
是否阻塞：仍阻塞 ACC-07 完整通过
下一步：按 espidf_runbook.md 断电接入 MAX98357A 和喇叭，完成“可听可说”；随后解决 GPIO18 与 GPS 的固件引脚冲突
```

补充说明：未修改 `main/` 固件源码；本次使用已校验的上游预编译固件。笔记本扬声器播放的是串口回复文本的临时 Windows TTS，不计入真实功放/喇叭验收。

## 8. 2026-07-18 自研平台真实硬件联调数据基线

主责角色：研发主管
执行对象：后端研发 agent、硬件/固件研发 agent、联调/验收 agent
状态：待后端补齐自动化重置命令后进入真实 ESP32 联调

本轮研发主管已确认的基线规则：

| 项 | 结论 |
| --- | --- |
| 假数据处理 | 本地库已清空既有打卡记录，后续验收前必须再次执行真实硬件测试数据重置 |
| 设备配置 | 保留 `device_001` 及其绑定角色、点位、NFC 配置，保证 ESP32 可拉配置 |
| 设备在线 | 清场后 `device_001` 不应被手工或模拟器冒充在线；最终在线必须来自真实 ESP32 心跳 |
| 局域网 API | ESP32 使用电脑局域网 IP，例如 `http://192.168.x.x:8000/api/v1`，禁止使用 `127.0.0.1` |
| 鉴权 | 设备接口使用 `X-Device-Id: device_001` + `X-Device-Token: demo-device-token` |
| NFC | `04AABBCCDD` 仅作为占位测试标签；PN532 读到真实 UID 后由后端替换或新增真实标签 |
| GPS | 仍按约 10 秒一次位置上报设计；未有真实 NMEA/fix 前不得标记 GPS 硬件验收通过 |

后端研发 agent 接手任务以 [development_task_ownership.md](development_task_ownership.md) 第 3.7 节为准。联调运行方式以 [release_operations_runbook.md](release_operations_runbook.md) 第 3.4 节为准。ACC-07 只有在真实 ESP32 触发心跳、GPS/NFC 事件，并能在前端看到对应状态后，才能从“部分通过”改为“通过”。

## 9. 2026-07-18 真实 ESP32 心跳接入补充

```text
模块：BE-13 局域网真实设备联调（心跳子项）
负责人：后端研发 / 设备接入联调
固件：仓库 2.2.6 基线 + 自研 device heartbeat client
完成任务：真实 ESP32 调用 POST /api/v1/device-heartbeats；后端鉴权、落库和在线状态验证
串口证据：18:54:54、18:55:25 对应测试窗口内连续两次 Heartbeat accepted: HTTP 200
服务端证据：同一测试窗口连续两次真实设备 POST 200；18:47 后仍持续每 30 秒接收
数据库证据：device_001=online；last_seen_at=2026-07-18T10:55:25.030958+00:00；firmware_version=blindbox-2.2.6；last_gps_status=not_connected
验证层级：hardware_verified（仅限真实设备心跳）
未完成：ESP32 拉取 device-config、GPS/NFC 真实事件、前端页面人工核对、功放/喇叭、电池、心跳版完整语音回归
是否阻塞：ACC-07 仍为部分通过
```

18:47 “后端保持 unknown、尚无真实 ESP32 心跳”的交接状态已由上述新一轮证据解除；当前不再阻塞 BE-13 心跳子项。该结论不扩展到尚未验收的设备配置拉取、GPS、NFC、功放/喇叭、电池和前端人工核对。

### 2026-07-19 复验补充

设备在家庭网络重新配网后获得 `192.168.1.10`，电脑地址为 `192.168.1.6`。固件完成心跳连接超时与周期重试修复并重新烧录，连续两轮真实请求均返回 HTTP 200；关闭串口后数据库 `last_seen_at` 仍按约 30 秒周期更新到 `2026-07-19T05:18:06.892342+00:00`。本轮未修改数据库架构。BE-13 心跳子项继续为通过，ACC-07 仍因 GPS/NFC、设备配置拉取、前端人工核对、功放/喇叭和电池未完成而保持部分通过。

本节更新后，第 7 节“未修改 `main/` 固件源码”的说明仅代表当时的上游预编译固件验证阶段，不再代表当前板内固件状态。
## 10. 2026-07-27 研发主管复核：GPS 已接入，当前平台上报受后端地址阻塞

复核角色：研发主管  
复核对象：硬件/固件工程师 GPS 接线与当前实机状态  
复核日期：2026-07-27  

### 10.1 复核结论

| 模块 | 结论 | 证据 |
| --- | --- | --- |
| GPS 物理接线 | 已接入 | 当前接线口径为 GPS `VCC -> 3V3`、`GND -> GND`、`TX -> ESP32 GPIO17`、GPS `RX` 悬空；`GPIO18` 禁止用于 GPS |
| GPS UART/NMEA | 通过当前无 fix 验收 | 串口出现 `BlindboxGps: NMEA GGA: fix=false satellites=0 hdop=0.0`，说明 GPS 模块已有真实 NMEA 数据输入 |
| GPS 真坐标 fix | 待室外复验 | 当前室内 `fix=false, satellites=0`，不能作为真坐标定位通过；需室外/窗边冷启动 5-15 分钟复验 |
| 自研平台实时上报 | 当前阻塞 | 串口持续出现 `Heartbeat request failed: ESP_ERR_HTTP_CONNECT`，后端数据库最新 `last_location_at` 仍停留在 2026-07-26 旧记录，原因是固件侧设备 API 地址仍未随本次局域网变更更新 |
| ACC-07 总状态 | 部分通过 | GPS 硬件接入与 NMEA 已通过；GPS 真 fix、NFC、电池、当前局域网下设备 API 上报仍未完整通过 |

### 10.2 当前不得误判的点

- 不得把 Wi-Fi 连接当作 GPS 定位能力。
- 不得把旧数据库中的 `last_gps_status=no_fix` 当作今天的实时上报证据。
- 不得把室内 `fix=false` 判定为 GPS 损坏；这属于已收 NMEA 但尚无卫星定位。
- 当前真实设备访问自研后端失败，优先处理固件侧 `BLINDBOX_DEVICE_API_URL` 运行期配置或重新烧录新后端地址。

### 10.3 下一步验收动作

1. 固件/硬件工程师保持 GPS `TX -> GPIO17` 不变，禁止改回 `GPIO18`。
2. 将设备 API 地址更新为当前启动脚本打印的 `ESP32 device API base URL`，或实现运行期配置。
3. 重新验证 `device-config`、`device-heartbeats`、`location-events` HTTP 200。
4. 室外或开阔窗边复验 GPS 真 fix：`fix=true`、卫星数大于 0、经纬度非零。
5. 完成后研发主管再把 ACC-07 从“部分通过”推进到更高状态。
