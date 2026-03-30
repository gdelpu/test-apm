#!/usr/bin/env bash
# =============================================================================
# run_stations.sh — Sequential AI Station Orchestrator
# =============================================================================
#
# Dynamically discovers all station prompt/agent files in
# ci-gates/stations/, sorts them by prefix (a0, a1, …), and
# executes each via GitHub Copilot CLI sequentially.
#
# The orchestrator is invoked as a single CI job AFTER the deterministic
# Python validators pass. It keeps the .gitlab-ci.yml stable — adding or
# removing a station file is all that's needed; no CI YAML changes required.
#
# Usage:
#   bash ci-gates/scripts/run_stations.sh
#
# Required env vars (set by .gitlab-ci.yml or .env):
#   CI_PROJECT_DIR                — repo root
#   CI_MERGE_REQUEST_IID          — MR internal ID
#   CI_MERGE_REQUEST_TARGET_BRANCH_NAME — target branch
#   CI_COMMIT_SHA                 — head commit
#   STATION_OUT                   — output directory (default: station_out)
#   COPILOT_MAX_DIFF_LINES        — max diff lines to feed (default: 2000)
#   ENABLE_COPILOT_CLI            — set to "true" to actually invoke Copilot CLI
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
PROJECT_DIR="${CI_PROJECT_DIR:-.}"
STATION_DIR="${PROJECT_DIR}/ci-gates/stations"
STATION_OUT="${STATION_OUT:-station_out}"
EXTRACT_JSON="${PROJECT_DIR}/ci-gates/scripts/extract_json.py"
MAX_DIFF="${COPILOT_MAX_DIFF_LINES:-500}"
TIMEOUT_SECS="${STATION_TIMEOUT:-900}"
ENABLE="${ENABLE_COPILOT_CLI:-false}"
# Per-station model overrides (comma-separated prefix=model pairs, no spaces).
# Defaults assign Haiku to mechanical stations and Sonnet to reasoning-heavy ones.
# Override all at once with COPILOT_MODEL_DEFAULT, or per-station via environment.
# Example: COPILOT_MODEL_a1=claude-haiku-4.5 to downgrade a single station.
COPILOT_MODEL_DEFAULT="${COPILOT_MODEL_DEFAULT:-claude-haiku-4.5}"
# Seconds to sleep between stations to stay within per-minute rate limits.
# Sonnet uses ~5-10x more premium requests, so the default is higher.
INTER_STATION_SLEEP="${COPILOT_INTER_STATION_SLEEP:-30}"
# Seconds to wait before retrying after a rate-limit response (Copilot says ~1 min).
RATE_LIMIT_WAIT="${COPILOT_RATE_LIMIT_WAIT:-70}"
# Maximum number of retry attempts per station on rate-limit.
RATE_LIMIT_RETRIES="${COPILOT_RATE_LIMIT_RETRIES:-3}"

mkdir -p "${STATION_OUT}"

