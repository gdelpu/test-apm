---
name: iteration-scoring
description: 'Score BMAD iteration outcomes using quantitative metrics and qualitative assessment to track progress across build-measure-analyze-decide cycles.'
triggers: ['iteration scoring', 'BMAD scoring', 'iteration assessment', 'cycle scoring']
---

# Skill: iteration-scoring

## Goal

Score a BMAD iteration outcome using quantitative metrics and qualitative assessment, enabling trend tracking and objective comparison across build-measure-analyze-decide cycles.

## When to use

- In BMAD workflows during the Analyze phase
- When the bmad-orchestrator needs to quantify iteration progress
- When comparing outcomes across multiple BMAD cycles

## Procedure

1. Load the iteration's build artifacts, measurements, and hypotheses.
2. Score quantitative metrics against targets (e.g., performance, adoption, error rate).
3. Assess qualitative outcomes (user feedback, team confidence, technical risk).
4. Compute an overall iteration score (0–100 scale).
5. Compare against previous iteration scores for trend analysis.
6. Identify the top contributing and detracting factors.
7. Write the iteration score report.

## Output

`specs/features/<feature>/iteration-score.md`

## Rules

- Scoring criteria must be consistent across iterations for trend validity.
- Both quantitative and qualitative factors must be included.
- Previous iteration scores must be referenced for context.
