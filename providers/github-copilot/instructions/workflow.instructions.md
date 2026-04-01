---
applyTo: '.apm/workflows/**'
---

# Workflow Instructions

Workflows in `.apm/workflows/` define station-based pipelines with quality gates.

## Key Rules

- Each workflow has a `.yml` (machine-parseable) and optional `.md` (human-readable) pair.
- The YAML schema is documented in `_schema.md`.
- Station agents and skills must reference existing definitions in `.apm/agents/` and `.apm/skills/`.
- Quality gates use `severity: blocker` (halt) or `severity: warning` (log and continue).
- Nested workflows are supported via stations that reference other workflow names.
- Stations with `parallel: true` can run concurrently.
- The PR validation workflow wraps the existing A0–A7 station pipeline.
