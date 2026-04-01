---
name: sdlc-test-1-campaign
mode: agent
description: 'Run Test E2E/UAT Campaign system (2 stations).'
---

# /sdlc-test-1-campaign

Run the Test campaign pipeline (E2E/UAT).

1. Read `.apm/contexts/sdlc-agent-registry.yaml` for campaign agent compositions.
2. Execute: campaign launch (prerequisites, seeds, Xray) → campaign report (anomaly classification, Go/No-Go).
3. Requires BA + Tech deliverables and a deployed application. Arg: "e2e" or "uat".
