# Web API 与数据契约

文档状态：confirmed  
主责智能体：架构师智能体 + 全栈工程师智能体  
更新时间：2026-07-12

## 0. 文档边界

本文档用于定义课题一期已确认最小业务后台方案下，设备端、管理端、演示页和调试页需要的 API 与数据对象契约。

当前一期框架已按 `Django/DRF + PostgreSQL + React/Ant Design Pro + xiaozhi.me 语音/MCP 不可见依赖` 收敛。本文已作为一期 API 与数据契约确认；后续仍需全栈工程师结合实现细节细化字段命名、分页、DRF serializer 和错误码落地。

## 1. 关联资料

| 文档 | 关系 |
| --- | --- |
| [README.md](README.md) | 项目资料入口 |
| [document_index.md](document_index.md) | 文档索引与阅读顺序 |
| [project_role_agents.md](project_role_agents.md) | 角色责任边界 |
| [agent_document_requirements.md](agent_document_requirements.md) | 文档责任和核对规则 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) | 已确认产品需求 |
| [mvp_product_alignment.md](mvp_product_alignment.md) | 已确认 MVP 口径 |
| [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | 已确认页面交互 |
| [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md) | 已确认 P0 交接清单 |
| [engineering_overview.md](engineering_overview.md) | 工程架构总览 |
| [frontend_backend_architecture_decision.md](frontend_backend_architecture_decision.md) | 前后端架构决策 |
| [fullstack_implementation_guide.md](fullstack_implementation_guide.md) | 已有 API 示例来源 |

## 2. 设计原则

| 原则 | 说明 |
| --- | --- |
| 产品 P0 不丢失 | 必须覆盖设备、角色、绑定、点位、NFC、打卡、数据集、模拟打卡 |
| 设备不可信任 | 后端以绑定关系为准，不信任设备直接传入的 `agent_id` |
| GPS 不直接打卡 | GPS 只产生接近状态，NFC 合法标签才确认打卡 |
| 模拟数据可区分 | 模拟打卡必须带 `source=simulation` 或等价标记 |
| 不保存连续轨迹 | 一期只保存打卡事件和定位质量摘要 |
| 语音流不进业务 API | ASR/LLM/TTS 继续由小智官方或兼容语音链路承载 |
| 状态码稳定 | 机器状态用英文 code，页面展示可本地化 |
| 官网能力不进业务 API | 一期官网/MCP 作为不可见入口，工具调用指向我方 API；自研 API 承载景区业务数据、设备配置源、知识库查询和打卡闭环 |
| 数据集真实但格式可变 | 一期接入真实景区数据，前端先用通用字段展示，后续统一整改数据集模块 |
| GPS 上报节流 | 一期保存定位质量摘要，设备侧或 API 网关按 10 秒级节流，避免连续轨迹上传 |

## 3. API 基础约定

| 项 | 草案 |
| --- | --- |
| Base URL | `/api/v1` |
| 请求格式 | JSON |
| 响应格式 | JSON |
| 时间格式 | ISO 8601，建议带时区 |
| ID 格式 | 对外使用稳定字符串 ID，如 `device_001`、`spot_gate_001` |
| 认证 | 一期管理端使用演示账号；设备端采用 `device_id + device_token` 静态 token |
| 幂等 | 打卡上报必须支持幂等 |
| 分页 | 列表接口建议 `page`、`page_size`，或 DRF 默认分页 |

通用响应草案：

```json
{
  "success": true,
  "data": {},
  "error": null,
  "request_id": "req_20260712_0001"
}
```

通用错误草案：

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "permission_denied",
    "message": "无权访问该资源",
    "details": {}
  },
  "request_id": "req_20260712_0002"
}
```

## 4. 数据对象

### 4.1 Device

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `device_id` | string | 是 | 设备唯一 ID |
| `sn` | string | 是 | 设备序列号 |
| `name` | string | 否 | 管理端显示名称 |
| `device_token_ref` | string | 否 | 设备 token 引用或掩码，不在列表接口返回明文 |
| `online_status` | string | 是 | `online` / `offline` / `unknown` / `config_error` |
| `bound_agent_id` | string | 是 | 当前绑定智能体 |
| `last_seen_at` | datetime | 否 | 最近在线时间 |
| `last_gps_status` | string | 否 | 最近 GPS 状态 |

### 4.2 Agent

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `agent_id` | string | 是 | 智能体 ID |
| `name` | string | 是 | 角色名称 |
| `personality_prompt` | string | 是 | 角色人设 |
| `voice_id` | string | 否 | 音色引用 |
| `dataset_id` | string | 否 | 关联景区数据集 |
| `status` | string | 是 | `active` / `disabled` / `draft` |
| `series` | string | 否 | 市场化预留 |
| `rarity` | string | 否 | 市场化预留 |

### 4.3 Binding

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `device_id` | string | 是 | 设备 ID |
| `agent_id` | string | 是 | 当前绑定角色 |
| `bound_by` | string | 否 | 操作者 |
| `bound_at` | datetime | 是 | 绑定时间 |
| `binding_type` | string | 是 | `factory` / `admin_override` / `demo` |

约束：一个 `device_id` 同一时间只能有一个当前有效 `agent_id`。

### 4.4 ScenicSpot

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `spot_id` | string | 是 | 点位 ID |
| `name` | string | 是 | 点位名称 |
| `scenic_area_name` | string | 否 | 景区名称 |
| `latitude` | number | 是 | 纬度 |
| `longitude` | number | 是 | 经度 |
| `gps_radius_meters` | number | 是 | GPS 接近提醒半径 |
| `dataset_id` | string | 否 | 关联数据集 |
| `checkin_message` | string | 否 | 打卡成功文案 |
| `status` | string | 是 | `active` / `disabled` |

### 4.5 NfcTag

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `tag_id` | string | 是 | NFC 标签 ID |
| `spot_id` | string | 是 | 所属点位 |
| `label` | string | 否 | 标签名称 |
| `status` | string | 是 | `active` / `disabled` / `unknown` |
| `last_seen_at` | datetime | 否 | 最近识别时间 |

### 4.6 Checkin

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `checkin_id` | string | 是 | 打卡记录 ID |
| `device_id` | string | 是 | 设备 ID |
| `agent_id` | string | 是 | 后端绑定关系解析出的角色 ID |
| `spot_id` | string | 是 | 点位 ID |
| `tag_id` | string | 否 | NFC 标签 ID |
| `result` | string | 是 | `success` / `duplicate` / `failed` / `simulated` |
| `failure_code` | string | 否 | 失败原因 |
| `source` | string | 是 | `device` / `simulation` |
| `checked_in_at` | datetime | 是 | 事件时间 |
| `location_quality` | object | 否 | 定位质量摘要 |

### 4.7 Dataset

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `dataset_id` | string | 是 | 数据集 ID |
| `name` | string | 是 | 数据集名称 |
| `source_type` | string | 否 | `document` / `faq` / `manual` |
| `status` | string | 是 | `draft` / `chunked` / `vectorized` / `failed` / `disabled` |
| `chunk_count` | number | 否 | chunk 数量 |
| `updated_at` | datetime | 否 | 最后更新时间 |
| `failure_reason` | string | 否 | 处理失败原因 |

一期最小通用展示 schema：

| 字段 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `dataset_id` | string | 是 | 数据集 ID |
| `name` | string | 是 | 数据集名称 |
| `status` | string | 是 | `draft` / `ready` / `failed` / `disabled`，可由后端映射真实处理状态 |
| `chunk_count` | number | 否 | 可展示片段数量 |
| `summary_items` | array | 否 | 前端通用展示片段，如标题、摘要、来源 |
| `updated_at` | datetime | 否 | 最后更新时间 |

`summary_items` 建议结构：

```json
[
  {
    "title": "景区入口介绍",
    "summary": "入口区域的历史、路线和注意事项摘要。",
    "source_ref": "doc_001#chunk_001"
  }
]
```

## 5. 设备侧 API

### 5.1 拉取设备配置

```http
GET /api/v1/device-config?device_id={device_id}
```

用途：设备启动或配置刷新时拉取当前绑定角色、点位、NFC 标签和数据集摘要。

认证：一期设备侧使用 `device_id + device_token` 静态 token。建议通过请求头传递：

```http
X-Device-Id: device_001
X-Device-Token: demo-device-token
```

响应示例：

```json
{
  "success": true,
  "data": {
    "device_id": "device_001",
    "agent": {
      "agent_id": "agent_alo",
      "name": "阿洛",
      "voice_id": "voice_alo_01",
      "personality_prompt": "你是一个活泼、好奇、喜欢讲故事的旅游伙伴。",
      "dataset_id": "dataset_spot_demo_001"
    },
    "spots": [
      {
        "spot_id": "spot_gate_001",
        "name": "景区入口",
        "latitude": 31.2304,
        "longitude": 121.4737,
        "gps_radius_meters": 50,
        "dataset_id": "dataset_spot_demo_001"
      }
    ],
    "nfc_tags": [
      {
        "tag_id": "04AABBCCDD",
        "spot_id": "spot_gate_001",
        "status": "active"
      }
    ]
  },
  "error": null,
  "request_id": "req_0001"
}
```

错误：

| code | 含义 |
| --- | --- |
| `device_not_found` | 设备不存在 |
| `device_not_bound` | 设备未绑定角色 |
| `config_not_ready` | 缺少点位、NFC 或数据集配置 |
| `invalid_device_token` | 设备 token 不正确 |

### 5.2 上报设备心跳

```http
POST /api/v1/device-heartbeats
```

请求示例：

```json
{
  "device_id": "device_001",
  "firmware_version": "demo-0.1.0",
  "battery_percent": 82,
  "gps_status": "fixed",
  "event_time": "2026-07-12T10:00:00+08:00"
}
```

用途：管理端展示在线状态和最近设备状态。

### 5.3 上报 GPS 接近事件

```http
POST /api/v1/location-events
```

请求示例：

```json
{
  "device_id": "device_001",
  "spot_id": "spot_gate_001",
  "event_type": "near_spot",
  "latitude": 31.2304,
  "longitude": 121.4737,
  "distance_meters": 36,
  "location_quality": {
    "fix": true,
    "satellites": 8,
    "hdop": 1.2
  },
  "event_time": "2026-07-12T10:01:00+08:00"
}
```

说明：该接口只记录接近事件和定位质量摘要，不产生成功打卡。

约束：

- 设备侧应按 10 秒级节流上报；后端对同设备高频定位事件可丢弃或聚合。
- 一期不保存连续 GPS 轨迹。
- 请求中的 `latitude`、`longitude` 可用于实时判断、演示页最近状态或计算距离，但不写入连续轨迹明细表。
- 如需保存最近状态，只保留设备最近一次位置摘要和定位质量，不保留历史轨迹序列。
- 打卡成功仍以 NFC 合法标签确认为准，GPS 只辅助附近提醒。

### 5.4 上报 NFC 打卡

```http
POST /api/v1/checkins
```

请求示例：

```json
{
  "device_id": "device_001",
  "spot_id": "spot_gate_001",
  "tag_id": "04AABBCCDD",
  "method": "gps_nearby_nfc_confirmed",
  "source": "device",
  "event_time": "2026-07-12T10:02:00+08:00",
  "location_quality": {
    "fix": true,
    "satellites": 8,
    "hdop": 1.2
  }
}
```

响应示例：

```json
{
  "success": true,
  "data": {
    "accepted": true,
    "result": "success",
    "checkin_id": "checkin_001",
    "agent_id": "agent_alo",
    "spot_id": "spot_gate_001",
    "speak_text": "你到啦！这里就是我们今天旅程的第一站。",
    "next_action": "start_spot_qa"
  },
  "error": null,
  "request_id": "req_0002"
}
```

重复打卡响应示例：

```json
{
  "success": true,
  "data": {
    "accepted": false,
    "result": "duplicate",
    "last_checkin_id": "checkin_001",
    "cooldown_seconds": 300
  },
  "error": null,
  "request_id": "req_0003"
}
```

业务错误：

| code | 含义 |
| --- | --- |
| `tag_unknown` | NFC 标签未登记 |
| `tag_disabled` | NFC 标签已停用 |
| `spot_mismatch` | 标签不属于当前点位 |
| `device_not_bound` | 设备未绑定角色 |
| `spot_disabled` | 点位已停用 |

## 6. 管理端 API

### 6.1 设备

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/devices` | 设备列表 |
| `GET` | `/api/v1/devices/{device_id}` | 设备详情 |
| `PATCH` | `/api/v1/devices/{device_id}` | 修改设备显示名称等非关键字段 |

