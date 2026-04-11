# MCP Integration Guide — Contributor Reference

> How to add new MCP servers, enhance existing skills with MCP support, and test MCP integrations.

---

## Table of Contents

- [Overview](#overview)
- [Adding a New MCP Server](#adding-a-new-mcp-server)
- [Enhancing an Existing Skill with MCP](#enhancing-an-existing-skill-with-mcp)
- [MCP Skill Template](#mcp-skill-template)
- [Registry Schema Reference](#registry-schema-reference)
- [Testing MCP Integration](#testing-mcp-integration)
- [Provider Parity Checklist](#provider-parity-checklist)

---

## Overview

MCP (Model Context Protocol) servers provide optional enrichments to agents and workflows. The architecture follows the established `required` / `optional` tool pattern from the SDLC agent registry.

**Key principle**: MCP tools are never required. Every skill must have a documented fallback path.

**Source of truth**: `.apm/contexts/mcp-registry.yaml` defines all curated servers, profiles, and metadata.

---

## Adding a New MCP Server

Follow these steps to add a new MCP server to the foundation:

### Step 1 — Add to registry

Add an entry to `.apm/contexts/mcp-registry.yaml`:

```yaml
- id: <server-id>           # Unique kebab-case identifier
  name: <Display Name>
  category: cloud|devops|collaboration|documentation|testing|design
  repo: <https://...>       # Link to official repository or docs
  description: '<One-line description of capabilities>'
  install:
    command: npx             # or pip, docker, etc.
    args: ['<package>@latest']
    env:                     # Environment variables for auth
      TOKEN_VAR: '${TOKEN_VAR}'
  default_version: '@latest' # or pinned version like '@1.2.0'
  auth: none|api-key|personal-access-token|azure-identity|aws-credentials|oauth
  platform_detection:
    markers: ['<file-pattern>']  # Files indicating this platform
    env: ['<ENV_VAR>']           # Env vars indicating this platform
  skills_new: [<new-skill-id>]
  skills_enhanced:
    - <existing-skill-1>
    - <existing-skill-2>
  fallback: '<One-line fallback description>'
```

### Step 2 — Create new skill

Create `.apm/skills/<server-verb>/SKILL.md` following the [MCP Skill Template](#mcp-skill-template) below.

### Step 3 — Enhance existing skills

For each skill listed in `skills_enhanced`, add MCP-enhanced procedure steps. See [Enhancing an Existing Skill](#enhancing-an-existing-skill-with-mcp).

### Step 4 — Update agent registry

Add the server ID to relevant agent `optional:` arrays in `.apm/contexts/sdlc-agent-registry.yaml`:

```yaml
tools:
  required: [file-read, file-write]
  optional: [jira-mcp, <new-server-id>]  # ← add here
```

### Step 5 — Add to profiles

Add the server to at least one profile in `mcp-registry.yaml` under the `profiles:` section.

### Step 6 — Create provider entries

- **Copilot**: If the server enables a new workflow entry point, create `providers/github-copilot/prompts/workflow-<name>.prompt.md`
- **Claude Code**: Create `providers/claude-code/commands/<name>.md` if needed
- **CLI**: Ensure `providers/cli/run-workflow.sh` handles the new capability
- Update `providers/github-copilot/sync-map.md` with the new mappings

### Step 7 — Update documentation

- Add a section to `docs/consumer/mcp-setup-guide.md` (per-server setup)
- Add the new skill to `docs/reference/skills.md` (MCP Skills category)
- If the server is client-specific, update `clients/<name>/CUSTOMIZATIONS.md`

### Step 8 — Validate

```bash
# Core asset validation
python scripts/validate_core_assets.py

# Copilot asset validation
python scripts/validate_copilot_assets.py

# Regenerate runtime
.\.apm\scripts\powershell\project-copilot.ps1 -Clean
```

---

## Enhancing an Existing Skill with MCP

When an existing skill can benefit from an MCP server:

### Pattern

Add a conditional MCP step to the skill's procedure section:

```markdown
### Step N — Enhanced: <description> (optional MCP)

**With `<server-id>` MCP**: <what the MCP tool provides>

**Without MCP (fallback)**: <what happens without it>
```

### Example: Adding SemGrep MCP to `security-scan`

**Before** (existing procedure step):
```markdown
### SAST (station: security-sast)

1. Check that Checkmarx CLI is installed
2. Run SAST scan against source code
3. Parse results
4. Produce `sast-report.md`
```

**After** (with MCP enhancement):
```markdown
### SAST (station: security-sast)

1. Check that Checkmarx CLI is installed
2. Run SAST scan against source code
3. **Enhanced**: If `semgrep-mcp` is available, run supplementary SemGrep rules
   for OWASP Top 10 coverage. Merge findings into the report.
   **Fallback**: Skip SemGrep supplementary scan — Checkmarx results are sufficient.
4. Parse results
5. Produce `sast-report.md`
```

### Rules

- The MCP step must be clearly marked as optional
- Fallback behavior must produce a usable deliverable, not a stub
- Add quality markers when degrading (e.g., `[SAST-BASIC-ONLY]`)
- Update the skill's tool declarations: `optional: [..., <server-id>]`

---

## MCP Skill Template

Use this template for new MCP skills:

```markdown
---
name: <server-verb>
description: '<What the skill does via the MCP server>'
triggers:
  - <trigger phrase 1>
  - <trigger phrase 2>
---

# Skill: <server-verb>

## Goal

<1-2 sentence description of what this skill accomplishes>

## MCP Server

- **Registry ID**: `<server-id>`
- **Repository**: <https://...>
- **Auth**: <auth type>
- **Env**: `<ENV_VAR_1>`, `<ENV_VAR_2>`

## When to use

- <Use case 1>
- <Use case 2>

## When NOT to use

- <Anti-pattern 1>
- <Anti-pattern 2>

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `<server-id>` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute operation

<MCP-enhanced procedure>

### Fallback (without MCP)

If `<server-id>` is unavailable:
1. <Primary fallback>
2. <Secondary fallback>
3. Warn that <specific capability> is unavailable

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/<output-file>.md`

## Security

- <Security constraint 1>
- <Security constraint 2>
```

---

## Registry Schema Reference

Each server entry in `mcp-registry.yaml` supports these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique kebab-case identifier |
| `name` | string | yes | Human-readable display name |
| `category` | enum | yes | `cloud`, `devops`, `collaboration`, `documentation`, `testing`, `design` |
| `repo` | URL | yes | Link to official repository or documentation |
| `description` | string | yes | One-line capability description |
| `install` | object | yes | Installation configuration |
| `install.command` | string | yes* | CLI command to run the server |
| `install.args` | string[] | yes* | Arguments for the command |
| `install.env` | object | no | Environment variables (key: `${VAR}` format) |
| `install.url` | string | no* | Remote MCP endpoint URL (alternative to command) |
| `install.prerequisite` | string | no | Pre-installation command (e.g., `pip install semgrep`) |
| `default_version` | string | yes | `@latest` or pinned version |
| `auth` | enum | yes | `none`, `api-key`, `api-key-optional`, `personal-access-token`, `azure-identity`, `aws-credentials`, `entra-admin-consent`, `oauth` |
| `platform_detection` | object | no | Auto-detection configuration |
| `platform_detection.markers` | string[] | no | File patterns that indicate this platform |
| `platform_detection.env` | string[] | no | Environment variables that indicate this platform |
| `cross_cutting` | boolean | no | If true, recommended for all consumers (e.g., Context7) |
| `security_notes` | string | no | Special security considerations |
| `skills_new` | string[] | yes | New skills created for this server |
| `skills_enhanced` | string[] | yes | Existing skills enhanced by this server |
| `fallback` | string | yes | One-line fallback description |

*Either `command`+`args` or `url` is required.

---

## Testing MCP Integration

### Local testing

1. **Install the MCP server** in VS Code or your IDE
2. **Set environment variables** for authentication
3. **Run the verify command**: `@hub-orchestrator verify MCP`
4. **Test the MCP path**: Execute the skill and verify it uses MCP tools
5. **Test the fallback path**: Unset env vars and verify graceful degradation
6. **Run validation**: `python scripts/validate_core_assets.py`

### Checklist

- [ ] New skill has frontmatter with `name`, `description`, `triggers`
- [ ] Procedure has explicit MCP check → fallback flow
- [ ] Fallback produces a usable deliverable (not a stub)
- [ ] Security section documents scope restrictions
- [ ] Registry entry has all required fields
- [ ] At least one profile includes the server
- [ ] Consumer docs updated (`mcp-setup-guide.md`)
- [ ] Skills reference updated (`docs/reference/skills.md`)
- [ ] Provider parity achieved (Copilot + Claude + CLI)

---

## Provider Parity Checklist

Every MCP-related entry point must exist across all three providers:

| Provider | Format | Location |
|----------|--------|----------|
| Copilot | `.prompt.md` slash command | `providers/github-copilot/prompts/` |
| Claude Code | `.md` command | `providers/claude-code/commands/` |
| CLI | Shell support | `providers/cli/run-workflow.sh` |

The `mcp-configuration` skill is exposed as:
- **Copilot**: `/workflow-configure-mcp`
- **Claude Code**: `/configure-mcp`
- **CLI**: `./providers/cli/run-workflow.sh --mcp-profile <profile>`
