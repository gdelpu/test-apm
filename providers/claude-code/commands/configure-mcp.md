# /configure-mcp

Configure MCP (Model Context Protocol) servers for the current workspace.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `sub-command` | No | `configure` | `configure`, `verify`, `list`, `add`, `remove` |
| `server-id` | For add/remove | — | MCP server ID from the registry |
| `profile` | No | auto-detect | Profile name: `github-stack`, `gitlab-stack`, `azure-devops-stack`, `full` |

## Steps

1. Read `.apm/skills/mcp-configuration/SKILL.md` for the full procedure.
2. Read `.apm/contexts/mcp-registry.yaml` for the server registry and profiles.
3. Read `.apm/instructions/mcp-integration.md` for behavioral rules.
4. Determine the sub-command:
   - **configure** (default) — auto-detect platform, recommend profile, interview (max 4 questions), generate `.claude/mcp.json`
   - **verify** — test connectivity of all configured MCP servers, report status table
   - **list** — show available servers grouped by category with profile membership
   - **add `<server-id>`** — add a single server to existing config
   - **remove `<server-id>`** — remove a single server from config
5. Execute the selected sub-command following the skill procedure.
6. **Write all generated configuration files to disk.** Do not merely display content in chat.

## Outputs

- `.claude/mcp.json` (Claude Code MCP configuration)
- `outputs/mcp-setup-report.md` (connectivity verification report, if `verify`)
