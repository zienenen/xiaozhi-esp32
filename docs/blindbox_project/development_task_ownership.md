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
| `development_task_ownership.md` | 模块分工、验收、交接边界 |
| `requirements_and_feature_inventory.md` | P0/P1/P2 功能范围 |
| `phase1_single_robot_implementation_plan.md` | 一期实施顺序和风险 |
| `development_process.md` | 阶段门、提交规则、协作规则 |
| `testing_and_quality.md` | 质量门和最低验收路径 |
| `release_operations_runbook.md` | 发布、公网演示、回滚、节点上传 |
| `rd_lead_question_list.md` | 已确认问题和待验证问题 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `web_api_contract.md` | 审后端、前端、模拟器、硬件接口时 |
| `security_and_data_governance.md` | 涉及 token、GPS、账号、公网、日志时 |
| `open_source_selection.md` | 涉及新增依赖或改技术栈时 |
| `phase1_single_robot_budget.md` | 涉及硬件采购或替代型号时 |

不要求逐字阅读：

- 市场化、竞品、早期综合 PRD，除非要重新评估产品方向。

### 后端研发

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 3 章 | 后端任务、交付物、边界 |
| `web_api_contract.md` | API、数据对象、错误码、认证 |
| `requirements_and_feature_inventory.md` 第 6、8、10 节 | P0 功能、共用管理端、非功能验收 |
| `security_and_data_governance.md` 第 2、3、4、6、10 节 | token、GPS、日志、后端安全要求 |
| `testing_and_quality.md` 后端/API 相关章节 | 后端质量门 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `release_operations_runbook.md` | 配合部署、公网环境、PostgreSQL 时 |
| `django_react_frontend_product_interaction_spec.md` | 前端需要字段或页面状态解释时 |

不需要看：

- 市场化需求全文。
- 竞品分析。
- 硬件预算全文，除非参与设备字段设计。

### 前端研发

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 4 章 | 前端页面、状态、边界 |
| `django_react_frontend_product_interaction_spec.md` | 页面交互和信息架构 |
| `web_api_contract.md` | API 字段、错误码、状态码 |
| `requirements_and_feature_inventory.md` 第 6、8、10 节 | P0 页面范围和验收 |
| `testing_and_quality.md` 前端相关章节 | 构建和三端质量门 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `security_and_data_governance.md` | 涉及 token 展示、账号、GPS 敏感信息时 |
| `release_operations_runbook.md` | 配置公网 API base URL 时 |

不需要看：

- ESP-IDF、硬件接线、预算细节。
- 开源选型全文，除非要新增前端依赖。

### 联调工具研发

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 5 章 | 模拟器任务和完成标准 |
| `web_api_contract.md` | 设备配置、心跳、GPS、NFC、打卡接口 |
| `testing_and_quality.md` 模拟器相关章节 | 软件闭环质量门 |
| `release_operations_runbook.md` 本地/公网运行章节 | 切换本地和公网后端 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `security_and_data_governance.md` | 处理 device token、模拟数据标记时 |
| `phase1_single_robot_implementation_plan.md` | 确认模拟器在整体顺序中的位置 |

不需要看：

- 产品市场化文档。
- 前端交互规格全文。
- 硬件预算全文。

### 硬件/固件研发

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 6 章 | 硬件固件任务、交付物、边界 |
| `phase1_single_robot_budget.md` | 已确认硬件清单和采购型号 |
| `xiaozhi_existing_capabilities_analysis.md` | 小智底座已有能力和可扩展点 |
| `web_api_contract.md` 设备/GPS/NFC 相关章节 | 上报格式和打卡接口 |
| `testing_and_quality.md` 硬件相关章节 | GPS/NFC 验收要求 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `security_and_data_governance.md` | 涉及 GPS 频率、token、日志脱敏时 |
| `release_operations_runbook.md` | 真实设备连接公网后端时 |
| `open_source_selection.md` | 涉及小智上游复用边界时 |

