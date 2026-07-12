# 一期发布与演示运行手册

文档状态：partially_confirmed
主责角色：研发主管 + 全栈工程师
更新时间：2026-07-12

## 1. 目的

本文用于指导一期本地运行、演示准备、故障恢复和阶段发布。当前阶段不引入 Docker Compose，先使用本地后端、前端和设备模拟器完成软件闭环。

## 2. 当前运行组件

| 组件 | 路径 | 用途 |
| --- | --- | --- |
| 后端 | `backend/` | Django + DRF API |
| 前端 | `frontend/` | React + Vite + Ant Design |
| 模拟器 | `tools/device_simulator/` | 模拟设备配置、心跳、GPS、NFC |
| 部署示例 | `deploy/` | `.env.example`、Nginx/Gunicorn 示例 |
| 固件 | `main/` | 后续接入真实 ESP32 |

## 3. 本地启动顺序

### 3.1 后端

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py check
python manage.py runserver 127.0.0.1:8000
```

说明：

- `.env` 不允许提交。
- 为降低迁移风险，主线开发、演示和公网环境统一使用 PostgreSQL。
- SQLite 只允许用于极短期无库 smoke test，不沉淀演示数据，不作为后续迁移来源。

### 3.2 前端

```powershell
cd frontend
npm install
npm run build
npm run dev
```

说明：

- `node_modules/` 不允许提交。
- `dist/` 不允许提交。

### 3.3 设备模拟器

```powershell
cd tools/device_simulator
python simulate_device.py --help
```

模拟器应覆盖：

- 拉取设备配置。
- 上报心跳。
- 模拟 GPS 接近。
- 模拟 NFC 打卡。

具体命令以后续 `tools/device_simulator/README.md` 为准。

## 4. 演示前检查

### 4.1 软件闭环检查

| 检查项 | 通过标准 |
| --- | --- |
| 后端启动 | `python manage.py check` 通过，API 可访问 |
| 前端构建 | `npm run build` 通过 |
| 前端页面 | 演示总览页可打开 |
| 模拟器配置拉取 | 返回设备、角色、点位、NFC 标签 |
| 模拟打卡 | 前端能看到打卡记录 |
| 数据集状态 | 页面能看到数据集和片段摘要 |

### 4.2 硬件演示检查

硬件阶段再执行：

| 检查项 | 通过标准 |
| --- | --- |
| ESP32 供电 | 无异常重启 |
| 小智语音 | 可唤醒、可播放 |
| GPS | 有有效定位或启用模拟坐标 |
| NFC | 可读取合法标签 |
| 网络 | 设备能访问公网后端 API，公网域名/地址、HTTPS/CORS 配置可用 |

## 5. 故障处理

| 问题 | 处理 |
| --- | --- |
| 后端启动失败 | 检查 `.env`、依赖、数据库连接、`manage.py check` 输出 |
| 前端接口失败 | 检查 API base URL、CORS、后端是否启动 |
| 模拟器失败 | 检查设备 token、device_id、后端地址 |
| 打卡重复 | 检查冷却时间和幂等规则 |
| 页面无数据 | 检查是否初始化演示数据 |
| GPS 无信号 | 使用模拟坐标或室外测试 |
| NFC 无效 | 检查标签 ID 是否登记并启用 |

## 6. 发布/提交检查

提交前执行：

```powershell
git status --short
```

不得出现：

- `backend/.venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- `__pycache__/`
- `.env`
- 真实密钥或 token

建议执行：

```powershell
cd backend
python manage.py check
```

```powershell
cd frontend
npm run build
```

## 7. 回滚策略

当前阶段以 Git 回滚为主。

规则：

1. 每个阶段门单独提交。
2. 文档和代码可分开提交。
3. 如框架变更导致无法启动，优先回退最近一次框架提交。
4. 不使用 `git reset --hard` 删除用户未确认改动。

## 8. 当前不做

- 不引入 Docker Compose。
- 一期需要公网演示环境。
- 不建设完整公网生产化治理。
- 不私有化小智语音服务。
- 不保存连续 GPS 轨迹。
- 不做完整权限系统。

## 9. 阶段交付物

| 阶段 | 交付物 |
| --- | --- |
| 框架阶段 | backend/frontend/tools/deploy 骨架、README、依赖文件 |
| 软件闭环 | API、模拟器、演示页、打卡记录 |
| 硬件接入 | GPS/NFC 固件模块、接线说明、串口日志 |
| 演示阶段 | 演示账号、演示数据、演示脚本、故障预案 |

## 9.1 公网演示环境要求

一期需要公网访问后端，用于设备、前端页面和小智官网侧工具/MCP 调用验证。

最低要求：

- 后端通过公网域名或公网 IP 可访问。
- 优先配置 HTTPS；如果临时使用 HTTP，必须只用于短期演示和技术验证。
- Nginx/Gunicorn 示例配置需要能支撑 Django API。
- CORS 只放行演示前端地址，不做全开放。
- `.env` 中配置公网 API base URL、数据库连接、`DEVICE_TOKEN`、`XIAOZHI_TOOL_TOKEN`。
- 公网环境使用 PostgreSQL，不使用 SQLite。
- 公网演示仍不是完整生产环境，不承诺高可用、自动备份、审计、限流和商业化安全治理。

## 10. 节点上传规则

用户要求每个重要节点上传 GitHub。执行规则：

1. 文档节点完成后提交。
2. 框架节点完成后提交。
3. 后端最小闭环完成后提交。
4. 前端最小闭环完成后提交。
5. device_simulator 软件闭环完成后提交。
6. 真实硬件接入完成后提交。

提交前必须执行：

```powershell
git status --short
```

如果出现以下路径，必须确认未被暂存：

```text
backend/.venv/
frontend/node_modules/
frontend/dist/
__pycache__/
.env
```
