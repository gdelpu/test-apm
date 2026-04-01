---
name: sdlc-steer-3-copil
mode: agent
description: 'Run Steer System P3 — COPIL & Go/No-Go (2 stations).'
---

# /sdlc-steer-3-copil

Run the Steer governance pipeline.

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-copil` and `steer-go-nogo`.
2. Execute: COPIL preparation (dual-register summary) → Go/No-Go decision.
3. Write to `docs/3-steer/`.
