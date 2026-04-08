#!/usr/bin/env bash
# ==============================================================================
# APM Bundle Builder
#
# Builds APM distribution archives for all configured targets.
# Reads apm.yml and bundles the canonical layer + target-specific provider
# files into .tar.gz archives without requiring an external apm CLI tool.
#
# Usage:
#   ./scripts/apm-build.sh [options]
#
# Options:
#   -o, --output-dir <dir>   Output directory (default: ./dist)
#   -t, --targets <list>     Comma-separated targets (default: copilot,claude,cli,all)
#   --checksum               Generate SHA-256 checksums (default: true)
#   --no-checksum            Disable SHA-256 checksums
#   -h, --help               Show this help
#
# Targets:
#   copilot   GitHub Copilot bundle  (canonical + providers/github-copilot + .github)
#   claude    Claude Code bundle     (canonical + providers/claude-code)
#   cli       CLI runner bundle      (canonical + providers/cli)
#   all       Combined bundle        (canonical + all providers)
#
# Examples:
#   ./scripts/apm-build.sh
#   ./scripts/apm-build.sh -o ./dist -t copilot,claude
#   ./scripts/apm-build.sh --no-checksum
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- Defaults ---
OUTPUT_DIR="${REPO_ROOT}/dist"
TARGETS="copilot,claude,cli,all"
GENERATE_CHECKSUMS=true

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -26 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output-dir)   OUTPUT_DIR="$2"; shift 2 ;;
        -t|--targets)      TARGETS="$2"; shift 2 ;;
        --checksum)        GENERATE_CHECKSUMS=true; shift ;;
        --no-checksum)     GENERATE_CHECKSUMS=false; shift ;;
        -h|--help)         usage ;;
        *)                 log_err "Unknown option: $1"; usage ;;
    esac
done

# --- Read package name from apm.yml ---
cd "${REPO_ROOT}"
PACKAGE_NAME=$(grep '^name:' apm.yml | head -1 | sed 's/^name:[[:space:]]*//' | tr -d '\r')
if [[ -z "${PACKAGE_NAME}" ]]; then
    log_err "Could not read 'name' from apm.yml"
    exit 1
fi
log_info "Package: ${PACKAGE_NAME}"

# --- Canonical (common) content included in every bundle ---
# Paths defined by the 'exports' and 'knowledge' keys in apm.yml.
CANONICAL_PATHS=(
    ".apm/agents"
    ".apm/skills"
    ".apm/prompts"
    ".apm/instructions"
    ".apm/contexts"
    ".apm/workflows"
    "knowledge"
    "apm.yml"
)

# --- Target → provider directory mapping (from apm.yml providers section) ---
declare -A PROVIDER_DIR
PROVIDER_DIR["copilot"]="providers/github-copilot"
PROVIDER_DIR["claude"]="providers/claude-code"
PROVIDER_DIR["cli"]="providers/cli"

# --- Validate that required paths exist ---
log_step "Validating source paths"
for path in "${CANONICAL_PATHS[@]}"; do
    if [[ ! -e "${path}" ]]; then
        log_err "Required path not found: ${path}"
        exit 1
    fi
done
log_ok "All canonical paths present"

# --- Prepare output directory ---
log_step "Preparing output directory"
rm -rf "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"
log_info "Output: ${OUTPUT_DIR}"

# --- Build helper: pack one archive ---
pack_target() {
    local target="$1"
    local archive="${OUTPUT_DIR}/${PACKAGE_NAME}-${target}.tar.gz"
    local extra_paths=("${@:2}")

    log_info "Packing target: ${target}"

    # Collect all paths to include, filtering out any that don't exist
    local include_paths=()
    for p in "${CANONICAL_PATHS[@]}" "${extra_paths[@]}"; do
        [[ -e "${p}" ]] && include_paths+=("${p}")
    done

    tar -czf "${archive}" "${include_paths[@]}"
    log_ok "Packed: $(basename "${archive}")"
}

# --- Build targets ---
IFS=',' read -ra TARGET_LIST <<< "${TARGETS}"

log_step "Building ${#TARGET_LIST[@]} target(s): ${TARGETS}"

for target in "${TARGET_LIST[@]}"; do
    target="$(echo "${target}" | xargs)"  # trim whitespace
    case "${target}" in
        copilot)
            pack_target "${target}" \
                "${PROVIDER_DIR[copilot]}" \
                ".github"
            ;;
        claude)
            pack_target "${target}" \
                "${PROVIDER_DIR[claude]}"
            ;;
        cli)
            pack_target "${target}" \
                "${PROVIDER_DIR[cli]}"
            ;;
        all)
            pack_target "${target}" \
                "${PROVIDER_DIR[copilot]}" \
                "${PROVIDER_DIR[claude]}" \
                "${PROVIDER_DIR[cli]}" \
                ".github"
            ;;
        *)
            log_err "Unknown target '${target}'. Valid: copilot, claude, cli, all"
            exit 1
            ;;
    esac
done

# --- Generate checksums ---
if [[ "${GENERATE_CHECKSUMS}" == true ]]; then
    log_step "Generating SHA-256 checksums"
    CHECKSUM_FILE="${OUTPUT_DIR}/SHA256SUMS"
    : > "${CHECKSUM_FILE}"

    for archive in "${OUTPUT_DIR}"/*.tar.gz "${OUTPUT_DIR}"/*.zip; do
        [[ -f "${archive}" ]] || continue
        sha256sum "${archive}" | sed "s|${OUTPUT_DIR}/||" >> "${CHECKSUM_FILE}"
    done

    if [[ -s "${CHECKSUM_FILE}" ]]; then
        log_ok "Checksums written to ${CHECKSUM_FILE}"
        cat "${CHECKSUM_FILE}"
    else
        log_info "No archives found for checksum generation"
        rm -f "${CHECKSUM_FILE}"
    fi
fi

# --- Summary ---
log_step "Build Summary"
ARCHIVE_COUNT=$(find "${OUTPUT_DIR}" -maxdepth 1 \( -name '*.tar.gz' -o -name '*.zip' \) | wc -l)
log_ok "Built ${ARCHIVE_COUNT} archive(s) in ${OUTPUT_DIR}/"
ls -lh "${OUTPUT_DIR}/"
