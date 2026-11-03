# Project Rules Agent Protocol

Use this protocol when a rules/coordination agent receives this skill and needs to apply it to a new software project. The goal is not to copy every rule blindly; the goal is to create a project-specific operating agreement with explicit user confirmation.

## 1. What The Rules Agent Must Read

First read this skill in this order:

1. `SKILL.md`
2. `references/lifecycle-sop.md`
3. `references/role-handbook.md`
4. `references/quality-gates.md`
5. `references/document-format-requirements.md`
6. `references/extracted-collaboration-rules.md`
7. `references/multi-agent-task-ownership.md` when multiple agents or scoped Codex threads will execute work
8. `references/document-status-and-confirmation.md` when project docs require user confirmation

Then inspect the target project:

- root `README`;
- `docs/` if present;
- package/dependency files;
- startup scripts;
- test scripts;
- deployment/config files;
- source directory structure;
- issue/task docs if present.

## 2. First User Confirmation

Before drafting project rules, ask the user these questions:

1. What stage is this project in: idea, MVP, active development, migration, production, or maintenance?
2. How many intelligent agents do you want involved?
3. Here is my recommended agent setup; do you accept it?
4. Should I create a minimal doc set, a full doc set, or only audit existing docs?
5. Are there any hard business, technical, legal, or team boundaries that must override the generic SOP?

Do not proceed with a large multi-agent or full-document setup without user confirmation.

## 3. Recommended Agent Setup

Recommend the smallest effective team:

| Project situation | Suggested agents |
| --- | --- |
| Small bugfix or narrow feature | 1 agent using role lenses as needed |
| MVP / small feature build | 2-3 agents: Product/Engineering Lead, Full-Stack Engineer, QA reviewer |
| Medium product build | 4-5 agents: Product Manager, Architect/Engineering Lead, Frontend, Backend, QA |
| Migration / production launch | 5-7 agents: Product, Architect, Engineering Lead, Frontend, Backend, QA, DevOps/Security as needed |
| Security/data-heavy system | Add Security/Data Governance explicitly |
| Analytics-heavy system | Add Data/Analytics explicitly |
| Public/user-facing docs or handoff-heavy project | Add Technical Writer explicitly |

If the user chooses fewer agents than recommended, consolidate roles and name the risk.
If the user chooses more agents than needed, ask what parallel work or risk reduction justifies the extra roles.

## 4. Section-By-Section Confirmation

Present proposed rules in batches. For each section, ask the user to mark:

```text
Accept / Modify / Defer / Reject
```

Required confirmation sections:

1. Project stage and project goal.
2. Agent/team setup.
3. Lifecycle workflow.
4. Requirement format.
5. Product and scope rules.
6. Architecture and technical decision rules.
7. Development workflow and branch/commit rules.
8. API/data contract rules.
9. Testing and quality gates.
10. Security/data/secrets rules.
11. Release/rollback/operations rules.
12. Documentation set and document format.
13. Review and handoff format.
14. Retrospective and rule-update process.
15. Multi-agent task ownership and scoped reading rules when execution will be split across agents.
16. Document status and confirmation rules.

Do not bury disagreements. If the user modifies or rejects a rule, record the resulting project-specific decision.

## 5. Output The Rules Agent Should Produce

After confirmation, generate one of these outputs depending on project size:

### Minimal Rules File

For small projects:

```text
docs/project_rules.md
```

Include:

- project goal;
- confirmed agent setup;
- workflow;
- requirements format;
- quality gates;
- release/rollback;
- handoff format.

### Full Documentation Set

For serious projects:

```text
docs/README.md
docs/requirements_and_feature_inventory.md
docs/mvp_product_alignment.md
docs/engineering_overview.md
docs/development_process.md
docs/testing_and_quality.md
docs/security_and_data_governance.md
docs/release_operations_runbook.md
docs/web_api_contract.md
```

Add architecture decision, migration blueprint, frontend interaction spec, runbook, domain operation runbook, and dependency selection docs only when relevant.

For multi-agent execution, also generate:

```text
docs/project_role_agents.md
docs/agent_document_requirements.md
docs/development_task_ownership.md
```

Use project-specific names if the repository already has a docs convention.

### Audit Report

For existing projects:

```text
docs/documentation_audit.md
```

Include:

- existing docs found;
- missing required docs;
- stale/conflicting docs;
- proposed doc set by priority;
- rules needing user confirmation.

## 6. Rule Quality Checklist

A valid project rule set must be:

- project-specific, not generic filler;
- small enough to follow;
- explicit about who decides what;
- explicit about what is not allowed;
- testable or reviewable;
- connected to commands, scripts, docs, or code paths where possible;
- clear about release and rollback;
- clear about how rules get changed later.
- clear about which documents are confirmed, pending, implemented, blocked, or deprecated.
- clear about which agent may read and edit which module when scoped execution is used.

## 7. Required Handoff

When done, report:

- confirmed agent count and role split;
- documents created or updated;
- document statuses and unresolved confirmations;
- rules accepted, modified, deferred, or rejected;
- unresolved questions;
- next implementation step.

If any section was not confirmed, state that clearly instead of implying the rule set is final.
