---
name: sdlc-ba-audit
description: 'Perform a functional snapshot of an existing system (brownfield audit) and produce an evolution delta matrix qualifying what is new, evolving, preserved, or deprecated.'
---

# Skill: sdlc-ba-audit

## Goal

Perform a functional snapshot of an existing system (brownfield audit) and produce an evolution delta matrix qualifying what is new, evolving, preserved, or deprecated.

## When to use

- At the start of any brownfield BA engagement (System S0)
- Before scoping to understand the current functional landscape
- As the first station in the `sdlc-ba` workflow when condition `brownfield_only` is met

## Procedure

### Phase 1 — Existing Audit (agent 0.1)
1. Load brownfield conventions and the existing audit template from `resources/`
2. Read client-provided documentation from `docs/0-inputs/ba/0-audit/`
3. Select audit mode based on documentation richness:
   - **Mode A** — Rich documentation: structured extraction from existing specs
   - **Mode B** — Partial documentation: inference + gap identification  
   - **Mode C** — No documentation: reverse-engineering from available artifacts
4. Produce the AS-IS functional snapshot with domain modules, integrations, and constraints
5. Write `docs/1-prd/0-audit/asis-001-existing-audit.md` with identifier `[ASIS-001]`

### Phase 2 — Delta Analysis (agent 0.2)
1. Load the existing audit `[ASIS-001]` as upstream input
2. Load the delta analysis template from `resources/`
3. Qualify each functional area as: **New** / **Evolving** / **Preserved** / **Deprecated**
4. Produce the evolution status matrix with impact assessment
5. Write `docs/1-prd/0-audit/delta-001-delta-analysis.md` with identifier `[DELTA-001]`

## Output

- `docs/1-prd/0-audit/asis-001-existing-audit.md` — `[ASIS-001]`
- `docs/1-prd/0-audit/delta-001-delta-analysis.md` — `[DELTA-001]`

## Rules

- Only runs for brownfield projects — skip entirely for greenfield
- Use structured Markdown with YAML front matter
- Maintain bracketed identifiers for traceability
- Run pre-input-validation hook before each phase
- Run post-quality-control hook after each phase for self-assessment

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-existing-audit.md` | Existing system audit template |
| `docs/tpl-delta-analysis.md` | Evolution delta matrix template |
| `docs/sk-0.1-existing-audit.md` | Detailed audit procedure (original harness skill) |
| `docs/sk-0.2-delta-analysis.md` | Detailed delta procedure (original harness skill) |
