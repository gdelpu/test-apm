---
name: sdlc-tech-2-design
mode: agent
description: 'Run Tech System T2 — Technical Design (4 stations).'
---

# /sdlc-tech-2-design

Run the Tech design pipeline.

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-data-model` through `tech-provider-bootstrap`.
2. Execute: data model → API contracts → test strategy → implementation plan → provider bootstrap (auto-detect provider).
3. Write to `outputs/docs/2-tech/`. Requires T1 deliverables.
