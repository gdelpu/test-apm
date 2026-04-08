---
name: fix-planning
description: 'Plan a minimal, targeted fix for a bug or incident with blast radius assessment, rollback path, and task breakdown.'
triggers: ['fix plan', 'fix planning', 'patch plan', 'fix proposal', 'incident fix']
---

# Skill: fix-planning

## Goal

Plan a minimal, targeted fix for a confirmed bug or incident — assessing blast radius, defining a rollback path, and breaking the fix into tasks.

## When to use

- In incident-resolution workflows after root cause is confirmed
- In bug-fixing workflows when moving from root-cause to fix implementation
- Whenever a fix needs to be scoped before coding begins

## Procedure

1. Load the root-cause analysis and reproduction scenario.
2. Identify the minimal code change that addresses the root cause.
3. Assess blast radius: what else could this change affect?
4. Define a rollback path: how to revert if the fix causes regression.
5. Break the fix into tasks (code change, tests, documentation).
6. Identify regression test requirements.
7. Write the fix plan.

## Output

- `specs/features/<feature>/plan.md`
- `specs/features/<feature>/tasks.md`

## Rules

- Prefer minimal, targeted changes over refactoring during incident response.
- Every fix must have a rollback path.
- Blast radius assessment is mandatory — no fix without impact analysis.
