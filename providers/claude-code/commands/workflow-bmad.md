# /workflow-bmad

Run the BMAD (Build → Measure → Analyze → Decide) feedback loop.

## Steps

1. Read `.apm/workflows/bmad.yml` for the station sequence.
2. Execute each station: build → measure → analyze → decide.
3. Evaluation uses scoring, drift detection, and adaptive decisions.
4. If decide station recommends retry, loop back to build.

## Inputs

- Hypothesis or feature to evaluate
- Success metrics and thresholds

## Outputs

- Build artifact or implementation summary
- Measurement data and metrics
- Analysis report with drift detection
- Decision record (proceed / pivot / retry)
