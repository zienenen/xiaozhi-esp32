# 一期研发流程

文档状态：pending_user_confirmation  
主责角色：研发主管  
更新时间：2026-07-12

## 1. 目的

本文定义一期单仓多模块工程的研发流程、职责边界、提交规则、评审门槛和阶段性交付顺序。

一期当前架构已确认：

```text
main/       小智 ESP32 固件
backend/    Django + DRF + PostgreSQL
frontend/   React + Vite + Ant Design
tools/      device_simulator 和调试脚本
deploy/     .env.example、Nginx/Gunicorn 示例
docs/       项目文档
```

## 2. 关联资料

| 文档 | 用途 |
| --- | --- |
| `requirements_and_feature_inventory.md` | 产品 P0/P1/P2 范围 |
| `frontend_backend_architecture_decision.md` | 已确认前后端架构 |
| `engineering_overview.md` | 工程边界和数据流 |
| `web_api_contract.md` | API 与数据契约 |
| `testing_and_quality.md` | 测试和质量门 |
| `release_operations_runbook.md` | 发布和演示运行手册 |

## 3. 当前工程原则

1. 先跑通软件闭环，再接真实硬件。
2. `main/` 暂不改小智固件核心，优先用 `tools/device_simulator/` 模拟设备。
3. `backend/` 先实现数据模型、Django Admin、DRF API 和演示种子数据。
4. `frontend/` 先实现三端响应式核心页面，不引入 Ant Design Pro 完整模板。
5. `deploy/` 当前不引入 Docker Compose，只保留示例配置。
6. 所有未实现能力必须标注为 stub，不得写成已完成。

## 4. 模块职责

| 模块 | 职责 | 当前阶段要求 |
| --- | --- | --- |
| `main/` | 小智 ESP32 固件、后续 GPS/NFC 接入 | 一期前半段不动核心；硬件到位后再接 |
| `backend/` | 设备、角色、点位、NFC、打卡、数据集、演示 API | 先按 `web_api_contract.md` 搭模型和接口 |
| `frontend/` | 管理页、演示页、模拟打卡页 | React + Vite + Ant Design，优先核心流程 |
| `tools/device_simulator/` | 模拟设备拉配置、心跳、GPS、NFC 打卡 | 必须严格对齐 API 契约 |
| `deploy/` | 环境变量、Nginx、Gunicorn 示例 | 不上 Docker Compose，先服务本地/单机部署 |
| `docs/` | 文档和交接 | 重大变更必须同步文档 |

## 5. 阶段门

### D0：资料和架构确认

通过条件：

- 产品 P0 已确认。
- 架构文档已 confirmed。
- API 契约已 confirmed。
- 单仓多模块结构已确认。

当前状态：已满足。

### D1：工程框架验收

通过条件：

- `backend/manage.py check` 通过。
- `frontend npm run build` 通过。
- `tools/device_simulator/` 有 README 和基础命令。
- `.gitignore` 排除 `.venv/`、`node_modules/`、`dist/`、`__pycache__/`、`.env`。
- 框架提交不包含依赖目录和构建产物。

### D2：后端最小闭环

通过条件：

- Django apps 固定为：
  - `devices`
  - `agents`
  - `spots`
  - `nfc_tags`
  - `checkins`
  - `datasets`
  - `demo`
- 设备配置接口可返回演示设备、角色、点位、NFC 标签。
- 打卡接口支持成功、重复、非法标签、设备未绑定等结果。
- 数据集接口可展示真实数据集状态和片段摘要。
- 模拟打卡接口写入 `source=simulation`。

### D3：前端最小闭环

通过条件：

- 可登录或进入演示账号模式。
- 设备、角色、点位、NFC、数据集、打卡记录有页面入口。
- 演示总览页可展示设备、角色、GPS/NFC、打卡结果。
- 手动模拟打卡页仅测试角色可见或明确标注。
- PC/平板/手机核心内容不遮挡。

### D4：模拟器软件闭环

通过条件：

- `device_simulator` 可拉取设备配置。
- 可上报心跳。
- 可模拟 GPS 接近。
- 可模拟 NFC 打卡。
- 前端能看到对应状态变化和记录。

### D5：真实硬件接入

通过条件：

- GPS 模块可输出有效 NMEA。
- NFC 模块可读取合法标签。
- 设备能调用后端打卡接口。
- 网络失败有可诊断日志或本地兜底。

## 6. 分支与提交规则

当前仓库可以先使用 `main` 直接推进，但每次提交必须保持单一目的。

提交建议：

| 类型 | 示例 |
| --- | --- |
| 文档 | `docs: add phase 1 development process` |
| 后端 | `backend: scaffold devices and checkins apps` |
| 前端 | `frontend: add demo overview page` |
| 工具 | `tools: add device simulator checkin flow` |
| 部署 | `deploy: add nginx and gunicorn examples` |

禁止提交：

- `backend/.venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- `__pycache__/`
- `.env`
- 真实 token、密码、私钥、账号 Cookie

## 7. 评审规则

每个变更至少自查：

1. 是否符合产品 P0。
2. 是否符合架构边界。
3. 是否影响小智原固件核心。
4. 是否新增敏感数据暴露。
5. 是否有验证命令或手动验证路径。
6. 是否同步文档。

## 8. 合并/上传规则

用户已要求重大变更上传 GitHub。执行规则：

1. 每完成一个阶段门，提交并推送。
2. 文档变更和代码变更可以分开提交。
3. 框架搭建提交前必须确认依赖目录未进入暂存区。
4. 推送失败时保留本地 commit，重试 GitHub push。

## 9. 当前研发主管后续动作

| 动作 | 状态 |
| --- | --- |
| 补研发流程文档 | 本文 |
| 补测试质量文档 | 待完成 |
| 补发布运行手册 | 待完成 |
| 校验工程框架是否可提交 | 待执行 |
| 修正一期实施计划 | 待执行 |

