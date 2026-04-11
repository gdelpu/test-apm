# Provider Setup

> How to configure and use each supported provider: GitHub Copilot, Claude Code, and CLI.

---

## GitHub Copilot (three-layer)

- **Provider layer** (source of truth for Copilot-format files):
  - Agents: `providers/github-copilot/agents/*.agent.md` (7 agents)
  - Prompts: `providers/github-copilot/prompts/*.prompt.md` (5 standalone + 14 workflow + 26 SDLC)
  - Instructions: `providers/github-copilot/instructions/*.instructions.md` (6 files, with `applyTo` patterns)
  - Docs: `providers/github-copilot/conventions.md` + `sync-map.md`
- **Runtime projection** (generated — gitignored):
  - Run `.apm/scripts/powershell/project-copilot.ps1` to copy into `.github/`
  - Hub context: `.github/copilot-instructions.md` (not generated, lives directly in `.github/`)
- Consult `sync-map.md` for the full canonical → provider mapping.

## Claude Code

- Context file: `providers/claude-code/CLAUDE.md`
- Commands: `providers/claude-code/commands/*.md` (8 workflow + 31 SDLC + 1 hub)

## CLI

```bash
# Run a workflow
./providers/cli/run-workflow.sh feature-implementation my-feature

# Dry run
./providers/cli/run-workflow.sh quality-validation my-feature --dry-run

# Resume from last pass
./providers/cli/run-workflow.sh modernization spring-upgrade --resume

# Single station
./providers/cli/run-workflow.sh pr-validation my-branch --station a1-policy-validation
```
