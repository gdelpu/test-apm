---
name: workflow-engine
description: 'Invoke a nested workflow pipeline (quality-validation or pr-validation) from within a parent delivery workflow.'
triggers: ['nested workflow', 'workflow engine', 'quality validation pipeline', 'sub-workflow', 'invoke workflow']
---

# Skill: workflow-engine

## Goal

Invoke a nested workflow pipeline from within a parent delivery workflow, enabling quality-validation and pr-validation to run as stations within feature-implementation, bug-fixing, and modernization workflows.

## When to use

- When a delivery workflow station needs to run the full quality-validation pipeline
- When a delivery workflow station needs to run pr-validation as a nested check
- In feature-implementation, bug-fixing, modernization, and sdlc-full workflows

## Procedure

1. Identify the nested workflow to invoke (e.g., `quality-validation`, `pr-validation`).
2. Load the workflow definition from `.apm/workflows/<workflow-name>.yml`.
3. Map the parent station's inputs to the nested workflow's entry inputs.
4. Execute the nested workflow's stations sequentially, respecting their gates.
5. Collect the nested workflow's final output (aggregate report).
6. Map the nested workflow's exit outputs back to the parent station's outputs.
7. If any blocker-severity gate fails in the nested workflow, propagate the failure to the parent.

## Output

Depends on nested workflow:
- Quality validation: `quality-report.md`
- PR validation: `pr-validation-report.md`

## Gate criteria

- **Pass**: All nested workflow stations pass their gates
- **Fail**: Any blocker-severity gate in the nested workflow fails
- **Skip**: Parent station is marked optional and nested workflow is unavailable

## Rules

- Nested workflows execute in their own output directory context.
- Gate failures in nested workflows propagate as gate failures in the parent station.
- The parent workflow's state file tracks nested workflow completion as a single station.
- Do not nest more than one level deep — no nested-within-nested workflows.
