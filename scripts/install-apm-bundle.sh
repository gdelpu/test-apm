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
#   -t, --target <target>      Target bundle: copilot, claude, all (default: copilot)
#   -d, --dest <dir>           Destination directory (default: ./.apm-dist)
#   -m, --mode <mode>          Install mode: standard or expandable (default: standard)
#   --provider <name>          Provider adapter (default: github-copilot)
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
#   # Install specific target with mode
#   ./install-apm-bundle.sh -v 2.0.0 -t copilot -m expandable --project-id 12345
#
#   # Standard mode (default) — only runtime projection is installed
#   ./install-apm-bundle.sh -v 1.0.0 -t copilot --project-id 12345
#
#   # Install with full registry URL
#   ./install-apm-bundle.sh -v 1.0.0 \
#       --registry-url https://gitlab.example.com/api/v4/projects/42/packages/generic
# ==============================================================================
set -euo pipefail

# --- Defaults ---
VERSION=""
TARGET="copilot"
DEST_DIR="./.apm-dist"
MODE="standard"
PROVIDER="github-copilot"
REGISTRY_URL="${APM_REGISTRY_URL:-}"
PROJECT_ID="${APM_PROJECT_ID:-}"
GITLAB_URL="${APM_GITLAB_URL:-https://gitlab.com}"
AUTH_TOKEN="${GITLAB_TOKEN:-}"
PACKAGE_NAME="ssg-ai-backbone"
VERIFY_CHECKSUMS=true
ACTUAL_CHECKSUM=""

# --- Source lock-file helpers ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/apm-lock.sh"

# --- Helpers ---
log_info()  { echo "ℹ️  $*"; }
log_ok()    { echo "✅ $*"; }
log_err()   { echo "❌ $*" >&2; }
log_step()  { echo ""; echo "── $* ──"; }

usage() {
    head -42 "$0" | grep '^#' | sed 's/^# \?//'
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
        -m|--mode)          MODE="$2"; shift 2 ;;
        --provider)         PROVIDER="$2"; shift 2 ;;
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

if [[ "$MODE" != "standard" && "$MODE" != "expandable" ]]; then
    log_err "Invalid mode: $MODE (must be 'standard' or 'expandable')"
    exit 1
fi

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
            computed_hash=$(sha256sum "${ARCHIVE_NAME}" | awk '{print $1}')
        else
            computed_hash=$(shasum -a 256 "${ARCHIVE_NAME}" | awk '{print $1}')
        fi
        expected_hash=$(grep "${ARCHIVE_NAME}" SHA256SUMS | awk '{print $1}')
        if [[ "$computed_hash" != "$expected_hash" ]]; then
            log_err "Checksum mismatch! Expected: ${expected_hash}, Got: ${computed_hash}"
            cd - >/dev/null
            exit 1
        fi
        ACTUAL_CHECKSUM="sha256:${computed_hash}"
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

# --- Detect existing install ---
# Standard mode writes the lock at repo root; expandable writes at $DEST_DIR.
# Try both locations so updates are detected regardless of prior mode.
REPO_ROOT="$(pwd)"
if read_apm_lock "$DEST_DIR"; then
    log_info "Existing install detected: v${APM_LOCK_VERSION} (${APM_LOCK_MODE} mode)"
elif read_apm_lock "$REPO_ROOT"; then
    log_info "Existing install detected: v${APM_LOCK_VERSION} (${APM_LOCK_MODE} mode)"
fi

# --- Helper: parse provider runtime path from apm.yml ---
get_provider_runtime() {
    local apm_file="$1" provider="$2"
    awk -v prov="$provider" '
        /^providers:/ { in_providers=1; next }
        in_providers && /^[^ ]/ { in_providers=0 }
        in_providers && $0 ~ "^  " prov ":" { in_block=1; next }
        in_block && /^  [^ ]/ { in_block=0 }
        in_block && /^    runtime:/ { sub(/^[^:]+:[[:space:]]*/, ""); gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit }
    ' "$apm_file"
}

