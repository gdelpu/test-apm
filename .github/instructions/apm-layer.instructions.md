---
name: apm-layer
description: 'Rules for working inside the canonical APM packaging layer (source of truth).'
applyTo: .apm/**
---

# APM Layer Instructions

You are working inside the canonical packaging layer (source of truth).

## Structure

| Folder | Content |
|--------|---------|
| `.apm/agents/` | Cross-provider agent definitions (provider-agnostic) |
| `.apm/skills/` | Skill packages with `SKILL.md` and optional `tools/`, `docs/` |
| `.apm/prompts/` | Reusable prompt templates |
| `.apm/instructions/` | Shared behavioral instructions |
| `.apm/contexts/` | Context documents agents can reference |
| `.apm/hooks/` | Pre/post execution hooks with schema and config |
| `.apm/workflows/` | YAML workflow definitions with stations and gates |

## Conventions

- Agent files define purpose, decision policy, required outputs, and skill references.
- Skill folders contain a `SKILL.md` (definition) and optional `tools/` (scripts, templates), `docs/`.
- Prompts are standalone and can be used across providers.
- The `.apm/` layer is the canonical cross-provider source.

## Sync Rule

When you add or modify an agent, skill, or prompt in `.apm/`, the corresponding
runtime file in `.github/` must be updated. Consult
`providers/github-copilot/sync-map.md` for the canonical → runtime mapping.
