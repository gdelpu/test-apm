---
mode: agent
description: 'Run Tech System T3 — Continuous Quality (2 stations).'
---

# /sdlc-tech-3-quality

Run the Tech continuous quality pipeline.

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-drift` and `tech-e2e-gen`.
2. Execute: drift detection (spec vs code) → E2E Playwright generation.
3. Can be run repeatedly per PR or before release.
