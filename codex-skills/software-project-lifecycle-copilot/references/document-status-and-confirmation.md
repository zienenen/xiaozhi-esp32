# Document Status And Confirmation

Use this reference when project documents guide multiple agents, carry product
or architecture decisions, or require user confirmation before downstream work
can rely on them.

## 1. Status Values

Recommended document statuses:

```text
draft
pending_user_confirmation
confirmed
partially_confirmed
implemented
external_blocked
deprecated
```

Meanings:

| Status | Meaning |
| --- | --- |
| `draft` | Written by an agent, not yet ready for user confirmation. |
| `pending_user_confirmation` | Ready for user review; downstream agents must not treat open items as final. |
| `confirmed` | User confirmed the content; downstream agents may rely on it. |
| `partially_confirmed` | Some sections are confirmed, others remain open and must be clearly marked. |
| `implemented` | The confirmed content has been implemented and verified at the stated validation level. |
| `external_blocked` | Correct plan exists, but verification or execution depends on external hardware, credentials, account, service, or user action. |
| `deprecated` | Kept for history; not a current source of truth. |

## 2. Confirmation Rules

- Do not treat a document as final just because it exists.
- User confirmation is required for product scope, architecture decisions,
  release boundaries, security/data risk acceptance, and document sets that will
  guide other agents.
- If the user confirms only part of a document, mark the rest as open or
  pending.
- Planned work must be marked as planned, todo, or pending. Do not present it as
  implemented.
- When behavior changes, update affected docs in the same change or hand off the
  exact doc update required.

## 3. Front Matter Or Header

Living project documents should include a short status header when useful:

```markdown
# <Document Title>

Document status: pending_user_confirmation
Owner role: R&D Lead
Updated: YYYY-MM-DD
```

Equivalent localized labels are fine when the project already uses them.

## 4. User Confirmation Workflow

For documents that need confirmation:

1. State the owning role.
2. List the documents to create or modify.
3. List the scope of each document.
4. List concrete questions for the user.
5. Wait for confirmation before writing final language when the questions affect
   scope, architecture, security, release, or cost.
6. After editing, summarize changes and ask for document-level confirmation.

Question format:

```markdown
Need you to confirm:

1. <question>
2. <question>
3. <question>
```

Avoid broad questions such as "Is this okay?" when separate decisions are
needed.

## 5. Source-Of-Truth Rules

Each project should identify the current source of truth for:

- product scope and P0/P1/P2;
- architecture boundaries and API/data contracts;
- implementation task ownership;
- test and quality gates;
- release and operations;
- security/data boundaries.

Indexes and READMEs should link these documents. If multiple documents conflict,
the agent must state the conflict and route it to the responsible role instead
of choosing silently.
