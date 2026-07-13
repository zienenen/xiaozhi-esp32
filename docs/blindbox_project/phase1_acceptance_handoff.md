# 一期验收与交接记录

文档状态：software_local_accepted_with_external_blockers  
主责角色：研发主管 / 验收 agent  
验收日期：2026-07-13

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
| ACC-07 | 真实硬件 | 未验收 | 需要 ESP32 + GPS + NFC 实物接入；当前只能由模拟器证明软件闭环 |
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
| Q-A01 | 真实 ESP32、GPS、NFC、电池到货并接线烧录后，是否由硬件研发按 [espidf_runbook.md](espidf_runbook.md) 接入 | 是，阻塞 ACC-07 | 硬件/固件研发执行，研发主管验收 |
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
