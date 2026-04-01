---
name: sdlc-ba-0-audit
mode: agent
description: 'Run BA System S0 — Brownfield Audit (2 stations).'
---

# /sdlc-ba-0-audit

Run the BA brownfield audit pipeline.

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-audit-existing` and `ba-audit-delta`.
2. Execute: existing system audit → delta analysis.
3. Write to `docs/1-prd/`. Brownfield only — skip for greenfield.