# ---------------------------------------------------------------------------
# Clean stale output files from prior runs
# ---------------------------------------------------------------------------
rm -f "${STATION_OUT}"/*_raw.json "${STATION_OUT}"/*_result.json

# ---------------------------------------------------------------------------
# Discover & sort station files (a0-… a1-… etc.)
# ---------------------------------------------------------------------------
mapfile -t STATIONS < <(
  find "${STATION_DIR}" -maxdepth 1 \
       \( -name '*.prompt.md' -o -name '*.agent.md' \) \
       -printf '%f\n' |
  sort -t'-' -k1,1
)

if [ ${#STATIONS[@]} -eq 0 ]; then
  echo "ERROR: No station files found in ${STATION_DIR}" >&2
  exit 1
fi

echo "========================================"
echo " Station Orchestrator"
echo " Discovered ${#STATIONS[@]} station(s):"
for s in "${STATIONS[@]}"; do echo "   • $s"; done
echo "========================================"

# ---------------------------------------------------------------------------
# Prepare shared context (computed once, reused by multiple stations)
# ---------------------------------------------------------------------------
echo "--- Preparing shared MR context ---"
DIFF_FILE="${STATION_OUT}/diff.patch"
CHANGED_FILE="${STATION_OUT}/changed_files.txt"

git fetch origin "${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main}" 2>/dev/null || true

git diff --name-status "origin/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main}" \
    "${CI_COMMIT_SHA:-HEAD}" > "${CHANGED_FILE}" 2>/dev/null || true

git diff "origin/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main}" \
    "${CI_COMMIT_SHA:-HEAD}" > "${DIFF_FILE}" 2>/dev/null || true

# ---------------------------------------------------------------------------
# invoke_station — run a single station through Copilot CLI
# ---------------------------------------------------------------------------
invoke_station() {
  local file="$1"
  local station_path="${STATION_DIR}/${file}"
  local prefix
  prefix=$(echo "${file}" | grep -oP '^a\d+' || echo "unknown")

  echo ""
  echo "════════════════════════════════════════"
  echo " Running station: ${file}  (${prefix})"
  echo "════════════════════════════════════════"

  if [ "${ENABLE}" != "true" ]; then
    echo "SKIP: ENABLE_COPILOT_CLI != true — station ${file} not executed."
    return 0
  fi

  # --- A7-specific pre-flight: skip when GitLab API is unavailable or gate approved ---
  if [ "${prefix}" = "a7" ]; then
    if [ -z "${GITLAB_TOKEN:-}" ]; then
      echo "  SKIP: GITLAB_TOKEN not set — A7 cannot call GitLab API."
      echo '{"station":"A7","status":"skipped","reason":"GITLAB_TOKEN not set"}' > "${STATION_OUT}/${prefix}_result.json"
      return 0
    fi

    local gate_decision
    gate_decision=$(jq -r '.decision // ""' "${STATION_OUT}/a6_result.json" 2>/dev/null || echo "")
    if [ "${gate_decision}" = "APPROVE" ]; then
      echo "  SKIP: Gate decision is APPROVE — no MR update needed."
      echo '{"station":"A7","status":"skipped","reason":"gate_approved"}' > "${STATION_OUT}/${prefix}_result.json"
      return 0
    fi
  fi

  local PROMPT
  PROMPT=$(cat "${station_path}")

  local raw_out="${STATION_OUT}/${prefix}_raw.json"

  # Per-station tool sets — minimal privilege:
  #   A0–A6: view (read workspace files/reports) + create (write JSON output)
  #   A7:    view (read reports) + fetch (GitLab REST API calls — no local writes)
  local tools='view,create'
  if [ "${prefix}" = "a7" ]; then
    tools='view,fetch'
  fi

  # Per-station model selection.
  # Haiku: mechanical stations — classification, pattern-matching, REST calls.
  # Sonnet: reasoning-heavy stations — multi-rule validation, adversarial analysis,
  #         cross-report aggregation. Sonnet completes these in far fewer tool calls.
  # Each station can still be overridden via COPILOT_MODEL_<prefix> env var.
  local model_var="COPILOT_MODEL_${prefix}"
  local model
  model="${!model_var:-}"
  if [ -z "${model}" ]; then
    case "${prefix}" in
      a0|a2|a7) model='claude-haiku-4.5' ;;
      a1|a3|a4|a5|a6) model='claude-sonnet-4.6' ;;
      *) model="${COPILOT_MODEL_DEFAULT}" ;;
    esac
  fi
  echo "  ℹ Model: ${model}"

  # Invoke Copilot CLI — with rate-limit detection and retry.
  # extract_json.py handles output from both assistant text and create-tool calls.
  local copilot_exit=0
  local attempt=0
  while true; do
    attempt=$(( attempt + 1 ))
    timeout "${TIMEOUT_SECS}" copilot -s --output-format json \
      --model "${model}" \
      --available-tools="${tools}" \
      -p "
${PROMPT}

MR_IID: ${CI_MERGE_REQUEST_IID:-0}
CHANGED_FILES:
$(cat "${CHANGED_FILE}")

DIFF (first ${MAX_DIFF} lines):
$(head -n "${MAX_DIFF}" "${DIFF_FILE}")

OUTPUT FORMAT: Respond with ONLY a raw JSON object, no markdown fences, no prose.
" > "${raw_out}" || copilot_exit=$?

    # Detect rate-limit response in the raw output.
    if grep -qi "rate limit" "${raw_out}" 2>/dev/null; then
      # The model may have produced valid JSON before the rate limit hit.
      # Try extraction first — if it succeeds, skip the retry entirely.
      if python3 "${EXTRACT_JSON}" < "${raw_out}" > "${STATION_OUT}/${prefix}_result.json" 2>/dev/null; then
        echo "  ⚠ Rate limit hit, but valid JSON was produced before the limit — using partial output."
        break
      fi

      if [ "${attempt}" -ge "${RATE_LIMIT_RETRIES}" ]; then
        echo "  ✖ ERROR: Rate limit hit ${attempt} times for station ${file} — giving up."
        break
      fi
      echo "  ⏳ Rate limit hit (attempt ${attempt}/${RATE_LIMIT_RETRIES}) — waiting ${RATE_LIMIT_WAIT}s before retry..."
      sleep "${RATE_LIMIT_WAIT}"
      continue
    fi
    break
  done

  if [ "${copilot_exit}" -eq 124 ]; then
    echo "  ⚠ WARNING: Station ${file} timed out after ${TIMEOUT_SECS}s — attempting partial extraction"
  elif [ "${copilot_exit}" -ne 0 ]; then
    echo "  ⚠ WARNING: Copilot CLI exited with code ${copilot_exit} for station ${file}"
  fi

  # Extract clean JSON from the Copilot JSONL envelope
  local clean_out="${STATION_OUT}/${prefix}_result.json"
  if ! python3 "${EXTRACT_JSON}" < "${raw_out}" > "${clean_out}" 2>/dev/null; then
    echo "  ⚠ WARNING: Could not extract JSON from station ${file} — skipping gate check"
    echo '{"station":"'"${prefix}"'","status":"error","error":"extraction_failed"}' > "${clean_out}"
  fi

  echo "  → Output: ${clean_out}"
  cat "${clean_out}"

  # Gate check — if the station result has status:"fail", abort the pipeline
  local status
  status=$(jq -r '.status // "pass"' "${clean_out}" 2>/dev/null || echo "pass")
  if [ "${status}" = "fail" ]; then
    echo ""
    echo "❌ GATE FAILED at station ${file} — status: fail"
    cat "${clean_out}"
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# Run each station sequentially with an inter-station throttle
# ---------------------------------------------------------------------------
first_station=true
for station_file in "${STATIONS[@]}"; do
  if [ "${first_station}" = "true" ]; then
    first_station=false
  elif [ "${ENABLE}" = "true" ] && [ "${INTER_STATION_SLEEP}" -gt 0 ] 2>/dev/null; then
    echo "  ⏱ Throttle: sleeping ${INTER_STATION_SLEEP}s between stations..."
    sleep "${INTER_STATION_SLEEP}"
  fi
  invoke_station "${station_file}"
done

echo ""
echo "========================================"
echo " All ${#STATIONS[@]} stations completed successfully"
echo "========================================"