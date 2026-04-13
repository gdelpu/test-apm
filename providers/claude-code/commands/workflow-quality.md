# /workflow-quality

Run the Quality Validation workflow against the current codebase.

## Steps

1. Read `.apm/workflows/quality-validation.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow quality-validation --feature quality \
     --stations "lint,static-analysis,sast,dependency-audit,coverage,dast,report"
   ```
   Capture the returned `trace_id` and `run_dir`. State and trace files are auto-created under `outputs/runs/quality-validation/<timestamp>-quality-<short-tid>/`.
3. Before each station, run `python -m engine --state update --station <id> --status running --trace-id <tid> --workflow quality-validation`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass --trace-id <tid> --workflow quality-validation`.
4. Execute each station: lint → static analysis → SAST → dependency audit →
   coverage → DAST → report.
5. **Write every report as an actual file on disk** under the run directory returned by init. Do not merely display content in chat — use file-writing tools to create each file.
6. Report overall pass/fail with gate results.
7. **After each station completes, re-display the full progress table** showing updated statuses (✅ completed, 🔄 in-progress, ⏳ pending) for all stations. Never leave the initial table stale.

## Outputs

- `specs/quality/lint-report.md`
- `specs/quality/static-analysis-report.md`
- `specs/quality/sast-report.md`
- `specs/quality/dependency-report.md`
- `specs/quality/coverage-report.md`
- `specs/quality/dast-report.md`
- `specs/quality/quality-report.md`
