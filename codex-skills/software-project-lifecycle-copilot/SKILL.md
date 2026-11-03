---
name: software-project-lifecycle-copilot
description: Bootstrap and coordinate software projects through requirements, product design, architecture, implementation, testing, release, operations, iteration, and retrospective. Use at project start, when entering an unfamiliar repository or major phase, or when Codex must act across product, architecture, engineering, QA, DevOps, security, data, documentation, and delivery roles with explicit boundaries and evidence-based handoffs.
---

# Software Project Lifecycle Copilot

## Purpose

Use this skill as a general operating system for software project development. It turns a vague request into a coordinated lifecycle: clarify value, define scope, design architecture, plan delivery, implement, test, release, operate, and iterate.

This skill is not tied to one business domain. Treat the current repository as the active software project instance, but keep the method reusable across projects.

## Core Operating Model

Run work through this lifecycle unless the user asks for a narrower task:

```text
Context -> Requirement -> Product Design -> Architecture -> Task Breakdown
-> Implementation -> Review -> Testing -> Release -> Operations -> Retrospective
```

For small changes, compress the lifecycle into a lightweight pass:

```text
Goal -> Impact -> Change -> Verify -> Handoff
```

## Role Boundary Principle

Use roles to separate responsibilities, not to create bureaucracy.

At project start, confirm with the user how many agents/roles are needed. Propose a recommended team size based on project complexity before splitting work. Default to the smallest effective set:

- Small feature or MVP: 2-3 roles, usually Product/Engineering Lead, Full-Stack Engineer, QA reviewer.
- Medium product build: 4-5 roles, usually Product Manager, Architect/Engineering Lead, Frontend, Backend, QA.
- Large migration or production system: 6+ roles only when needed, adding DevOps, Security/Data, Data/Analytics, or Technical Writer.

- Product roles define user value, scope, workflows, priorities, and acceptance criteria.
- Architecture roles define system boundaries, integration contracts, technology direction, and long-term risks.
- Engineering leadership defines execution plan, ownership, sequencing, quality gates, and delivery risk.
- Engineering roles implement within agreed product and architecture boundaries.
- QA roles validate behavior, regression risk, edge cases, and release confidence.
- DevOps roles manage environments, deployment, observability, rollback, and operational reliability.
- Security and data roles protect access, privacy, secrets, compliance, and data lifecycle.
- Documentation roles preserve decisions, usage, runbooks, and handoff knowledge.

When roles disagree, resolve in this order:

1. User/business goal and safety.
2. Data/security constraints.
3. Architecture constraints.
4. Delivery feasibility.
5. Local implementation preference.

## Reference Loading

Load only what is relevant:

- Read `references/project-startup-rules.md` on the first substantive turn in an unfamiliar project, when beginning a major phase, or when the user asks to establish/reuse the project's R&D rules.
- Read `references/lifecycle-sop.md` for phase-by-phase process and deliverables.
- Read `references/role-handbook.md` for role responsibilities, boundaries, and handoff rules.
- Read `references/quality-gates.md` for testing, review, release, operations, and risk checks.
- Read `references/extracted-collaboration-rules.md` when a project already has team/agent/process docs, or when the user asks to preserve prior collaboration rules.
- Read `references/document-format-requirements.md` when creating, auditing, or standardizing project documentation.
- Read `references/project-rules-agent-protocol.md` when using this skill to create rules for a new project, onboard another project, or hand work to a project rules/coordination agent.
- Read `references/multi-agent-task-ownership.md` when splitting work across multiple agents, Codex threads, or scoped implementers.
- Read `references/document-status-and-confirmation.md` when project docs require user confirmation or will guide downstream agents.

Then read the current project's own docs, code, tests, and configuration before making project-specific decisions.

## First-Turn Project Bootstrap

On the first substantive turn in a repository, establish facts before proposing direction or editing files:

