#!/usr/bin/env bash
# ==============================================================================
# APM Bundle Builder
#
# Builds APM distribution archives for all configured targets.
#
# Usage:
#   ./scripts/apm-build.sh [options]
#
# Options:
#   -o, --output-dir <dir>   Output directory (default: ./dist)
#   -t, --targets <list>     Comma-separated targets (default: copilot,claude,all)
#   --skip-install           Skip apm install step
#   --checksum               Generate SHA-256 checksums (default: true)
#   --no-checksum            Disable SHA-256 checksums
#   -h, --help               Show this help
#
# Examples:
#   ./scripts/apm-build.sh
#   ./scripts/apm-build.sh -o ./dist -t copilot,claude
#   ./scripts/apm-build.sh --skip-install --no-checksum
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- Defaults ---
OUTPUT_DIR="${REPO_ROOT}/dist"
TARGETS="copilot,claude,all"
SKIP_INSTALL=false
GENERATE_CHECKSUMS=true

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -22 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output-dir)   OUTPUT_DIR="$2"; shift 2 ;;
        -t|--targets)      TARGETS="$2"; shift 2 ;;
        --skip-install)    SKIP_INSTALL=true; shift ;;
        --checksum)        GENERATE_CHECKSUMS=true; shift ;;
        --no-checksum)     GENERATE_CHECKSUMS=false; shift ;;
        -h|--help)         usage ;;
        *)                 log_err "Unknown option: $1"; usage ;;
    esac
done

# --- Prepare output directory ---
log_step "Preparing output directory"
rm -rf "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"
log_info "Output: ${OUTPUT_DIR}"

# --- Install dependencies ---
if [[ "${SKIP_INSTALL}" == false ]]; then
    log_step "Installing APM dependencies"
    cd "${REPO_ROOT}"
    apm install
    log_ok "apm install completed"
else
    log_info "Skipping apm install (--skip-install)"
fi

# --- Build targets ---
IFS=',' read -ra TARGET_LIST <<< "${TARGETS}"

log_step "Building ${#TARGET_LIST[@]} target(s): ${TARGETS}"

for target in "${TARGET_LIST[@]}"; do
    target="$(echo "${target}" | xargs)"  # trim whitespace
    log_info "Packing target: ${target}"
    apm pack --target "${target}" --archive -o "${OUTPUT_DIR}/"
    log_ok "Packed: ${target}"
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
