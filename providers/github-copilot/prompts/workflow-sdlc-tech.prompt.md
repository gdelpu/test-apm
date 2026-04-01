---
mode: agent
description: 'Run full Tech pipeline — architecture through continuous quality (12 stations).'
---

# /workflow-sdlc-tech

Run the Tech pipeline (Systems T0 through T3).

1. Read `.apm/workflows/sdlc-tech.yml` for the station sequence.
2. Execute all 12 stations: audit → architecture (C4, ADRs, stack, enablers) → design (data model, APIs, tests, impl plan) → quality (drift, E2E).
3. Write all artifacts to `docs/2-tech/`.
4. Track state in `docs/2-tech/workflow-state.md`.
