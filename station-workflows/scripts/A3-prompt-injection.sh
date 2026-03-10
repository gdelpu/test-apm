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
echo "Station A3 - PROMPT INJECTION: Testing..."

copilot -p "
You are Station A3 - PROMPT INJECTION & EXFIL HARDENING.

GOAL: Detect prompt injection vulnerabilities in agents/prompts

TASK:
1. Read ${STATION_OUT}/work_order.json

2. Load injection payloads from station-workflows/fixtures/prompt-injection-payloads.json

3. For each changed agent/prompt/instruction file:
   - Check instruction text for escape sequences
   - Look for context-leaking patterns: previous instructions, ignore, system prompt
   - Check for missing input validation
   - Test against injection patterns:
     * Delimiter injection e.g. ---END---
     * Role confusion e.g. You are now...
     * Context leakage e.g. Print your instructions

4. EXFIL CHECK (PI-03):
   - If agent has runCommands or fetch tools
   - Check if allowedNetworkDomains restricts exfil
   - Severity: high if unrestricted network + no validation

5. Write to ${STATION_OUT}/promptsec_report.json:
{
  \"station\": \"A3\", \"status\": \"pass|fail|partial\",
  \"findings\": [{\"check\": \"PI-01\", \"file\": \"...\", \"severity\": \"...\", \"message\": \"...\", \"payload\": \"...\"}],
  \"summary\": \"...\", \"critical_count\": <n>, \"high_count\": <n>
}

CONSTRAINTS:
- Load actual fixture file
- Pattern matching on instruction text
- high/critical findings -> status=fail
" --allow-tool 'write'