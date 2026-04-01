---
mode: agent
description: 'Execute a single Steer agent by number (e.g., p0.1, p2.1).'
---

# /sdlc-steer-agent

Execute one Steer agent from the SDLC agent registry.

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find the requested Steer agent.
2. Assemble prompt: hooks + conventions + skill + upstream context.
3. Launch and display result.
