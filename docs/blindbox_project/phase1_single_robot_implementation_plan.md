# 一期工程实施计划

文档状态：pending_user_confirmation
主责角色：研发主管
更新时间：2026-07-12

## 1. 当前确认口径

一期不再按“纯硬件四周 Demo”执行，而按已确认架构拆成软件闭环优先、硬件接入后置的工程计划。

已确认工程结构：

```text
main/       小智 ESP32 固件
backend/    Django + DRF + PostgreSQL
frontend/   React + Vite + Ant Design
tools/      device_simulator 和调试脚本
deploy/     .env.example、Nginx/Gunicorn 示例
docs/       项目文档
```

已确认技术路线：

- 后端：Django + DRF + PostgreSQL。
- 前端：React + Vite + Ant Design，不采用 Ant Design Pro 完整模板。
- 数据集：一期不启用 pgvector，先用普通 PostgreSQL + 数据集状态/片段摘要展示。
- 数据库迁移：主线开发、演示和公网环境统一 PostgreSQL；SQLite 只允许极短期 smoke test，不沉淀演示数据。
- 工具：先用 `tools/device_simulator/` 跑通软件闭环。
- 固件：先不动 ESP32 固件核心，待软件闭环稳定后接 GPS/NFC。
- 部署：一期需要公网演示环境；当前不引入 Docker Compose，先保留 Nginx/Gunicorn 示例。

## 2. 一期目标

一期目标是跑通“景区数据智能体 + GPS/NFC 打卡 + 三端演示管理”的最小闭环：

```text
演示账号登录
  -> 管理设备、角色、点位、NFC、数据集
  -> device_simulator 拉取设备配置
  -> 模拟心跳 / GPS 接近 / NFC 打卡
  -> 后端记录打卡结果
  -> 前端演示页和记录页展示状态
  -> 后续再接真实 ESP32 GPS/NFC
```

## 3. 阶段拆分

### P0-S0：节点整理与文档基线

目标：保证所有角色看到同一套工程口径。

任务：

- 确认单仓多模块结构。
- 确认架构文档为 confirmed。
- 补齐研发主管三份文档：
  - [development_process.md](development_process.md)
  - [testing_and_quality.md](testing_and_quality.md)
  - [release_operations_runbook.md](release_operations_runbook.md)
- 建立研发主管问题清单：
  - [rd_lead_question_list.md](rd_lead_question_list.md)
- 提交并推送 GitHub 节点。

验收：

- `git status` 干净。
- GitHub 可见当前节点。
- 文档索引能找到研发主管文档。

### P0-S1：工程框架校验

目标：确认框架不是空目录，而是可启动/可构建的基础。

任务：

- 后端执行：

```powershell
cd backend
python manage.py check
```

- 前端执行：

```powershell
cd frontend
npm run build
```

- 检查 Git 忽略规则：
  - `.venv/`
  - `node_modules/`
  - `dist/`
  - `__pycache__/`
  - `.env`
  - `*.tsbuildinfo`

验收：

- 后端 check 通过。
- 前端 build 通过。
- 无依赖目录、构建产物、环境密钥进入 Git。

### P0-S2：后端最小数据模型与 Admin

目标：后端具备承载 P0 数据的模型和管理入口。

任务：

- 建立或完善 Django apps：
  - `devices`
  - `agents`
  - `spots`
  - `nfc_tags`
  - `checkins`
  - `datasets`
  - `demo`
- 实现基础模型。
- 接入 Django Admin。
- 增加演示种子数据方案。

验收：

- 可创建演示设备。
- 可创建 2 个角色。
- 可配置 1 个点位。
- 可配置 NFC 标签。
- 可配置数据集状态和片段摘要。
- 可查看打卡记录。

### P0-S3：后端 API 契约落地

目标：按 [web_api_contract.md](web_api_contract.md) 跑通 API。

任务：