### 6.2 角色智能体

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/agents` | 角色列表 |
| `GET` | `/api/v1/agents/{agent_id}` | 角色详情 |
| `POST` | `/api/v1/agents` | 新建角色 |
| `PATCH` | `/api/v1/agents/{agent_id}` | 编辑角色 |
| `POST` | `/api/v1/agents/{agent_id}/disable` | 停用角色 |

### 6.2.1 智能体上下文

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/agents/{agent_id}/context` | 返回角色 prompt、当前景点上下文、知识库摘要和打卡状态 |

用途：供小智官网侧工具/MCP 或调试页面获取我方生成的智能体上下文。官网侧不保存完整景区知识，只配置调用入口。

### 6.3 绑定

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/bindings?device_id={device_id}` | 查询绑定 |
| `POST` | `/api/v1/bindings` | 建立或更换绑定 |
| `GET` | `/api/v1/binding-events` | 查询绑定变更记录 |

绑定请求示例：

```json
{
  "device_id": "device_001",
  "agent_id": "agent_alo",
  "binding_type": "admin_override",
  "reason": "demo setup"
}
```

### 6.4 景点点位

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/spots` | 点位列表 |
| `GET` | `/api/v1/spots/{spot_id}` | 点位详情 |
| `POST` | `/api/v1/spots` | 新建点位 |
| `PATCH` | `/api/v1/spots/{spot_id}` | 修改点位 |
| `POST` | `/api/v1/spots/{spot_id}/disable` | 停用点位 |

