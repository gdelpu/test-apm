#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq curl git jq ca-certificates

# Trust volume-mounted workspace (container uid differs from host)
git config --global --add safe.directory /workspace

# Copilot CLI needs a token; export before install so post-check passes
[ -n "${GH_TOKEN:-}" ] || { echo "ERROR: GH_TOKEN not set"; exit 1; }
export COPILOT_GITHUB_TOKEN="${GH_TOKEN}"

# Install Copilot CLI — tolerate installer post-check failures
curl -fsSL https://gh.io/copilot-install | bash || true

export PATH="$HOME/.local/bin:$PATH"
copilot --version || { echo "ERROR: copilot CLI install failed"; exit 1; }
mkdir -p /workspace/station_out
cd /workspace
echo "Station A1 - POLICY VALIDATION: Checking schemas..."

copilot -p "
You are Station A1 - POLICY VALIDATION for the Agent Factory pipeline.

GOAL: Validate agent/skill manifests against JSON schemas

TASK:
1. Read ${STATION_OUT}/work_order.json

2. If scope is non-agent, write skipped report and exit:
   {\"station\":\"A1\",\"status\":\"skipped\",\"findings\":[],\"summary\":\"No agent/skill files changed.\",\"files_checked\":0,\"critical_count\":0,\"high_count\":0}

3. For each changed file where type is agent:
   - Parse YAML frontmatter
   - Validate against station-workflows/schemas/agent-manifest.schema.json
   - Check required fields: name, description, tools (array)
   - Validate tools are in allowlist:
     [codebase, search, edit, problems, runCommands, github, terminal, fetch, vscode]
   - If runCommands is present, check allowedNetworkDomains and allowedFilePaths exist
   - Severity: critical if schema fails, high if security fields missing

4. For each changed file where type is skill:
   - Parse YAML frontmatter
   - Validate against station-workflows/schemas/skill-manifest.schema.json
   - Check required fields: name, description, triggers (non-empty array)
   - Severity: critical if schema fails

5. Write to ${STATION_OUT}/policy_report.json:
{
  \"station\": \"A1\", \"status\": \"pass|fail|partial\",
  \"findings\": [{\"rule\": \"P-01\", \"file\": \"...\", \"severity\": \"...\", \"message\": \"...\"}],
  \"summary\": \"...\", \"files_checked\": <n>, \"critical_count\": <n>, \"high_count\": <n>
}

CONSTRAINTS:
- Load actual schema files from disk
- Perform real validation - do not fake results
- critical findings -> status=fail
" --allow-tool 'write'