- `/api/v1/device-config`
- `/api/v1/device-heartbeats`
- `/api/v1/location-events`
- `/api/v1/checkins`
- `/api/v1/demo/overview`
- `/api/v1/demo/simulate-checkin`
- `/api/v1/agents/{agent_id}/context`
- `/api/v1/knowledge/search`

验收：

- 合法设备能拉取配置。
- 心跳能更新最近状态。
- GPS 接近事件不产生成功打卡。
- NFC 合法标签可成功打卡。
- 重复打卡返回 duplicate。
- 模拟打卡写入 `source=simulation`。
- 知识查询可返回数据集片段摘要或简化搜索结果。

### P0-S4：设备模拟器软件闭环

目标：硬件未到货时完成软件闭环。

任务：

- `tools/device_simulator/` 支持：
  - 拉取配置
  - 上报心跳
  - 上报 GPS 接近
  - 上报 NFC 打卡
  - 模拟非法标签
  - 模拟重复打卡
- 模拟器参数对齐 [web_api_contract.md](web_api_contract.md)。

验收：

- 后端产生对应记录。
- 前端可见状态变化。
- 模拟数据与真实数据可区分。

### P0-S5：前端核心页面

目标：提供可演示、可管理、可调试的响应式页面。

任务：

- 演示总览页。
- 设备页。
- 角色页。
- 点位页。
- NFC 标签页。
- 数据集页。
- 打卡记录页。
- 手动模拟打卡页。

验收：

- PC/平板/手机核心信息不遮挡。
- 演示页能显示设备、角色、GPS、NFC、打卡、数据集状态。
- 模拟打卡页明确标记测试入口。
- 错误状态可读，不只显示“失败”。

### P0-S6：真实硬件接入

目标：将软件闭环接入 ESP32、GPS、NFC。

任务：

- 接入 GPS UART NMEA。
- 接入 PN532 NFC。
- ESP32 拉取后端配置。
- ESP32 按约 10 秒一次上报 GPS 位置信息和定位质量。
- ESP32 上报 NFC 打卡。
- 打卡成功触发角色播报。

验收：

- 室外或靠窗可读取 GPS。
- 后端能看到约 10 秒级 GPS 位置更新。
- NFC 可读取合法标签。
- 后端记录真实设备打卡。
- 演示页可展示真实设备状态。
- 小智语音链路可完成播报或问答兜底。

### P0-S7：演示验收

目标：形成可演示、可复现、可回滚的阶段成果。

任务：

- 准备演示账号。
- 准备演示数据。
- 准备演示脚本。
- 执行 3 轮完整演示。
- 记录失败项和修复项。
- 提交 GitHub 节点。

验收：

- 软件模拟闭环可稳定复现。
- 如硬件到位，真实硬件闭环至少跑通一次。
- 有测试记录。
- 有回滚路径。

## 4. 当前优先级

当前下一步顺序：

1. 完成研发主管文档和问题清单。
2. 校验现有 backend/frontend/tools/deploy 框架。
3. 进入后端最小模型和 API。
4. 进入 device_simulator 软件闭环。
5. 进入前端页面。
6. 最后接真实硬件。

## 5. 主要风险

| 风险 | 控制 |
| --- | --- |
| 过早改 ESP32 固件核心 | 先用 device_simulator 跑通软件闭环 |
| pgvector 增加复杂度 | 一期不启用，先用普通 PostgreSQL 展示数据集状态 |
| 小智官网 MCP 调用不稳定 | 先保留固定播报和后端上下文接口，MCP 联调作为独立验证 |
| 前端范围膨胀 | 只做 P0 页面，不做完整后台系统 |
| 登录权限过重 | 一期演示账号即可 |
| 模拟数据误导验收 | 强制 `source=simulation` 标记 |
| SQLite 后续迁移成本 | 主线开发、演示、公网环境统一 PostgreSQL |
| 公网演示带来安全范围扩大 | 只做公网演示环境，不做完整生产化治理；token、CORS、日志脱敏必须到位 |
