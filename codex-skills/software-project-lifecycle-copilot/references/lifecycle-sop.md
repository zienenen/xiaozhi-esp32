# Lifecycle SOP

## 1. Context Discovery

Goal: understand the project before acting.

Do:

- Identify the product, users, environment, repo structure, tech stack, current entry points, and constraints.
- Read existing docs before inventing new direction.
- Locate code ownership boundaries, tests, config, and deployment scripts.
- Identify whether the task is exploratory, planning, implementation, review, release, or operations.

Output:

- project framing;
- affected modules;
- known constraints;
- next phase.

## 2. Requirements

Goal: define the problem and success.

Capture:

- user or business problem;
- target users/personas;
- current pain;
- inputs and outputs;
- in-scope and out-of-scope behavior;
- acceptance criteria;
- data, security, legal, operational, and performance constraints.

Do not let technical implementation details replace requirements too early.

## 3. Product Design

Goal: turn requirements into workflows and user-facing behavior.

Define:

- primary workflow;
- edge cases and empty states;
- user permissions and role differences;
- status/state model;
- copy/text expectations;
- success and failure feedback;
- analytics or observability signals if needed.

Output:

- product brief;
- interaction flow;
- acceptance checklist.

## 4. Architecture

Goal: create a maintainable system plan.

Define:

- system boundaries;
- module ownership;
- data model;
- API/events/contracts;
- integrations;
- async vs sync responsibilities;
- security model;
- scaling assumptions;
- migration strategy.

When there are multiple options, write a short decision record:

```text
Context
Options
Decision
Consequences
Migration / rollback
```

## 5. Task Breakdown

Goal: make delivery executable.

Split by vertical slices when possible:

- backend model/API/service;
- frontend page/component/state;
- data migration;
- tests;
- docs/runbook;
- release/ops.

Prioritize:

- P0: must work for the workflow to be usable.
- P1: needed for first complete release.
- P2: hardening, scale, polish, automation.

Each task should include acceptance and validation.

## 6. Implementation

Goal: change the system with minimal unnecessary disruption.

Do:

- inspect current patterns first;
- keep edits scoped;
- reuse existing helpers and conventions;
- avoid unrelated refactors;
- add or update tests when behavior changes;
- preserve backwards compatibility when existing data/users depend on it.

For frontend:

- build the actual usable workflow first;
- keep operational tools information-dense and predictable;
- provide loading, empty, error, and success states.

For backend:

- keep permissions and data ownership explicit;
- put complex business logic in services/domain modules;
- validate inputs and return clear errors.

## 7. Review

Goal: catch defects before release.

Review for:

- requirement mismatch;
- role boundary violations;
- security/privacy issues;
- data migration risk;
- backwards compatibility;
- missing tests;
- operational blind spots;
- unclear user-facing errors.

For code review, lead with findings ordered by severity.

## 8. Testing

Goal: prove enough correctness for the risk level.

Use:

- unit tests for pure logic;
- integration tests for APIs/services/data;
- E2E or manual checks for critical workflows;
- regression tests for previously broken behavior;
- smoke tests for deployment/startup.

Test no-config, failure, permission, and edge cases where relevant.

## 9. Release

Goal: ship with a rollback path.

Prepare:

- version or change summary;
- migration steps;
- environment variables/config;
- deployment command;
- smoke test;
- rollback plan;
- monitoring/log checks;
- known limitations.

## 10. Operations

Goal: keep the software reliable after release.

Maintain:

- runbooks;
- logs and metrics;
- backup and restore;
- incident response;
- dependency update policy;
- capacity and performance checks;
- support/troubleshooting notes.

## 11. Retrospective

Goal: improve the system and the process.

Record:

- what changed;
- what worked;
- what was painful;
- what defects escaped;
- what docs/tests/process should change;
- next iteration priorities.

Update the relevant SOP, docs, tests, or templates when a lesson should persist.
