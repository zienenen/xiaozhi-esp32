# 一期研发模块责任分工

文档状态：pending_user_confirmation
主责角色：研发主管
更新时间：2026-07-12

## 1. 目的

本文把一期演示机器人研发工作拆成可直接分配给研发人员的模块。每个模块都明确：

- 负责范围
- 输入资料
- 输出物
- P0 任务
- 验收标准
- 交接边界

统一原则：后端、前端、硬件、联调、部署及最终验收均由研发主管负责兜底。具体研发人员可以按模块执行，但不得跨模块擅自改接口、字段、硬件接线或验收口径。

## 2. 总体责任矩阵

| 模块 | 执行负责人 | 最终责任人 | 主要目录 | 阶段门 |
| --- | --- | --- | --- | --- |
| 后端模块 | 后端研发 | 研发主管 | `backend/` | D2 后端最小闭环 |
| 前端模块 | 前端研发 | 研发主管 | `frontend/` | D3 前端最小闭环 |
| 联调工具模块 | 联调研发 | 研发主管 | `tools/device_simulator/` | D4 模拟器软件闭环 |
| 硬件固件模块 | 硬件/固件研发 | 研发主管 | `main/`、硬件接线资料 | D5 真实硬件接入 |
| 部署模块 | 部署研发或后端兼任 | 研发主管 | `deploy/`、服务器环境 | D6 公网演示环境 |
| 验收模块 | 研发主管 | 研发主管 | `docs/`、实际演示环境 | D7 演示验收 |

说明：

- 可以一人兼任多个执行负责人，但责任边界仍按模块拆分。
- 每个模块交付前必须更新对应 README、运行命令或测试记录。
- 任何模块不得提交 `.env`、`node_modules/`、`.venv/`、`dist/`、`__pycache__/`、真实 token 或密码。

## 2.1 内部文档边界

本文是研发主管和研发工程师内部执行文档，不替代产品、架构、安全、预算等角色文档。

使用规则：

- 分配任务时，优先让研发只看本文件对应模块章节和本节列出的必读文档。
- 研发人员不需要完整阅读 `docs/blindbox_project/` 全部文档。
- 产品、架构、安全文档如有冲突，以研发主管确认为准，不允许研发人员自行改口径。
- 如果研发人员发现文档冲突，只记录问题并提交给研发主管，不直接扩大任务范围。

## 2.2 各角色阅读清单

### 研发主管

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) | 模块分工、验收、交接边界 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) | P0/P1/P2 功能范围 |
| [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) | 一期实施顺序和风险 |
| [development_process.md](development_process.md) | 阶段门、提交规则、协作规则 |
| [testing_and_quality.md](testing_and_quality.md) | 质量门和最低验收路径 |
| [release_operations_runbook.md](release_operations_runbook.md) | 发布、公网演示、回滚、节点上传 |
| [rd_lead_question_list.md](rd_lead_question_list.md) | 已确认问题和待验证问题 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [web_api_contract.md](web_api_contract.md) | 审后端、前端、模拟器、硬件接口时 |
| [security_and_data_governance.md](security_and_data_governance.md) | 涉及 token、GPS、账号、公网、日志时 |
| [open_source_selection.md](open_source_selection.md) | 涉及新增依赖或改技术栈时 |
| [phase1_single_robot_budget.md](phase1_single_robot_budget.md) | 涉及硬件采购或替代型号时 |

不要求逐字阅读：

- 市场化、竞品、早期综合 PRD，除非要重新评估产品方向。

