#!/usr/bin/env bash
# Workflow YAML parser — extracts stations from a workflow definition
#
# Uses grep/sed/awk for YAML parsing (no external YAML library dependency).
# This is a simplified parser that handles the workflow schema structure.

# Parse a workflow YAML file and populate a station array.
# Each station is stored as a pipe-delimited string:
#   id|name|agent|skills|inputs|outputs|optional|gate_criteria|gate_severity|gate_reviewer
#
# Usage: parse_workflow <yaml_file> <array_name>
parse_workflow() {
    local yaml_file="$1"
    local -n _stations=$2

    _stations=()

    local in_stations=false
    local current_station=""
    local field=""
    local id="" name="" agent="" skills="" inputs="" outputs="" optional="false"
    local gate_criteria="" gate_severity="" gate_reviewer=""

    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// /}" ]] && continue

        # Detect stations section
        if [[ "$line" =~ ^stations: ]]; then
            in_stations=true
            continue
        fi

        # Detect config section (end of stations)
        if [[ "$line" =~ ^config: ]]; then
            in_stations=false
            # Save last station
            if [[ -n "$id" ]]; then
                _stations+=("${id}|${name}|${agent}|${skills}|${inputs}|${outputs}|${optional}|${gate_criteria}|${gate_severity}|${gate_reviewer}")
            fi
            continue
        fi

        if [[ "$in_stations" != true ]]; then
            continue
        fi

        # New station (starts with "  - id:")
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*id:[[:space:]]*(.*) ]]; then
            # Save previous station
            if [[ -n "$id" ]]; then
                _stations+=("${id}|${name}|${agent}|${skills}|${inputs}|${outputs}|${optional}|${gate_criteria}|${gate_severity}|${gate_reviewer}")
            fi
            # Reset
            id="${BASH_REMATCH[1]}"
            name="" agent="" skills="" inputs="" outputs="" optional="false"
            gate_criteria="" gate_severity="" gate_reviewer=""
            field=""
            continue
        fi

        # Station fields
        if [[ "$line" =~ ^[[:space:]]+name:[[:space:]]*(.*) ]]; then
            name="${BASH_REMATCH[1]}"
            field=""
        elif [[ "$line" =~ ^[[:space:]]+agent:[[:space:]]*(.*) ]]; then
            agent="${BASH_REMATCH[1]}"
            field=""
        elif [[ "$line" =~ ^[[:space:]]+optional:[[:space:]]*(.*) ]]; then
            optional="${BASH_REMATCH[1]}"
            field=""
        elif [[ "$line" =~ ^[[:space:]]+skills: ]]; then
            field="skills"
        elif [[ "$line" =~ ^[[:space:]]+inputs: ]]; then
            field="inputs"
        elif [[ "$line" =~ ^[[:space:]]+outputs: ]]; then
            field="outputs"
        elif [[ "$line" =~ ^[[:space:]]+gate: ]]; then
            field="gate"
        elif [[ "$line" =~ ^[[:space:]]+criteria: ]]; then
            field="criteria"
        elif [[ "$line" =~ ^[[:space:]]+severity:[[:space:]]*(.*) ]]; then
            gate_severity="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+reviewer:[[:space:]]*(.*) ]]; then
            gate_reviewer="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+-[[:space:]]+(.*) ]]; then
            local value="${BASH_REMATCH[1]}"
            # Remove quotes
            value="${value%\"}"
            value="${value#\"}"
            case "$field" in
                skills)   skills="${skills:+${skills},}${value}" ;;
                inputs)   inputs="${inputs:+${inputs},}${value}" ;;
                outputs)  outputs="${outputs:+${outputs},}${value}" ;;
                criteria) gate_criteria="${gate_criteria:+${gate_criteria};}${value}" ;;
            esac
        fi
    done < "$yaml_file"

    # Save final station if file doesn't end with config:
    if [[ -n "$id" ]]; then
        _stations+=("${id}|${name}|${agent}|${skills}|${inputs}|${outputs}|${optional}|${gate_criteria}|${gate_severity}|${gate_reviewer}")
    fi
}
