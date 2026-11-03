# Extracted Collaboration Rules

These rules were abstracted from the current project's prior collaboration/process docs. Use them as reusable software-project collaboration patterns. When a future project has its own rules, extract and adapt them the same way.

## Rule 1: Existing Process Docs Are Source Material

Before creating a new SOP, inspect and reuse existing project rules:

- docs index / README;
- development process;
- architecture plan;
- migration plan;
- frontend/product interaction spec;
- API/data contract;
- testing and quality guide;
- security/data governance guide;
- release and operations runbook.

Do not replace existing team decisions with generic advice unless the user asks for a reset.

## Rule 2: Every Requirement Needs Six Fields

For non-trivial work, capture:

- background: why this matters and which real problem it solves;
- user: who uses or maintains it;
- input: what data, config, file, API, or user action enters the workflow;
- output: what page state, API response, file, report, database record, or artifact is produced;
- boundary: what is explicitly not done;
- acceptance: which command, test, page flow, or review proves completion.

This format keeps product, architecture, engineering, and QA aligned.

## Rule 3: Design Starts With Impact Surface

Before implementation, classify the affected surface and confirm the right details:

- CLI command: parameters, output, state files, errors, tests.
- Web/API: route, request body, response body, status codes, frontend compatibility.
- Data structure: tables, JSON/files, defaults, migration, backward compatibility.
- Scoring/rules/business logic: weights, thresholds, sample cases, false positives, false negatives.
- Generation/content logic: fact/source of truth, output format, review point, downloadable artifacts.
- AI/external call: prompt, model/config, timeout, failure fallback, privacy boundary.
- Browser/automation: selectors, visible user interaction, login/session boundary, platform or abuse risk.
- Frontend/product UI: navigation, page ownership, loading/empty/error states, task status, responsive behavior.

Design notes should include current state, proposed solution, data/API changes, risks, fallback/degradation, test plan, and rollback.

## Rule 4: Role Handoffs Must Be Explicit

When multiple agents or roles cooperate, each role must start from shared docs and finish with a handoff.

Start-of-work checklist:

- read the project's architecture/task plan;
- read migration or product interaction specs when relevant;
- read requirements/features inventory or equivalent;
- read the actual code and tests for the target module.

Completion handoff:

- modules/files changed;
- task or requirement identifier if any;
- API/page/user-flow acceptance path;
- test commands and results;
- whether legacy/fallback entry points are affected;
- commit/push/deployment status when applicable;
- remaining risks and next action.

## Rule 4.1: Scoped Execution Agents Read Only Their Assignment

When a project uses multiple execution agents, first create a module ownership
document. Each execution agent should read only its assigned section and the
required input docs named there, plus directly relevant code/tests/config.

This reduces context drift and prevents agents from changing unrelated product,
architecture, API, hardware, or release decisions. If the assigned section is
insufficient or conflicts with another source, the agent should stop and report
the conflict to the responsible upstream role.

## Rule 5: Prioritize With P0/P1/P2

Use priority levels to prevent scope blur:

- P0: necessary for a usable workflow or core architecture boundary.
- P1: needed for a complete first release.
- P2: scale, hardening, observability, polish, automation, or future productization.

Do not let P2 work block a P0 usable path unless it is a security/data integrity prerequisite.

## Rule 6: Migration Uses Bypass, Not Big-Bang Rewrite

When replacing architecture:

- keep the old system working as a legacy/fallback path;
- build the new path alongside it;
- migrate one vertical slice at a time;
- keep old data read-only where possible during import;
- write new data to the new system;
- reconcile counts and important records;
- document rollback.

Avoid deleting the old path before the new path passes the main workflow and data reconciliation.

## Rule 7: State Source And File Artifacts Must Be Clear

For productized systems:

- define the system of record;
- store metadata, ownership, status, and paths in durable state;
- treat generated files as artifacts, not hidden state;
- avoid frontends scraping local folders or implementation details as their primary API;
- preserve version history when users can review or rely on generated artifacts.

## Rule 8: Long Tasks Need Status

Operations that can block, fail externally, or consume heavy resources should expose task state instead of only a toast or synchronous spinner.

Minimum state model:

```text
idle -> queued -> running -> success | failed
```

Failure should include a readable reason and a retry or next-action path.

## Rule 9: Frontend Workbench Rules

For operational software tools:

- first screen should be the workbench, not a marketing page;
- use stable navigation and module pages instead of a single endless form;
- tables are appropriate for pools, inventories, records, and progress;
- drawers/modals keep create/edit/detail flows in context;
- show loading, empty, error, success, and permission states;
- make status and next action visible;
- page structure should follow the user's workflow, not backend table names alone.

## Rule 10: API And Data Contracts Must Stay Compatible

When changing APIs or schemas:

- keep old data readable;
- provide defaults for new fields;
- add migration or import compatibility where needed;
- parse malformed/old JSON defensively when historical data exists;
- update frontend callers and tests in the same change;
- update API/data docs.

## Rule 11: Quality Gates Are Risk-Based

Minimum validation depends on the change:

- docs-only: proofread and ensure links/claims match current code;
- pure logic: unit tests;
- API/data: integration tests for success and failure;
- frontend workflow: build/typecheck plus manual or automated flow verification;
- external/browser/PDF: mockable tests plus targeted manual verification;
- migration: dry run, backup note, reconciliation report;
- security/permissions: negative tests.

Always report what was run. If a test was skipped, say why.

Validation must name the level actually achieved: unit tested, build passed,
integration tested, local formal environment verified, public demo verified,
hardware verified, or externally blocked. A simulator or mock flow must not be
reported as real hardware or production readiness.

## Rule 11.1: Stop Conditions Are Part Of Quality

Stopping can be the correct outcome when safe execution depends on missing
hardware, credentials, environment, API contracts, user confirmation, or
security decisions. A good stop report lists what was checked, why continuing
would be unsafe, what is needed, and what will be done after confirmation.

## Rule 12: Review Prioritizes Risk

Review should lead with findings, not compliments or summaries.

Check first:

- data loss;
- privacy/secret exposure;
- permission isolation;
- incorrect source-of-truth assumptions;
- irreversible deletion;
- broken version history;
- unsupported no-config/no-key fallback;
- missing tests beyond happy path;
- legacy/fallback path breakage during migration.

## Rule 13: Release Requires Verification And Rollback

A release handoff should include:

- change summary;
- data compatibility notes;
- config/secrets/environment changes;
- commands run;
- smoke/manual workflow verification;
- known issues;
- rollback instructions.

For local or small deployments, backup persistent data before risky changes.

## Rule 14: Operations Feed Back Into Product And Tests

After substantial delivery, record:

- whether the user can complete the intended flow;
- which outputs required manual correction;
- which steps failed often;
- which errors were unclear;
- which rules/config should change;
- which tests or docs should be added.

Feed lessons back into configuration, requirements docs, tests, and runbooks rather than leaving them in chat only.

## Rule 15: Project-Specific Boundaries Must Stay Separate From Role Boundaries

Distinguish:

- role boundaries: who decides product, architecture, implementation, QA, release, security;
- project/business boundaries: what this software is allowed or not allowed to do.

In a reusable lifecycle skill, keep role boundaries in the main method. Place project/business boundaries in project-specific docs or extracted notes, and do not generalize them unless they are broadly applicable.