### 后端研发

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 3 章 | 后端任务、交付物、边界 |
| [web_api_contract.md](web_api_contract.md) | API、数据对象、错误码、认证 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、8、10 节 | P0 功能、共用管理端、非功能验收 |
| [security_and_data_governance.md](security_and_data_governance.md) 第 2、3、4、6、10 节 | token、GPS、日志、后端安全要求 |
| [testing_and_quality.md](testing_and_quality.md) 后端/API 相关章节 | 后端质量门 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [release_operations_runbook.md](release_operations_runbook.md) | 配合部署、公网环境、PostgreSQL 时 |
| [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | 前端需要字段或页面状态解释时 |

不需要看：

- 市场化需求全文。
- 竞品分析。
- 硬件预算全文，除非参与设备字段设计。

### 前端研发

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 4 章 | 前端页面、状态、边界 |
| [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | 页面交互和信息架构 |
| [web_api_contract.md](web_api_contract.md) | API 字段、错误码、状态码 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、8、10 节 | P0 页面范围和验收 |
| [testing_and_quality.md](testing_and_quality.md) 前端相关章节 | 构建和三端质量门 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [security_and_data_governance.md](security_and_data_governance.md) | 涉及 token 展示、账号、GPS 敏感信息时 |
| [release_operations_runbook.md](release_operations_runbook.md) | 配置公网 API base URL 时 |

不需要看：

- ESP-IDF、硬件接线、预算细节。
- 开源选型全文，除非要新增前端依赖。

### 联调工具研发

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 5 章 | 模拟器任务和完成标准 |
| [web_api_contract.md](web_api_contract.md) | 设备配置、心跳、GPS、NFC、打卡接口 |
| [testing_and_quality.md](testing_and_quality.md) 模拟器相关章节 | 软件闭环质量门 |
| [release_operations_runbook.md](release_operations_runbook.md) 本地/公网运行章节 | 切换本地和公网后端 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [security_and_data_governance.md](security_and_data_governance.md) | 处理 device token、模拟数据标记时 |
| [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) | 确认模拟器在整体顺序中的位置 |

不需要看：

- 产品市场化文档。
- 前端交互规格全文。
- 硬件预算全文。

### 硬件/固件研发

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 6 章 | 硬件固件任务、交付物、边界 |
| [phase1_single_robot_budget.md](phase1_single_robot_budget.md) | 已确认硬件清单和采购型号 |
| [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md) | 小智底座已有能力和可扩展点 |
| [web_api_contract.md](web_api_contract.md) 设备/GPS/NFC 相关章节 | 上报格式和打卡接口 |
| [testing_and_quality.md](testing_and_quality.md) 硬件相关章节 | GPS/NFC 验收要求 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [security_and_data_governance.md](security_and_data_governance.md) | 涉及 GPS 频率、token、日志脱敏时 |
| [release_operations_runbook.md](release_operations_runbook.md) | 真实设备连接公网后端时 |
| [open_source_selection.md](open_source_selection.md) | 涉及小智上游复用边界时 |

还需补齐：

- [espidf_runbook.md](espidf_runbook.md)。硬件开工前应补，否则烧录、串口、接线验收容易不一致。

不需要看：

- 前端页面交互全文。
- 市场化竞品和商业化需求。

### 部署研发

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 7 章 | 部署任务和验收 |
| [release_operations_runbook.md](release_operations_runbook.md) | 本地、公网、回滚、故障处理 |
| [security_and_data_governance.md](security_and_data_governance.md) | `.env`、token、公网、日志边界 |
| [web_api_contract.md](web_api_contract.md) | 公网 API base URL、认证、CORS 影响 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [open_source_selection.md](open_source_selection.md) | 涉及 Nginx/Gunicorn/PostgreSQL 选型边界时 |
| [testing_and_quality.md](testing_and_quality.md) | 做公网 smoke test 时 |

不需要看：

- 产品需求全文。
- 前端交互规格全文。
- 硬件预算全文。

### 小智工具/MCP 验证人员

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 8 章 | MCP 验证任务和兜底 |
| [web_api_contract.md](web_api_contract.md) 智能体上下文/知识查询接口 | 工具调用接口 |
| [security_and_data_governance.md](security_and_data_governance.md) 小智工具调用边界 | `X-Tool-Token`、日志、安全边界 |
| [release_operations_runbook.md](release_operations_runbook.md) 公网演示环境 | 公网 URL、HTTPS、CORS |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [open_source_selection.md](open_source_selection.md) | 判断是否越界到自建小智服务端时 |

不需要看：

- 前端页面实现细节。
- 硬件接线细节。
- 市场化文档。

### 验收/QA

必读：

| 文档 | 用途 |
| --- | --- |
| [development_task_ownership.md](development_task_ownership.md) 第 9 章 | 最终验收路径 |
| [testing_and_quality.md](testing_and_quality.md) | 质量门、回归清单 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、10、11 节 | P0 功能、非功能验收、确认项 |
| [release_operations_runbook.md](release_operations_runbook.md) | 演示前检查、故障处理、回滚 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| [web_api_contract.md](web_api_contract.md) | 验证 API 状态码、错误码、字段时 |
| [security_and_data_governance.md](security_and_data_governance.md) | 验证 token、GPS、日志、权限边界时 |

不需要看：

- 竞品分析。
- 市场化长期规划。
- 开源选型全文，除非验收新增依赖。

## 3. 后端模块

### 3.1 负责范围

后端研发负责 Django/DRF + PostgreSQL 的业务数据、API、Admin、演示数据初始化和接口鉴权。

涉及目录：

```text
backend/
  apps/devices/
  apps/agents/
  apps/spots/
  apps/nfc_tags/
  apps/checkins/
  apps/datasets/
  apps/demo/
  config/
```

### 3.2 输入资料

- [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md)
- [web_api_contract.md](web_api_contract.md)
- [security_and_data_governance.md](security_and_data_governance.md)
- [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md)
- [testing_and_quality.md](testing_and_quality.md)

### 3.3 P0 任务

| 编号 | 任务 | 验收 |
| --- | --- | --- |
| BE-01 | 建立 PostgreSQL 数据模型 | 设备、角色、点位、NFC、打卡、数据集表可迁移 |
| BE-02 | 建立 Django Admin | 可通过 Admin 管理核心数据 |
| BE-03 | 实现设备配置接口 | `device_simulator` 可拉取设备、角色、点位、NFC 配置 |
| BE-04 | 实现设备心跳接口 | 设备最近在线状态可更新 |
| BE-05 | 实现 GPS 上报接口 | 约 10 秒一次 GPS 位置信息可接收，保存最近位置和定位质量 |
| BE-06 | 实现 NFC 打卡接口 | 合法标签成功，非法标签失败，重复打卡幂等 |
| BE-07 | 实现数据集状态接口 | 前端可查看数据集状态、片段摘要、关联角色或点位 |
| BE-08 | 实现演示总览接口 | 前端可聚合展示设备、角色、GPS/NFC、打卡、数据集 |
| BE-09 | 实现手动模拟打卡接口 | 生成 `source=simulation` 记录 |
| BE-10 | 实现演示种子数据初始化 | 一条命令生成演示设备、角色、点位、NFC、数据集 |
| BE-11 | 实现小智工具接口基础能力 | `/agents/{agent_id}/context`、`/knowledge/search` 可被公网调用验证 |
| BE-12 | 建立真实硬件测试数据重置命令 | 可一键清空模拟/手工打卡和手工心跳状态，保留 `device_001` 配置供真实 ESP32 拉取 |
| BE-13 | 支持局域网真实设备联调 | 后端监听 `0.0.0.0:8000` 时，ESP32 可通过电脑局域网 IP 调用 `/device-config` 和 `/device-heartbeats` |
| BE-14 | 建立真实 NFC `tag_id` 替换流程 | PN532 读到真实 UID 后，可替换占位标签并在前端/NFC 页面核对，不把占位标签当最终验收数据 |
| BE-15 | 建立角色配置版本与官网同步状态 | 角色 prompt、性格、voice_id、知识库引用有版本、同步状态、最后同步时间和失败原因 |
| BE-16 | 建立对话记录模型 | 可保存设备、角色、用户输入、AI 回复、来源、点位、时间和摘要 |
| BE-17 | 建立官网同步日志 | 可记录人工/半自动同步到小智官网的配置快照、操作人、状态和错误 |
| BE-18 | 建立工具调用日志 | 小智工具/MCP 调用我方接口时有入参摘要、结果、耗时、失败原因和 token 脱敏日志 |

### 3.4 明确不做

- 不启用 pgvector。
- 不使用 SQLite 沉淀演示数据。
- 不做复杂 RBAC、多租户、企业 SSO。
- 不把小智官网账号、数据库密码、token 明文返回给前端。

### 3.5 交付物

- 数据模型和 migration。
- DRF serializer / view / url。
- Django Admin 配置。
- `.env.example` 后端变量说明。
- 演示数据初始化命令或脚本。
- 后端 README 更新。
- 最低测试或手动验证记录。

### 3.6 后端完成标准

```powershell
cd backend
python manage.py check
python manage.py migrate
```

并满足：

- API 与 [web_api_contract.md](web_api_contract.md) 不冲突。
- 设备 token 日志脱敏。
- 模拟数据有 `source=simulation`。
- GPS 不保存长期连续轨迹。
- PostgreSQL 为主线数据库。

### 3.7 真实硬件联调追加任务（2026-07-18）

触发背景：用户已开始接入真实 ESP32-S3、GPS、麦克风、后续 PN532/NFC、电池与功放喇叭。研发主管已要求删除当前假数据，后续演示数据必须能区分“真实硬件上报”和“模拟器/手工模拟”。

后端研发接手前只需要阅读：

- 本文件第 3 章、第 9-12 章。
- [web_api_contract.md](web_api_contract.md) 中设备配置、心跳、GPS、NFC 打卡接口。
- [release_operations_runbook.md](release_operations_runbook.md) 第 3.4 节。
- [testing_and_quality.md](testing_and_quality.md) QG-2、QG-5。
- [phase1_acceptance_handoff.md](phase1_acceptance_handoff.md) 第 7、8 节。

当前真实硬件联调基线：

| 项 | 当前值/规则 |
| --- | --- |
| 设备 ID | `device_001` |
| 设备 token | `demo-device-token` |
| 本机局域网 API 示例 | `http://192.168.168.155:8000/api/v1`，实际以运行机器当天 IP 为准 |
| ESP32 访问地址 | 禁止写 `127.0.0.1`，必须使用电脑局域网 IP 或公网地址 |
| 当前数据库状态 | 已清空打卡记录；`device_001` 保留配置但在线状态重置为 `unknown` |
| NFC 标签 | 当前 `04AABBCCDD` 仅为占位；PN532 读到真实 UID 后必须替换或新增真实标签 |
| 真实在线判定 | 只能由真实 ESP32 调用 `/device-heartbeats` 后形成，不用模拟器或手工请求冒充验收 |

后端 agent 的落地任务：

1. 增加或整理一个后端管理命令，例如 `reset_hw_test_data`，用于真实硬件验收前清空模拟打卡、手工打卡、过期心跳、旧 GPS 状态，同时保留最小配置。
2. 补充 `seed_demo` 或独立命令参数，明确“演示种子数据”和“真实硬件测试基线”的区别。
3. 用局域网 IP 验证：
   - `GET /api/v1/device-config`
   - `POST /api/v1/device-heartbeats`
   - 请求头包含 `X-Device-Id` 和 `X-Device-Token`
4. 修正 README 或运行手册中的示例，避免硬件研发误填 `127.0.0.1`。
5. 在测试记录中写明本轮是否由真实 ESP32 触发；没有真实串口/设备证据时，不得把联调标记为 ACC-07 完成。

完成标准：

- `python manage.py check` 通过。
- `python manage.py migrate --check --noinput` 通过。
- 真实硬件测试基线命令可重复执行，重复执行不破坏 `device_001` 配置。
- 前端总览页能在真实 ESP32 心跳后显示设备在线；未收到真实心跳时保持未知/离线。

#### 2026-07-18 BE-13 执行记录

| 子项 | 状态 | 真实证据 |
| --- | --- | --- |
| ESP32 调用 `/device-heartbeats` | 通过；18:47 阻塞已解除 | 2026-07-19 家庭网再次验证：ESP32 `192.168.1.10` 连续两次 `Heartbeat accepted: HTTP 200`；PostgreSQL 中 `device_001=online`、`last_seen_at=2026-07-19T05:16:01.306886+00:00`、`firmware_version=blindbox-2.2.6`。此前 2026-07-18 办公网验证证据继续保留 |
| ESP32 调用 `/device-config` | 待验收 | 当前无设备侧调用日志，不用电脑手工请求替代 |
| 局域网地址与白名单 | 通过本轮环境验证 | ESP32 `192.168.101.10`，电脑 WLAN `192.168.101.119`；本地 `.env` 已加入当天地址；下次联调需重新确认 IP |
| GPS/NFC 真实事件 | 待验收 | `last_gps_status=not_connected`；尚无 PN532 `tag_id` |

因此 BE-13 当前为**部分通过**：真实 ESP32 心跳已接入自研平台，但设备配置拉取和 GPS/NFC 事件仍需后续设备侧证据。

## 4. 前端模块

### 4.1 负责范围

前端研发负责 React + Vite + Ant Design 页面、API 调用、状态展示、三端适配和演示可视化。

涉及目录：

```text
frontend/
  src/
```

### 4.2 输入资料

- [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md)
- [web_api_contract.md](web_api_contract.md)
- [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md)
- [testing_and_quality.md](testing_and_quality.md)

### 4.3 P0 页面

| 编号 | 页面 | 验收 |
| --- | --- | --- |
| FE-01 | 登录/演示账号入口 | 可进入演示模式，不暴露密码或 token |
| FE-02 | 演示总览页 | 展示设备在线、角色、GPS、NFC、打卡、数据集状态 |
| FE-03 | 设备页 | 展示 device_id、绑定角色、最近在线、最近 GPS 状态 |
| FE-04 | 角色页 | 展示和编辑角色名称、prompt、voice_id、数据集关联 |
| FE-05 | 景点/点位页 | 展示和编辑点位、经纬度、半径、启用状态 |
| FE-06 | NFC 标签页 | 展示 tag_id、绑定点位、启用状态、最近识别 |
| FE-07 | 数据集页 | 展示数据集状态、片段摘要、关联角色或点位 |
| FE-08 | 打卡记录页 | 展示成功、失败、重复、模拟打卡记录 |
| FE-09 | 手动模拟打卡页 | 可触发模拟记录，并明显标记模拟数据 |
| FE-10 | 对话记录页 | 展示会话、用户内容、AI 回复、关联设备/角色/点位和来源 |
| FE-11 | 角色配置版本页 | 展示 prompt、性格、voice_id、知识库引用、配置版本和预览 |
| FE-12 | 官网同步状态页 | 展示每个角色/设备是否已同步到小智官网、最后同步时间、失败原因和人工操作备注 |

### 4.4 状态要求

每个核心页面必须有：

- loading
- empty
- error
- success
- disabled/offline 状态

演示总览页必须能解释失败原因：

- 后端不可用
- 设备离线
- GPS 无 fix
- NFC 标签未登记
- NFC 标签停用
- 重复打卡
- 数据集失败

### 4.5 明确不做

- 不引入 Ant Design Pro 完整模板。
- 不引入复杂状态管理库，除非研发主管确认。
- 不在前端写死 token、数据库连接、小智账号。
- 不做商城、支付、用户 App。

### 4.6 交付物

- 页面和路由。
- API client。
- 三端适配样式。
- 前端 README 更新。
- 页面截图或手动验收记录。

### 4.7 前端完成标准

```powershell
cd frontend
npm run build
```

并满足：

- PC/平板/手机核心信息不遮挡。
- 真实记录和模拟记录可区分。
- 接口失败时页面有可读错误。
- 不展示完整 token。

## 5. 联调工具模块

### 5.1 负责范围

联调研发负责 `device_simulator`，在真实硬件不稳定或未到货时，先跑通完整软件闭环。

涉及目录：

```text
tools/device_simulator/
```

### 5.2 输入资料

- [web_api_contract.md](web_api_contract.md)
- [testing_and_quality.md](testing_and_quality.md)
- [release_operations_runbook.md](release_operations_runbook.md)

### 5.3 P0 任务

| 编号 | 任务 | 验收 |
| --- | --- | --- |
| SIM-01 | 支持配置后端 base URL | 可切换本地/公网后端 |
| SIM-02 | 支持配置 `device_id`、`device_token` | 可模拟合法/非法设备 |
| SIM-03 | 拉取设备配置 | 返回角色、点位、NFC 标签 |
| SIM-04 | 上报心跳 | 后端设备状态变化 |
| SIM-05 | 约 10 秒 GPS 位置上报 | 后端最近位置更新 |
| SIM-06 | GPS 接近事件模拟 | 前端显示接近状态 |
| SIM-07 | NFC 成功打卡 | 后端生成成功记录 |
| SIM-08 | NFC 异常用例 | 未登记、停用、重复打卡均可模拟 |
| SIM-09 | 模拟打卡来源标记 | 所有模拟记录带 `source=simulation` |

### 5.4 明确不做

- 不模拟完整小智语音链路。
- 不替代真实 ESP32 验收。
- 不生成和真实设备混淆的生产编号。

### 5.5 交付物

- 可执行脚本。
- `.env.example` 或配置示例。
- README 命令说明。
- 成功和失败用例输出样例。

### 5.6 联调工具完成标准

至少能按顺序跑通：

```text
拉配置 -> 心跳 -> GPS 上报 -> GPS 接近 -> NFC 打卡 -> 前端看到记录
```

## 6. 硬件固件模块

### 6.1 负责范围

硬件/固件研发负责 ESP32-S3、小智固件、GPS、PN532 NFC、麦克风、功放、电池供电和串口日志。

涉及目录和资料：

```text
main/
docs/blindbox_project/phase1_single_robot_budget.md
docs/blindbox_project/espidf_runbook.md
docs/blindbox_project/phase1_hardware_wiring_manual.md
```

### 6.2 输入资料

- [phase1_single_robot_budget.md](phase1_single_robot_budget.md)
- [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md)
- [web_api_contract.md](web_api_contract.md)
- [testing_and_quality.md](testing_and_quality.md)
- [espidf_runbook.md](espidf_runbook.md)
- [phase1_hardware_wiring_manual.md](phase1_hardware_wiring_manual.md)

### 6.3 P0 任务

| 编号 | 任务 | 验收 |
| --- | --- | --- |
| HW-01 | 确认 ESP32-S3 开发板型号 | 可运行小智固件 |
| HW-02 | 接入麦克风和功放 | 小智基础语音可听可说 |
| HW-03 | 接入 GPS | NEO-6M 或 ATGM336H 输出 UART NMEA |
| HW-04 | 接入 PN532 NFC | 可读取合法 NFC 标签 |
| HW-05 | 实现 GPS 约 10 秒上报 | 后端看到最近位置和定位质量 |
| HW-06 | 实现 NFC 打卡调用 | 合法标签触发后端打卡接口 |
| HW-07 | 保留小智原语音链路 | 唤醒、对话、播放不被破坏 |
| HW-08 | 串口日志可诊断 | GPS、NFC、网络、后端错误有日志 |
| HW-09 | 电池供电演示验证 | 可脱离电脑完成短时演示 |

### 6.3.1 2026-07-25 硬件工程师当前任务包

当前背景：小智官网语音链路已由真实硬件跑通；INMP441 麦克风通过；MAX98357A + 3W 喇叭已能实体发声但杂音较大；真实 ESP32 心跳已进入自研后端。下一步不能继续把 Wi-Fi 当定位能力，Wi-Fi 只代表联网，不能替代 GPS 经纬度。

硬件工程师接手前只读以下文档，避免 token 消耗过大：

- 本文件第 6 章、第 9-10 章。
- [phase1_hardware_wiring_manual.md](phase1_hardware_wiring_manual.md) 全文。
- [espidf_runbook.md](espidf_runbook.md) 第 2、3、5、6、10、11、12.1、12.2 节。
- [web_api_contract.md](web_api_contract.md) 第 5.1-5.4 节。
- [testing_and_quality.md](testing_and_quality.md) QG-5 与第 8.1 节。

当前硬件任务状态：

| 任务 | 当前状态 | 下一步 |
| --- | --- | --- |
| HW-01 ESP32-S3 | 通过 | 保持现有板卡和串口记录，不重新选板 |
| HW-02 麦克风/功放 | 功能通过，音质待优化 | 降低音量/增益、缩短 I2S 线、检查共地和电源去耦；不因杂音阻塞 GPS/NFC 主线 |
| HW-03 GPS | 未通过 | 先解决 GPIO18 冲突；确认新的 GPS UART RX/TX；再接 NEO-6M 读 NMEA |
| HW-04 PN532 NFC | 未通过 | 先确认实物接口模式和电压，再接线读取真实 UID/tag_id |
| HW-05 GPS 上报 | 未开始 | NMEA 读通后按约 10 秒调用 `/api/v1/location-events` |
| HW-06 NFC 打卡 | 未开始 | 读到真实 tag_id 后调用 `/api/v1/checkins`，后端替换占位标签 |
| HW-07 小智语音链路 | 通过 | 后续改 GPS/NFC 时必须回归：唤醒、识别、官网记录、喇叭播放 |
| HW-08 串口诊断 | 部分通过 | 补 GPS/NFC/device-config 成功和失败日志 |
| HW-09 电池供电 | 未开始 | GPS/NFC/喇叭稳定后再接 TP4056、升压和 18650 |

硬件工程师本轮只做四个 P0 闭环：

1. `device-config` 设备侧拉取：ESP32 开机或联网后调用 `GET /api/v1/device-config`，串口打印成功/失败摘要，不输出 token。
2. GPS：确认安全引脚，读取 NMEA，能区分 `fix` / `no fix`，再按约 10 秒上报定位摘要。
3. NFC：确认 PN532 接口，读取真实 UID，交给后端替换占位 tag，随后触发真实打卡。
4. 电池后置：前三项稳定前不接电池；电池只做短时演示压测，不做低功耗优化。

禁止事项：

- 禁止继续把 GPS TX 接 GPIO18。
- 禁止用 Wi-Fi 连接状态冒充 GPS 定位。
- 禁止同时新增 GPS、PN532、电池三个模块。
- 禁止在串口、截图、文档中输出 Wi-Fi 密码、激活码、device token。
- 禁止为了接 GPS/NFC 破坏已通过的小智官网语音链路。

交付证据格式：

```text
模块：
接线照片：
修改 main/ 文件：
串口关键日志：
后端接口日志：
前端页面核对：
是否真实硬件触发：
失败项：
下一步：
```

### 6.4 必须补充的硬件文档

硬件研发必须补：

- [espidf_runbook.md](espidf_runbook.md)
- [phase1_hardware_wiring_manual.md](phase1_hardware_wiring_manual.md)
- GPS 接线表
- PN532 接线表
- 麦克风/功放接线表
- 烧录命令
- 串口日志判断标准
- 常见故障处理

### 6.5 明确不做

- 不重写小智语音服务端。
- 不改坏原有小智状态机和基础语音链路。
- 不做正式外壳。
- 不做复杂低功耗优化。
- 不做动态 NFC 防复制。

### 6.6 硬件完成标准

必须现场或视频证明：

- 设备可启动并联网。
- 小智基础语音可用。
- GPS 有有效 NMEA 或明确显示无 fix。
- PN532 可读取标签。
- 后端收到 GPS 和 NFC 事件。
- 前端演示页能看到真实设备状态。

## 7. 部署模块

### 7.1 负责范围

部署研发负责公网演示环境。研发主管最终负责公网演示是否可用。

涉及目录：

```text
deploy/
backend/.env.example
frontend/.env.example
```

### 7.2 输入资料

- [release_operations_runbook.md](release_operations_runbook.md)
- [security_and_data_governance.md](security_and_data_governance.md)
- [open_source_selection.md](open_source_selection.md)
- [web_api_contract.md](web_api_contract.md)

### 7.3 P0 任务

| 编号 | 任务 | 验收 |
| --- | --- | --- |
| DEP-01 | 准备公网服务器 | 后端可从公网访问 |
| DEP-02 | 配置 PostgreSQL | 后端连接正式演示库，不使用 SQLite |
| DEP-03 | 配置 Gunicorn | Django API 可由进程服务承载 |
| DEP-04 | 配置 Nginx | API 反代和前端静态资源可访问 |
| DEP-05 | 配置 HTTPS 或短期公网 HTTP 验证 | 小智工具调用和前端访问可验证 |
| DEP-06 | 配置 CORS | 只放行演示前端地址 |
| DEP-07 | 配置环境变量 | `DEVICE_TOKEN`、`XIAOZHI_TOOL_TOKEN`、数据库连接不入库 |
| DEP-08 | 配置前端 API base URL | 前端访问公网后端 |
| DEP-09 | 公网 smoke test | 设备/模拟器/前端均能访问公网后端 |

### 7.4 明确不做

- 不引入 Docker Compose。
- 不建设完整 CI/CD。
- 不建设高可用、自动扩缩容、蓝绿发布。
- 不建设完整生产审计和安全运营体系。

### 7.5 部署完成标准

公网演示环境必须通过：

```text
后端 health/check -> 前端访问 -> 模拟器公网拉配置 -> 模拟器公网打卡 -> 前端看到记录
```

## 8. 小智工具/MCP 验证模块

### 8.1 负责范围

该模块是技术验证项，由联调研发或部署研发执行，研发主管兜底。

### 8.2 P0 任务

| 编号 | 任务 | 验收 |
| --- | --- | --- |
| MCP-01 | 确认小智官网侧工具配置方式 | 能配置调用我方公网接口 |
| MCP-02 | 验证上下文接口 | 可调用 `/api/v1/agents/{agent_id}/context` |
| MCP-03 | 验证知识查询接口 | 可调用 `/api/v1/knowledge/search` |
| MCP-04 | 验证 token | 无 token 或错误 token 被拒绝 |
| MCP-05 | 验证超时兜底 | 接口失败时不影响基础播报兜底 |
| MCP-06 | 记录工具调用日志 | 每次 context/knowledge 调用有调用摘要、结果、耗时、失败原因 |
| MCP-07 | 建立官网同步操作记录 | 官网侧工具、prompt、voice_id 的人工同步结果能在我方平台留痕 |

### 8.3 完成标准

- 小智侧能成功调用至少一个我方公网接口。
- 失败时有明确日志。
- 如果官网工具/MCP 不稳定，演示仍可走固定播报或后端预置上下文兜底。

## 8.4 2026-07-26 产品经理最新 P0 后的研发待办分配

本节用于承接产品经理最新确认项，避免前端、后端、硬件分别理解导致口径不一致。

依据文档：

| 文档 | 需关注内容 |
| --- | --- |
| [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md) | D-13、D-14、D-15；第 3 节 P0；第 5.1.2、5.1.6 节 |
| [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | 页面清单、角色智能体配置、A-09-1、A-09-2 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) | R-P0-32、R-P0-33、R-P0-34、R-P0-35；R-P1-05 |
| [mvp_product_alignment.md](mvp_product_alignment.md) | T-P0-16、T-P0-17、T-P0-18；Q-05、Q-06、Q-07 |

### 8.4.1 后端研发待办

目标：让自研平台成为一期“角色配置源”和“演示数据中心”。即使小智官网仍负责真实语音链路，自研平台也必须能看到配置、同步状态、对话记录和操作留痕。

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| BE-PM-01 | 扩展角色/智能体配置模型 | `Agent` 或关联配置表，包含提示词/性格设定、`voice_id`、知识引用、配置版本、官网同步状态、最近同步时间 | 修改角色配置后，后端能标记为“待同步到官网” |
| BE-PM-02 | 实现对话记录模型和 API | `ConversationSession`、`ConversationMessage` 的迁移、序列化、列表/详情接口 | 至少返回设备、角色、用户输入、AI 回复、景点、知识片段摘要、时间、来源 |
| BE-PM-03 | 实现官网同步快照/日志 API | `OfficialSyncLog` 或等价表；提供待复制到官网的配置快照 | 能记录“待同步/已同步/失败/需人工处理”、操作者、时间、备注 |
| BE-PM-04 | 清理假数据并补真实演示测试数据 | seed 命令中加入最小真实演示数据；标记数据来源 | 前端打开不空白，且数据可解释为演示机器人真实链路测试数据 |
| BE-PM-05 | 补接口权限和脱敏 | device token、tool token、后台接口不泄露密钥 | API 响应不返回真实 token/密码 |
| BE-PM-06 | 补迁移和测试 | Django migration、`manage.py check`、核心 API 测试 | PostgreSQL 下迁移通过，核心接口返回 2xx/4xx 符合契约 |

暂缓项：`ToolInvocationLog` 属于 P1，可以先建模型或预留接口，但不得影响 P0 对话记录和官网同步状态交付。

后端研发只需优先阅读：

- 本文第 3 章和第 8.4 节。
- [web_api_contract.md](web_api_contract.md)。
- [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、8、10 节。
- [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md) D-13、D-14、D-15。

### 8.4.2 前端研发待办

目标：让演示时“看起来是一套完整自研平台”，能看到角色设置、对话内容、官网同步状态和同步快照。

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| FE-PM-01 | 角色配置页增强 | 展示/编辑提示词、性格设定、`voice_id`、知识引用、配置版本 | 修改后页面显示“待同步到官网” |
| FE-PM-02 | 官网同步状态展示 | 状态标签、最近同步时间、操作者、失败原因 | 支持“待同步/已同步/失败/需人工处理” |
| FE-PM-03 | 官网同步快照页 | 可复制的官网配置快照，包括提示词、音色、工具 URL、知识引用 | 演示人员能按页面内容手动同步到小智官网 |
| FE-PM-04 | 对话记录页 | 列表、筛选、详情，支持设备/角色/时间/景点/来源筛选 | 能看到用户输入、AI 回复、知识片段摘要、来源 |
| FE-PM-05 | 首页入口和空状态 | 首页/侧边栏加入对话记录、官网同步状态入口 | 无数据、加载中、失败状态都有明确提示 |
| FE-PM-06 | 构建验证 | `npm run build` | 构建通过，PC/平板/手机宽度下无阻塞性问题 |

暂缓项：工具调用日志页面属于 P1，不阻塞一期演示；如果后端已提供模型，可只放入口或占位状态。

前端研发只需优先阅读：

- 本文第 4 章和第 8.4 节。
- [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md)。
- [web_api_contract.md](web_api_contract.md)。
- [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) 第 6、8、10 节。

### 8.4.3 硬件/固件研发待办

目标：保持小智官网语音链路已跑通的成果，同时把真实设备状态、配置版本、GPS/NFC 和必要对话证据接入自研平台。

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| HW-PM-01 | 保持小智官网语音链路稳定 | 串口日志、官网记录、现场视频/照片 | 唤醒、收音、回复、喇叭播放均可复现 |
| HW-PM-02 | 接入自研平台配置拉取 | 固件调用 `GET /api/v1/device-config`，日志打印配置版本 | ESP32 使用局域网 IP 或公网域名访问，不能写 `127.0.0.1` |
| HW-PM-03 | 接入设备心跳 | 固件调用 `POST /api/v1/device-heartbeats` | 后端和前端能显示设备在线 |
| HW-PM-04 | 提供对话记录导入证据 | 如果官网暂不能自动回传对话，则提供串口日志/人工导入字段规范 | 自研平台能形成至少一条真实演示对话记录 |
| HW-PM-05 | GPS 验证 | 避开 GPIO18 冲突，完成 NMEA 读取和位置上报 | 平台能看到真实或明确标记的 GPS 测试点 |
| HW-PM-06 | NFC 验证 | PN532 读取真实 UID，并上报打卡 | 平台能看到真实 NFC tag_id/checkin |
| HW-PM-07 | 硬件变更控制 | 每次只改一个模块，电池最后接入 | 出问题能快速回退，不把音频、GPS、NFC、电池一起混改 |

硬件侧约束：

- Wi-Fi 只负责联网，不等同于 GPS 定位。
- GPS 不使用 GPIO18；该脚位已与当前固件灯控存在冲突风险。
- 电池、TP4056、升压/供电链路放到 GPS/NFC/音频稳定之后再处理。
- 固件日志不得打印真实 `device_token`。

硬件/固件研发只需优先阅读：

- 本文第 6 章和第 8.4 节。
- [phase1_hardware_wiring_manual.md](phase1_hardware_wiring_manual.md)。
- [espidf_runbook.md](espidf_runbook.md)。
- [web_api_contract.md](web_api_contract.md) 设备、心跳、GPS、NFC 相关章节。
- [phase1_single_robot_budget.md](phase1_single_robot_budget.md) 已采购硬件清单。

### 8.4.4 跨模块执行顺序

| 顺序 | 模块 | 交付点 |
| --- | --- | --- |
| 1 | 后端 | 先落库表、迁移、API、seed 数据 |
| 2 | 前端 | 基于后端 API 做角色配置、对话记录、官网同步页 |
| 3 | 硬件/固件 | 先接 device-config/heartbeat，再接 GPS/NFC，对话记录先走可导入证据 |
| 4 | 小智官网同步 | 先人工/半自动同步提示词、音色、工具 URL，并在自研平台留痕 |
| 5 | 研发主管验收 | 用一条真实演示链路贯穿：角色配置 -> 官网同步 -> 设备在线 -> 对话记录 -> GPS/NFC |

### 8.4.5 可直接发给各研发 Agent 的任务句

后端 Agent：

> 请只阅读 `docs/blindbox_project/development_task_ownership.md` 第 3 章和第 8.4 节、`docs/blindbox_project/web_api_contract.md`、`docs/blindbox_project/requirements_and_feature_inventory.md` 第 6/8/10 节、`docs/blindbox_project/product_manager_handoff_checklist.md` D-13/D-14/D-15，然后完成 BE-PM-01 到 BE-PM-06；重点是角色配置源、对话记录、官网同步快照/日志、真实演示 seed 数据、PostgreSQL 迁移和 API 测试。

前端 Agent：

> 请只阅读 `docs/blindbox_project/development_task_ownership.md` 第 4 章和第 8.4 节、`docs/blindbox_project/django_react_frontend_product_interaction_spec.md`、`docs/blindbox_project/web_api_contract.md`、`docs/blindbox_project/requirements_and_feature_inventory.md` 第 6/8/10 节，然后完成 FE-PM-01 到 FE-PM-06；重点是角色配置页、对话记录页、官网同步状态/快照页和构建验证。

硬件/固件 Agent：

> 请只阅读 `docs/blindbox_project/development_task_ownership.md` 第 6 章和第 8.4 节、`docs/blindbox_project/phase1_hardware_wiring_manual.md`、`docs/blindbox_project/espidf_runbook.md`、`docs/blindbox_project/web_api_contract.md` 设备/GPS/NFC 相关章节、`docs/blindbox_project/phase1_single_robot_budget.md` 已采购清单，然后完成 HW-PM-01 到 HW-PM-07；重点是保持小智官网语音链路稳定、接入自研平台 device-config/heartbeat、验证 GPS/NFC，并提供可进入自研平台的真实对话记录证据。

## 8.5 2026-07-26 实时对话入库链路任务

本节承接用户最新确认：一期不优先从小智官网后台拉取历史聊天记录。既然硬件端已经能在小智官方语音链路中捕获 user/assistant 文本，就采用“硬件实时上报，我方后端按句入库”的方式形成真实对话记录。

目标链路：

```text
用户对 ESP32 说话
  -> ESP32 连接小智官方语音链路
  -> 固件捕获 user/assistant 文本和 official_session_id
  -> ESP32 POST 到我方 Django
  -> Django 写入 ConversationSession / ConversationMessage
  -> 前端用户端展示最近真实对话和当前沟通状态
```

### 8.5.1 后端任务

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| BE-RT-01 | 新增设备鉴权的对话事件上报接口 | `POST /api/v1/device-conversation-events` | 使用 `X-Device-Id` / `X-Device-Token`，不要求后台登录 |
| BE-RT-02 | 按官网 session 聚合会话 | 根据 `official_session_id` 自动创建或复用 `ConversationSession` | 同一 `official_session_id` 下 user/assistant 消息进入同一会话 |
| BE-RT-03 | 按句写入消息 | 每次上报写入一条 `ConversationMessage` | user/assistant 顺序和时间可追溯 |
| BE-RT-04 | 后端绑定关系兜底 | 不盲信设备传入的 `agent_id`，优先以后端 `device_id -> bound_agent` 为准 | 设备传错 agent_id 不会污染绑定关系 |
| BE-RT-05 | 用户端最近对话查询 | 最近真实对话查询接口或复用现有 conversation 接口加过滤 | 前端可展示当前设备最近若干条真实对话 |
| BE-RT-06 | 测试与脱敏 | 单元测试/API smoke，日志不打印 device token | `manage.py check` 通过，测试覆盖鉴权、创建会话、追加消息 |

建议请求体：

```json
{
  "official_session_id": "a4681f38",
  "role": "user",
  "content": "帮我介绍一下这个景点",
  "content_source": "xiaozhi_official_device_log",
  "session_source": "xiaozhi_official",
  "agent_id": "agent_alo",
  "spot_id": "spot_gate_001",
  "created_at": "2026-07-26T21:30:00+08:00"
}
```

#### 8.5.1.1 后端执行记录（2026-07-26）

| 编号 | 状态 | 实际交付与验证 |
| --- | --- | --- |
| BE-RT-01 | 已完成 | 新增 `POST /api/v1/device-conversation-events`，复用 `X-Device-Id` / `X-Device-Token` 鉴权，不要求后台登录；错误 token 返回 `401 invalid_device_token` |
| BE-RT-02 | 已完成 | `ConversationSession` 新增 `official_session_id`，并增加 `(device, official_session_id)` 唯一约束；同一设备的同一官网 session 自动复用 |
| BE-RT-03 | 已完成 | 每个有效事件新增一条 `ConversationMessage`；首次建会话返回 `201`，后续追加返回 `200`，角色与时间可追溯 |
| BE-RT-04 | 已完成 | 会话 `agent` 强制取后端 `DeviceBinding`；请求中的 `agent_id` 只作为审计 metadata，错误报告值不会污染绑定关系 |
| BE-RT-05 | 已完成 | 复用 `GET /api/v1/conversation-sessions?device_id=...` 和 `GET /api/v1/user/companion`，未重复建立 conversation 查询资源 |
| BE-RT-06 | 已完成 | metadata 对 token、password、secret、authorization、credential、API key、access key、private key、cookie 等敏感键递归遮蔽；响应不回显设备凭据 |

数据库迁移 `conversations.0002_conversationsession_official_session_id` 已应用到 PostgreSQL。后端全量 29 项测试通过，`manage.py check`、`makemigrations --check`、`migrate --check` 均通过。后端测试覆盖设备鉴权、会话创建与复用、逐句追加、绑定角色优先、非法角色拒绝和敏感 metadata 脱敏。

### 8.5.2 硬件/固件任务

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| HW-RT-01 | 扩展 `CONVERSATION_EVIDENCE` | 捕获 user/assistant 文本后继续打印串口证据 | 断网时仍有可读兜底日志 |
| HW-RT-02 | 实时 POST 对话事件 | 固件调用 `POST /api/v1/device-conversation-events` | 每句 user/assistant 都能进入后端 |
| HW-RT-03 | 设备鉴权 | 请求头带 `X-Device-Id` / `X-Device-Token` | 后端认证通过，串口不打印明文 token |
| HW-RT-04 | 会话字段 | 上报 `official_session_id`、`role`、`content`、来源、时间 | 后端可按官方 session 聚合 |
| HW-RT-05 | 失败兜底 | 网络失败时不影响小智语音链路 | 对话继续，串口保留待补证据 |

#### 8.5.2.1 硬件/固件执行记录（2026-07-26）

HW-RT-01～HW-RT-05 已完成真实硬件验收：

| 编号 | 状态 | 实机证据 |
| --- | --- | --- |
| HW-RT-01 | 通过 | 官方链路每次捕获 user/assistant 句子时继续打印完整 `CONVERSATION_EVIDENCE` |
| HW-RT-02 | 通过 | 独立 FreeRTOS 队列异步 POST；真实会话首句返回 HTTP 201，后续 8 句返回 HTTP 200 |
| HW-RT-03 | 通过 | 复用 `X-Device-Id` / `X-Device-Token`；串口、文档和提交文件均未输出明文 token |
| HW-RT-04 | 通过 | 每句包含 `official_session_id`、`role`、`content`、`content_source`、`session_source` 和带 `+08:00` 的 ISO 8601 时间 |
| HW-RT-05 | 通过 | HTTP 在独立任务执行；网络/队列/内存失败分支只记录告警并保留串口证据，不阻塞官方 STT/TTS 回调 |

真实验收会话：

```text
official_session_id=d0d109c0
device_id=device_001
agent_id=agent_alo（以后端绑定关系为准）
source=device_log
message_count=9
```

串口关键结果：

```text
CONVERSATION_EVIDENCE {..."role":"user"...}
Conversation event accepted: HTTP 201
CONVERSATION_EVIDENCE {..."role":"assistant"...}
Conversation event accepted: HTTP 200
```

用户确认喇叭正常回应；同轮心跳和 GPS 约 10 秒上报继续返回 HTTP 200，证明实时对话入库没有破坏小智官方语音链路。当前刷入固件 SHA-256 为 `B9201141E7F004F6C58FFD7D633CAE04E62FFB933365CED1953722190B33208D`。

### 8.5.3 前端任务

| 编号 | 任务 | 输出物 | 验收标准 |
| --- | --- | --- | --- |
| FE-RT-01 | 修正用户端“锁死”表达 | 文案改为“已绑定专属伙伴 / 用户不可自行切换” | 不再出现“锁死”“锁定不可用”等误导文案 |
| FE-RT-02 | 我的伙伴页展示真实状态 | 当前绑定角色、设备在线、聆听/思考/回复/空闲状态 | 用户能理解设备已连接且正在对话 |
| FE-RT-03 | 展示最近真实对话 | 从后端 conversation 接口读取最近消息 | 不使用前端假数据冒充实时对话 |
| FE-RT-04 | 轻量刷新 | 先用 3-5 秒轮询刷新，后续再评估 WebSocket | 新消息能在用户端较快出现 |
| FE-RT-05 | 来源标识 | 明确显示 `xiaozhi_official_device_log` / `manual_import` / `simulation` 等来源 | 真实、模拟、手工导入不混淆 |

#### 2026-07-26 FE-RT 执行记录

| 编号 | 完成情况 | 实现位置 | 验证结果 |
| --- | --- | --- | --- |
| FE-RT-01 | 已完成 | `frontend/src/app/App.tsx`、`frontend/src/pages/UserExperiencePages.tsx` | 用户端统一使用“已绑定专属伙伴，用户不可自行切换”；源码扫描未发现“锁死”“锁定不可用”“未解锁不可用” |
| FE-RT-02 | 已完成前端展示 | `frontend/src/pages/UserExperiencePages.tsx` | 展示当前绑定角色、设备在线状态、最近在线时间和根据最近入库消息呈现的对话状态；真实硬件状态仍以联调结果为准 |
| FE-RT-03 | 已完成 | `frontend/src/pages/UserExperiencePages.tsx`、`frontend/src/shared/types.ts` | 从 `GET /api/v1/user/companion?recent_limit=5` 返回的 `recent_conversations.messages` 渲染最近消息；已删除静态示例问答 |
| FE-RT-04 | 已完成 | `frontend/src/shared/useApi.ts`、`frontend/src/pages/UserExperiencePages.tsx` | 使用 5 秒静默轮询；轮询时不切回整页 loading 状态 |
| FE-RT-05 | 已完成前端识别与展示 | `frontend/src/shared/types.ts`、`frontend/src/pages/UserExperiencePages.tsx` | 仅将 `device_log` / `xiaozhi_official_device_log` 展示为最近真实硬件对话，并逐条展示来源；模拟、手工来源类型保持独立 |

前端验证命令：

```powershell
cd frontend
npm run build
```

验证结果：TypeScript 与 Vite 生产构建通过。当前结论仅代表前端实现和契约类型检查通过，不代表 ESP32 -> Django -> React 真实对话链路已经完成硬件验收；最终验收需由真实设备产生 user/assistant 消息并确认页面在 5 秒轮询窗口内更新。

### 8.5.4 可直接发给各研发 Agent 的任务句

后端 Agent：

> 请只阅读 `docs/blindbox_project/development_task_ownership.md` 第 8.5 节、`docs/blindbox_project/web_api_contract.md` 对话记录相关章节、`docs/blindbox_project/django_react_frontend_product_interaction_spec.md` 第 5.2 和 6.11 节，然后新增设备鉴权接口 `POST /api/v1/device-conversation-events`。ESP32 每次捕获小智官方链路的 user/assistant 文本后会上报该接口；后端需按 `official_session_id` 自动创建或复用 `ConversationSession`，每句写入 `ConversationMessage`，优先以后端设备绑定关系确定 agent，不要求后台登录，并补测试和脱敏。

硬件/固件 Agent：

> 请只阅读 `docs/blindbox_project/development_task_ownership.md` 第 8.5 节、`docs/blindbox_project/espidf_runbook.md`、`docs/blindbox_project/web_api_contract.md` 设备鉴权相关章节，然后把当前只打印串口的 `CONVERSATION_EVIDENCE` 扩展为同时 POST 到 `POST /api/v1/device-conversation-events`。每次捕获小智官方链路 user 文本或 assistant 回复时，都带 `official_session_id`、`role`、`content`、来源、时间和设备鉴权；失败时保留串口日志，不影响小智语音链路。

前端 Agent：

> 请只阅读 `docs/blindbox_project/django_react_frontend_product_interaction_spec.md` 第 5.2、6.11、12 节，`docs/blindbox_project/frontend_style_demo/interactive_prototype_design_notes.md` 用户端相关章节，以及 `docs/blindbox_project/development_task_ownership.md` 第 8.5 节，然后修正用户端文案：不要显示“锁死”，改成“已绑定专属伙伴，用户不可自行切换”；“我的伙伴”页展示当前绑定角色、设备在线/对话状态和从后端 conversation 接口读取的最近真实对话，先用 3-5 秒轮询刷新，不能用假数据冒充实时聊天。

## 9. 验收模块

### 9.1 负责范围

研发主管负责最终验收，不建议交给某个单模块研发自己验自己的模块。

### 9.2 P0 验收路径

| 编号 | 验收项 | 通过标准 |
| --- | --- | --- |
| ACC-01 | 后端检查 | `python manage.py check` 通过 |
| ACC-02 | 前端构建 | `npm run build` 通过 |
| ACC-03 | 数据库 | PostgreSQL migrate 成功 |
| ACC-04 | 演示数据 | 一键初始化演示设备、角色、点位、NFC、数据集 |
| ACC-05 | 模拟器闭环 | 拉配置、心跳、GPS、NFC、打卡全通 |
| ACC-06 | 前端三端 | PC/平板/手机核心页面可用 |
| ACC-07 | 真实硬件 | GPS/NFC 事件进入后端 |
| ACC-08 | 公网环境 | 前端、后端、模拟器公网访问可用 |
| ACC-09 | 小智工具 | 工具接口可用或有播报兜底 |
| ACC-10 | 安全边界 | `.env`、token、密码未提交，日志脱敏 |
| ACC-11 | GitHub 节点 | 每个阶段门完成后提交并推送 |

### 9.3 验收记录格式

每个模块交付时必须填写：

```text
模块：
负责人：
提交 commit：
涉及目录：
完成任务：
运行命令：
验证结果：
遗留问题：
是否阻塞：
下一步：
```

## 10. 模块交接规则

1. 后端改 API 字段，必须同步 [web_api_contract.md](web_api_contract.md) 并通知前端、模拟器、硬件。
2. 前端发现接口缺字段，不得自行假造业务字段，必须提给后端和研发主管。
3. 模拟器必须严格按 API 契约，不允许绕过后端直接改数据库。
4. 硬件上报格式必须和模拟器一致。
5. 部署环境变量名必须和 `.env.example` 一致。
6. 小智工具/MCP 验证失败时，先保留兜底路径，不阻塞后端/前端软件闭环。
7. 所有阶段门完成后必须提交 GitHub 节点。

## 11. 建议执行顺序

```text
D0 文档和接口确认
  -> D1 框架检查
  -> D2 后端模型/API/演示数据
  -> D3 device_simulator 软件闭环
  -> D4 前端页面接入
  -> D5 公网演示环境
  -> D6 小智工具/MCP 验证
  -> D7 真实硬件 GPS/NFC 接入
  -> D8 最终演示验收
```

执行原则：

- 后端和前端可以并行，但前端先用 mock 数据，最终必须接真实 API。
- 模拟器必须早于真实硬件完成。
- 公网环境必须早于小智工具/MCP 验证完成。
- 真实硬件最后接入，避免在硬件不稳定时阻塞软件闭环。

## 12. 当前仍需逐项确认

| 编号 | 确认项 | 建议 |
| --- | --- | --- |
| C-01 | 每个模块具体研发人员姓名 | 用户分配 |
| C-02 | 部署研发是否由后端兼任 | 人少时可兼任，但任务必须单独验收 |
| C-03 | QA/验收是否由研发主管本人执行 | 建议研发主管执行，避免模块自测自验 |
| C-04 | `R-P0-19 景区数据向量库` 是否改名为“一期景区数据集/知识摘要” | 建议改名，避免误做 pgvector |
| C-05 | 是否立刻补 [espidf_runbook.md](espidf_runbook.md) | 建议硬件开工前补 |