还需补齐：

- `espidf_runbook.md`。硬件开工前应补，否则烧录、串口、接线验收容易不一致。

不需要看：

- 前端页面交互全文。
- 市场化竞品和商业化需求。

### 部署研发

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 7 章 | 部署任务和验收 |
| `release_operations_runbook.md` | 本地、公网、回滚、故障处理 |
| `security_and_data_governance.md` | `.env`、token、公网、日志边界 |
| `web_api_contract.md` | 公网 API base URL、认证、CORS 影响 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `open_source_selection.md` | 涉及 Nginx/Gunicorn/PostgreSQL 选型边界时 |
| `testing_and_quality.md` | 做公网 smoke test 时 |

不需要看：

- 产品需求全文。
- 前端交互规格全文。
- 硬件预算全文。

### 小智工具/MCP 验证人员

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 8 章 | MCP 验证任务和兜底 |
| `web_api_contract.md` 智能体上下文/知识查询接口 | 工具调用接口 |
| `security_and_data_governance.md` 小智工具调用边界 | `X-Tool-Token`、日志、安全边界 |
| `release_operations_runbook.md` 公网演示环境 | 公网 URL、HTTPS、CORS |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `open_source_selection.md` | 判断是否越界到自建小智服务端时 |

不需要看：

- 前端页面实现细节。
- 硬件接线细节。
- 市场化文档。

### 验收/QA

必读：

| 文档 | 用途 |
| --- | --- |
| `development_task_ownership.md` 第 9 章 | 最终验收路径 |
| `testing_and_quality.md` | 质量门、回归清单 |
| `requirements_and_feature_inventory.md` 第 6、10、11 节 | P0 功能、非功能验收、确认项 |
| `release_operations_runbook.md` | 演示前检查、故障处理、回滚 |

按需：

| 文档 | 什么时候看 |
| --- | --- |
| `web_api_contract.md` | 验证 API 状态码、错误码、字段时 |
| `security_and_data_governance.md` | 验证 token、GPS、日志、权限边界时 |

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

- `requirements_and_feature_inventory.md`
- `web_api_contract.md`
- `security_and_data_governance.md`
- `phase1_single_robot_implementation_plan.md`
- `testing_and_quality.md`

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

- API 与 `web_api_contract.md` 不冲突。
- 设备 token 日志脱敏。
- 模拟数据有 `source=simulation`。
- GPS 不保存长期连续轨迹。
- PostgreSQL 为主线数据库。

## 4. 前端模块

### 4.1 负责范围

前端研发负责 React + Vite + Ant Design 页面、API 调用、状态展示、三端适配和演示可视化。

涉及目录：

```text
frontend/
  src/
```

### 4.2 输入资料

- `django_react_frontend_product_interaction_spec.md`
- `web_api_contract.md`
- `requirements_and_feature_inventory.md`
- `testing_and_quality.md`

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

- `web_api_contract.md`
- `testing_and_quality.md`
- `release_operations_runbook.md`

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
后续补充 espidf_runbook.md
```

### 6.2 输入资料

- `phase1_single_robot_budget.md`
- `xiaozhi_existing_capabilities_analysis.md`
- `web_api_contract.md`
- `testing_and_quality.md`

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

### 6.4 必须补充的硬件文档

硬件研发必须补：

- `espidf_runbook.md`
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

- `release_operations_runbook.md`
- `security_and_data_governance.md`
- `open_source_selection.md`
- `web_api_contract.md`

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

### 8.3 完成标准

- 小智侧能成功调用至少一个我方公网接口。
- 失败时有明确日志。
- 如果官网工具/MCP 不稳定，演示仍可走固定播报或后端预置上下文兜底。

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

1. 后端改 API 字段，必须同步 `web_api_contract.md` 并通知前端、模拟器、硬件。
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
| C-05 | 是否立刻补 `espidf_runbook.md` | 建议硬件开工前补 |
