# /workflow-maturity-assessment

Run the Maturity Assessment workflow to evaluate project or team maturity.

## Steps

1. Read `.apm/workflows/maturity-assessment.yml` for the station sequence.
2. Execute each station: scope definition → analysis → scoring →
   report generation → roadmap → stakeholder review.
3. **Write every artifact as an actual file on disk** under `outputs/specs/assessments/<name>/`. Do not merely display content in chat — use file-writing tools to create each file.

## Inputs

- Assessment scope and context
- Maturity model or criteria to evaluate against

## Outputs

- `outputs/specs/assessments/<name>/scope.md`
- `outputs/specs/assessments/<name>/analysis.md`
- `outputs/specs/assessments/<name>/scoring.md`
- `outputs/specs/assessments/<name>/report.md`
- `outputs/specs/assessments/<name>/roadmap.md`
- `outputs/specs/assessments/<name>/review-notes.md`
