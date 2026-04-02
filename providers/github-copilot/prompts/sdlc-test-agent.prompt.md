---
name: sdlc-test-agent
mode: agent
description: 'Execute a single Test agent by ID (e.g., camp.1, perf.2).'
---

# /sdlc-test-agent

Execute one Test agent from the SDLC agent registry.

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find the requested Test agent.
2. Assemble prompt: hooks + conventions + skill + upstream context.
3. Launch and display result.
