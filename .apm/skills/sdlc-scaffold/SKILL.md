---
name: sdlc-scaffold
description: 'Create the standard docs/ directory structure for an SDLC project — both the base scaffold and per-feature scaffolds after fan-out discovery.'
---

# Skill: sdlc-scaffold

## Goal

Create the standard `docs/` directory structure for an SDLC project — both the base scaffold (inputs + deliverables) and per-feature scaffolds after fan-out discovery.

## When to use

- At pipeline start (Mode 1 — base scaffold)
- After epic/feature discovery in S2 (Mode 2 — feature scaffold)
- On-demand via `/scaffold` command
- Idempotent: safe to run multiple times

## Procedure

### Mode 1 — Base Scaffold
Create the full `docs/` directory tree:

```
docs/
  0-inputs/
    ba/_source/, ba/0-audit/, ba/1-scoping/, ba/2-spec/, ba/3-design/
    tech/_source/, tech/0-audit/, tech/1-archi/, tech/2-design/
    steer/
  1-prd/
    0-audit/, 1-scoping/, 2-specification/, 3-epics/, 4-tests/, 5-tools/, 6-workshops/
  2-tech/
    0-audit/, 1-architecture/, 2-design/, 3-quality/, 4-workshops/
  3-steer/
    0-sprint-reports/, 1-committees/
```

### Mode 2 — Feature Scaffold
For each discovered feature path:
- Create `docs/0-inputs/ba/3-design/{feature_id}/` for client documents
- Create the deliverable subtree under the feature's epic directory

## Output

- Directory structure (no files created — only directories)

## Rules

- Idempotent: never deletes existing content, only creates missing directories
- Base scaffold runs once at pipeline start
- Feature scaffold runs after each fan-out discovery (S2 epics → features)
- Directory naming follows convention: `{domain}/{system}/`

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/sk-scaffold.md` | Detailed scaffold procedure (original harness tool) |