### 6.5 NFC 标签

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/nfc-tags` | 标签列表 |
| `GET` | `/api/v1/nfc-tags/{tag_id}` | 标签详情 |
| `POST` | `/api/v1/nfc-tags` | 新增标签 |
| `PATCH` | `/api/v1/nfc-tags/{tag_id}` | 修改标签 |
| `POST` | `/api/v1/nfc-tags/{tag_id}/disable` | 停用标签 |

### 6.6 打卡记录

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/checkins` | 打卡记录列表 |
| `GET` | `/api/v1/checkins/{checkin_id}` | 打卡记录详情 |

查询参数建议：

| 参数 | 说明 |
| --- | --- |
| `device_id` | 按设备筛选 |
| `spot_id` | 按点位筛选 |
| `result` | 按结果筛选 |
| `source` | `device` / `simulation` |
| `date_from` / `date_to` | 时间范围 |

### 6.7 数据集

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/api/v1/datasets` | 数据集列表 |
| `GET` | `/api/v1/datasets/{dataset_id}` | 数据集详情 |
| `GET` | `/api/v1/datasets/{dataset_id}/chunks` | 查看片段摘要 |
| `POST` | `/api/v1/knowledge/search` | 查询景区知识，供官网侧工具/MCP 或前端调试调用 |
| `POST` | `/api/v1/datasets/{dataset_id}/reprocess` | 重新处理，P1，可选 |

说明：P0 使用真实景区数据集，但格式暂不固定。前端可先按通用字段展示数据集名称、状态、片段摘要、关联角色/点位；上传、重新切分和统一数据格式整改不一定进入 P0。

## 7. 演示与调试 API

### 7.1 演示总览

```http
GET /api/v1/demo/overview
```

用途：实时演示状态页聚合设备、角色、GPS、NFC、打卡和数据集状态。

### 7.2 手动模拟打卡

```http
POST /api/v1/demo/simulate-checkin
```

请求示例：

```json
{
  "device_id": "device_001",
  "spot_id": "spot_gate_001",
  "tag_id": "04AABBCCDD",
  "simulate_gps_nearby": true,
  "reason": "indoor demo"
}
```

响应要求：

| 要求 | 说明 |
| --- | --- |
| 仅测试/原厂账号可用 | 普通演示查看者不可见 |
| 必须写入 `source=simulation` | 不得混入真实记录 |
| 页面必须显示模拟标记 | 避免验收误判 |

## 8. 权限草案

| 角色 | 权限 |
| --- | --- |
| `factory_admin` | 设备、角色、绑定、点位、NFC、数据集、打卡全量管理 |
| `project_admin` | 点位、NFC、数据集、打卡记录、演示页 |
| `tester` | 查看状态、执行模拟打卡 |
| `viewer` | 只看演示总览和打卡结果 |
| `device` | 拉取配置、上报心跳、上报 GPS/NFC 事件 |

## 9. 兼容规则

| 规则 | 说明 |
| --- | --- |
| 新字段必须有默认值 | 避免旧设备解析失败 |
| 设备配置响应允许忽略未知字段 | 固件升级可渐进 |
| 打卡接口幂等 | 同一设备、点位、标签在冷却时间内不重复成功 |
| 模拟数据不参与真实验收统计 | 除非页面明确切换到模拟模式 |
| API 错误必须有稳定 `code` | 前端按 code 展示状态 |
| 历史记录不可因角色改绑丢失 | 打卡记录保留当时解析出的 `agent_id` |

## 10. 待确认问题

| 编号 | 问题 | 责任角色 |
| --- | --- | --- |
| Q-01 | 设备认证二期是否从静态 token 升级为签名或动态 token | 架构师、安全/研发主管 |
| Q-02 | 是否使用 pgvector；一期真实数据集若只做通用展示，可暂不启用 | 架构师、全栈工程师 |
| Q-03 | 数据集最终格式和统一整改时机 | 产品经理、架构师、全栈工程师 |
| Q-04 | 是否需要导出打卡记录 | 产品 P1，研发主管确认排期 |
| Q-05 | 小智官网侧工具/MCP 接入点是否能稳定调用 `/api/v1/agents/{agent_id}/context` 和 `/api/v1/knowledge/search` | 架构师、全栈工程师、产品经理 |

## 11. 当前结论

本文档确认一期自研业务后台需要的 API 能力和数据对象，并以 `/api/v1` REST 风格作为当前建议契约。

后续仍需由全栈工程师结合实现细节确认字段命名、分页格式、认证方式、DRF serializer 和错误码落地。若演示阶段引入 Mock，也必须保留本文中的核心资源、状态码、错误码和兼容规则。
