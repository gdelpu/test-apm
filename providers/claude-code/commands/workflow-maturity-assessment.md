# /workflow-maturity-assessment

Run the Maturity Assessment workflow to evaluate project or team maturity.

## Steps

1. Read `.apm/workflows/maturity-assessment.yml` for the station sequence.
2. Execute each station: scope definition → analysis → scoring →
   report generation → roadmap → stakeholder review.
3. Write artifacts to `specs/assessments/<name>/`.

## Inputs

- Assessment scope and context
- Maturity model or criteria to evaluate against

## Outputs

- `specs/assessments/<name>/scope.md`
- `specs/assessments/<name>/analysis.md`
- `specs/assessments/<name>/scoring.md`
- `specs/assessments/<name>/report.md`
- `specs/assessments/<name>/roadmap.md`
- `specs/assessments/<name>/review-notes.md`
