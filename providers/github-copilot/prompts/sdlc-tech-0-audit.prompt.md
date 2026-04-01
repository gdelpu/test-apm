---
mode: agent
description: 'Run Tech System T0 — Brownfield Technical Audit (2 stations).'
---

# /sdlc-tech-0-audit

Run the Tech brownfield audit pipeline.

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-audit` and `tech-gap`.
2. Execute: technical stack audit → gap analysis with migration paths.
3. Write to `docs/2-tech/`. Brownfield only — skip for greenfield.
