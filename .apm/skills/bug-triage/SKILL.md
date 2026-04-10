---
name: bug-triage
description: 'Classify and prioritize bug reports by assigning severity, priority, affected components, and reproduction feasibility.'
triggers: ['bug triage', 'bug classification', 'bug priority', 'defect triage']
---

# Skill: bug-triage

## Goal

Classify and prioritize a bug report by assigning severity, priority, identifying affected components, and assessing reproduction feasibility.

## When to use

- As the first station in bug-fixing workflows
- When a new bug report arrives and needs initial assessment
- When the bug-fixer agent needs to decide how to approach a defect

## Procedure

1. Load the bug report for context.
2. Classify severity (critical / high / medium / low) based on user impact.
3. Assign priority (P1–P4) based on severity, frequency, and business impact.
4. Identify affected components and modules from the bug description.
5. Assess reproduction feasibility (easily reproducible / intermittent / not yet reproduced).
6. Extract or refine reproduction steps if provided.
7. Check for related known issues or duplicates.
8. Write the triage document.

## Output

`outputs/specs/bugs/<bug-id>/triage.md`

## Rules

- Severity is about impact to users; priority is about business urgency — they are not the same.
- If reproduction steps are missing, flag the bug as needing reproduction before root-cause work.
- Do not propose fixes during triage — focus on classification only.
