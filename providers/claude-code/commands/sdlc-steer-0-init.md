# /sdlc-steer-0-init

Execute the **Steer System P0 — Project Initialization** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-project-sheet` and `steer-kpi-baseline`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for steer-p0.1 and steer-p0.2.
3. Execute:
   - Wave 1: p0.1 (Project Sheet — team, capacity, LLM budget).
   - Wave 2: p0.2 (KPI Baseline — effort + token budgets per phase).
4. Write to `docs/3-steer/`.

This is typically run once at the start of the project.

## Outputs

- `pil-001-project-sheet.md` — team composition, capacity, budget
- `kpi-001-baseline.md` — effort and token baselines, velocity targets
