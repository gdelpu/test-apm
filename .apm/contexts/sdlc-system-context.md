# SDLC Agentic Harness — System Context

> Canonical reference for cross-cutting conventions used by all SDLC domain agents.
> Migrated from `SDLC-agenticharness/orchestration/system-prompt.md`.

## Deliverable Structure

```
docs/
  0-inputs/       # Client-provided documents (read-only for agents)
    ba/           # Functional inputs (_source, 0-audit, 1-scoping, 2-spec, 3-design)
    tech/         # Technical inputs (_source, 0-audit, 1-archi, 2-design)
    steer/        # COPIL decisions, arbitrations, scope changes
  1-prd/          # BA deliverables (Product Requirements Document)
    0-audit/      # (brownfield) AS-IS audit + delta analysis
    1-scoping/    # Vision, glossary, actors, functional requirements
    2-specification/  # Domain model, cross-cutting business rules
    3-epics/      # Hierarchical: epic > feature > stories, journeys, screens, tests
    4-tests/      # Campaign-level: shared seeds, E2E plan
    5-tools/      # On-demand outputs: impact, validation, GDPR, UAT
    6-workshops/  # Review workshop reports
  2-tech/         # Tech deliverables
    0-audit/      # Technical audit + gap analysis
    1-architecture/ # System context, ADRs, stack, enablers
    2-design/     # Data model, APIs, test strategy, impl plan
    3-implementation/ # Wave-state, sprint summaries, per-wave subdirs (W0/, W1/, ...)
      W{wave_id}/   # impl-logs, test-logs, validation reports, wave reports
    4-quality/    # Drift reports, code reviews, E2E scripts
    5-workshops/  # Tech review reports
  3-steer/        # Steering deliverables
    0-sprint-reports/ # Sprint progress, health, risks
    1-committees/     # COPIL packs, Go/No-Go
```

## Cross-cutting Conventions

### Identifiers
All deliverables use bracketed identifiers: `[EP-001]`, `[FT-012]`, `[US-034]`, `[BR-005]`.
Files are named with the identifier as lowercase prefix: `ep-001-authentication.md`.

### Statuses
| Status | Meaning |
|--------|---------|
| `draft` | Produced by agent, not yet reviewed |
| `review` | Under human review |
| `validated` | Validated, ready for next phase |

### Traceability Chains
- **BA**: `EXF → EP → FT → US → BR → SCE` (Requirements to Test Scenarios)
- **Tech**: `DOM → DAT`, `US → API`, `BR → Constraints`, `ADR → ENB`, `ACT → Auth`
- **Steer**: `PLAN → STA`, `RDP → PLAN`, `RSK → COP`

### Language
- Deliverable content is produced in the project's working language
- Technical identifiers and YAML keys remain in English

### Client Inputs Convention
- Agents read, users write. Agents never deposit files in `0-inputs/`
- Directory naming follows `{domain}/{system}/` matching the target agent
- An empty directory never blocks an agent

## Available Commands

### Pipeline commands
| Command | Domain | Canonical Workflow |
|---------|--------|--------------------|
| `/sdlc-ba` | BA | `sdlc-ba.yml` |
| `/sdlc-tech` | Tech | `sdlc-tech.yml` |
| `/sdlc-steer` | Steer | `sdlc-steer.yml` |
| `/sdlc-full` | All | `sdlc-full.yml` |

### Utility commands
| Command | Skill |
|---------|-------|
| `/scaffold` | `sdlc-scaffold` |
| `/validate` | `sdlc-deliverable-validation` |
| `/coherence` | `sdlc-deliverable-validation` |
| `/impact` | `sdlc-change-impact` |
| `/confluence-push` | `sdlc-confluence-sync` |
| `/confluence-pull` | `sdlc-confluence-sync` |

## Hooks (applied as pre/post procedures)

### Pre-hooks
- **pre-input-validation**: Verifies upstream deliverable sufficiency (GO / WARN / STOP)
- **pre-amendment-mode**: Surgical delta application for change requests (activated by `[IMPACT-xxx]`)

### Post-hooks
- **post-quality-control**: Self-check for template conformance, Production Confidence score
- **post-confluence-push**: Auto-push deliverable to Confluence with Mermaid→PNG conversion
