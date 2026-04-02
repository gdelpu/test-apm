---
name: sdlc-validate
mode: agent
description: 'Quality audit a SDLC deliverable (PASS / WARN / BLOCK).'
---

# /sdlc-validate

Validate a SDLC deliverable file.

1. Load validation skill from `.apm/skills/sdlc-deliverable-validation/`.
2. Route by domain: BA (`docs/1-prd/`) or Tech (`docs/2-tech/`).
3. Execute: structural analysis, semantic analysis, production confidence check.
4. Display verdict with detailed findings. Write report next to the deliverable.
