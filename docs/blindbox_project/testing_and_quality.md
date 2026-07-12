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
- `/api/v1/location-events` 可接收 GPS 接近摘要。
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
3. 上报 GPS 接近事件。
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
- GPS 不保存连续轨迹。
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

