# /workflow-maturity-assessment

Run the Maturity Assessment workflow to evaluate project or team maturity.

## Steps

1. Read `.apm/workflows/maturity-assessment.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow maturity-assessment --feature <name> \
     --stations "scope,analysis,scoring,report,roadmap,review"
   ```
   Capture the returned `trace_id` and `run_dir`. State and trace files are auto-created under `outputs/runs/maturity-assessment/<timestamp>-<name>-<short-tid>/`.
3. Before each station, run `python -m engine --state update --station <id> --status running --trace-id <tid> --workflow maturity-assessment`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass --trace-id <tid> --workflow maturity-assessment`.
4. Execute each station: scope definition → analysis → scoring →
   report generation → roadmap → stakeholder review.
5. **Write every artifact as an actual file on disk** under the run directory returned by init. Do not merely display content in chat — use file-writing tools to create each file.

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
