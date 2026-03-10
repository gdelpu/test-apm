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

echo "Station A0 - INTAKE: Extracting MR context..."
BASE_SHA=$(git rev-parse "${CI_MERGE_REQUEST_DIFF_BASE_SHA:-}" 2>/dev/null \
  || git rev-list --max-parents=0 HEAD)

copilot -p "
You are Station A0 - INTAKE for the Agent Factory SDLC pipeline.

GOAL: Extract merge request context and create work_order.json

TASK:
1. Extract MR metadata from environment variables:
   MR Number: ${CI_MERGE_REQUEST_IID}
   MR Title: ${CI_MERGE_REQUEST_TITLE}
   Author: ${CI_MERGE_REQUEST_AUTHOR}
   Source Branch: ${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME}
   Target Branch: ${CI_MERGE_REQUEST_TARGET_BRANCH_NAME}

2. Get changed files: run git diff --name-only ${BASE_SHA}

3. Classify each file by type:
   **/agents/**/*.agent.md       -> agent
   **/skills/**/SKILL.md         -> skill
   **/prompts/**/*.prompt.md     -> prompt
   **/instructions/**/*.md       -> instruction
   .github/workflows/**/*.yml    -> workflow
   other                         -> other

4. Detect change type per file: added, modified, or deleted

5. Set risk_hints[] by scanning the diff:
   exec-tool             if tools contains runCommands
   unconstrained-network if allowedNetworkDomains is * or missing
   unconstrained-files   if allowedFilePaths is ** or missing
   shell-pipe            if diff contains curl|wget|bash with pipes
   eval-usage            if diff contains eval()
   agent-removed         if any .agent.md deleted

6. scope = agent-change if any agent/skill/prompt/instruction changed, else non-agent

7. Write to ${STATION_OUT}/work_order.json:
{
  \"station\": \"A0\", \"pr_number\": <n>, \"pr_title\": \"...\",
  \"author\": \"...\", \"base_branch\": \"...\", \"head_branch\": \"...\",
  \"created_at\": \"<ISO8601>\", \"scope\": \"agent-change|non-agent\",
  \"changed_files\": [{\"path\":\"...\",\"type\":\"...\",\"change\":\"...\"}],
  \"risk_hints\": [], \"diff_summary\": \"...\"
}

CONSTRAINTS: run real git commands; write valid JSON only; no markdown
" --allow-tool 'shell(git)' --allow-tool 'write'