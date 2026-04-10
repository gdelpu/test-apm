# /workflow-bmad

Run the BMAD (Build → Measure → Analyze → Decide) feedback loop.

## Steps

1. Read `.apm/workflows/bmad.yml` for the station sequence.
2. Execute each station: build → measure → analyze → decide.
3. Evaluation uses scoring, drift detection, and adaptive decisions.
4. If decide station recommends retry, loop back to build.
5. **Write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat — use file-writing tools to create each file.

## Inputs

- Hypothesis or feature to evaluate
- Success metrics and thresholds

## Outputs

- Build artifact or implementation summary
- Measurement data and metrics
- Analysis report with drift detection
- Decision record (proceed / pivot / retry)
