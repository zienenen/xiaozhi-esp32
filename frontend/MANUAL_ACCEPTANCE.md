# 前端手动验收记录

日期：2026-07-26

范围：FE-PM-01 ～ FE-PM-06，以及一期用户端 / 管理员端重构

命令：`npm run build`

## 需求验收

| 编号 | 验收结果 |
| --- | --- |
| FE-PM-01 | 角色配置页可展示和编辑性格 Prompt、voice_id、知识引用与配置版本；列表和预览展示官网同步状态，保存成功后明确提示待同步 |
| FE-PM-02 | 角色页和官网同步页支持待同步、已同步、失败、需人工处理状态，并展示时间、操作人与失败原因 |
| FE-PM-03 | 官网同步页展示 Prompt、voice_id、工具 URL、知识引用和配置版本，可复制完整脱敏快照 |
| FE-PM-04 | 对话记录支持设备、角色、点位、来源、起止日期筛选；详情展示用户输入、AI 回复、知识片段和来源 |
| FE-PM-05 | 首页及侧栏均加入角色配置、对话记录、官网同步入口；统一提供 loading、empty、error 和重试状态 |
| FE-PM-06 | TypeScript 与 Vite 生产构建通过；响应式 CSS 在桌面、平板、手机断点分别采用侧栏/抽屉、三列/两列/单列布局 |
| 一期角色边界 | `viewer` 只能进入我的伙伴、景区地图、我的图鉴；访问 `/admin/*` 会回到用户端，页面不出现切换智能体或后台配置 |
| 管理员工作台 | 非用户身份进入 `/admin/*`；左侧菜单可收起，移动端使用抽屉；智能体使用卡片工作台和配置弹窗 |
| 用户聚合接口 | 用户端只调用 `/user/companion` 与 `/user/map`，真实印章由后端排除 simulation 后聚合 |

浏览器视口检查：

| 视口 | 页面宽度 | 横向溢出 |
| --- | --- | --- |
| 1440 × 900（PC） | 1440px | 无 |
| 834 × 1112（平板） | 834px | 无 |
| 390 × 844（手机） | 390px；登录卡片收缩为 342px | 无 |

## 接口联调边界

当前前端按以下 P0 资源路径实现：

- `GET /api/v1/conversation-sessions`
- `GET /api/v1/conversation-sessions/{session_id}`
- `GET /api/v1/official-sync-logs`
- `PATCH /api/v1/official-sync-logs/{sync_id}`

当前工作树已提供上述后台资源路由，以及用户端 `GET /api/v1/user/companion`、`GET /api/v1/user/map` 聚合路由。构建与契约类型检查已通过，真实设备的 GPS/NFC 状态仍需在硬件环境联调确认。

## 安全检查

- 页面不展示官网账号、密码、device token 或 tool token。
- 同步快照仅展示契约允许的 Prompt、voice_id、工具 URL、知识引用和配置版本。
- 对话来源使用独立状态标签，人工导入、设备日志、工具回调与自建语音链路可区分。

## 用户端实时对话整改记录

日期：2026-07-26

范围：FE-RT-01 ～ FE-RT-05

| 检查项 | 结果 |
| --- | --- |
| 专属伙伴文案 | 已改为“已绑定专属伙伴，用户不可自行切换”，不再使用“锁死”“锁定不可用”“未解锁不可用” |
| 当前状态 | “我的伙伴”展示绑定角色、设备在线状态、最近在线时间和最近入库消息对应的对话状态 |
| 最近真实对话 | 从 `/api/v1/user/companion?recent_limit=5` 的 `recent_conversations.messages` 读取，不再渲染静态示例问答 |
| 真实来源过滤 | `device_log`、`xiaozhi_official_device_log` 可作为真实硬件消息展示；模拟和手工来源不冒充真实对话 |
| 刷新方式 | 5 秒静默轮询，刷新时保留当前页面内容，不反复进入全页 loading |
| 空数据 | 没有真实设备消息时显示“尚未收到真实硬件对话”，不生成占位聊天内容 |
| 构建 | `npm run build` 通过 |

待真实硬件联调：

1. ESP32 在小智官方链路中分别产生一条 user 和 assistant 消息。
2. 确认 Django 按 `official_session_id` 聚合并返回到 `recent_conversations.messages`。
3. 确认用户端在 5 秒轮询窗口内出现新消息、时间和 `xiaozhi_official_device_log` 来源。
4. 确认模拟或手工导入消息不会显示为真实硬件对话。
