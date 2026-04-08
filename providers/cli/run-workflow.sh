#!/usr/bin/env bash
# ==============================================================================
# Workflow Runner — Execute workflow definitions from .apm/workflows/
#
# Usage:
#   ./run-workflow.sh <workflow> <feature> [options]
#
# Options:
#   --station <id>       Run a single station only
#   --resume             Resume from last successful station
#   --skip-gate <id>     Force past a blocker gate for a station
#   --dry-run            Parse workflow and list stations without executing
#   --verbose            Enable detailed logging
#   -h, --help           Show this help message
#
# Examples:
#   ./run-workflow.sh quality-validation my-feature
#   ./run-workflow.sh feature-implementation user-auth --dry-run
#   ./run-workflow.sh modernization spring-upgrade --resume
#   ./run-workflow.sh pr-validation my-branch --station a1-policy-validation
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"
# shellcheck source=lib/workflow-parser.sh
source "${SCRIPT_DIR}/lib/workflow-parser.sh"
# shellcheck source=lib/station-runner.sh
source "${SCRIPT_DIR}/lib/station-runner.sh"
# shellcheck source=lib/gate-checker.sh
source "${SCRIPT_DIR}/lib/gate-checker.sh"
# shellcheck source=lib/state-manager.sh
source "${SCRIPT_DIR}/lib/state-manager.sh"

# --- Defaults ---
WORKFLOW=""
FEATURE=""
SINGLE_STATION=""
RESUME=false
SKIP_GATE=""
DRY_RUN=false
VERBOSE=false

# --- Parse arguments ---
usage() {
    head -25 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --station)    SINGLE_STATION="$2"; shift 2 ;;
        --resume)     RESUME=true; shift ;;
        --skip-gate)  SKIP_GATE="$2"; shift 2 ;;
        --dry-run)    DRY_RUN=true; shift ;;
        --verbose)    VERBOSE=true; shift ;;
        -h|--help)    usage ;;
        -*)           log_error "Unknown option: $1"; usage ;;
        *)
            if [[ -z "$WORKFLOW" ]]; then
                WORKFLOW="$1"
            elif [[ -z "$FEATURE" ]]; then
                FEATURE="$1"
            else
                log_error "Unexpected argument: $1"; usage
            fi
            shift ;;
    esac
done

# --- Validate arguments ---
if [[ -z "$WORKFLOW" || -z "$FEATURE" ]]; then
    log_error "Usage: run-workflow.sh <workflow> <feature> [options]"
    exit 1
fi

WORKFLOW_FILE="${REPO_ROOT}/.apm/workflows/${WORKFLOW}.yml"
if [[ ! -f "$WORKFLOW_FILE" ]]; then
    log_error "Workflow not found: ${WORKFLOW_FILE}"
    log_info "Available workflows:"
    ls "${REPO_ROOT}/.apm/workflows/"*.yml 2>/dev/null | xargs -I{} basename {} .yml | sed 's/^/  /'
    exit 1
fi

OUTPUT_DIR="${REPO_ROOT}/specs/features/${FEATURE}"
mkdir -p "$OUTPUT_DIR"

# --- Generate trace correlation ID ---
export TRACE_ID
TRACE_ID=$(generate_trace_id)
TRACE_FILE="${OUTPUT_DIR}/audit-trace.jsonl"

# --- Load workflow ---
log_header "Workflow: ${WORKFLOW}"
log_info "Feature: ${FEATURE}"
log_info "Output: ${OUTPUT_DIR}"
log_info "Trace ID: ${TRACE_ID}"

STATIONS=()
parse_workflow "$WORKFLOW_FILE" STATIONS

