# /workflow-bmad

Run the BMAD (Build → Measure → Analyze → Decide) feedback loop.

## Steps

1. Read `.apm/workflows/bmad.yml` for the station sequence.
2. **Initialise workflow state**:
   ```bash
   cd .apm/hooks && python -m engine --state init \
     --workflow bmad --feature <feature> \
     --stations "build,measure,analyze,decide" \
     --trace-file outputs/specs/features/<feature>/audit-trace.jsonl
   ```
3. Before each station, run `python -m engine --state update --station <id> --status running ...`.
   After each station, run `python -m engine --state update --station <id> --status passed --gate pass ...`.
4. Execute each station: build → measure → analyze → decide.
5. Evaluation uses scoring, drift detection, and adaptive decisions.
6. If decide station recommends retry, loop back to build.
7. **Write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat — use file-writing tools to create each file.

## Inputs

- Hypothesis or feature to evaluate
- Success metrics and thresholds

## Outputs

- Build artifact or implementation summary
- Measurement data and metrics
- Analysis report with drift detection
- Decision record (proceed / pivot / retry)
