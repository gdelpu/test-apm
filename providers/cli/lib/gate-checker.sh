#!/usr/bin/env bash
# Gate checker — evaluates quality gate criteria for a station

# Check the quality gate for a station.
# Returns 0 if gate passes, 1 if gate fails.
# Usage: check_gate <station_string> <output_dir> <skip_gate_id>
check_gate() {
    local station="$1"
    local output_dir="$2"
    local skip_gate_id="$3"

    local station_id
    station_id=$(get_station_field "$station" "id")
    local gate_criteria
    gate_criteria=$(get_station_field "$station" "gate_criteria")
    local gate_severity
    gate_severity=$(get_station_field "$station" "gate_severity")
    local optional
    optional=$(get_station_field "$station" "optional")

    # No gate defined — pass
    if [[ -z "$gate_criteria" ]]; then
        return 0
    fi

    # Skip gate if explicitly requested
    if [[ "$station_id" == "$skip_gate_id" ]]; then
        log_warn "Gate skipped (--skip-gate): ${station_id}"
        return 0
    fi

    # Optional station with no output — skip
    if [[ "$optional" == "true" ]]; then
        local outputs
        outputs=$(get_station_field "$station" "outputs")
        IFS=',' read -ra output_files <<< "$outputs"
        local has_output=false
        for ofile in "${output_files[@]}"; do
            if [[ -f "${output_dir}/${ofile}" ]]; then
                has_output=true
                break
            fi
        done
        if [[ "$has_output" == false ]]; then
            log_info "Optional station skipped: ${station_id}"
            return 0
        fi
    fi

    # Check each output file for failure indicators
    local outputs
    outputs=$(get_station_field "$station" "outputs")
    IFS=',' read -ra output_files <<< "$outputs"

    for ofile in "${output_files[@]}"; do
        local report="${output_dir}/${ofile}"
        if [[ -f "$report" ]]; then
            # Check for explicit failure in JSON reports
            if grep -qi '"decision"[[:space:]]*:[[:space:]]*"fail\|"status"[[:space:]]*:[[:space:]]*"fail' "$report" 2>/dev/null; then
                log_error "Gate check failed — report indicates failure: ${ofile}"
                return 1
            fi
            # Check for explicit failure in Markdown reports
            if grep -qi "Status.*failed\|Status.*fail\|Overall.*failed" "$report" 2>/dev/null; then
                log_error "Gate check failed — report indicates failure: ${ofile}"
                return 1
            fi
        else
            log_warn "Gate check — output not found: ${ofile}"
            # Missing output for non-optional station is a failure
            if [[ "$optional" != "true" ]]; then
                return 1
            fi
        fi
    done

    return 0
}
