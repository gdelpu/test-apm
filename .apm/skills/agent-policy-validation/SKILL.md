---
name: agent-policy-validation
description: 'Combined policy validation skill that orchestrates agent-policy-guard (A1) structural checks and prompt-hardening checks (A3 PI-02/PI-04) into a single validation pass for agent and skill definitions.'
triggers: ['validate agent', 'agent compliance', 'policy check', 'agent review', 'full validation']
version: '1.0.0'
---

# Skill: Agent Policy Validation

## Purpose

Orchestrate a combined validation pass that covers both structural policy (A1) and prompt-hardening (A3) checks. This skill is the umbrella validator that composes `agent-policy-guard` (structural) and `injection-detection` (prompt security) into a single report.

## Component Skills

| Skill | Coverage |
|-------|----------|
| `agent-policy-guard` | P-01 through P-06 (frontmatter, tool allowlists, naming) |
| `injection-detection` | PI-01 through PI-06 (jailbreak, refusal anchors, exfiltration) |

## Reference Station

Combines logic from:
- `ci-gates/stations/a1-policy-validation.prompt.md` (structural)
- `ci-gates/stations/a3-prompt-injection.prompt.md` (hardening)

## Procedure

1. Run `agent-policy-guard` structural checks (P-01 – P-06).
2. Run `injection-detection` prompt-security checks (PI-01 – PI-06).
3. Merge findings into a single report, preserving rule IDs and severities.
4. Determine overall status: `fail` if any critical or high finding exists.

## Gate Criteria

| Condition | Status |
|-----------|--------|
| Any `critical` or `high` finding from either check | `fail` |
| Only `medium` / `low` findings | `pass` |
| No findings | `pass` |

## Output

Combined validation report:

```json
{
  "skill": "agent-policy-validation",
  "status": "pass|fail",
  "structural_findings": [...],
  "security_findings": [...],
  "summary": "N critical, N high, N medium, N low"
}
```
