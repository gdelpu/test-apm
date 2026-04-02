---
name: sdlc-steer-2-sprint
mode: agent
description: 'Run Steer System P2 — Sprint Tracking, recurring (3 stations).'
---

# /sdlc-steer-2-sprint

Run the Steer sprint tracking pipeline (recurring per sprint).

1. Read `.apm/workflows/sdlc-steer.yml` — stations `steer-sprint-progress` through `steer-sprint-risks`.
2. Execute: sprint progress → system health → sprint risks.
3. Write to `docs/3-steer/`. Provide sprint number as argument.
