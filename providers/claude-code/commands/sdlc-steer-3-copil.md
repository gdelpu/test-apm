# /sdlc-steer-3-copil

Execute the **Steer System P3 — Steering Committee** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-copil` and `steer-go-nogo`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for steer-p3.1 and steer-p3.2.
3. Execute:
   - Wave 1: p3.1 (COPIL Preparation — dual-register executive summary).
   - Wave 2: p3.2 (Release Go/No-Go — UAT + debt + NFR aggregation).
4. Write to `docs/3-steer/`.

Prerequisites: P2 sprint reports, risk register, UAT report, tech debt report.

## Outputs

- `copil.md` — steering committee preparation (technical + sponsor sections)
- `gng-001-go-nogo.md` — Go/No-Go decision with evidence
