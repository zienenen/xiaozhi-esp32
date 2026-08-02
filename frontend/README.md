# 景区智能体前端

React + Vite + TypeScript + Ant Design 一期前端。应用按身份拆分为用户端和管理员端，并适配 PC、平板和手机。

## 已实现页面

| 路由 | 功能 |
| --- | --- |
| `/login` | 后端演示账号认证与演示身份入口 |
| `/` | 用户端“我的伙伴”，只展示设备唯一绑定的智能体 |
| `/map` | 游戏化景区地图；GPS 发现、NFC 精准确认和真实印章进度 |
| `/stamps` | 用户真实设备打卡图鉴，不计入模拟记录 |
| `/admin` | 管理员演示总览 |
| `/admin/agents` | 智能体卡片工作台；Prompt、音色、知识引用等在弹窗中配置 |
| `/admin/devices`、`/admin/devices/:id` | 设备搜索、在线筛选与详情 |
| `/admin/bindings` | 单设备单角色绑定与变更记录 |
| `/admin/spots`、`/admin/nfc-tags` | 点位与 NFC 标签后台管理 |
| `/admin/datasets` | 景区数据集与角色 / 点位关联 |
| `/admin/checkins` | 成功、失败、重复、真实 / 模拟打卡记录 |
| `/admin/conversations` | 对话筛选、消息详情与内容来源 |
| `/admin/official-sync` | 小智官网同步状态、脱敏配置快照和人工留痕 |
| `/admin/simulate-checkin` | 仅测试 / 原厂身份可见的模拟打卡 |

页面统一提供加载、空数据、错误、成功和禁用 / 离线状态。前端不展示完整设备 token、官网账号密码或工具 token。

## 新增 P0 API

前端按资源契约调用：

- `GET /api/v1/conversation-sessions`
- `GET /api/v1/conversation-sessions/{session_id}`
- `GET /api/v1/official-sync-logs`
- `PATCH /api/v1/official-sync-logs/{sync_id}`
- `GET /api/v1/user/companion`
- `GET /api/v1/user/map`

列表接口兼容通用 envelope、数组和 DRF `{ results, count }` 分页结构。

## 本地运行

```powershell
cd frontend
npm install
npm run dev
```

开发服务器默认把同源 `/api/v1` 代理到 `http://127.0.0.1:8000`。登录凭据只保存在当前页面内存中，刷新或退出后清除。

## 构建验收

```powershell
cd frontend
npm run build
```

响应式与功能验收记录见 [MANUAL_ACCEPTANCE.md](MANUAL_ACCEPTANCE.md)。
