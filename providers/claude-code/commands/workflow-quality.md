# /workflow-quality

Run the Quality Validation workflow against the current codebase.

## Steps

1. Read `.apm/workflows/quality-validation.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow quality-validation --feature quality \
     --stations "lint,static-analysis,sast,dependency-audit,coverage,dast,report" \
     --trace-file outputs/specs/quality/audit-trace.jsonl
   ```
3. Before each station, run `python -m engine --state update --station <id> --status running ...`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass ...`.
4. Execute each station: lint → static analysis → SAST → dependency audit →
   coverage → DAST → report.
5. **Write every report as an actual file on disk** under `outputs/specs/quality/`. Do not merely display content in chat — use file-writing tools to create each file.
6. Report overall pass/fail with gate results.

## Outputs

- `specs/quality/lint-report.md`
- `specs/quality/static-analysis-report.md`
- `specs/quality/sast-report.md`
- `specs/quality/dependency-report.md`
- `specs/quality/coverage-report.md`
- `specs/quality/dast-report.md`
- `specs/quality/quality-report.md`