# --- Install mode logic ---
if [[ "$MODE" == "standard" ]]; then
    # ── Standard mode: project to runtime dir only ──────────────────────
    log_step "Standard mode — projecting runtime"

    TEMP_DIR=$(mktemp -d "${DEST_DIR}/apm-install.XXXXXX")
    trap 'rm -rf "$TEMP_DIR"' EXIT

    # Move extracted content into temp working directory
    find "$DEST_DIR" -mindepth 1 -maxdepth 1 \
        ! -name "$(basename "$TEMP_DIR")" \
        ! -name "${ARCHIVE_NAME}" \
        ! -name "SHA256SUMS" \
        ! -name "${APM_LOCK_FILENAME:-".apm.lock.yaml"}" \
        -exec mv {} "$TEMP_DIR/" \;

    # Run projection in the temp directory
    PROJ_SCRIPT="${TEMP_DIR}/scripts/project-copilot.sh"
    if [[ ! -f "$PROJ_SCRIPT" ]]; then
        PROJ_SCRIPT="${SCRIPT_DIR}/project-copilot.sh"
    fi
    chmod +x "$PROJ_SCRIPT"
    (cd "$TEMP_DIR" && bash "$PROJ_SCRIPT" --provider "$PROVIDER" --full --clean)

    # Resolve runtime directory from apm.yml
    RUNTIME_DIR=$(get_provider_runtime "$TEMP_DIR/apm.yml" "$PROVIDER")
    RUNTIME_DIR="${RUNTIME_DIR:-.github}"

    # Copy runtime directory to consumer repo root (not into staging dir)
    if [[ -d "$REPO_ROOT/$RUNTIME_DIR" ]]; then
        log_info "Removing previous runtime directory: $RUNTIME_DIR"
        rm -rf "${REPO_ROOT:?}/$RUNTIME_DIR"
    fi
    cp -r "$TEMP_DIR/$RUNTIME_DIR" "$REPO_ROOT/$RUNTIME_DIR"
    log_ok "Copied runtime: $RUNTIME_DIR"

    # Copy hook engine so consumers can use the state tracker CLI
    if [[ -d "$TEMP_DIR/.apm/hooks" ]]; then
        rm -rf "$REPO_ROOT/.apm/hooks"
        mkdir -p "$REPO_ROOT/.apm"
        cp -r "$TEMP_DIR/.apm/hooks" "$REPO_ROOT/.apm/hooks"
        log_ok "Copied hook engine: .apm/hooks/"
    fi

    # Write lock file at repo root
    write_apm_lock "$REPO_ROOT" "$VERSION" "standard" "$PROVIDER" "$ARCHIVE_NAME" "${ACTUAL_CHECKSUM}"

    # Clean up temp dir (trap handles this, but be explicit)
    rm -rf "$TEMP_DIR"
    trap - EXIT

elif [[ "$MODE" == "expandable" ]]; then
    # ── Expandable mode: full content + local overrides ─────────────────
    log_step "Expandable mode — full install with local overlay scaffold"

    # On update: preserve providers-local, re-extract upstream already done above

    # Scaffold providers-local directory
    LOCAL_DIR="$DEST_DIR/providers-local/$PROVIDER"
    mkdir -p "$LOCAL_DIR/agents"
    mkdir -p "$LOCAL_DIR/prompts"
    mkdir -p "$LOCAL_DIR/instructions"

    if [[ ! -f "$LOCAL_DIR/README.md" ]]; then
        cat > "$LOCAL_DIR/README.md" <<'README_EOF'
# providers-local

Local overrides for the APM provider layer.

Files placed here will be overlaid on top of upstream provider assets during
projection. To override an upstream file, place a file with the same name in
the matching subdirectory.

## Structure

    providers-local/<provider>/
      agents/       # Custom or overridden agent definitions
      prompts/      # Custom or overridden prompt definitions
      instructions/ # Custom or overridden instruction files

## Re-projecting

After adding or modifying local files, re-run the projection script:

    ./scripts/project-copilot.sh --provider <provider> --clean
README_EOF
    fi

    # Run projection (no --full for expandable — consumers extend in-place)
    PROJ_SCRIPT="$DEST_DIR/scripts/project-copilot.sh"
    chmod +x "$PROJ_SCRIPT"
    (cd "$DEST_DIR" && bash "$PROJ_SCRIPT" --provider "$PROVIDER" --clean)

    # Write lock file
    write_apm_lock "$DEST_DIR" "$VERSION" "expandable" "$PROVIDER" "$ARCHIVE_NAME" "${ACTUAL_CHECKSUM}"

    # Generate .gitignore for runtime projection artefacts
    RUNTIME_DIR=$(get_provider_runtime "$DEST_DIR/apm.yml" "$PROVIDER")
    RUNTIME_DIR="${RUNTIME_DIR:-.github}"
    if ! grep -qF "${RUNTIME_DIR}/agents/" "$DEST_DIR/.gitignore" 2>/dev/null; then
        cat >> "$DEST_DIR/.gitignore" <<GITIGNORE

# Generated by APM installer — runtime projection
${RUNTIME_DIR}/agents/
${RUNTIME_DIR}/prompts/
${RUNTIME_DIR}/instructions/
GITIGNORE
    fi

    # Promote all content from staging dir to repo root
    REPO_ROOT="$(pwd)"
    find "$DEST_DIR" -mindepth 1 -maxdepth 1 \
        ! -name "${ARCHIVE_NAME}" \
        ! -name "SHA256SUMS" \
        -exec mv -f {} "$REPO_ROOT/" \;
    log_ok "Promoted content to repo root"
fi

# --- Cleanup downloaded archive and staging dir ---
rm -f "${DEST_DIR}/${ARCHIVE_NAME}" "${DEST_DIR}/SHA256SUMS"
rm -rf "${DEST_DIR}"

# --- Summary ---
log_step "Installation Complete"
log_ok "${PACKAGE_NAME} v${VERSION} (${TARGET}, ${MODE} mode) installed to $(pwd)"
ls -lh ./
