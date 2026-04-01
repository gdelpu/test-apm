---
mode: agent
description: 'Run full SDLC pipeline — BA + Tech + Test + Steer (11 stations).'
---

# /workflow-sdlc-full

Run the full SDLC pipeline.

1. Read `.apm/workflows/sdlc-full.yml` for the station sequence.
2. Execute all phases: scaffold → init → BA (S0-S3) → planning → Tech (T0-T3) → implementation → test → tracking → quality → governance.
3. Write all artifacts to `docs/`.
4. Track state in `docs/workflow-state.md`.
