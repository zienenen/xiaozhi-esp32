# Quality Gates

## Universal Gate

Before considering work complete, answer:

- What user or system behavior changed?
- What data can be affected?
- What could fail?
- How was it verified?
- What remains risky or untested?

## Requirements Gate

Pass when:

- problem is clear;
- target user is clear;
- in-scope and out-of-scope behavior is clear;
- acceptance criteria exist;
- risky assumptions are documented.

## Architecture Gate

Pass when:

- system boundaries are clear;
- data ownership is clear;
- integration contracts are clear;
- security/privacy implications are considered;
- migration/rollback path exists when needed;
- long-running or high-cost work has an execution model.

## Implementation Gate

Pass when:

- code follows local patterns;
- unrelated changes are avoided;
- errors are understandable;
- permissions/data isolation are preserved;
- behavior has tests or justified manual verification;
- docs/config are updated when behavior changed.

## Review Gate

Check:

- correctness;
- edge cases;
- data loss;
- privacy/secret leakage;
- authorization;
- performance;
- observability;
- maintainability;
- test gaps.

For review output, list findings first with severity and file/line references when possible.

## Test Gate

Choose by risk:

- Low-risk docs-only: proofread and link check if relevant.
- Small code change: targeted unit or build check.
- API/data change: unit + integration tests for success and failure.
- User workflow: manual or automated E2E/smoke path.
- Security/permissions: explicit negative tests.
- Migration: dry run, backup note, reconciliation.

Always report tests run and results. If tests were not run, report why.

## Validation Level Gate

Do not collapse different validation levels into "done". Report the highest
level actually verified:

```text
unit_tested
build_passed
integration_tested
local_formal_env_verified
public_demo_verified
hardware_verified
external_blocked
```

Examples:

- A simulator proves software flow, not real hardware behavior.
- A real HTTP integration test proves API contract behavior, not formal
  PostgreSQL or public deployment unless those environments were used.
- A frontend build proves compileability, not real data flow unless tested
  against a backend.

If formal environment, public URL, credentials, or hardware are missing, mark
the missing verification explicitly instead of implying release readiness.

## Release Gate

Pass when:

- deployment steps are known;
- required config/secrets are listed;
- migrations are ordered;
- smoke test exists;
- rollback path exists;
- known limitations are documented;
- monitoring/logs can show success or failure.

## Operations Gate

Pass when:

- startup and shutdown are documented;
- health checks or basic observability exist;
- backups/restores are considered for persistent data;
- common failures have troubleshooting steps;
- ownership and escalation are clear.

## Security And Data Gate

Block or escalate when:

- secrets can be exposed;
- users can access each other's data;
- destructive actions are irreversible without confirmation;
- sensitive data is sent externally without need;
- logs include private data;
- authentication/authorization is bypassed;
- compliance-sensitive data lifecycle is undefined.

## Handoff Gate

A good handoff includes:

- current phase and role;
- what changed or was decided;
- files/modules affected;
- commands/tests run;
- acceptance status;
- validation level;
- what could not be verified and why;
- remaining risks;
- next recommended action.

## Stop Gate

Stop or escalate instead of implementing when safe work depends on missing
external facts or authority:

- hardware model, pins, voltage, bus mode, or wiring are unknown;
- required `.env`, database, credentials, account, or public service is missing;
- API/data contract or ownership conflicts across docs;
- implementation would change product scope or architecture without
  confirmation;
- security/privacy risk is unresolved;
- tests would only pass by faking success or hiding failures.

The stop report must include what was checked, why work cannot safely continue,
what is needed, and the next steps after confirmation.
