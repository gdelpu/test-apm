# GitHub Copilot — Sync Map

Maps canonical `.apm/` capabilities to their `.github/` Copilot runtime
projection. When a canonical file is added or changed, the corresponding
projection must be created or updated.

> **Architecture**: `.apm/` is the single canonical source of truth.
> `.github/` is the Copilot runtime projection derived from `.apm/`.

---

## Agents

| Canonical (`.apm/agents/`) | Runtime (`.github/agents/`) | Status |
|-----------------------------|------------------------------|--------|
| `brand-styler.md` | `brand-styler.agent.md` | synced |
| `repository-analyzer.md` | `repository-analyzer.agent.md` | synced |
| `reverse-backlog.md` | `reverse-backlog.agent.md` | synced |
| `reverse-user-story.md` | `reverse-user-story.agent.md` | synced |
| `security-reviewer.md` | `security-reviewer.agent.md` | synced |
| `soprasteria-branding.md` | `soprasteria-branding.agent.md` | synced |

## Prompts (standalone)

| Canonical (`.apm/prompts/`) | Runtime (`.github/prompts/`) | Status |
|-----------------------------|-------------------------------|--------|
| `convert-md-to-docx-and-pdf.md` | `convert-md-to-docx-and-pdf.prompt.md` | synced |
| `create-one-pager.md` | `create-one-pager.prompt.md` | synced |
| `soprasteria-brand-audit.md` | `soprasteria-brand-audit.prompt.md` | synced |
| `soprasteria-brand-refactor.md` | `soprasteria-brand-refactor.prompt.md` | synced |

## Workflows → Prompts

Each canonical workflow gets a `/workflow-*` slash command in Copilot.

| Canonical (`.apm/workflows/`) | Projection (`.github/prompts/`) | Status |
|-------------------------------|--------------------------------|--------|
| `feature-implementation.yml` | `workflow-feature.prompt.md` | synced |
| `modernization.yml` | `workflow-modernization.prompt.md` | synced |
| `quality-validation.yml` | `workflow-quality.prompt.md` | synced |
| `bmad.yml` | `workflow-bmad.prompt.md` | synced |
| `bug-fixing.yml` | `workflow-bug-fixing.prompt.md` | synced |
| `spec-kit.yml` | `workflow-spec-kit.prompt.md` | synced |
| `pr-validation.yml` | `workflow-pr-validation.prompt.md` | synced |
| `maturity-assessment.yml` | `workflow-maturity-assessment.prompt.md` | synced |

## Instructions

| Canonical concept | Projection (`.github/instructions/`) | `applyTo` |
|-------------------|--------------------------------------|-----------|
| APM layer rules | `apm-layer.instructions.md` | `.apm/**` |
| Knowledge base rules | `knowledge-base.instructions.md` | `knowledge/**` |
| Workflow conventions | `workflow.instructions.md` | `.apm/workflows/**` |
| README conventions | `readme.instructions.md` | `README.md` |
| Corrections | `corrections.instructions.md` | `**` |

## Hub-wide context

| Source | Projection |
|--------|-----------|
| `.github/copilot-instructions.md` | *(Copilot-specific — lives at runtime layer)* |

---

## Sync rules

1. **Adding an agent**: Create `.apm/agents/<name>.md` (canonical) → create `.github/agents/<name>.agent.md` (runtime, with Copilot frontmatter)
2. **Adding a prompt**: Create `.apm/prompts/<name>.md` → create `.github/prompts/<name>.prompt.md`
3. **Adding a workflow**: Create `.apm/workflows/<name>.yml` → create `.github/prompts/workflow-<name>.prompt.md`
4. **Changing an agent or prompt**: Update the `.apm/` canonical first, then sync `.github/`
5. **Validation**: Run `python scripts/validate_copilot_assets.py` to check required files exist

## Canonical-only (no Copilot projection)

Some canonical assets are internal and do not need a Copilot runtime projection:

- `.apm/instructions/security-hardening.md` — applied internally by skills
- `.apm/instructions/canonical-layer.md` — for canonical layer governance
- `.apm/contexts/*.md` — consumed by workflows, not directly by Copilot
