---
applyTo: 'providers/**,.apm/workflows/**'
description: 'Enforces provider parity: every command or workflow entry point must exist across all three providers (Claude Code, GitHub Copilot, CLI).'
---

# Provider Parity Instructions

Every user-facing command or workflow entry point **must be projected across all three providers**.
This is a mandatory rule — follow it whenever adding, renaming, or removing commands.

## Provider locations

| Provider | Path | Format | Naming |
|----------|------|--------|--------|
| Claude Code | `providers/claude-code/commands/` | `# /<command>` + Steps/Inputs/Outputs | `<name>.md` |
| GitHub Copilot | `providers/github-copilot/prompts/` | YAML frontmatter (`mode: agent`) + steps | `<name>.prompt.md` or `workflow-<name>.prompt.md` |
| CLI | `providers/cli/` | `run-workflow.sh` handles `.apm/workflows/*.yml` dynamically | Document new station IDs in `sdlc-commands.md` |

## Rules

1. **Adding a workflow**: Create `.apm/workflows/<name>.yml` + `.md` (canonical) → create `providers/claude-code/commands/workflow-<name>.md` → create `providers/github-copilot/prompts/workflow-<name>.prompt.md` → run `project-copilot.ps1` → verify CLI runner discovers it automatically.
2. **Adding a command** (sub-pipeline, agent dispatch, or tool): Create in `providers/claude-code/commands/<name>.md` → create matching `providers/github-copilot/prompts/<name>.prompt.md` → run `project-copilot.ps1` → if the command maps to a station, add it to `providers/cli/sdlc-commands.md`.
3. **Renaming or removing**: Apply the same change in all three providers simultaneously.
4. **Sync map**: Update `providers/github-copilot/sync-map.md` with any new mappings.
5. **CLAUDE.md**: Update `providers/claude-code/CLAUDE.md` command table with new entries.

## Naming conventions

- SDLC commands are prefixed with `sdlc-` (e.g., `sdlc-ba-1-scoping`, `sdlc-validate`).
- Composite workflow commands: `sdlc-<domain>` (e.g., `sdlc-ba`, `sdlc-tech`, `sdlc-full`).
- Sub-pipeline commands: `sdlc-<domain>-<N>-<name>` (e.g., `sdlc-ba-0-audit`, `sdlc-tech-2-design`).
- Agent dispatch commands: `sdlc-<domain>-agent` (e.g., `sdlc-ba-agent`, `sdlc-tech-agent`).
- Tool commands: `sdlc-<name>` (e.g., `sdlc-validate`, `sdlc-coherence`, `sdlc-impact`).

## Checklist for new commands

When adding any new command, verify all items before considering the task complete:

- [ ] Claude Code command file exists in `providers/claude-code/commands/`
- [ ] GitHub Copilot prompt file exists in `providers/github-copilot/prompts/`
- [ ] CLI documentation updated (if station-based, add to `providers/cli/sdlc-commands.md`)
- [ ] `providers/github-copilot/sync-map.md` updated with new mapping
- [ ] `providers/claude-code/CLAUDE.md` command table updated
- [ ] `.github/copilot-instructions.md` workflow table updated (if workflow)
- [ ] `project-copilot.ps1` run to update `.github/` runtime projection