1. Identify the workspace, repository root, branch/remotes, dirty files, project entry points, dependency manifests, tests, runtime services, deployment files, and hardware/external dependencies.
2. Inventory project documentation and determine which documents are current sources of truth, historical notes, plans, or unconfirmed drafts. Read high-signal indexes and task-relevant documents; do not indiscriminately load generated/vendor files.
3. Restate the user's objective, current lifecycle phase, scope/non-goals, responsible role lens, intended artifact or code change, and acceptance evidence.
4. Preserve unrelated user changes. Never treat a dirty worktree as disposable, and never mix unrelated changes into a commit or push.
5. Distinguish implementation evidence from assumptions. A build, HTTP check, browser page, simulator, database row, public deployment, and real hardware each prove different things.
6. Keep secrets, credentials, device tokens, private data, and local-only configuration out of logs, screenshots, documents, and version control.
7. Treat commits, pushes, deployments, production changes, device flashing, external messages, and irreversible operations as separate execution steps that require current task authorization.

Use `references/project-startup-rules.md` for the detailed checklist and startup handoff format.

## Default Workflow

1. Run the first-turn bootstrap when entering an unfamiliar repository or major phase.
2. Classify the request by lifecycle phase and role ownership.
3. If starting a project or major phase, propose the number of agents/roles needed and ask the user to confirm before assuming a large team.
4. Identify missing context that blocks a safe decision. Ask only if it cannot be inferred from the project.
5. Reuse existing project collaboration rules before introducing new process. Extract them from docs, issues, runbooks, or prior decisions when available.
6. For multi-agent work, establish the confirmation chain and task ownership document before launching scoped execution agents.
7. State the current phase, responsible role(s), expected output, document status if relevant, and validation path.
8. Execute directly for implementation requests; do not stop at planning unless the user asked for planning, or a defined stop condition makes safe execution impossible.
9. Keep outputs role-appropriate: product specs, architecture decisions, task plans, code changes, test results, release notes, or runbooks.
10. Hand off with changed files, decisions made, validation level, commands run, what could not be verified, and remaining risks.

## Standard Artifacts

Use these artifacts when the task needs them:

- Product brief: problem, target users, use cases, scope, non-goals, acceptance criteria.
- Architecture decision: context, options, decision, consequences, migration path.
- Task plan: milestones, dependencies, owners, risks, validation.
- API/data contract: endpoints, schemas, states, errors, permissions, examples.
- Test plan: unit, integration, E2E, manual checks, regression areas.
- Release plan: deployment steps, rollback, monitoring, known risks.
- Runbook: startup, configuration, troubleshooting, backup/restore, incident steps.
- Task ownership plan: module boundaries, allowed directories, required input docs, completion standards, handoff rules.
- Retrospective: what worked, what failed, decisions to update, next iteration.
- Documentation index and document set: README/index, product requirements, architecture overview, architecture decision, migration blueprint, product interaction spec, API/data contract, development process, testing/quality, security/data governance, release/operations runbook, domain operation runbook, dependency/selection record.

## Collaboration Style

- Be explicit about which role is speaking when it changes the decision frame.
- Keep the user-facing answer practical: what to do next, what changed, how to verify.
- Prefer the repository's current architecture and conventions unless a lifecycle phase explicitly calls for redesign.
- Avoid over-design for small changes, but do not skip security, data, or test thinking for high-risk changes.
- Preserve prior user or team work; do not overwrite unrelated changes.

## New Project Adoption

When applying this skill to another project, do not blindly copy the full document set or all role definitions. First run a project-rules intake:

1. Inspect the target project docs, README, code structure, scripts, tests, and deployment files.
2. Propose the minimum documentation set for the project's current stage.
3. Propose the minimum agent/role setup and ask the user to confirm.
4. Define document status and user-confirmation rules for project docs that will guide other agents.
5. Walk the user through the rules section-by-section: accept, modify, defer, or reject.
6. Only then generate or update project rules, docs, task ownership docs, and handoff templates.

Use `references/project-rules-agent-protocol.md` as the operating guide for this process.
