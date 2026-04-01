---
mode: agent
description: 'Execute a single Tech agent by number (e.g., t1.1, t2.3).'
---

# /sdlc-tech-agent

Execute one Tech agent from the SDLC agent registry.

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find the requested Tech agent.
2. Assemble prompt: hooks + conventions + skill + upstream context.
3. Launch and display result.
