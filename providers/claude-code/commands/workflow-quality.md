# /workflow-quality

Run the Quality Validation workflow against the current codebase.

## Steps

1. Read `.apm/workflows/quality-validation.yml` for the station sequence.
2. Execute each station: lint → static analysis → SAST → dependency audit →
   coverage → DAST → report.
3. Write reports to `specs/quality/`.
4. Report overall pass/fail with gate results.

## Outputs

- `specs/quality/lint-report.md`
- `specs/quality/static-analysis-report.md`
- `specs/quality/sast-report.md`
- `specs/quality/dependency-report.md`
- `specs/quality/coverage-report.md`
- `specs/quality/dast-report.md`
- `specs/quality/quality-report.md`
