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
echo "Station A2 - SECURITY STATIC CHECKS: Scanning..."
GITLEAKS_VER="8.18.4"
curl -sSfL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VER}/gitleaks_${GITLEAKS_VER}_linux_x64.tar.gz" \
  | tar -xz -C /usr/local/bin gitleaks
gitleaks version

copilot -p "
You are Station A2 - SECURITY STATIC CHECKS for the Agent Factory pipeline.

GOAL: Detect secrets, dangerous patterns, and vulnerable dependencies

TASK:
1. Read ${STATION_OUT}/work_order.json

2. If scope is non-agent, write skipped report and exit

3. SECRET SCAN (S-01):
   - Run: gitleaks detect --source=. --no-git --verbose
   - Look for: API keys (ghp_, sk-, AKIA), passwords, tokens
   - Check .env files, YAML frontmatter, prompt bodies
   - Severity: critical for any confirmed secret

4. DANGEROUS PATTERN SCAN (S-03):
   - In changed agent files, scan for:
     * Unrestricted allowedFilePaths: **, /, ~
     * Unrestricted allowedNetworkDomains: *
     * Shell injection: rm -rf, eval, exec
     * Path traversal: ../../../
   - Severity: high

5. DEPENDENCY SCAN (S-02) if package files changed:
   - Check package-lock.json, requirements.txt, go.mod
   - Report CVEs; map CVSS: >=9.0=critical, 7.0-8.9=high, 4.0-6.9=medium

6. Write to ${STATION_OUT}/security_report.json:
{
  \"station\": \"A2\", \"status\": \"pass|fail|partial\",
  \"findings\": [{\"check\": \"S-01\", \"file\": \"...\", \"severity\": \"...\", \"message\": \"...\", \"line\": <n>}],
  \"summary\": \"...\", \"critical_count\": <n>, \"high_count\": <n>
}

CONSTRAINTS:
- Run actual gitleaks scan
- Real pattern matching on changed files
- critical -> status=fail
" --allow-tool 'shell(gitleaks)' --allow-tool 'shell(grep)' --allow-tool 'shell(find)' --allow-tool 'write'