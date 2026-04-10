---
name: sdlc-steer-0-init
mode: agent
description: 'Run Steer System P0 — Project Initialization (2 stations).'
---

# /sdlc-steer-0-init

Run the Steer project initialization pipeline.

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-project-sheet` and `steer-kpi-baseline`.
2. Execute: project sheet (team, capacity, budget) → KPI baseline (effort, tokens, velocity).
3. Write to `outputs/docs/3-steer/`. Run once at project start.
