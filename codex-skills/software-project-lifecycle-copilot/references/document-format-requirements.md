# Document Format Requirements

These requirements are extracted from the current project's `docs/` directory and generalized for future software projects. Use them when creating a new project documentation set or auditing an existing one.

## 1. Required Document Set

Every serious software project should maintain these documents under `docs/`:

| File | Purpose |
| --- | --- |
| `README.md` | Documentation index, recommended reading order, maintenance rules. |
| `requirements_and_feature_inventory.md` | Product requirements, feature inventory, current completion status, known limits, roadmap. |
| `mvp_product_alignment.md` | Product positioning, target users, P0/P1/P2 scope, demand judgment rules. |
| `engineering_overview.md` | Current architecture, tech stack, runtime entries, modules, data flow, storage, state model, risks. |
| `frontend_backend_architecture_decision.md` | Architecture decision record and option comparison for frontend/backend/database/task choices. |
| `migration_blueprint_<target>.md` | Migration strategy, target architecture, data mapping, API strategy, schedule, rollback, acceptance. Required when changing architecture. |
| `<stack>_architecture_task_plan.md` | Confirmed architecture direction and executable backend/frontend/task breakdown. |
| `<stack>_frontend_product_interaction_spec.md` | Frontend product information architecture, page behavior, components, API dependencies, UI acceptance. |
| `<stack>_runbook.md` | Startup, build, migration, environment variables, integrated serving, deployment notes. |
| `web_api_contract.md` | API routes, request/response shape, data models, compatibility rules, errors. |
| `development_process.md` | Development lifecycle, requirements format, design checks, coding rules, branch/commit rules, review/merge standards. |
| `testing_and_quality.md` | Test objectives, commands, test layers, minimum test requirements, regression checklist, known quality debt. |
| `security_and_data_governance.md` | Sensitive data, commit boundaries, external calls, secrets, deletion/recovery, backups, security checklist. |
| `release_operations_runbook.md` | Release checks, smoke tests, version notes, backup/restore, common failures, rollback, operations checklist. |
| `<domain>_application_runbook.md` | Real user workflow runbook for the domain's operational process. |
| `open_source_selection.md` | Upstream/dependency selection principles, adopted projects, local adaptation layer, verified workflow. |

Projects may rename stack/domain prefixes, but should preserve the document responsibilities.

## 2. Documentation Index Requirements

`docs/README.md` must include:

- one-sentence purpose for the documentation folder;
- recommended reading order;
- list of current business/domain documents;
- document maintenance rules.

Maintenance rules must state:

- feature changes update architecture, API, or runbooks when affected;
- data structure changes update contracts and migration/compatibility notes;
- external calls, generation logic, automation, or high-risk behavior changes update testing and risk boundaries;
- docs must match current code; plans must be explicitly marked as planned or todo.

## 3. Product Requirement Document Format

Use this structure:

```markdown
# <Project> 需求说明书与功能清单

更新时间：YYYY-MM-DD

## 0. 需求方向调整
## 0.1 当前已实现
## 1. 项目背景
## 2. 项目目标
### 2.1 核心目标
### 2.2 使用边界 / 非目标
## 3. 选型或依赖来源
## 4. 用户画像 / 目标用户 / 业务画像
## 5. 已实现功能清单
## 6. 当前目录结构
## 7. 当前主要命令或入口总览
## 8. 当前已知限制
## 9. 后续规划
### 9.1 短期
### 9.2 中期
### 9.3 长期
## 10. 当前完成度总结
```

Feature entries should include:

- command/API/page entry;
- behavior;
- input/output files or data;
- status changes;
- example artifacts;
- validation status where known.

## 4. MVP/Product Alignment Document Format

Use when product scope can drift.

Required sections:

- one-sentence positioning;
- primary customer/user;
- users not prioritized;
- core problems;
- product mainline workflow;
- P0 required capabilities;
- P1 enhancements;
- P2 deferred capabilities;
- demand judgment criteria;
- AI/agent collaboration requirements if applicable;
- current-stage product boundary.

Demand judgment should answer:

- Does this serve the main workflow?
- Does it improve user certainty or completion?
- Does it increase maintenance burden?
- Does it require platform/external complexity?
- Can it fit the current release boundary?

## 5. Engineering Overview Format

Required sections:

- project positioning;
- tech stack;
- runtime modes / entry points;
- core modules table: module, file/path, responsibility;
- data flow diagrams where useful;
- storage structure table;
- state model;
- rule vs AI/external capability boundary if applicable;
- architecture risk points.

Use stable state codes plus display labels when possible. Avoid using localized display strings as primary state values in long-lived systems.

## 6. Architecture Decision Format

Use for major technical choices.

Required sections:

- document purpose;
- decision summary;
- current state;
- why change may or may not be required;
- candidate options;
- comparison table;
- recommendation by product goal or scale;
- concurrency/operations impact;
- migration cost and risk;
- decision questions;
- final recommendation.

For each option, cover:

- architecture shape;
- suitable scenarios;
- advantages;
- disadvantages;
- concurrency impact;
- deployment impact;
- migration cost;
- conclusion.

## 7. Migration Blueprint Format

Use when moving frameworks, data stores, architecture, or runtime shape.

Required sections:

- migration conclusion;
- whether migration is necessary by scenario;
- target goals: technical, product, engineering;
- current architecture problems;
- target architecture tree;
- data model mapping;
- API migration strategy;
- frontend migration strategy;
- phased schedule;
- bypass/parallel migration rationale;
- rollback strategy;
- acceptance checklist;
- first implementation tasks;
- decision record.

