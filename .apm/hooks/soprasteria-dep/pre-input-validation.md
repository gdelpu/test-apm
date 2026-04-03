# Hook: DEP Pre-Input Validation

## Objective

This hook runs **before** any DEP Agent executes. It verifies that the declared inputs exist, are in a validated state, and meet the sufficiency criteria defined in the skill. If critical inputs are missing, the agent is blocked.

---

## Phase 0 — Input existence check

For each input declared in the skill's `## Inputs` section:

1. Attempt to read the file at the declared path.
2. Check the YAML front matter `status` field:
   - `validated` → input is ready
   - `draft` → issue a **WARN** (proceed but flag)
   - Missing or unreadable file → issue a **STOP** (block execution)

---

## Phase 1 — Sufficiency criteria evaluation

For each input marked **MANDATORY**, evaluate all sufficiency criteria listed in the skill:

- If **all mandatory criteria pass** → GO
- If **at least one mandatory criterion fails** → STOP — produce a blocking report
- If **optional input is absent** → WARN — proceed with reduced context, note gaps

---

## Phase 2 — Tech-Agent traceability check

Verify that at least one upstream Tech-Agent deliverable is present when required:

- `[STK-001]` Stack Conventions — needed by dep1.1 (CI) and dep2.1 (workstation)
- `[CTX-001]` System Context — needed by dep3.1 (IaC)
- `[IMP-001]` Implementation Plan — enriches all three agents if present

If none of the above are available: issue a **WARN** — the agent will produce a generic configuration rather than a project-specific one.

---

## Decision matrix

| Mandatory inputs present | Sufficiency criteria met | Decision |
|--------------------------|--------------------------|----------|
| All | All | GO |
| All | Partial | WARN + proceed |
| Partial | — | WARN + proceed with gaps noted |
| None | — | STOP |

---

## STOP report format

If the decision is STOP, output the following before halting:

```
## ⛔ DEP Input Validation — BLOCKED

Agent: [agent-id]
Timestamp: [YYYY-MM-DD]

### Missing mandatory inputs:
- [input-id] [description] — [reason]

### Failed sufficiency criteria:
- [input-id] criterion: [description]

### Resolution:
Provide the missing input(s) and re-run the agent.
```

---

## WARN annotation format

For every warning, append to the skill's `## ⚠ Points of attention` section:

```
| N | Dependency | [input-id] absent — [field] unknown | [provide or accept generic config] |
```
