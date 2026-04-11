# Contributing

> How to add agents, skills, workflows, and prompts — plus naming conventions, prerequisites, and maintenance rules.

---

## Prerequisites

| Tool | Version | Required For |
|------|---------|-------------|
| Python | 3.11+ | Validators, validation scripts |
| Git | 2.x+ | Diff generation, validation |
| Node.js | 20+ | Copilot CLI (AI stations), APM |
| APM CLI | latest | Bundle building and distribution |
| GitHub Copilot CLI | 1.0.4 | AI station execution |
| jq | 1.6+ | Gate enforcement |
| curl | — | Package registry publishing / consumption |
| Podman | — | Local pipeline execution (optional) |
| Pandoc | — | Brand Styler document conversion (optional) |

---

## Adding Capabilities

<!-- These checklists are the canonical self-maintenance protocol.
     Follow them exactly when extending the repository. -->

### New agent

1. Create `.apm/agents/<name>.md` (canonical, provider-agnostic)
2. Create `.github/agents/<name>.agent.md` (Copilot runtime, with frontmatter) — if user-facing
3. Update `providers/github-copilot/sync-map.md`
4. Update `docs/reference/agents.md`: agent table (new row) and count in heading

### New skill

1. Create `.apm/skills/<name>/SKILL.md` (+ optional `tools/`, `docs/`)
2. Update `docs/reference/skills.md`: skills table (new row in correct category) and count in heading

### New workflow

1. Create `.apm/workflows/<name>.yml` following `_schema.md`
2. Create `.github/prompts/workflow-<name>.prompt.md` (Copilot runtime)
3. Add provider commands: `providers/claude-code/commands/workflow-<name>.md`
4. Update `providers/github-copilot/sync-map.md`
5. Update `docs/reference/workflows.md`: add detailed station table under correct category, update count in heading

### New prompt

1. Create `.apm/prompts/<name>.md` (canonical)
2. Create `.github/prompts/<name>.prompt.md` (Copilot runtime)
3. Update `providers/github-copilot/sync-map.md`
4. Update `docs/reference/prompts.md`: prompts table (new row) and count in heading

### After any change

```bash
# Always run cross-layer validation after changes
python scripts/validate_all.py
```

---

## Self-Maintenance Checklist

When modifying this repository, update all affected locations:

- [ ] **Root README** asset summary table — counts match actual files
- [ ] **Root README** architecture diagram — counts in the ASCII art match reality
- [ ] **`docs/reference/` catalogs** — agents.md, skills.md, workflows.md, hooks.md, prompts.md are current
- [ ] **Provider Setup** — Copilot/Claude file counts are current
- [ ] **Cross-layer validation passes** — `python scripts/validate_all.py`

---

## Contributing Workflow

### From shared resources

1. Canonical definitions go in `.apm/` (agents, skills, prompts, workflows, templates, scripts)
2. Copilot runtime projections go in `.github/` (agents, prompts, instructions)
3. Adapter docs go in `providers/<provider>/` (conventions, sync-map, CLAUDE.md)
4. Brand assets live in `knowledge/brand/`
5. Open an MR targeting the `staged` branch

### From a client engagement

1. Create `clients/<client-name>/` with client-specific overrides
2. Open an MR — reusable items get promoted to `.apm/`

---

## Naming Conventions

- **lowercase, hyphens**: `code-review.agent.md`, `brand-core/SKILL.md`
- YAML frontmatter required: `name`, `description` (single-quoted)
- Copilot instructions need `applyTo` in frontmatter
