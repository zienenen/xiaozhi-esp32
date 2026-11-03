# Project Startup Rules

Use this reference on the first substantive turn in an unfamiliar repository,
at the beginning of a major phase, or when restoring context after a handoff.
The goal is to establish a reliable project baseline before planning or editing.

## 1. Establish The Workspace Baseline

Confirm, without changing project state:

- workspace and repository root;
- active branch, configured remotes, and upstream relationship;
- tracked modifications, untracked files, staged changes, and relevant ignored
  local artifacts;
- source, tests, docs, scripts, dependency manifests, build files, deployment
  files, and runtime entry points;
- active services, databases, external APIs, devices, accounts, and hardware
  dependencies when relevant.

Do not assume the current directory is the repository root. Do not discard,
reset, overwrite, commit, or push pre-existing changes merely to obtain a clean
working tree.

## 2. Build A Documentation Map

Inventory documentation before creating new rules or plans. Classify each
high-signal document as one of:

```text
current_source_of_truth
confirmed_decision
partially_confirmed
unconfirmed_plan
historical_record
deprecated
```

Prioritize reading:

1. root README and docs index;
2. project rules and development process;
3. product scope and requirements;
4. architecture and API/data contracts;
5. task ownership and current phase plan;
6. testing, release, operations, security, and hardware runbooks relevant to
   the request.

Do not read every generated file, dependency, archive, or historical artifact
just because it exists. Read all project documents only when the user explicitly
requests a full-document review; even then, inventory first and report unreadable
or duplicate artifacts.

When documents conflict, state the conflict and route it to the owning role.
Do not silently choose the convenient version.

## 3. Frame The Work Before Execution

For non-trivial work, state or derive:

- objective and user/business value;
- lifecycle phase;
- responsible role lens;
- affected modules and data;
- in-scope and out-of-scope behavior;
- expected artifact or code change;
- acceptance evidence and validation level;
- known assumptions, risks, and external dependencies.

Ask only for decisions that materially change scope, architecture, cost, risk,
or acceptance. Ordinary implementation details should be inferred from the
repository when safe.

## 4. Protect Existing Work

- Treat all pre-existing changes as user-owned unless proven otherwise.
- Edit only files required by the task and work around unrelated changes.
- Before committing, inspect the exact diff and stage explicit paths.
- Never use a broad commit to sweep unrelated files into the requested change.
- Before pushing, verify the remote, branch, commit content, and whether the
  user authorized the push in the current task.
- Do not rewrite history, force-push, reset, or remove work unless the user
  explicitly requested that exact operation and the target is verified.

## 5. Separate Authorization Boundaries

Treat these as distinct steps rather than implied consequences of editing:

- commit;
- push or pull-request creation;
- deployment or production configuration change;
- database migration against persistent data;
- firmware/device flashing;
- external communication or account action;
- destructive or irreversible operation.

Authorization to inspect, explain, diagnose, plan, or edit does not automatically
authorize every later step. Use the current request and project-specific rules to
determine what is authorized.

## 6. Evidence Hierarchy

Report the highest validation actually achieved:

```text
static_reviewed
unit_tested
build_passed
integration_tested
local_formal_env_verified
public_demo_verified
hardware_verified
external_blocked
```

Examples:

- A successful build does not prove runtime behavior.
- A browser page does not prove a physical device sent the data.
- A local HTTP 200 does not prove another LAN client can reach the service.
- A database row proves persistence, not necessarily the full user workflow.
- Simulator output does not prove hardware behavior.
- Real hardware evidence should include device logs or observable behavior plus
  the downstream system evidence when both are part of acceptance.

## 7. Secrets And Local Configuration

- Never print or commit passwords, tokens, private keys, activation codes,
  personal data, precise private locations, or production secrets.
- Keep local addresses and environment-specific configuration out of reusable
  rules unless clearly marked as examples.
- Store secret configuration in the project's accepted local mechanism and
  document only variable names and setup requirements.
- Sanitize logs and screenshots before using them as handoff evidence.

## 8. Startup Brief

After discovery, give a compact startup brief:

```text
Project:
Current phase:
User objective:
Role lens:
Source-of-truth docs:
Affected modules:
Existing changes to preserve:
Planned action:
Acceptance evidence:
Open risks/blockers:
```

For a narrow fix, this may be a short commentary update rather than a new
document. For a project launch or multi-agent phase, record it in the project's
rules, plan, or task-ownership document.
