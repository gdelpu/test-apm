---
mode: agent
description: 'Execute a single BA agent by number (e.g., 1.2, 3.5).'
---

# /sdlc-ba-agent

Execute one BA agent from the SDLC agent registry.

1. Read `.apm/contexts/sdlc-agent-registry.yaml` — find the requested BA agent.
2. Assemble prompt: hooks + conventions + template + skill + upstream context.
3. Launch and display result. For per-feature agents (3.x), provide the feature path.
