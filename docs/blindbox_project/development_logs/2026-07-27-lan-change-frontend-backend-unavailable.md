# 研发日志：换 Wi-Fi 后前端提示“后端服务不可用”

| 字段 | 内容 |
| --- | --- |
| 日期 | 2026-07-27 |
| 责任角色 | 研发主管 |
| 问题类型 | 本地演示环境 / 前后端联调 / 局域网配置 |
| 当前状态 | 已修复 |
| 影响范围 | 自研 React 前端、Django 后端本地演示、ESP32 局域网访问提示 |

## 1. 问题现象

用户更换 ESP32/电脑连接的 Wi-Fi 后，前端页面提示：

```text
后端服务不可用，请确认服务已启动后重试。
```

但研发主管在本机检查发现：

- Django 后端进程实际已启动。
- `http://127.0.0.1:8000/api/v1/health` 返回正常。
- `http://192.168.168.155:8000/api/v1/health` 返回正常。
- Vite 前端进程也已启动。

因此该问题不是后端进程死亡，而是前端请求目标地址错误。

## 2. 排查过程

1. 检查端口监听：

```powershell
Get-NetTCPConnection -LocalPort 8000,5173 -State Listen
```

确认 Django 监听 `0.0.0.0:8000`，Vite 监听 `0.0.0.0:5173`。

2. 检查健康接口：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
Invoke-RestMethod http://127.0.0.1:5173/api/v1/health
```

确认后端和前端代理都能返回：

```json
{"success":true,"data":{"status":"ok"},"error":null}
```

3. 搜索前端报错文案来源：

```powershell
rg -n "后端服务不可用|VITE_API_BASE_URL|8000|192.168" frontend -S
```

定位到 `frontend/.env` 写死了旧局域网地址。

## 3. 根因

`frontend/.env` 中写死了旧后端地址：

```text
VITE_API_BASE_URL=http://192.168.1.9:8000/api/v1
```

换 Wi-Fi 后，电脑局域网 IP 已变为：

```text
192.168.168.155
```

前端仍请求旧 IP，浏览器无法拿到 HTTP 响应，因此 Axios 进入 `!error.response` 分支并显示“后端服务不可用”。

这是典型的“演示环境 IP 写死”问题，不是数据库、Django 或接口契约问题。

## 4. 修复方案

采用类似若依后台管理系统的思路：

- 前端默认请求同源相对路径 `/api/v1`。
- 开发态由 Vite proxy 把 `/api` 转发到 Django。
- 启动脚本负责自动识别当前局域网 IP，并打印给用户/ESP32 使用。
- 不再要求用户每次换 Wi-Fi 后手动修改前端 `.env`。

涉及修改：

| 文件 | 修改内容 |
| --- | --- |
| `frontend/.env` | `VITE_API_BASE_URL` 置空，本地演示不写死 IP |
| `frontend/.env.example` | 说明本地开发默认走 `/api/v1` |
| `frontend/src/shared/api.ts` | 空字符串也回退到 `/api/v1` |
| `scripts/start_local_demo.ps1` | 自动识别 LAN IP，更新后端 `DJANGO_ALLOWED_HOSTS` 和 `CORS_ALLOWED_ORIGINS`，以 `0.0.0.0` 启动前后端，并打印访问地址 |

核心前端逻辑：

```ts
baseURL: String(import.meta.env.VITE_API_BASE_URL || "").trim() || "/api/v1"
```

## 5. 验证结果

已执行：

```powershell
[System.Management.Automation.Language.Parser]::ParseFile(...)
.\backend\.venv\Scripts\python.exe manage.py check
npm run build
```

结果：

- `start_local_demo.ps1` 语法通过。
- Django `manage.py check` 通过。
- 前端 `npm run build` 通过。
- 新前端端口 `/api/v1/health` 验证通过。
- 旧进程清理后，使用新脚本重启成功。

当前新脚本启动后会输出类似：

```text
Open on this computer: http://127.0.0.1:5173
Open from LAN/mobile: http://192.168.168.155:5173
Backend health: http://192.168.168.155:8000/api/v1/health
ESP32 device API base URL: http://192.168.168.155:8000/api/v1
Login: root / root
```

## 6. 后续规避规则

1. 前端本地演示不允许提交固定局域网 IP。
2. 换 Wi-Fi 后，只需要重新运行：

```powershell
cd D:\mysterybox\xiaozhi-esp32-main
.\scripts\start_local_demo.ps1
```

3. 如果页面仍显示“后端服务不可用”，优先检查：

```powershell
Invoke-RestMethod http://127.0.0.1:5173/api/v1/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
```

4. ESP32 固件侧仍存在后端地址写死风险。后续硬件/固件任务应将 `BLINDBOX_DEVICE_API_URL` 改为运行期配置，优先从 NVS/配网页面读取，避免每次换网重新烧录。

## 7. 给后续研发 agent 的一句话

如果前端提示“后端服务不可用”，不要先怀疑 Django 没启动；先检查 `frontend/.env` 是否写死了旧 IP，以及 `/api/v1/health` 代理是否正常。
