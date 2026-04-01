---
mode: agent
description: 'Change impact analysis with optional amendment cascade.'
---

# /sdlc-impact

Run change impact analysis on SDLC deliverables.

1. Load `.apm/skills/sdlc-change-impact/SKILL.md` and `.apm/contexts/sdlc-impact-graph.yaml`.
2. Identify changes, traverse impact graph, classify impacts.
3. Offer amendment: if accepted, re-execute affected agents and run coherence check.
