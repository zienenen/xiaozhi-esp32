# 盲盒交互陪伴机器人项目资料

本目录用于集中存放本项目二次开发产生的资料，避免与小智开源项目自带文档混在 `docs` 根目录。

## 文档入口

建议先读：

1. [document_index.md](document_index.md) - 项目文档索引与阅读顺序
2. [project_role_agents.md](project_role_agents.md) - 项目角色分工与协作规则
3. [agent_document_requirements.md](agent_document_requirements.md) - 智能体文档责任、缺口补齐和用户核对规则
4. [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) - 一期工程实施计划
5. [development_process.md](development_process.md) - 一期研发流程
6. [testing_and_quality.md](testing_and_quality.md) - 一期测试与质量门
7. [release_operations_runbook.md](release_operations_runbook.md) - 一期发布与演示运行手册
8. [rd_lead_question_list.md](rd_lead_question_list.md) - 研发主管问题清单
9. [security_and_data_governance.md](security_and_data_governance.md) - 一期最低安全与数据治理边界
10. [open_source_selection.md](open_source_selection.md) - 一期开源选型与复用边界
11. [phase1_single_robot_budget.md](phase1_single_robot_budget.md) - 一期预算与淘宝/京东采购清单

## 当前一期范围

- 1 台自装演示机器人
- ESP32-S3 主控
- GPS 需要
- NFC 需要
- 电池需要
- 基础固定即可，不做正式外壳
- 包含焊接工具和耗材
- 不计算云服务器
- 目标成本控制在 500 元以内

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [document_index.md](document_index.md) | 项目文档总索引 |
| [xiaozhi_existing_capabilities_analysis.md](xiaozhi_existing_capabilities_analysis.md) | 小智现有能力分析 |
| [blindbox_agent_tourism_demo_prd.md](blindbox_agent_tourism_demo_prd.md) | 盲盒角色旅游打卡 Demo 需求 |
| [phase1_phase2_architecture_plan.md](phase1_phase2_architecture_plan.md) | 一期/二期架构建议 |
| [phase1_single_robot_implementation_plan.md](phase1_single_robot_implementation_plan.md) | 一期工程实施计划 |
| [development_process.md](development_process.md) | 一期研发流程、阶段门、提交规则 |
| [testing_and_quality.md](testing_and_quality.md) | 一期测试与质量门 |
| [release_operations_runbook.md](release_operations_runbook.md) | 一期发布、演示和故障处理手册 |
| [rd_lead_question_list.md](rd_lead_question_list.md) | 需要用户确认的问题清单和默认推进规则 |
| [security_and_data_governance.md](security_and_data_governance.md) | 一期最低安全与数据治理边界，覆盖设备凭据、GPS/NFC、日志和演示账号 |
| [open_source_selection.md](open_source_selection.md) | 一期开源选型与复用边界，明确当前采用组件、暂缓组件和商业化前治理项 |
| [phase1_single_robot_budget.md](phase1_single_robot_budget.md) | 一期预算和采购清单 |
| [fullstack_implementation_guide.md](fullstack_implementation_guide.md) | 全栈实施说明 |
| [project_role_agents.md](project_role_agents.md) | 项目角色与协作边界 |
| [agent_document_requirements.md](agent_document_requirements.md) | 智能体文档责任、缺失文档补齐顺序和用户核对规则 |
| [requirements_and_feature_inventory.md](requirements_and_feature_inventory.md) | 双主线需求、优先级、既有功能和待确认项清单 |
| [mvp_product_alignment.md](mvp_product_alignment.md) | 课题优先、市场化兼容的 MVP 产品口径 |
| [django_react_frontend_product_interaction_spec.md](django_react_frontend_product_interaction_spec.md) | Django + React 三端页面产品交互规格草案 |
| [product_manager_handoff_checklist.md](product_manager_handoff_checklist.md) | 产品经理交接给架构、研发、全栈的 P0 结论和缺口清单 |
| [engineering_overview.md](engineering_overview.md) | 已确认的工程架构总览，说明一期工程边界、模块划分、数据流、状态模型和风险 |
| [frontend_backend_architecture_decision.md](frontend_backend_architecture_decision.md) | 前后端架构决策，确认一期采用 Django/DRF + PostgreSQL + React 轻量三端，并套用 xiaozhi.me 语音/MCP 能力 |
| [web_api_contract.md](web_api_contract.md) | 已确认的一期 Web API 与数据契约，覆盖设备、角色、点位、NFC、打卡、数据集、智能体上下文和知识库查询入口 |
| [../../PROJECT_STRUCTURE.md](../../PROJECT_STRUCTURE.md) | 当前单仓多模块工程结构说明，标明 `backend/`、`frontend/`、`tools/device_simulator/`、`deploy/` 职责 |
| [marketization_related.md](marketization_related.md) | 市场化方向资料 |
| [market_competitor_analysis_internal.md](market_competitor_analysis_internal.md) | 内部竞品分析 |
| [research_topic_related.md](research_topic_related.md) | 课题/科研方向资料 |
