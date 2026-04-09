---
name: drift-detection
description: 'Detect specification drift by comparing current implementation state against the approved specification and plan.'
triggers: ['drift detection', 'spec drift', 'implementation drift', 'specification compliance']
---

# Skill: drift-detection

## Goal

Detect drift between the approved specification/plan and the current implementation state, flagging deviations that may indicate scope creep, missed requirements, or unauthorized changes.

## When to use

- In BMAD workflows to check alignment between iterations
- During implementation reviews to verify spec compliance
- When the bmad-orchestrator suspects implementation has diverged from plan

## Procedure

1. Load the approved specification, plan, and task list.
2. Analyze the current implementation (code, config, infrastructure).
3. Compare implementation against each specification requirement.
4. Identify:
   - Missing requirements (specified but not implemented)
   - Extra features (implemented but not specified)
   - Modified behavior (implemented differently than specified)
5. Classify each drift item by impact (high / medium / low).
6. Write the drift report.

## Output

`specs/features/<feature>/drift-report.md`

## Rules

- Not all drift is bad — extra features may be improvements. Flag, don't judge.
- Missing requirements are always high-impact drift.
- Drift from NFRs (security, performance) is critical.
