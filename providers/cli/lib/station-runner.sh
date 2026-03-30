#!/usr/bin/env bash
# Station runner — executes a single workflow station by invoking the appropriate adapter
#
# For SDLC workflows (spec, plan, implement, etc.), stations require agent-based
# execution via Copilot or Claude. The CLI runner handles quality-validation and
# PR-validation stations that have deterministic tool adapters.
#
# For PR validation, delegates to ci-gates/scripts/run_stations.sh.

# Run a station's tool adapter.
# Usage: run_station <station_string> <output_dir> <repo_root> <verbose>
run_station() {
    local station="$1"
    local output_dir="$2"
    local repo_root="$3"
    local verbose="${4:-false}"

    local station_id
    station_id=$(get_station_field "$station" "id")
    local skills
    skills=$(get_station_field "$station" "skills")

    # Check inputs exist
    local inputs
    inputs=$(get_station_field "$station" "inputs")
    if [[ -n "$inputs" ]]; then
        IFS=',' read -ra input_files <<< "$inputs"
        for input_file in "${input_files[@]}"; do
            local resolved="${output_dir}/${input_file}"
            if [[ ! -f "$resolved" ]]; then
                log_warn "Input not found: ${resolved} (station: ${station_id})"
            fi
        done
    fi

    # Dispatch to the appropriate adapter based on skills
    local result=0

    IFS=',' read -ra skill_list <<< "$skills"
    for skill in "${skill_list[@]}"; do
        case "$skill" in
            # --- Quality validation adapters ---
            lint-analysis)
                run_lint_adapters "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;
            static-analysis)
                run_static_analysis "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;
            security-scan)
                if [[ "$station_id" == "security-dast" ]]; then
                    run_dast_scan "$output_dir" "$repo_root" "$verbose"
                else
                    run_sast_scan "$output_dir" "$repo_root" "$verbose"
                fi
                result=$?
                ;;
            dependency-audit)
                run_dependency_audit "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;
            coverage-assessment)
                run_coverage "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;
            quality-report)
                run_quality_report "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;

            # --- PR validation adapters ---
            pr-intake|policy-validation|security-static|prompt-injection-check|red-team-simulation|sandbox-execution|policy-gate|gitlab-update)
                run_pr_station "$station_id" "$output_dir" "$repo_root" "$verbose"
                result=$?
                ;;

            # --- Nested workflow ---
            workflow-engine)
                log_info "Nested workflow execution — use agent-based runner for this"
                result=0
                ;;

            # --- Agent-based skills (spec, plan, implement, etc.) ---
            *)
                log_info "Skill '${skill}' requires agent-based execution (Copilot/Claude)"
                result=0
                ;;
        esac
    done

    return $result
}

# --- Quality validation adapters ---

run_lint_adapters() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${repo_root}/package.json" ]] && [[ -f "${adapter_dir}/eslint.sh" ]]; then
        source "${adapter_dir}/eslint.sh"
        run_eslint "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${repo_root}/pyproject.toml" || -f "${repo_root}/setup.py" ]] && [[ -f "${adapter_dir}/pylint.sh" ]]; then
        source "${adapter_dir}/pylint.sh"
        run_pylint "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${repo_root}/Cargo.toml" ]] && [[ -f "${adapter_dir}/clippy.sh" ]]; then
        source "${adapter_dir}/clippy.sh"
        run_clippy "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No recognized project type for lint analysis"
        echo "# Lint Report" > "${output_dir}/lint-report.md"
        echo "" >> "${output_dir}/lint-report.md"
        echo "- **Status**: skipped — no recognized project type" >> "${output_dir}/lint-report.md"
    fi
}

run_static_analysis() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${adapter_dir}/sonarqube.sh" ]]; then
        source "${adapter_dir}/sonarqube.sh"
        run_sonar "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No static analysis adapter available"
    fi
}

run_sast_scan() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${adapter_dir}/checkmarx.sh" ]]; then
        source "${adapter_dir}/checkmarx.sh"
        run_checkmarx "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No SAST adapter available"
    fi
}

run_dast_scan() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${adapter_dir}/owasp-zap.sh" ]]; then
        source "${adapter_dir}/owasp-zap.sh"
        run_zap "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No DAST adapter available"
    fi
}

run_dependency_audit() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${adapter_dir}/trivy.sh" ]]; then
        source "${adapter_dir}/trivy.sh"
        run_trivy "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${adapter_dir}/snyk.sh" ]]; then
        source "${adapter_dir}/snyk.sh"
        run_snyk "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${adapter_dir}/owasp-depcheck.sh" ]]; then
        source "${adapter_dir}/owasp-depcheck.sh"
        run_depcheck "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No dependency audit adapter available"
    fi
}

run_coverage() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"
    local adapter_dir="${SCRIPT_DIR}/adapters"

    if [[ -f "${repo_root}/package.json" ]] && [[ -f "${adapter_dir}/istanbul.sh" ]]; then
        source "${adapter_dir}/istanbul.sh"
        run_istanbul "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${repo_root}/pyproject.toml" || -f "${repo_root}/setup.py" ]] && [[ -f "${adapter_dir}/coveragepy.sh" ]]; then
        source "${adapter_dir}/coveragepy.sh"
        run_coveragepy "$output_dir" "$repo_root" "$verbose"
    elif [[ -f "${repo_root}/pom.xml" ]] && [[ -f "${adapter_dir}/jacoco.sh" ]]; then
        source "${adapter_dir}/jacoco.sh"
        run_jacoco "$output_dir" "$repo_root" "$verbose"
    else
        log_warn "No coverage adapter available"
    fi
}

run_quality_report() {
    local output_dir="$1"
    local repo_root="$2"
    local verbose="$3"

    log_info "Aggregating quality report from station outputs"
    {
        echo "# Quality Validation Report"
        echo ""
        echo "**Generated**: $(now_utc)"
        echo ""
        for report in "${output_dir}"/*-report.md; do
            if [[ -f "$report" ]]; then
                echo "---"
                echo ""
                cat "$report"
                echo ""
            fi
        done
    } > "${output_dir}/quality-summary.md"
}

# --- PR validation adapter ---
# Delegates to ci-gates/scripts/run_stations.sh for A0-A7 stations
run_pr_station() {
    local station_id="$1"
    local output_dir="$2"
    local repo_root="$3"
    local verbose="$4"

    local station_scripts="${repo_root}/ci-gates/scripts"
    if [[ -f "${station_scripts}/run_stations.sh" ]]; then
        log_info "Delegating to ci-gates runner for: ${station_id}"
        bash "${station_scripts}/run_stations.sh" "$station_id" "$output_dir"
    else
        log_warn "ci-gates/scripts/run_stations.sh not found — skipping PR station"
    fi
}
