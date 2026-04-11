---
name: mcp-configuration
description: 'Configure MCP servers for a consumer repository — auto-detect platform, recommend profiles, interview for fine-tuning, generate configuration, and verify connectivity.'
triggers:
  - configure mcp
  - setup mcp
  - enable mcp
  - mcp servers
  - mcp profile
  - mcp config
---

# Skill: mcp-configuration

## Goal

Configure MCP (Model Context Protocol) servers for a consumer repository. Auto-detect the development platform, recommend a curated profile, fine-tune via interview, generate provider-specific configuration files, and verify server connectivity.

## Sub-commands

| Sub-command | Purpose |
|-------------|---------|
| `configure` (default) | Full setup: detect → recommend → interview → generate |
| `verify` | Health-check: test connectivity for all configured MCP servers |
| `list` | Show all available MCP servers and their status |
| `add <server-id>` | Add a specific MCP server to the current configuration |
| `remove <server-id>` | Remove a specific MCP server from the configuration |

## Procedure

### Sub-command: configure (default)

#### Step 1 — Load registry

Read `.apm/contexts/mcp-registry.yaml` for the full server catalog and profile definitions.

#### Step 2 — Auto-detect platform

Scan the consumer repository for platform markers:

| Marker | Detected platform |
|--------|-------------------|
| `.github/` directory | GitHub |
| `.gitlab-ci.yml` | GitLab |
| `azure-pipelines.yml` | Azure DevOps |
| `*.csproj`, `*.sln` | .NET stack |
| `package.json` | Node.js stack |
| `playwright.config.ts` | Playwright testing |
| `.semgrep.yml` | SemGrep configured |
| `FIGMA_ACCESS_TOKEN` env | Figma available |

Also check environment variables: `GITHUB_TOKEN`, `GITLAB_TOKEN`, `AZURE_DEVOPS_ORG`, `AZURE_SUBSCRIPTION_ID`, `AWS_PROFILE`, `ATLASSIAN_SITE`, `CONTEXT7_API_KEY`.

#### Step 3 — Recommend profile

Based on detection, recommend one of the curated profiles:

| Profile | When recommended |
|---------|-----------------|
| `github-stack` | `.github/` detected, no GitLab/ADO markers |
| `gitlab-stack` | `.gitlab-ci.yml` detected |
| `azure-devops-stack` | `azure-pipelines.yml` detected, Microsoft stack indicators |
| `full` | Multiple platform markers, or user requests all servers |

Present the recommendation with the list of included servers.

#### Step 4 — Interview for fine-tuning

Ask up to 4 questions to refine the profile:

1. **Cloud provider(s)**: "Which cloud platform(s) does this project use?" → Azure, AWS, both, neither
2. **Project management**: "Which project management tool?" → Jira (Atlassian), Azure Boards, GitHub Issues, none
3. **Browser testing**: "Do you need browser automation for E2E testing?" → Yes (Playwright MCP), No
4. **Design tool**: "Do you use Figma for design?" → Yes (Figma MCP), No

Add or remove servers from the profile based on answers.

Always include `context7` (cross-cutting documentation value) unless the user explicitly excludes it.

#### Step 5 — Generate configuration

Write the provider-specific MCP configuration file:

**For VS Code / GitHub Copilot** — `.vscode/mcp.json`:
```json
{
  "servers": {
    "<server-id>": {
      "command": "<install.command>",
      "args": ["<install.args>"],
      "env": { "<key>": "${input:<key>}" }
    }
  }
}
```

**For Claude Code** — `.claude/mcp.json` (same format)

**For CLI** — `providers/cli/mcp-config.json`

#### Step 6 — Generate setup guide

Write `outputs/mcp-setup-guide.md` with:
- Selected profile and servers
- Per-server authentication setup instructions
- Environment variable checklist
- Next steps (run `verify` sub-command)

### Sub-command: verify

#### Step 1 — Load configuration

Read the generated MCP configuration file (`.vscode/mcp.json` or equivalent).

#### Step 2 — Test each server

For each configured server:
1. Check if the required environment variables are set
2. Attempt to invoke the MCP server's tool list endpoint
3. Record: server ID, status (available / unavailable / auth-error), response time

#### Step 3 — Report results

Write verification results to stdout and `outputs/mcp-verify-report.md`:

```
MCP Server Verification Report
───────────────────────────────
✅ context7          Available (120ms)
✅ playwright-mcp    Available (85ms)
⚠️  github-mcp       Auth error — GITHUB_TOKEN not set
❌ azure-mcp         Unavailable — server not installed
───────────────────────────────
3 configured │ 2 available │ 1 auth error │ 1 unavailable
```

### Sub-command: list

Show all servers from `mcp-registry.yaml` with their current configuration status:
- ✅ Configured and verified
- ⚙️ Configured but not verified
- ─ Not configured

### Sub-command: add / remove

Add or remove a specific server by ID from the current configuration file. Validate the server ID against the registry.

## Output

Use `edit/editFiles` to write:
- `.vscode/mcp.json` (or provider equivalent) — MCP server configuration
- `outputs/mcp-setup-guide.md` — personalized setup instructions
- `outputs/mcp-verify-report.md` — connectivity verification results

## Rules

- Never write credentials or tokens into configuration files — use `${input:VAR}` placeholders
- Always include `context7` as a recommended default
- All servers are optional — never block workflows if MCP is unavailable
- Respect client-specific overrides in `clients/<name>/mcp-overrides.yaml`
- Merge overrides on top of profile defaults at generation time
