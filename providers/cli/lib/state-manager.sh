#!/usr/bin/env bash
# State manager — DEPRECATED: use Python state tracker instead.
#
# This file is kept for backward compatibility during migration.
# New code should call the canonical Python tracker:
#
#   cd .apm/hooks && python -m engine --state init   ...
#   cd .apm/hooks && python -m engine --state update ...
#   cd .apm/hooks && python -m engine --state query  ...
#   cd .apm/hooks && python -m engine --state resume ...
#
# See .apm/hooks/engine/state_tracker.py for the canonical implementation.

# Initialize workflow state file.
# Usage: init_state <state_file> <workflow> <feature> <stations_array_name>
init_state() {
    local state_file="$1"
    local workflow="$2"
    local feature="$3"
    local -n _st=$4

    # Don't overwrite if resuming
    if [[ -f "$state_file" ]]; then
        return 0
    fi

    {
        echo "# Workflow State: ${workflow}"
        echo ""
        echo "**Feature**: ${feature}"
        echo "**Started**: $(now_utc)"
        echo "**Status**: in-progress"
        echo "**Trace ID**: ${TRACE_ID:-unset}"
        echo ""
        echo "| Station | Status | Started | Completed | Gate |"
        echo "|---------|--------|---------|-----------|------|"
        for station in "${_st[@]}"; do
            local sid
            sid=$(get_station_field "$station" "id")
            echo "| ${sid} | pending | — | — | — |"
        done
    } > "$state_file"
}

# Update a station's state in the state file.
# Usage: update_station_state <state_file> <station_id> <status> <completed> <gate>
update_station_state() {
    local state_file="$1"
    local station_id="$2"
    local status="$3"
    local completed="${4:-—}"
    local gate="${5:-—}"
    local started
    started=$(now_utc)

    if [[ ! -f "$state_file" ]]; then
        return 1
    fi

    # Replace the line for this station
    local pattern="| ${station_id} |"
    local replacement="| ${station_id} | ${status} | ${started} | ${completed} | ${gate} |"

    if grep -q "^${pattern}" "$state_file" 2>/dev/null; then
        sed -i "s|^| ${station_id} |.*|${replacement}|" "$state_file" 2>/dev/null || \
        sed -i '' "s|^| ${station_id} |.*|${replacement}|" "$state_file" 2>/dev/null || true
    fi
}

# Get the index to resume from (first non-passed station).
# Usage: get_resume_index <state_file> <stations_array_name>
get_resume_index() {
    local state_file="$1"
    local -n _resume_st=$2
    local index=0

    for station in "${_resume_st[@]}"; do
        local sid
        sid=$(get_station_field "$station" "id")
        if grep -q "| ${sid} | passed |" "$state_file" 2>/dev/null; then
            ((index++))
        else
            break
        fi
    done

    echo "$index"
}
