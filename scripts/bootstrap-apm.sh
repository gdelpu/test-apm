#!/usr/bin/env bash
# ==============================================================================
# APM Bootstrap — One-liner installer for consumer repos (Linux / macOS)
#
# THIS IS THE ONLY FILE YOU NEED TO DOWNLOAD.
#
# Downloads the multi-part installer and its dependencies into a hidden temp
# directory, runs the full install, then removes all temp files automatically.
# End result: .github/ (Copilot runtime) and .apm.lock.yaml — nothing else.
#
# Steps performed internally:
#   1. Downloads scripts/install-apm-bundle.sh  (the full installer)
#   2. Downloads scripts/lib/apm-lock.sh        (lock-file helper)
#   3. Runs the installer against the chosen version + target
#   4. Deletes the temp directory
#
# Usage:
#   ./bootstrap-apm.sh --project-id <id> [options]
#
# Options:
#   -v, --version <semver>     Version to install (default: 0.0.1, or "latest")
#   --project-id <id>          GitLab project ID of ai-sdlc-foundation (required)
#   --gitlab-url <url>         GitLab instance URL (default: https://innersource.soprasteria.com)
#   --token <token>            Auth token (default: $GITLAB_TOKEN)
#   -t, --target <target>      Target: copilot, claude, all (default: copilot)
#   -m, --mode <mode>          Install mode: standard or expandable (default: standard)
#   --ref <branch>             Git ref to fetch installer from (default: main)
#   -h, --help                 Show this help
#
# Examples:
#   # Minimal — relies on GITLAB_TOKEN env var
#   ./bootstrap-apm.sh --project-id 12345
#
#   # Explicit version and token
#   ./bootstrap-apm.sh -v 0.0.1 --project-id 12345 --token "glpat-xxx"
#
#   # Expandable mode for customization
#   ./bootstrap-apm.sh -v 0.0.1 --project-id 12345 -m expandable
# ==============================================================================
set -euo pipefail

# --- Defaults ---
VERSION="latest"
PROJECT_ID="545119"
GITLAB_URL="${APM_GITLAB_URL:-https://innersource.soprasteria.com}"
AUTH_TOKEN="${GITLAB_TOKEN:-}"
TARGET="copilot"
MODE="standard"
REF="main"
TEMP_DIR=".apm-bootstrap-tmp"

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -34 "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

cleanup() {
    if [ -d "${TEMP_DIR}" ]; then
        rm -rf "${TEMP_DIR}"
        log_info "Cleaned up bootstrap temp files"
    fi
}
trap cleanup EXIT

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--version)       VERSION="$2"; shift 2 ;;
        --project-id)       PROJECT_ID="$2"; shift 2 ;;
        --gitlab-url)       GITLAB_URL="$2"; shift 2 ;;
        --token)            AUTH_TOKEN="$2"; shift 2 ;;
        -t|--target)        TARGET="$2"; shift 2 ;;
        -m|--mode)          MODE="$2"; shift 2 ;;
        --ref)              REF="$2"; shift 2 ;;
        -h|--help)          usage ;;
        *)                  log_err "Unknown option: $1"; usage ;;
    esac
done

# --- Validate ---
if [ -z "${PROJECT_ID}" ]; then
    log_err "--project-id is required (default: 545119)"
    exit 1
fi
if [ -z "${AUTH_TOKEN}" ]; then
    log_err "No token provided. Use --token or set \$GITLAB_TOKEN"
    exit 1
fi

API_BASE="${GITLAB_URL}/api/v4/projects/${PROJECT_ID}"

# --- Resolve "latest" version ---
if [ "${VERSION}" = "latest" ]; then
    log_step "Resolving latest version"
    LATEST_TAG=$(curl --fail --silent --show-error \
        --header "PRIVATE-TOKEN: ${AUTH_TOKEN}" \
        "${API_BASE}/repository/tags?order_by=version&sort=desc&per_page=1" \
        | python3 -c "import sys,json; tags=json.load(sys.stdin); print(tags[0]['name'].lstrip('v') if tags else '')" 2>/dev/null || true)
    if [ -z "${LATEST_TAG}" ]; then
        log_err "No tags found. Publish a version first."
        exit 1
    fi
    VERSION="${LATEST_TAG}"
    log_info "Latest version: ${VERSION}"
fi

log_step "Bootstrapping AI SDLC Foundation v${VERSION} (${MODE} mode, target: ${TARGET})"
log_info "Source: ${GITLAB_URL} (project ${PROJECT_ID})"

# --- Download installer scripts ---
mkdir -p "${TEMP_DIR}/lib"

download_file() {
    local remote_path="$1"
    local local_path="$2"
    local encoded
    encoded=$(echo "${remote_path}" | sed 's|/|%2F|g')
    local url="${API_BASE}/repository/files/${encoded}/raw?ref=${REF}"
    log_info "Downloading ${remote_path}..."
    curl --fail --silent --show-error \
        --header "PRIVATE-TOKEN: ${AUTH_TOKEN}" \
        -o "${TEMP_DIR}/${local_path}" \
        "${url}"
}

download_file "scripts/install-apm-bundle.sh" "install-apm-bundle.sh"
download_file "scripts/lib/apm-lock.sh"       "lib/apm-lock.sh"

chmod +x "${TEMP_DIR}/install-apm-bundle.sh"
log_ok "Installer scripts downloaded"

# --- Run the installer ---
log_step "Running installer"
"${TEMP_DIR}/install-apm-bundle.sh" \
    --version "${VERSION}" \
    --target "${TARGET}" \
    --mode "${MODE}" \
    --project-id "${PROJECT_ID}" \
    --gitlab-url "${GITLAB_URL}" \
    --token "${AUTH_TOKEN}"

# --- Summary ---
echo ""
log_step "Done!"
echo ""
if [ "${MODE}" = "standard" ]; then
    echo "  Next steps:"
    echo "    git add .github/ .apm.lock.yaml"
    echo "    git commit -m \"feat: install AI SDLC Foundation v${VERSION}\""
    echo "    git push"
    echo ""
    echo "  Copilot will auto-discover agents and prompts from .github/"
    echo "  Try: @hub-orchestrator or /workflow-feature"
else
    echo "  Next steps:"
    echo "    git add .apm/ providers/ providers-local/ .apm.lock.yaml apm.yml"
    echo "    git commit -m \"feat: install AI SDLC Foundation v${VERSION} (expandable)\""
    echo "    git push"
    echo ""
    echo "  Customize via providers-local/<provider>/ — then re-project."
fi
echo ""
