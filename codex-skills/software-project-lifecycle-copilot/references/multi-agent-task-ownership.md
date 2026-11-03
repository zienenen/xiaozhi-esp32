# Multi-Agent Task Ownership

Use this reference when a project splits work across several Codex threads,
specialized agents, or role-based implementers. The goal is to make agents
parallelizable without letting them read everything, change everything, or
silently redefine product and architecture decisions.

## 1. Confirmation Chain

For multi-agent project work, confirm upstream decisions in this order:

```text
Product Manager
-> Architect
-> Product Manager review if architecture changes product scope
-> R&D Lead / Engineering Lead
-> Execution agents
-> Integration / QA
-> R&D Lead final acceptance
```

Rules:

- Product scope must be clear before architecture is treated as final.
- Architecture boundaries must be clear before execution agents implement.
- R&D Lead owns module sequencing, quality gates, and final acceptance.
- Execution agents must not silently change product scope, architecture,
  interfaces, security boundaries, or acceptance criteria.

## 2. Task Ownership Document

Before launching several execution agents, the R&D Lead should create or update
a module ownership document such as:

```text
docs/development_task_ownership.md
```

The document should include:

- module responsibility matrix;
- each module's owner and final accountable role;
- each module's allowed directories;
- required input documents;
- P0 tasks;
- explicit non-goals;
- completion standard;
- handoff format;
- cross-module escalation rules.

Execution agents should be assigned from this document, not from a vague
high-level project description.

## 3. Scoped Reading Protocol

When assigning a specialized execution agent, prefer this prompt pattern:

```text
You are the <module> agent. Read only development_task_ownership.md section <N>
and the documents listed in that section as required inputs. Complete only the
module described there. If you find a conflict or missing upstream decision,
stop and report it instead of expanding scope.
```

The agent may:

- read the specified section;
- read only the section's required input documents;
- inspect relevant code/tests/config under the module's allowed directories;
- read additional files only when needed to understand direct imports, build
  configuration, or runtime entry points.

The agent must not:

- read the whole project just because it is available;
- edit outside its allowed directories except for required docs/tests/runbooks;
- redefine API fields, data models, hardware pins, routes, product scope, or
  acceptance criteria without escalation;
- hide failures with mock data or fake success states.

## 4. Execution Agent Handoff

Every execution agent handoff should include:

- module name and role;
- required docs read;
- directories/files changed;
- tasks completed;
- commands/tests run and results;
- acceptance status;
- what could not be verified;
- cross-module changes needed;
- whether upstream docs/contracts need updates.

If the agent stopped, the handoff should include:

- what was checked;
- why work could not safely continue;
- exact missing information or external condition;
- what to do after the blocker is resolved.

## 5. Cross-Module Conflict Rule

If a module discovers a conflict, route it to the accountable role:

| Conflict | Escalate to |
| --- | --- |
| Product scope, P0/P1/P2, user flow, acceptance | Product Manager + R&D Lead |
| Architecture boundary, API/data contract, module ownership | Architect + R&D Lead |
| Test quality, delivery sequence, release readiness | R&D Lead |
| Security, secrets, GPS/location, tokens, privacy | Architect + R&D Lead; add Security/Data role if active |
| Missing hardware, deployment, credentials, external account | R&D Lead + user |

Execution agents should record the conflict and stop or continue only within a
safe unaffected area.

## 6. Stop Conditions

An agent must stop or switch to a blocker report when safe implementation
depends on missing information that cannot be inferred from the project.

Common stop conditions:

- hardware model, pins, bus mode, voltage, or wiring are unknown;
- real device, account, cloud service, public URL, or logged-in session is
  required for verification and unavailable;
- `.env`, secrets, database, external service, or dependency runtime is missing
  for a formal environment;
- API/data contract is missing or conflicts across documents;
- security/privacy risk is unresolved;
- implementation would require changing product scope or architecture;
- tests can only be made to pass by faking success or hiding failures.

Stop report format:

```text
Stopped before implementation.

Checked:
- ...

Cannot safely continue because:
- ...

Needed from user or upstream role:
1. ...
2. ...

After confirmation, next steps:
1. ...
2. ...
```

## 7. Validation Level Labels

Do not collapse different validation levels into "done". Use clear labels:

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

- A real HTTP integration test can prove API contract behavior, but does not
  prove PostgreSQL or public deployment unless those environments were used.
- A frontend production build can prove compileability, but not real data flow
  unless tested against a running backend.
- A simulator can prove software flow, but not GPS/NFC hardware behavior.
