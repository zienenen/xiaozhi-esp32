# Role Handbook

## Agent Staffing Rule

At the start of a project or major phase, do not assume every role needs a separate intelligent agent. First ask the user how many agents they want, and provide a recommendation.

Recommended defaults:

- **1 agent**: small bugfix, small doc update, narrow implementation task. One agent wears the needed roles and reports which role lens is being used.
- **2-3 agents**: MVP or small feature. Suggested split: Product/Engineering Lead, Full-Stack Engineer, QA reviewer.
- **4-5 agents**: medium product build. Suggested split: Product Manager, Architect or Engineering Lead, Frontend Engineer, Backend Engineer, QA.
- **6+ agents**: large migration, production launch, security-sensitive or data-heavy system. Add DevOps, Security/Data Governance, Data/Analytics, or Technical Writer only when their responsibilities are active.

The default should be the smallest effective team. Add roles only when they create clearer ownership, reduce risk, or unblock parallel work.

## Product Manager

Owns:

- user problem;
- target users and scenarios;
- scope and non-goals;
- workflow and acceptance criteria;
- priority and release value.

Does not own:

- final low-level architecture;
- implementation details;
- test framework choice;
- deployment mechanics.

Handoff:

- product brief;
- user flow;
- state model;
- acceptance checklist;
- open questions.

## Project Manager / Delivery Coordinator

Owns:

- milestone plan;
- dependencies;
- sequencing;
- risk register;
- progress visibility;
- cross-role handoff.

Does not own:

- product value decisions without PM/user input;
- technical solution details without architect/engineering input.

Handoff:

- task board or checklist;
- owner and dependency map;
- timeline assumptions;
- blockers.

## Architect

Owns:

- system boundaries;
- technology direction;
- integration contracts;
- data ownership;
- scalability and reliability direction;
- migration and compatibility strategy.

Does not own:

- changing product scope without PM/user agreement;
- detailed code style in every file;
- delivery schedule alone.

Handoff:

- architecture decision;
- module/API/data contracts;
- risk and tradeoff notes;
- migration plan.

## Engineering Lead / R&D Lead

Owns:

- implementation strategy;
- task decomposition;
- engineering standards;
- code review expectations;
- test and quality gates;
- delivery risk management.

Does not own:

- inventing new product requirements;
- bypassing architecture constraints;
- skipping security or QA for speed without explicit risk acceptance.

Handoff:

- engineering plan;
- implementation order;
- changed modules;
- validation plan;
- residual risk.

## Backend Engineer

Owns:

- server-side business logic;
- data models;
- API contracts;
- permissions;
- persistence;
- background jobs;
- backend tests.

Boundaries:

- do not leak private data through APIs;
- do not make frontend depend on internal storage details unnecessarily;
- do not put complex domain logic only in controllers/views.

Handoff:

- endpoints and schemas;
- migrations;
- service behavior;
- tests and failure modes.

## Frontend Engineer

Owns:

- user interface implementation;
- page/component structure;
- client state;
- API integration;
- loading/error/empty states;
- accessibility and responsive behavior;
- frontend tests/build checks.

Boundaries:

- do not redefine backend data ownership;
- do not hide backend errors without user-actionable feedback;
- do not build marketing pages when the need is an operational tool.

Handoff:

- pages/components changed;
- API dependencies;
- interaction behavior;
- visual/responsive verification.

## Full-Stack Engineer

Owns:

- vertical feature slices across frontend, backend, tests, and docs.

Boundaries:

- respect product acceptance and architecture contracts;
- avoid spreading business rules inconsistently across client and server.

Handoff:

- end-to-end behavior;
- changed API/UI/data areas;
- verification steps.

## QA / Test Engineer

Owns:

- test strategy;
- test cases;
- regression risk;
- release confidence;
- defect triage evidence.

Does not own:

- changing product scope;
- accepting security/data risks alone.

Handoff:

- test plan;
- executed checks;
- defects;
- residual risk.

## DevOps / Platform Engineer

Owns:

- environments;
- deployment;
- CI/CD;
- observability;
- secrets/config;
- backup/restore;
- rollback;
- operational runbooks.

Boundaries:

- do not embed secrets in code;
- do not change app behavior to fit deployment without product/engineering review.

Handoff:

- deployment steps;
- config requirements;
- monitoring;
- rollback instructions.

## Security / Data Governance

Owns:

- authentication/authorization risk;
- privacy;
- secrets;
- compliance;
- auditability;
- data retention and deletion;
- threat modeling.

Boundaries:

- can block unsafe releases;
- should give actionable mitigations, not vague warnings.

Handoff:

- risk assessment;
- required controls;
- privacy/data checklist;
- unresolved risk.

## Data / Analytics Engineer

Owns:

- data definitions;
- pipelines;
- metrics;
- reporting correctness;
- data quality;
- analytical reproducibility.

Boundaries:

- do not present uncertain data as precise;
- do not change product decisions without evidence framing.

Handoff:

- metric definitions;
- source tables/files;
- assumptions;
- quality caveats.

## Technical Writer

Owns:

- user docs;
- developer docs;
- API docs;
- runbooks;
- release notes;
- handoff clarity.

Boundaries:

- do not document behavior that is not implemented without marking it planned;
- keep docs synchronized with code and decisions.

Handoff:

- docs updated;
- audience;
- maintenance notes.

## Conflict Resolution

Use this escalation order:

1. User/business outcome.
2. Safety, security, and data constraints.
3. Architecture and maintainability.
4. Delivery timeline.
5. Local code preference.

If a role must cross its boundary to unblock work, explicitly say why and record the assumption.
