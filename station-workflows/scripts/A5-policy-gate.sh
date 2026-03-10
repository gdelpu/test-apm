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
echo "Station A5 - POLICY GATE: Making decision..."

copilot -p "
You are Station A5 - POLICY GATE, the final decision maker.

GOAL: Aggregate all station reports and make the gate decision

TASK:
1. Read all reports from ${STATION_OUT}/:
   work_order.json, policy_report.json, security_report.json,
   promptsec_report.json, sim_report.json

2. Apply gate logic:
   IF any report has critical_count > 0:
     status = BLOCK; justification = Critical severity findings must be resolved
   ELSE IF sum of high_count across all reports >= 3:
     status = REVIEW; justification = Multiple high-severity findings require human review
   ELSE IF any report status is fail:
     status = BLOCK; justification = One or more stations failed validation
   ELSE:
     status = APPROVE; justification = All validations passed

3. Write to ${STATION_OUT}/gate_decision.json:
{
  \"station\": \"A5\", \"status\": \"APPROVE|BLOCK|REVIEW\",
  \"justification\": \"...\", \"timestamp\": \"<ISO8601>\",
  \"summary\": {\"total_findings\": <n>, \"critical\": <n>, \"high\": <n>, \"medium\": <n>, \"low\": <n>},
  \"blocking_issues\": [...], \"recommendations\": [...]
}

CONSTRAINTS:
- Load and parse ALL report JSONs
- Apply exact gate logic above
- BLOCK or REVIEW must list specific issues
" --allow-tool 'write'

# Extract decision and enforce exit code
echo ""
echo ""
echo "  POLICY GATE DECISION"
echo ""
jq -C . "${STATION_OUT}/gate_decision.json"
echo ""

STATUS=$(jq -r '.status' "${STATION_OUT}/gate_decision.json")

if [ "$STATUS" = "BLOCK" ]; then
  echo ""
  echo "GATE STATUS: BLOCKED - MR cannot merge until issues are resolved."
  exit 1
elif [ "$STATUS" = "REVIEW" ]; then
  echo ""
  echo "GATE STATUS: NEEDS REVIEW - Human review required before merge."
  exit 0
else
  echo ""
  echo "GATE STATUS: APPROVED - All validations passed. Safe to merge."
  exit 0
fi