if [[ ${#STATIONS[@]} -eq 0 ]]; then
    log_error "No stations found in workflow"
    exit 1
fi

log_info "Stations: ${#STATIONS[@]}"

# --- Dry run ---
if [[ "$DRY_RUN" == true ]]; then
    log_header "Dry run — station list"
    for station in "${STATIONS[@]}"; do
        echo "  $(get_station_field "$station" "id") — $(get_station_field "$station" "name")"
    done
    exit 0
fi

# --- Initialize state ---
STATE_FILE="${OUTPUT_DIR}/workflow-state.md"
init_state "$STATE_FILE" "$WORKFLOW" "$FEATURE" STATIONS

# --- Determine starting station ---
START_INDEX=0
if [[ "$RESUME" == true ]]; then
    START_INDEX=$(get_resume_index "$STATE_FILE" STATIONS)
    log_info "Resuming from station index: ${START_INDEX}"
fi

# --- Execute stations ---
OVERALL_RESULT="passed"

for ((i=START_INDEX; i<${#STATIONS[@]}; i++)); do
    station="${STATIONS[$i]}"
    station_id=$(get_station_field "$station" "id")
    station_name=$(get_station_field "$station" "name")

    # Single station mode
    if [[ -n "$SINGLE_STATION" && "$station_id" != "$SINGLE_STATION" ]]; then
        continue
    fi

    log_header "Station ${i+1}/${#STATIONS[@]}: ${station_name}"

    # Update state: running
    update_station_state "$STATE_FILE" "$station_id" "running" "" ""

    # --- Pre-hooks ---
    local hook_blocked=false
    local station_skills
    station_skills=$(get_station_field "$station" "skills")
    local station_agent
    station_agent=$(get_station_field "$station" "agent")
    local station_inputs
    station_inputs=$(get_station_field "$station" "inputs")

    if check_command python3; then
        local hook_input_file=""
        if [[ -n "$station_inputs" ]]; then
            IFS=',' read -ra _inp <<< "$station_inputs"
            hook_input_file="${OUTPUT_DIR}/${_inp[0]}"
        fi
        local pre_args=(
            python3 -m hooks --phase pre
            --trace-id "$TRACE_ID"
            --workflow "$WORKFLOW"
            --station "$station_id"
            --agent "$station_agent"
            --skill "$station_skills"
            --provider cli
            --trace-file "$TRACE_FILE"
        )
        if [[ -n "$hook_input_file" && -f "$hook_input_file" ]]; then
            pre_args+=(--input "$hook_input_file")
        fi

        pushd "${REPO_ROOT}/.apm/scripts" >/dev/null 2>&1 || true
        if ! "${pre_args[@]}" 2>/dev/null; then
            log_warn "Pre-hook flagged station ${station_id}"
            # Non-zero from pre-hook means blocked
            hook_blocked=true
        fi
        popd >/dev/null 2>&1 || true
    fi

    if [[ "$hook_blocked" == true ]]; then
        OVERALL_RESULT="failed"
        update_station_state "$STATE_FILE" "$station_id" "failed" "$(now_utc)" "blocked-by-hook"
        log_error "Station blocked by pre-hook: ${station_name}"
        break
    fi

    # Run station
    if run_station "$station" "$OUTPUT_DIR" "$REPO_ROOT" "$VERBOSE"; then
        log_success "Station completed: ${station_name}"

        # --- Post-hooks ---
        if check_command python3; then
            local station_outputs
            station_outputs=$(get_station_field "$station" "outputs")
            local hook_output_file=""
            if [[ -n "$station_outputs" ]]; then
                IFS=',' read -ra _outp <<< "$station_outputs"
                hook_output_file="${OUTPUT_DIR}/${_outp[0]}"
            fi
            local post_args=(
                python3 -m hooks --phase post
                --trace-id "$TRACE_ID"
                --workflow "$WORKFLOW"
                --station "$station_id"
                --agent "$station_agent"
                --skill "$station_skills"
                --provider cli
                --trace-file "$TRACE_FILE"
            )
            if [[ -n "$hook_output_file" && -f "$hook_output_file" ]]; then
                post_args+=(--output "$hook_output_file")
            fi

            pushd "${REPO_ROOT}/.apm/scripts" >/dev/null 2>&1 || true
            "${post_args[@]}" 2>/dev/null || log_warn "Post-hook warning for ${station_id}"
            popd >/dev/null 2>&1 || true
        fi

        # Check gate
        gate_result="pass"
        if ! check_gate "$station" "$OUTPUT_DIR" "$SKIP_GATE"; then
            gate_severity=$(get_station_field "$station" "gate_severity")
            if [[ "$gate_severity" == "blocker" ]]; then
                gate_result="fail"
                OVERALL_RESULT="failed"
                update_station_state "$STATE_FILE" "$station_id" "failed" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$gate_result"
                log_error "Blocker gate failed for: ${station_name}"
                log_error "Use --skip-gate ${station_id} to force past this gate"
                break
            else
                gate_result="warning"
                log_warn "Warning gate for: ${station_name}"
            fi
        fi

        update_station_state "$STATE_FILE" "$station_id" "passed" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$gate_result"
    else
        OVERALL_RESULT="failed"
        update_station_state "$STATE_FILE" "$station_id" "failed" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "fail"
        log_error "Station failed: ${station_name}"
        break
    fi

    # Single station mode — stop after running the one we wanted
    if [[ -n "$SINGLE_STATION" ]]; then
        break
    fi
done

# --- Final report ---
log_header "Workflow complete: ${OVERALL_RESULT}"
if [[ "$OVERALL_RESULT" == "passed" ]]; then
    log_success "All stations passed"
else
    log_error "Workflow failed — check ${STATE_FILE} for details"
    exit 1
fi
