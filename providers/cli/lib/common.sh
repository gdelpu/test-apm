#!/usr/bin/env bash
# Common utilities for the workflow CLI runner

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# --- Logging ---
log_info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[PASS]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[FAIL]${NC} $*"; }
log_header()  { echo -e "\n${BOLD}=== $* ===${NC}\n"; }

# --- Prerequisite checks ---
check_command() {
    local cmd="$1"
    if command -v "$cmd" &>/dev/null; then
        return 0
    else
        return 1
    fi
}

require_command() {
    local cmd="$1"
    local install_hint="${2:-}"
    if ! check_command "$cmd"; then
        log_error "Required command not found: ${cmd}"
        if [[ -n "$install_hint" ]]; then
            log_info "Install with: ${install_hint}"
        fi
        return 1
    fi
}

# --- File utilities ---
ensure_dir() {
    local dir="$1"
    mkdir -p "$dir"
}

file_exists() {
    [[ -f "$1" ]]
}

# --- Timestamp ---
now_utc() {
    date -u +%Y-%m-%dT%H:%M:%SZ
}

# --- Field extraction from pipe-delimited station strings ---
# Station format: id|name|agent|skills|inputs|outputs|optional|gate_criteria|gate_severity|gate_reviewer
get_station_field() {
    local station="$1"
    local field_name="$2"
    local index

    case "$field_name" in
        id)             index=1 ;;
        name)           index=2 ;;
        agent)          index=3 ;;
        skills)         index=4 ;;
        inputs)         index=5 ;;
        outputs)        index=6 ;;
        optional)       index=7 ;;
        gate_criteria)  index=8 ;;
        gate_severity)  index=9 ;;
        gate_reviewer)  index=10 ;;
        *) echo ""; return 1 ;;
    esac

    echo "$station" | cut -d'|' -f"$index"
}
