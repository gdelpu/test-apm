#!/usr/bin/env bash
# ==============================================================================
# APM Bundle Installer (Linux / macOS)
#
# Downloads and installs an APM bundle from the GitLab Generic Package Registry.
#
# Usage:
#   ./install-apm-bundle.sh --version <semver> [options]
#
# Options:
#   -v, --version <semver>     Version to install (required, or "latest")
#   -t, --target <target>      Target bundle: copilot, claude, all (default: all)
#   -d, --dest <dir>           Destination directory (default: ./.apm-dist)
#   --registry-url <url>       Full Generic Package Registry URL
#   --project-id <id>          GitLab project ID (alternative to --registry-url)
#   --gitlab-url <url>         GitLab instance URL (default: https://gitlab.com)
#   --token <token>            Private/job token for authentication
#   --verify                   Verify SHA-256 checksums (default: true)
#   --no-verify                Skip checksum verification
#   -h, --help                 Show this help
#
# Environment variables:
#   GITLAB_TOKEN               Fallback auth token
#   APM_REGISTRY_URL           Fallback registry URL
#   APM_PROJECT_ID             Fallback project ID
#   APM_GITLAB_URL             Fallback GitLab instance URL
#
# Examples:
#   # Install from registry using project ID
#   ./install-apm-bundle.sh -v 1.2.0 --project-id 12345 --token "$GITLAB_TOKEN"
#
#   # Install specific target
#   ./install-apm-bundle.sh -v 2.0.0 -t copilot --project-id 12345
#
#   # Install with full registry URL
#   ./install-apm-bundle.sh -v 1.0.0 \
#       --registry-url https://gitlab.example.com/api/v4/projects/42/packages/generic
# ==============================================================================
set -euo pipefail

# --- Defaults ---
VERSION=""
TARGET="all"
DEST_DIR="./.apm-dist"
REGISTRY_URL="${APM_REGISTRY_URL:-}"
PROJECT_ID="${APM_PROJECT_ID:-}"
GITLAB_URL="${APM_GITLAB_URL:-https://gitlab.com}"
AUTH_TOKEN="${GITLAB_TOKEN:-}"
PACKAGE_NAME="ssg-ai-backbone"
VERIFY_CHECKSUMS=true

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -36 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

check_dependency() {
    if ! command -v "$1" &>/dev/null; then
        log_err "Required command not found: $1"
        exit 1
    fi
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--version)       VERSION="$2"; shift 2 ;;
        -t|--target)        TARGET="$2"; shift 2 ;;
        -d|--dest)          DEST_DIR="$2"; shift 2 ;;
        --registry-url)     REGISTRY_URL="$2"; shift 2 ;;
        --project-id)       PROJECT_ID="$2"; shift 2 ;;
        --gitlab-url)       GITLAB_URL="$2"; shift 2 ;;
        --token)            AUTH_TOKEN="$2"; shift 2 ;;
        --verify)           VERIFY_CHECKSUMS=true; shift ;;
        --no-verify)        VERIFY_CHECKSUMS=false; shift ;;
        -h|--help)          usage ;;
        *)                  log_err "Unknown option: $1"; usage ;;
    esac
done

# --- Validate ---
check_dependency curl
check_dependency tar
check_dependency sha256sum || check_dependency shasum

if [[ -z "${VERSION}" ]]; then
    log_err "--version is required"
    exit 1
fi

VERSION="${VERSION#v}"

if [[ -z "${REGISTRY_URL}" ]]; then
    if [[ -z "${PROJECT_ID}" ]]; then
        log_err "Provide --registry-url or --project-id"
        exit 1
    fi
    REGISTRY_URL="${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/packages/generic"
fi

HEADER_ARGS=()
if [[ -n "${AUTH_TOKEN}" ]]; then
    HEADER_ARGS=(--header "PRIVATE-TOKEN: ${AUTH_TOKEN}")
fi

# --- Download ---
log_step "Installing ${PACKAGE_NAME} v${VERSION} (target: ${TARGET})"
mkdir -p "${DEST_DIR}"

BASE_URL="${REGISTRY_URL}/${PACKAGE_NAME}/${VERSION}"

# Determine archive filename pattern based on target
# apm pack produces: <package>-<target>.tar.gz
ARCHIVE_NAME="${PACKAGE_NAME}-${TARGET}.tar.gz"
DOWNLOAD_URL="${BASE_URL}/${ARCHIVE_NAME}"

log_info "Downloading: ${ARCHIVE_NAME}"
HTTP_CODE=$(curl --silent --output "${DEST_DIR}/${ARCHIVE_NAME}" --write-out "%{http_code}" \
    "${HEADER_ARGS[@]}" \
    "${DOWNLOAD_URL}")

if [[ ! "${HTTP_CODE}" =~ ^2 ]]; then
    log_err "Download failed (HTTP ${HTTP_CODE}): ${DOWNLOAD_URL}"
    rm -f "${DEST_DIR}/${ARCHIVE_NAME}"
    exit 1
fi
log_ok "Downloaded: ${ARCHIVE_NAME}"

# --- Verify checksum ---
if [[ "${VERIFY_CHECKSUMS}" == true ]]; then
    log_info "Downloading checksums"
    CHECKSUM_URL="${BASE_URL}/SHA256SUMS"
    if curl --silent --fail "${HEADER_ARGS[@]}" "${CHECKSUM_URL}" -o "${DEST_DIR}/SHA256SUMS"; then
        log_info "Verifying SHA-256 checksum"
        cd "${DEST_DIR}"
        if command -v sha256sum &>/dev/null; then
            grep "${ARCHIVE_NAME}" SHA256SUMS | sha256sum --check --status
        else
            grep "${ARCHIVE_NAME}" SHA256SUMS | shasum -a 256 --check --status
        fi
        log_ok "Checksum verified"
        cd - >/dev/null
    else
        log_info "Checksums not available — skipping verification"
    fi
fi

# --- Extract ---
log_step "Extracting to ${DEST_DIR}"
tar -xzf "${DEST_DIR}/${ARCHIVE_NAME}" -C "${DEST_DIR}"
log_ok "Extracted: ${ARCHIVE_NAME}"

# --- Summary ---
log_step "Installation Complete"
log_ok "${PACKAGE_NAME} v${VERSION} (${TARGET}) installed to ${DEST_DIR}"
ls -lh "${DEST_DIR}/"
