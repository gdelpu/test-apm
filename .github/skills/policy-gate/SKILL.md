---
name: policy-gate
description: 'Aggregate all upstream station reports and decide whether to APPROVE, BLOCK, or escalate a PR for human REVIEW. Applies rules G-BLOCK, G-REVIEW, and G-APPROVE with justified reasoning.'
triggers: ['policy gate', 'gate decision', 'merge decision', 'PR gate', 'approval gate', 'final gate']
version: '1.0.0'
---

# Skill: Policy Gate

## Purpose

Aggregate structured JSON reports from all upstream CI-gate stations and produce a definitive, justified gate decision. Maps directly to the **A6 — Policy Gate** CI-gate station.

## Reference Station

`ci-gates/stations/a6-policy-gate.agent.md`

## Inputs

| File | Station |
|------|---------|
| `outputs/station_out/work_order.json` | A0 |
| `outputs/station_out/policy_report.json` | A1 |
| `outputs/station_out/security_report.json` | A2 |
| `outputs/station_out/promptsec_report.json` | A3/A4 |
| `outputs/station_out/sim_report.json` | A5 |

## Decision Rules

Apply in priority order — first matching rule wins.

### Rule G-BLOCK (highest priority)

Set `"decision": "BLOCK"` if **any** of the following are true:

- Any report has `"status": "fail"`
- Any report contains a finding with `"severity": "critical"`

A BLOCK prevents merge. The PR author must remediate all critical/high findings before re-submission.

### Rule G-REVIEW

Set `"decision": "REVIEW"` if **all** of these are true:
- No `"status": "fail"` in any report
- At least one finding has `"severity": "high"`
- OR `work_order.json` contains risk hints: `"exec-tool"`, `"unconstrained-network"`, `"unconstrained-files"`

A REVIEW requires explicit approval from a human reviewer with the `agent-security-approver` role.

### Rule G-APPROVE

Set `"decision": "APPROVE"` if:
- No `"fail"` statuses
- No `"high"` or `"critical"` findings
- All simulated scenarios returned `"resistant"` or `"partial"` (no `"vulnerable"`)

### Skipped Stations

If a station has `"status": "skipped"`, treat it as `"pass"` with no findings. Note skipped stations in `"notes"`.

## Labels

| Decision | Labels |
|----------|--------|
| BLOCK | `security:blocker`, `agent-factory:blocked` |
| REVIEW | `agent-factory:needs-review`, plus risk-specific labels |
| APPROVE | `agent-factory:approved` |

Always add `agent-factory:scanned` regardless of decision.

## Procedure

1. Read all upstream station reports.
2. Apply G-BLOCK, G-REVIEW, G-APPROVE rules in order.
3. For every finding that influenced the decision, include it in `blocking_findings` or `review_findings`.
4. Determine recommended labels.
5. Produce a structured gate decision report.

## Rules of Conduct

1. Never approve a PR with an unresolved `critical` finding. If in doubt, decide REVIEW.
2. Do not soften a finding's severity to avoid blocking.
3. Justification must quote the specific finding that drove the decision.
4. If all station reports are skipped (scope was `"non-agent"`), output `"decision": "APPROVE"` with note `"No agent/skill artefacts changed."`.

## Output

Structured JSON report following `outputs/station_out/gate_decision.json` schema:

```json
{
  "station": "A6",
  "decision": "BLOCK|REVIEW|APPROVE",
  "labels": ["agent-factory:scanned", "..."],
  "blocking_findings": [...],
  "review_findings": [...],
  "warnings": [...],
  "notes": "...",
  "summary": "PR BLOCKED — 1 critical finding in A3. Remediate before re-submission."
}
```
