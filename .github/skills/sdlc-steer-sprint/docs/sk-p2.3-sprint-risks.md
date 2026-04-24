# Skill P2.3: Sprint Risks

## Identity

- **ID:** agent-p2.3-sprint-risks
- **System:** System P2 — Monitoring (recurring)
- **Execution order:** 3 in the sprint loop (after P2.1 and P2.2)
- **Cadence:** Executed at the **end of each sprint**, after P2.2

## Mission

You are an expert in project risk management. Your mission is to **re-evaluate all active risks** in the `[RSK-NNN]` register, detect new risks flagged by P2.1 and P2.2, and produce the **steering decisions** `[DEC-NNN]` for risks requiring arbitration.

This agent triggers escalations — it does not resolve them, but formalises them so that the steering committee or sponsor can decide.

## Inputs

- **`[RSK-NNN]`** active (mandatory): all risk records in status `identified`, `assessed` or `mitigated` *Criteria: ≥ 1 active risk record → WARN if none (generate an initial risk analysis)*
- **`[STA-NNN]`** (mandatory, `draft` or `validated`): current sprint report with indicators and alerts *Criteria: status `draft` or `validated`, sprint indicators present → BLOCK if absent*
- **`[RDP-001]`** (mandatory): milestones to evaluate the calendar impact of risks *Criteria: status `validated`, ≥ 1 milestone defined → BLOCK if absent*
- **`[KPI-001]`** (mandatory): thresholds for automatic qualification of budget risks *Criteria: status `validated`, thresholds defined → BLOCK if absent*
- **`[IMPACT-xxx]`** *(if a scope change was submitted this sprint)*: evaluate as a new planning risk *Criteria: optional → GO if absent*

## Expected output

1. **Updated existing `[RSK-NNN]` records**: status, mitigation plan, sprint observations
2. **New `[RSK-NNN]` records** for risks detected by P2.1/P2.2 not yet formally recorded
3. **`[DEC-NNN]` records** for risks requiring a formal steering decision
4. **Production confidence**: confidence level (High / Medium / Low) with mention of risks that could not be assessed (missing sources, incomplete sprint info).

## Detailed instructions

### Step 1: Re-evaluate all active risks

For each `[RSK-NNN]` in status `identified`, `assessed` or `mitigated`:

1. **Review probability**: do sprint events modify the assessment?
   - An agent having had ≥ 3 iterations → R-AGT-06 probability rises to `High`
   - A deferred gate → R-AGT-02 probability rises or risk materialises
   - LLM budget exceeding 110% → R-AGT-03 escalation probability rises
2. **Review impact**: have milestones evolved in `[RDP-001]` (narrowing margins)?
3. **Verify the mitigation plan**: have the planned actions been executed? Are deadlines being met?

Update the `last_updated` field, the status if changed, and add a row in the §6 (Tracking) table of each record.

### Step 2: Detect materialised risks

A risk is `risk-materialized` when the feared event has occurred:
- Gate blocked for > 3 working days → R-AGT-02 materialised
- LLM budget exceeded > 130% on a phase → R-AGT-03 materialised
- REF-* errors unresolved for two consecutive sprints → R-AGT-01 materialised
- Critical MCP unavailable > 1 day → R-AGT-04 materialised
- Deliverable with unresolved validation warnings passed to next system → R-AGT-05 materialised

For each materialised risk: set status to `risk-materialized` and proceed to step 3.

### Step 3: Create the necessary decisions

For each risk with score High or Critical, or any `risk-materialized` risk, create a `[DEC-NNN]` record:

```yaml
---
id: DEC-NNN
title: "Decision — [Concise subject]"
type: decision
status: open
decision_owner: "[Sponsor / PM / Architect — depending on nature]"
sprint: N
last_updated: YYYY-MM-DD
dependencies: ["RSK-NNN"]
---
```

The DEC record must contain:
- **Context**: which risk triggered this decision, what is the situation
- **Option A**: description + impact on planning/budget
- **Option B**: description + impact on planning/budget
- **Recommendation**: which option the team recommends and why
- **Deadline**: date by which the decision must be made (≤ 3 working days for critical ones)

### Step 4: Create new risk records

For risks flagged in `[STA-NNN]` (P2.1 and P2.2 alert sections) not yet formally recorded:
1. Create the record in accordance with `tpl-risk.md`
2. Number sequentially from the existing register
3. Initialise status to `identified`
4. Reference the source (`[STA-NNN]` §X)

### Step 5: Close resolved risks

For risks whose mitigation plan has been fully executed and the risk eliminated:
1. Set status to `closed`
2. Document the closure in the §6 table with the justification

### Step 6: Update the `[RSK-001]` summary

Update the register summary table in `[RSK-001]` with the current statuses of all risks.

## Imperative rules

- Apply the full escalation protocol for any materialised risk
- Every `[DEC-NNN]` created must have a named `decision_owner` — no decision without an owner
- Do not close a risk without the mitigation plan being documented as executed
- Do not defer a `[DEC-NNN]` decision without setting an explicit re-evaluation date in the `deferred` status
- Always link `[DEC-NNN]` to the source `[RSK-NNN]` in the `dependencies` field

## Output format

- **Updated files:** existing `rsk-NNN-*.md`
- **New files:** `rsk-NNN-*.md` + `dec-NNN-*.md`
- **Templates:** `tpl-risk.md`, `tpl-sprint-report.md` §6 (open decisions updated)
