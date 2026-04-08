#!/usr/bin/env bash
# ==============================================================================
# APM Bundle Publisher — GitLab Generic Package Registry
#
# Uploads APM distribution archives to the GitLab Generic Package Registry.
#
# Usage:
#   ./scripts/apm-publish.sh --version <semver> [options]
#
# Options:
#   -v, --version <semver>     Package version (required; must be valid semver)
#   -d, --dist-dir <dir>       Directory containing archives (default: ./dist)
#   -n, --package-name <name>  Package name (default: ssg-ai-backbone)
#   --registry-url <url>       Registry base URL (default: CI_API_V4_URL/projects/CI_PROJECT_ID)
#   --token <token>            Auth token (default: CI_JOB_TOKEN)
#   --dry-run                  Print upload commands without executing
#   -h, --help                 Show this help
#
# Examples:
#   ./scripts/apm-publish.sh --version 1.2.0
#   ./scripts/apm-publish.sh -v 2.0.0-rc.1 -d ./dist --dry-run
#
# Environment variables (GitLab CI defaults):
#   CI_API_V4_URL      GitLab API base URL
#   CI_PROJECT_ID      Project ID for registry scope
#   CI_JOB_TOKEN       Authentication token
# ==============================================================================
set -euo pipefail

# --- Defaults ---
VERSION=""
DIST_DIR="./dist"
PACKAGE_NAME="ssg-ai-backbone"
REGISTRY_URL=""
AUTH_TOKEN=""
DRY_RUN=false

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -26 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

validate_semver() {
    local ver="$1"
    local semver_regex='^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$'
    if [[ ! "${ver}" =~ ${semver_regex} ]]; then
        log_err "Invalid semver: '${ver}'"
        log_err "Expected format: MAJOR.MINOR.PATCH[-prerelease][+build]"
        exit 1
    fi
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--version)       VERSION="$2"; shift 2 ;;
        -d|--dist-dir)      DIST_DIR="$2"; shift 2 ;;
        -n|--package-name)  PACKAGE_NAME="$2"; shift 2 ;;
        --registry-url)     REGISTRY_URL="$2"; shift 2 ;;
        --token)            AUTH_TOKEN="$2"; shift 2 ;;
        --dry-run)          DRY_RUN=true; shift ;;
        -h|--help)          usage ;;
        *)                  log_err "Unknown option: $1"; usage ;;
    esac
done

# --- Validate inputs ---
if [[ -z "${VERSION}" ]]; then
    log_err "--version is required"
    exit 1
fi

# Strip leading 'v' if present (v1.2.3 → 1.2.3)
VERSION="${VERSION#v}"
validate_semver "${VERSION}"

if [[ ! -d "${DIST_DIR}" ]]; then
    log_err "Distribution directory not found: ${DIST_DIR}"
    exit 1
fi

# --- Resolve registry URL and token ---
if [[ -z "${REGISTRY_URL}" ]]; then
    if [[ -z "${CI_API_V4_URL:-}" || -z "${CI_PROJECT_ID:-}" ]]; then
        log_err "Cannot resolve registry URL: set --registry-url or ensure CI_API_V4_URL and CI_PROJECT_ID are defined"
        exit 1
    fi
    REGISTRY_URL="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic"
fi

if [[ -z "${AUTH_TOKEN}" ]]; then
    AUTH_TOKEN="${CI_JOB_TOKEN:-}"
fi

if [[ -z "${AUTH_TOKEN}" && "${DRY_RUN}" == false ]]; then
    log_err "No auth token: set --token or ensure CI_JOB_TOKEN is defined"
    exit 1
fi

# --- Collect files to upload ---
log_step "Publishing ${PACKAGE_NAME} v${VERSION}"
log_info "Registry: ${REGISTRY_URL}"
log_info "Source:   ${DIST_DIR}"

UPLOAD_COUNT=0
FAILED=0

for file in "${DIST_DIR}"/*.tar.gz "${DIST_DIR}"/*.zip "${DIST_DIR}"/SHA256SUMS; do
    [[ -f "${file}" ]] || continue
    filename="$(basename "${file}")"
    upload_url="${REGISTRY_URL}/${PACKAGE_NAME}/${VERSION}/${filename}"

    if [[ "${DRY_RUN}" == true ]]; then
        log_info "[dry-run] Would upload: ${filename} → ${upload_url}"
        UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
        continue
    fi

    log_info "Uploading: ${filename}"
    HTTP_CODE=$(curl --silent --output /dev/null --write-out "%{http_code}" \
        --header "JOB-TOKEN: ${AUTH_TOKEN}" \
        --upload-file "${file}" \
        "${upload_url}") || true

    if [[ "${HTTP_CODE}" =~ ^2 ]]; then
        log_ok "Published: ${filename} (HTTP ${HTTP_CODE})"
        UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    else
        log_err "Failed: ${filename} (HTTP ${HTTP_CODE})"
        FAILED=$((FAILED + 1))
    fi
done

# --- Summary ---
log_step "Publish Summary"
if [[ "${DRY_RUN}" == true ]]; then
    log_info "[dry-run] ${UPLOAD_COUNT} file(s) would be published"
elif [[ ${FAILED} -gt 0 ]]; then
    log_err "${FAILED} upload(s) failed out of $((UPLOAD_COUNT + FAILED))"
    exit 1
else
    log_ok "${UPLOAD_COUNT} file(s) published to ${PACKAGE_NAME} v${VERSION}"
fi
