---
name: configure-mcp
mode: agent
description: 'Configure MCP (Model Context Protocol) servers for the current workspace.'
---

# /configure-mcp

Configure MCP servers for the current workspace using the canonical registry.

1. Read `.apm/skills/mcp-configuration/SKILL.md` for the full procedure.
2. Read `.apm/contexts/mcp-registry.yaml` for the server registry and profiles.
3. Read `.apm/instructions/mcp-integration.md` for behavioral rules.
4. Determine the sub-command from the user's intent:
   - **configure** (default) — auto-detect platform, recommend profile, interview, generate `.vscode/mcp.json`
   - **verify** — test connectivity of all configured MCP servers
   - **list** — show available servers and profiles
   - **add `<server-id>`** — add a single server to existing config
   - **remove `<server-id>`** — remove a single server from config
5. Execute the selected sub-command following the skill procedure.
6. **Write the generated configuration files to disk** using file-writing tools. Do not merely display content in chat.

## Outputs

- `.vscode/mcp.json` (VS Code / Copilot MCP configuration)
- `outputs/mcp-setup-report.md` (connectivity verification report, if `verify` sub-command)
