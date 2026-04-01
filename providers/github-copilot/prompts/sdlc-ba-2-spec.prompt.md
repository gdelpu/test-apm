---
mode: agent
description: 'Run BA System S2 — Specification with epic/feature fan-out (4 stations).'
---

# /sdlc-ba-2-spec

Run the BA specification pipeline.

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-domain-model` through `ba-business-rules`.
2. Execute: domain model → epic decomposition → feature spec (fan-out per epic) → business rules (fan-in).
3. Write to `docs/1-prd/`. Requires S1 deliverables.
