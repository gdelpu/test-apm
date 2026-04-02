---
name: sdlc-test-2-perf
mode: agent
description: 'Run Test Performance system (2 stations).'
---

# /sdlc-test-2-perf

Run the Test performance pipeline.

1. Read `.apm/contexts/sdlc-agent-registry.yaml` for performance agent compositions.
2. Execute: performance campaign (k6/Artillery) → performance report (thresholds, baseline).
3. Requires Tech deliverables (NFR specs) and a deployed application.
