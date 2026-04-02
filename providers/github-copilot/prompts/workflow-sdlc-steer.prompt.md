---
name: workflow-sdlc-steer
mode: agent
description: 'Run full Steer pipeline — project init through Go/No-Go (10 stations).'
---

# /workflow-sdlc-steer

Run the Steer pipeline (Systems P0 through P3).

1. Read `.apm/workflows/sdlc-steer.yml` for the station sequence.
2. Execute all 10 stations: init (project sheet, KPIs) → planning (sprints, roadmap, risks) → tracking (progress, health, risks) → governance (COPIL, Go/No-Go).
3. Write all artifacts to `docs/3-steer/`.
4. Track state in `docs/3-steer/workflow-state.md`.
