# 项目文档索引与关联关系

## 1. 文档分层

| 层级 | 文档 | 作用 |
| --- | --- | --- |
| 底座分析 | [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md) | 说明小智 ESP32 已有能力，以及对市场化/课题方向的支撑 |
| 市场化需求 | [marketization_related.md](marketization_related.md) | 面向 18-26 岁潮玩用户的 AI 盲盒实体机器人需求说明 |
| 市场化竞品 | [market_competitor_analysis_internal.md](market_competitor_analysis_internal.md) | 内部竞品分析，支撑市场化定位和一期取舍 |
| 课题需求 | [research_topic_related.md](research_topic_related.md) | 面向课题/科研/项目申报的景区数据 + GPS 智能体方向 |
| 综合早期 PRD | [blindbox_agent_tourism_demo_prd.md](blindbox_agent_tourism_demo_prd.md) | 早期综合版，包含盲盒、景区、GPS、后台等混合需求，后续应拆分引用 |
| 架构建议 | [phase1_phase2_architecture_plan.md](phase1_phase2_architecture_plan.md) | 一期/二期架构建议，偏课题 Demo 与工程落地 |
| 实施计划 | [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) | 单台演示机器人落地计划，偏研发执行 |
| 全栈实施 | [fullstack_implementation_guide.md](fullstack_implementation_guide.md) | 后端、前端、设备端联调实施说明 |
| 预算采购 | [phase1_single_robot_budget.md](phase1_single_robot_budget.md) | 单台演示机器人采购预算 |
| 角色分工 | [project_role_agents.md](project_role_agents.md) | 产品、架构、研发、全栈等角色责任边界 |

## 2. 当前推荐阅读顺序

### 市场化方向

1. [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md)
2. [market_competitor_analysis_internal.md](market_competitor_analysis_internal.md)
3. [marketization_related.md](marketization_related.md)
4. [project_role_agents.md](project_role_agents.md)

### 课题方向

1. [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md)
2. [research_topic_related.md](research_topic_related.md)
3. [phase1_phase2_architecture_plan.md](phase1_phase2_architecture_plan.md)
4. [fullstack_implementation_guide.md](fullstack_implementation_guide.md)
5. [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md)
6. [phase1_single_robot_budget.md](phase1_single_robot_budget.md)

## 3. 口径说明

| 问题 | 当前口径 |
| --- | --- |
| 市场化主线 | AI 智能体结合拉布布式盲盒商业模式，面向 18-26 岁潮玩用户 |
| 课题主线 | 基于景区数据集、向量数据库和 GPS 到点触发的智能体交互系统 |
| 小智 ESP32 | 两个方向共用的硬件语音交互底座 |
| 景区/GPS | 课题方向 P0；市场化方向作为后续场景扩展 |
| 管理端 | 市场化和课题方向都需要一期最小管理能力，但管理对象不同 |
| 早期综合 PRD | 保留为需求演进记录，不作为单一最终口径 |