Migration must preserve a working fallback until the new path passes the main workflow and data reconciliation.

## 8. Architecture Task Plan Format

Use after architecture direction is decided.

Required sections:

- total goal;
- architecture confirmation;
- current problem judgment;
- target information architecture;
- first-version feature mapping table;
- backend task breakdown with task IDs;
- frontend task breakdown with task IDs;
- recommended directory structure;
- migration priorities: P0/P1/P2;
- scale/productization requirements;
- agent handoff method;
- acceptance checklist;
- next recommended implementation order.

Task entries should include:

- goal;
- suggested API/page/component;
- implementation notes;
- safety or compatibility boundary;
- acceptance.

## 9. Frontend Product Interaction Spec Format

Use for workbench/admin/product UI.

Required sections:

- document purpose;
- product positioning;
- navigation/information architecture;
- global interaction principles;
- long-task feedback model;
- user confirmation model for AI/generated content;
- page-by-page specification;
- component suggestions;
- API dependency list;
- P0 frontend delivery order;
- acceptance checklist.

For each page:

- goal;
- content;
- key interactions;
- components;
- states;
- acceptance.

Operational tools should start at the workbench, not a marketing page.

## 10. API And Data Contract Format

Required sections:

- overview and base URL/context;
- common conventions;
- endpoint groups by domain;
- method/path;
- purpose;
- request body example;
- response fields/example;
- side effects;
- errors;
- data tables/models;
- compatibility requirements.

Compatibility requirements:

- old data remains readable;
- new fields have defaults;
- malformed/historical JSON has fallback;
- response shape changes update frontend and tests;
- docs are updated with API changes.

## 11. Development Process Format

Required sections:

- goal and applicable change types;
- requirement-stage required fields: background, user, input, output, boundary, acceptance;
- design-stage impact table;
- development environment;
- branch and commit rules;
- coding standards;
- development checklist;
- code review standards;
- merge standards;
- retrospective and continuous improvement.

The design impact table should cover CLI, Web/API, data structures, business rules, generated content, AI/external calls, browser/automation, and frontend UI as applicable.

## 12. Testing And Quality Format

Required sections:

- test objectives;
- test commands;
- current coverage table;
- test layers: unit, integration, manual/E2E;
- minimum test requirements by change type;
- test data rules;
- quality gate;
- regression focus;
- known quality debt.

Test data must avoid real secrets and private user data. External/browser/API behavior should be mockable for automated tests.

## 13. Security And Data Governance Format

Required sections:

- principles;
- sensitive data inventory table;
- git commit boundaries: prohibited and allowed;
- external/AI/API call boundary;
- platform/automation boundary if applicable;
- local config and secret handling;
- deletion and recovery;
- backup recommendations;
- security checklist.

Secrets must not be returned by GET endpoints, printed in logs, committed to git, or exposed to frontend code.

## 14. Release And Operations Runbook Format

Required sections:

- release goal;
- pre-release checks and commands;
- manual smoke-test flow;
- release note template;
- local or production run commands;
- backup and restore;
- common failures and troubleshooting;
- rollback strategy;
- operations checklist.

For every release, record:

- added/fixed/changed items;
- data compatibility notes;
- validation commands;
- known issues;
- rollback instructions.

## 15. Domain Operation Runbook Format

Use for real user workflows.

Required sections:

- purpose and scope;
- start-before checks;
- prerequisite data/config confirmation;
- step-by-step workflow;
- commands/UI actions;
- expected outputs;
- manual review points;
- status marking;
- batch workflow if any;
- common issues;
- recommended daily/weekly cadence.

This document should be usable without reading source code.

## 16. Open Source / Dependency Selection Format

Required sections:

- selection principles;
- upstream/dependency list;
- purpose of each upstream/dependency;
- adoption reason;
- planned local adaptation;
- local added layer;
- verified workflow.

Do not only list dependencies; explain which responsibilities are borrowed and which are deliberately changed.

## 17. Cross-Document Rules

- Use Markdown.
- Use `更新时间：YYYY-MM-DD` for living decision/product docs when useful.
- Use numbered major sections for stable long documents.
- Use tables for module lists, comparisons, API/data contracts, test coverage, and completion summaries.
- Use fenced code blocks for commands, env vars, paths, API examples, directory trees, and state codes.
- Keep command examples copy-pasteable.
- Mark plans as “计划” or “待办”; do not present planned work as implemented.
- Prefer stable English codes for machine state and localized labels for display.
- Document rollback for risky architecture, migration, release, or data changes.
- Keep docs aligned with current code; update docs in the same change when behavior changes.

## 18. Minimum Documentation Set By Project Stage

Small MVP:

- `README.md`
- `requirements_and_feature_inventory.md`
- `engineering_overview.md`
- `development_process.md`
- `testing_and_quality.md`
- `release_operations_runbook.md`

Productized web app:

- all Small MVP docs;
- `mvp_product_alignment.md`;
- `frontend_backend_architecture_decision.md`;
- `web_api_contract.md`;
- `security_and_data_governance.md`;
- stack-specific runbook.

Major migration:

- all Productized web app docs;
- `migration_blueprint_<target>.md`;
- `<stack>_architecture_task_plan.md`;
- `<stack>_frontend_product_interaction_spec.md`;
- migration acceptance and rollback notes.

Domain with repeatable operations:

- all relevant above;
- `<domain>_application_runbook.md`;
- `open_source_selection.md` when using upstream projects or large dependencies.
