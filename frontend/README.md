# 景区智能体前端

React + Vite + TypeScript + Ant Design 响应式管理与演示前端，一套 Web 应用适配 PC、平板和手机。

## 已实现页面

| 路由 | 功能 |
| --- | --- |
| `/login` | 无密码、无 token 的演示身份入口 |
| `/` | 设备、角色、GPS、NFC、打卡、数据集聚合总览与失败原因 |
| `/devices`、`/devices/:id` | 设备搜索、在线筛选与详情 |
| `/agents` | 角色、Prompt、voice_id、数据集关联编辑 |
| `/bindings` | 单设备单角色绑定与变更记录 |
| `/spots` | 点位、经纬度、GPS 半径、启停编辑 |
| `/nfc-tags` | 标签、点位绑定、启停与最近识别 |
| `/datasets` | 处理状态、片段摘要及角色 / 点位关联 |
| `/checkins` | 成功、失败、重复、真实 / 模拟记录筛选 |
| `/simulate-checkin` | 仅测试 / 原厂身份可见的模拟打卡 |

页面统一提供加载、空数据、错误、成功和禁用 / 离线状态。接口错误会转换为可读提示，模拟记录始终以 `source=simulation` 标记，前端不请求或展示完整设备 token。

## 本地运行

```powershell
cd frontend
npm install
npm run dev
```

默认使用同源 `/api/v1`。需要直连独立后端时，在未提交的本地 `.env` 中配置：

```text
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## 构建验收

```powershell
cd frontend
npm run build
```

响应式与功能验收记录见 [MANUAL_ACCEPTANCE.md](MANUAL_ACCEPTANCE.md)。
