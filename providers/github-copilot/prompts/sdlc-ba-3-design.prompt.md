---
name: sdlc-ba-3-design
mode: agent
description: 'Run BA System S3 — Functional Design per feature (5 stations).'
---

# /sdlc-ba-3-design

Run the BA functional design pipeline.

1. Read `.apm/workflows/sdlc-ba.yml` — stations `ba-user-stories` through `ba-e2e-plan`.
2. Execute per feature: user stories → journeys → screen specs → test scenarios → E2E plan (fan-in).
3. Write to `outputs/docs/1-prd/`. Requires S2 deliverables. Use `--scope sprint-N` to limit scope.
