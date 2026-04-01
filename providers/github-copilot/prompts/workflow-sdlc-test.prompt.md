---
mode: agent
description: 'Run full Test pipeline — E2E/UAT campaign + performance.'
---

# /workflow-sdlc-test

Run the Test pipeline (campaign + performance).

1. Read `.apm/contexts/sdlc-agent-registry.yaml` for Test agent compositions.
2. Execute campaign system (launch + report) then performance system (execution + report).
3. Display cumulative Go/No-Go recommendation.
