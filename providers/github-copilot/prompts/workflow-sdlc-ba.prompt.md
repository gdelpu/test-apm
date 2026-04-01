---
mode: agent
description: 'Run full BA pipeline — brownfield audit through functional design (16 stations).'
---

# /workflow-sdlc-ba

Run the BA pipeline (Systems S0 through S3).

1. Read `.apm/workflows/sdlc-ba.yml` for the station sequence.
2. Execute all 16 stations: audit → scoping → specification (with fan-out) → functional design (per feature) → validation.
3. Write all artifacts to `docs/1-prd/`.
4. Track state in `docs/1-prd/workflow-state.md`.
