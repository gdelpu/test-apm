---
name: adaptive-decision
description: 'Make data-driven pivot-or-persevere decisions in BMAD loops by evaluating experiment results against success criteria.'
triggers: ['adaptive decision', 'pivot or persevere', 'BMAD decision', 'experiment evaluation']
---

# Skill: adaptive-decision

## Goal

Evaluate experiment results against predefined success criteria to make a data-driven pivot-or-persevere decision in a Build-Measure-Analyze-Decide (BMAD) iteration.

## When to use

- In BMAD workflows at the Decide station
- When the bmad-orchestrator needs to determine next steps after an experiment
- Whenever a build-measure-learn cycle needs a formal decision point

## Procedure

1. Load the experiment hypothesis and success criteria from the Analyze phase.
2. Compare measured results against success criteria.
3. Classify the outcome: success, partial success, or failure.
4. For partial success: identify what worked and what didn't.
5. Recommend next action: persevere (continue), pivot (change approach), or stop.
6. Justify the decision with data.
7. Write the decision record.

## Output

`outputs/specs/features/<feature>/decision.md`

## Rules

- Decisions must be justified with measured data, not opinions.
- "Pivot" must include a concrete alternative direction.
- "Persevere" must state what additional evidence would trigger a future pivot.
