# 项目文档索引与关联关系

## 1. 文档分层

| 层级 | 文档 | 作用 |
| --- | --- | --- |
| 底座分析 | [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md) | 说明小智 ESP32 已有能力，以及对市场化/课题方向的支撑 |
| 市场化需求 | [marketization_related.md](marketization_related.md) | 面向 18-26 岁潮玩用户的 AI 盲盒实体机器人需求说明 |
| 市场化竞品 | [market_competitor_analysis_internal.md](market_competitor_analysis_internal.md) | 内部竞品分析，支撑市场化定位和一期取舍 |
| 需求清单 | [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) | 产品经理维护的双主线需求、优先级、既有功能和待确认项清单 |
| MVP 对齐 | [mvp_product_alignment.md](mvp_product_alignment.md) | 课题优先、市场化兼容的 MVP 产品口径 |
| 页面交互 | [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | Django + React 三端页面的产品交互规格草案 |
| 产品交接 | [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md) | 产品经理交给架构、研发、全栈的 P0 结论、验收和缺口清单 |
| 工程总览 | [engineering_overview.md](engineering_overview.md) | 架构师文档，描述已确认的一期工程边界、目标模块、数据流、状态模型和待确认风险 |
| 架构决策 | [frontend_backend_architecture_decision.md](frontend_backend_architecture_decision.md) | 前后端架构决策，确认一期采用最小业务后台、响应式 Web、Django/DRF、PostgreSQL、React 和官网语音链路 |
| API 契约 | [web_api_contract.md](web_api_contract.md) | 基于一期已确认框架的 Web API 与数据契约，覆盖设备、角色、点位、NFC、打卡、数据集、智能体上下文和知识库查询入口 |
| 工程结构 | [../../PROJECT_STRUCTURE.md](../../PROJECT_STRUCTURE.md) | 当前单仓多模块目录说明，面向研发主管和全栈工程师交接 |
| 课题需求 | [research_topic_related.md](research_topic_related.md) | 面向课题/科研/项目申报的景区数据 + GPS 智能体方向 |
| 综合早期 PRD | [blindbox_agent_tourism_demo_prd.md](blindbox_agent_tourism_demo_prd.md) | 早期综合版，包含盲盒、景区、GPS、后台等混合需求，后续应拆分引用 |
| 架构建议 | [phase1_phase2_architecture_plan.md](phase1_phase2_architecture_plan.md) | 一期/二期架构建议，偏课题 Demo 与工程落地 |
| 实施计划 | [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) | 单台演示机器人落地计划，偏研发执行 |
| 全栈实施 | [fullstack_implementation_guide.md](fullstack_implementation_guide.md) | 后端、前端、设备端联调实施说明 |
| 预算采购 | [phase1_single_robot_budget.md](phase1_single_robot_budget.md) | 单台演示机器人采购预算 |
| 角色分工 | [project_role_agents.md](project_role_agents.md) | 产品、架构、研发、全栈等角色责任边界 |
| 智能体文档要求 | [agent_document_requirements.md](agent_document_requirements.md) | 四类智能体的文档责任、缺失资料补齐顺序和逐项核对规则 |

## 2. 当前推荐阅读顺序

### 市场化方向

1. [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md)
2. [market_competitor_analysis_internal.md](market_competitor_analysis_internal.md)
3. [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md)
4. [mvp_product_alignment.md](mvp_product_alignment.md)
5. [marketization_related.md](marketization_related.md)
6. [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md)
7. [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md)
8. [project_role_agents.md](project_role_agents.md)
9. [agent_document_requirements.md](agent_document_requirements.md)

### 课题方向

1. [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md)
2. [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md)
3. [mvp_product_alignment.md](mvp_product_alignment.md)
4. [research_topic_related.md](research_topic_related.md)
5. [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md)
6. [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md)
7. [engineering_overview.md](engineering_overview.md)
8. [frontend_backend_architecture_decision.md](frontend_backend_architecture_decision.md)
9. [web_api_contract.md](web_api_contract.md)
10. [phase1_phase2_architecture_plan.md](phase1_phase2_architecture_plan.md)
11. [fullstack_implementation_guide.md](fullstack_implementation_guide.md)
12. [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md)
13. [phase1_single_robot_budget.md](phase1_single_robot_budget.md)
14. [project_role_agents.md](project_role_agents.md)
15. [agent_document_requirements.md](agent_document_requirements.md)

## 3. 口径说明

| 问题 | 当前口径 |
| --- | --- |
| 市场化主线 | AI 智能体结合拉布布式盲盒商业模式，面向 18-26 岁潮玩用户 |
| 课题主线 | 基于景区数据集、向量数据库、GPS 粗定位和 NFC 精准打卡的智能体交互系统 |
| 小智 ESP32 | 两个方向共用的硬件语音交互底座 |
| 景区/GPS | 课题方向 P0；市场化方向作为后续场景扩展 |
| 管理端 | 市场化和课题方向都需要一期最小管理能力，但管理对象不同 |
| 一期技术框架 | ESP32 小智固件 + `xiaozhi.me` 语音/MCP 不可见依赖 + Django/DRF + PostgreSQL + React/Ant Design Pro 轻量三端 |
| 官网能力 | 一期不复刻官网页面；官网仅作为内部依赖，对外展示自研页面和景区业务闭环 |
| 工程脚手架 | 已采用单仓多模块：`main/` 保留固件，`backend/` 放 Django/DRF，`frontend/` 放 React/Vite，`tools/device_simulator/` 放无硬件模拟器，`deploy/` 放部署参考 |
| 早期综合 PRD | 保留为需求演进记录，不作为单一最终口径 |
