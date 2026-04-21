# Pre-Hook: Input Validation (Phase 0) — Base Protocol

> **Type:** pre | **Scope:** agent + station | **Domain:** universal | **Severity:** blocker

## Objective

Executed **before any production** by the agent. Verifies that all declared inputs are present, valid, and semantically sufficient. Produces either a GO/WARN decision (continue) or a STOP decision (blocking report instead of deliverable).

Domain-specific extensions (ba.md, tech.md, steer.md, test.md) add identifier namespaces and domain-specific rules. Read the relevant extension after this base protocol.

---

## Phase 0a — Presence and Status Check

For each input declared in the agent's skill:

### Mandatory inputs
- [ ] The file is available (provided or accessible at the declared path)
- [ ] The YAML front matter contains an `id` field matching the expected identifier
- [ ] The `status` field is set to `validated` or `draft`:
  - `validated` → input is fully approved — **GO**
  - `draft` → check provenance:
    - If the input was produced **within the same workflow run** (same `trace_id` or present in the workflow state as a completed station output) → accept with **WARN** ("intra-workflow draft input — not yet externally validated")
    - If the input comes from a **previous workflow run** or external source → **STOP** ("input has status: draft and was not produced in this workflow run — require validation before consumption")
  - Absent or unrecognised status → **STOP**
- [ ] The `dependencies` declared in that file are themselves satisfied (cascading check, 1 level)

**If a mandatory input fails any of these criteria:**
- Stop execution immediately.
- Produce a **blocking report** (see format below) instead of the deliverable.
- Never silently generate a partial output.

### Recommended inputs (optional)
- [ ] Check for presence
- If absent: note the gap in the `Production confidence` section of the output, continue execution.
- If present but `status: draft`: treat as present with degraded confidence — note WARN.

### Special case: audit agents (0.1, 0.2)
These agents operate in adaptive mode (A/B/C depending on source availability). The selected mode replaces status verification. Document the retained mode in the output.

---

## Phase 0b — Sufficiency Criteria Evaluation

Each input includes a `**Sufficiency criteria**` block. For each available input:

1. Read the content of the input
2. Evaluate each listed criterion as **satisfied / partial / absent**
3. Apply the defined threshold (BLOCK / WARN / GO):
   - **BLOCK**: cannot reason correctly to produce the deliverable — stop + blocking report
   - **WARN**: production possible but with uncertainty zones explicitly documented
   - **GO**: all critical criteria are satisfied

**Judgement rule:** The criteria are observable and thresholded. Never infer that a criterion is satisfied from vague content. When in doubt, note WARN with justification.

---

## Phase 0c — Global Confidence Score and Decision

After evaluating all inputs:

| Score | Condition | Action |
|-------|-----------|--------|
| **GO** | All mandatory inputs present + validated + >= GO threshold on sufficiency criteria | Continue execution normally |
| **WARN** | Mandatory inputs OK, but >= 1 input with WARN sufficiency criteria | Continue with flag in `Production confidence` |
| **STOP** | >= 1 mandatory input absent / not validated / BLOCK on sufficiency criteria | Stop — produce blocking report |

---

## Blocking Report Format

If the agent must stop (STOP decision), produce the following content instead of the normal deliverable:

```markdown
# Blocking Report — [Agent ID] — [date]

## Blocking inputs

| Input | Problem | Impact |
|-------|---------|--------|
| [ID] | absent / status: draft / criterion X not satisfied | [description of the impact on production] |

## Warning inputs

| Input | Problem | Estimated impact |
|-------|---------|-----------------|
| [ID] | criterion Y partial | [areas of the deliverable that will be degraded] |

## Required actions

1. [Concrete action to resolve blocker #1]
2. [Concrete action to resolve blocker #2]

## Next step

Once the blockers are resolved, re-run agent [name] with the corrected inputs.
```
