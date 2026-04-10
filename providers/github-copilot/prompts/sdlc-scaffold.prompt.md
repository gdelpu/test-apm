---
name: sdlc-scaffold
mode: agent
description: 'Create docs/ directory structure for SDLC project.'
---

# /sdlc-scaffold

Create the docs/ directory scaffold for the project.

1. Read `.apm/skills/sdlc-scaffold/SKILL.md` for scaffold logic.
2. Collect project name and language, create `docs/project.yml`.
3. Create client input directories (`docs/0-inputs/`) and deliverable directories (`outputs/docs/1-prd/`, `outputs/docs/2-tech/`, `outputs/docs/3-steer/`).
4. If "features" argument provided, also scaffold per-feature design directories.
