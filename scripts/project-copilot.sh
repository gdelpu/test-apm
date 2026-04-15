#!/usr/bin/env bash
# ==============================================================================
# Project Copilot — Provider-agnostic runtime projection
#
# Projects provider adapter files into the runtime directory.
# Supports all providers defined in apm.yml.
#
# Usage:
#   ./project-copilot.sh [options]
#
# Options:
#   --provider <name>   Provider to project (default: github-copilot)
#   --full              Copy canonical content + rewrite paths
#   --clean             Remove target directories before copying
#   -h, --help          Show help
#
# Examples:
#   ./project-copilot.sh
#   ./project-copilot.sh --clean
#   ./project-copilot.sh --provider github-copilot --full --clean
#   ./project-copilot.sh --provider claude-code
# ==============================================================================
set -euo pipefail

# ── Bash version check (associative arrays & ${var^^} require bash 4+) ───────
if (( BASH_VERSINFO[0] < 4 )); then
  echo "ERROR: project-copilot.sh requires bash 4+. Found: bash ${BASH_VERSION}" >&2
  echo "  macOS ships bash 3.2. Install a modern bash:  brew install bash" >&2
  exit 1
fi

# ── Defaults ─────────────────────────────────────────────────────────────────
PROVIDER="github-copilot"
FULL=false
CLEAN=false

# ── Help ─────────────────────────────────────────────────────────────────────
show_help() {
  sed -n '2,/^set -euo pipefail$/{ /^#/s/^# \?//p }' "$0"
  exit 0
}

# ── Argument parsing ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --provider)
      PROVIDER="${2:?--provider requires a value}"
      shift 2
      ;;
    --full)
      FULL=true
      shift
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run with --help for usage information." >&2
      exit 1
      ;;
  esac
done

# ── Resolve repo root ───────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Parse apm.yml ────────────────────────────────────────────────────────────
APM_FILE="$REPO_ROOT/apm.yml"
if [[ ! -f "$APM_FILE" ]]; then
  echo "  ERROR  apm.yml not found at $APM_FILE" >&2
  exit 1
fi

# Extract provider block from apm.yml using awk.
# Finds the line matching "  <provider>:" under the "providers:" section and
# collects all indented key-value pairs until the next provider or section.
parse_provider_field() {
  local provider="$1" field="$2"
  awk -v prov="$provider" -v fld="$field" '
    /^providers:/ { in_providers=1; next }
    in_providers && /^[^ ]/ { in_providers=0 }
    in_providers && $0 ~ "^  " prov ":" { in_block=1; next }
    in_block && /^  [^ ]/ { in_block=0 }
    in_block && $0 ~ "^    " fld ":" {
      sub(/^[^:]+:[[:space:]]*/, "")
      gsub(/^[[:space:]]+|[[:space:]]+$/, "")
      print
      exit
    }
  ' "$APM_FILE"
}

ADAPTER_PATH="$(parse_provider_field "$PROVIDER" "adapter")"
RUNTIME_PATH="$(parse_provider_field "$PROVIDER" "runtime")"

# Validate provider exists — at least adapter or runtime must be defined
if [[ -z "$ADAPTER_PATH" && -z "$RUNTIME_PATH" ]]; then
  echo "  ERROR  Provider '$PROVIDER' not found in apm.yml or has no adapter/runtime paths." >&2
  exit 1
fi

# Fall back: runtime defaults to adapter path if not specified
SOURCE_DIR="$REPO_ROOT/${ADAPTER_PATH:-.}"
TARGET_DIR="$REPO_ROOT/${RUNTIME_PATH:-$ADAPTER_PATH}"

echo "  PROVIDER  $PROVIDER — adapter: ${ADAPTER_PATH:-(none)}, runtime: ${RUNTIME_PATH:-$ADAPTER_PATH}"

# ── Helper: portable sed in-place ────────────────────────────────────────────
# Uses temp-file approach to avoid GNU vs BSD sed -i differences.
sed_inplace() {
  local expression="$1" file="$2"
  sed -e "$expression" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

# ── Determine asset types ───────────────────────────────────────────────────
# Scan source directory for subdirectories — each becomes an asset type.
if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "  ERROR  Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

ASSET_TYPES=()
for dir in "$SOURCE_DIR"/*/; do
  [[ -d "$dir" ]] || continue
  ASSET_TYPES+=("$(basename "$dir")")
done

# ── Clean ────────────────────────────────────────────────────────────────────
if [[ "$CLEAN" == true ]]; then
  for type in "${ASSET_TYPES[@]}"; do
    dst="$TARGET_DIR/$type"
    if [[ -d "$dst" ]]; then
      rm -rf "$dst"
      echo "  CLEAN $dst"
    fi
  done
fi

# ── Copy provider adapter files ─────────────────────────────────────────────
for type in "${ASSET_TYPES[@]}"; do
  src="$SOURCE_DIR/$type"
  dst="$TARGET_DIR/$type"

  if [[ ! -d "$src" ]]; then
    echo "  SKIP  $type — source folder not found ($src)"
    continue
  fi

  mkdir -p "$dst"

  count=0
  for file in "$src"/*; do
    [[ -f "$file" ]] || continue
    cp -f "$file" "$dst/"
    (( ++count ))
  done
  echo "  COPY  $type — $count files -> $dst"
done

# ── Overlay providers-local/ ────────────────────────────────────────────────
LOCAL_DIR="$REPO_ROOT/providers-local/$PROVIDER"
if [[ -d "$LOCAL_DIR" ]]; then
  for dir in "$LOCAL_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    type="$(basename "$dir")"
    dst="$TARGET_DIR/$type"
    mkdir -p "$dst"

    count=0
    for file in "$dir"/*; do
      [[ -f "$file" ]] || continue
      cp -f "$file" "$dst/"
      (( ++count ))
    done
    if (( count > 0 )); then
      echo "  OVERLAY   $type — $count files from providers-local/"
    fi
  done
fi

# ── Full mode ────────────────────────────────────────────────────────────────
if [[ "$FULL" == true ]]; then
  echo ""

  # Canonical directories to copy into the runtime target
  declare -A CANONICAL_DIRS=(
    ["skills"]=".apm/skills"
    ["workflows"]=".apm/workflows"
    ["contexts"]=".apm/contexts"
    ["templates"]=".apm/templates"
    ["knowledge"]=".apm/knowledge"
    ["hooks"]=".apm/hooks"
  )

  for type in "${!CANONICAL_DIRS[@]}"; do
    src="$REPO_ROOT/${CANONICAL_DIRS[$type]}"
    dst="$TARGET_DIR/$type"

    if [[ ! -d "$src" ]]; then
      echo "  SKIP  $type — canonical folder not found ($src)"
      continue
    fi

    mkdir -p "$dst"
    count=0
    while IFS= read -r -d '' file; do
      # Preserve subdirectory structure relative to source
      rel="${file#"$src"/}"
      target_file="$dst/$rel"
      mkdir -p "$(dirname "$target_file")"
      cp -f "$file" "$target_file"
      (( ++count ))
    done < <(find "$src" -type f -print0)
    echo "  FULL-COPY $type — $count files -> $dst"
  done

  # Path rewrites in all .md files under the runtime target
  RUNTIME_REL="${TARGET_DIR#"$REPO_ROOT"/}"

  declare -a REWRITE_PAIRS=(
    ".apm/skills/|${RUNTIME_REL}/skills/"
    ".apm/workflows/|${RUNTIME_REL}/workflows/"
    ".apm/contexts/|${RUNTIME_REL}/contexts/"
    ".apm/templates/|${RUNTIME_REL}/templates/"
    ".apm/prompts/|${RUNTIME_REL}/prompts/"
    ".apm/agents/|${RUNTIME_REL}/agents/"
    ".apm/instructions/|${RUNTIME_REL}/instructions/"
    ".apm/knowledge/|${RUNTIME_REL}/knowledge/"
    ".apm/hooks/|${RUNTIME_REL}/hooks/"
    ".apm/hooks|${RUNTIME_REL}/hooks"
  )

  # Provider-specific rewrite
  if [[ "$PROVIDER" == "github-copilot" ]]; then
    REWRITE_PAIRS+=("providers/github-copilot|${RUNTIME_REL}")
  fi

  rewrite_count=0
  while IFS= read -r -d '' mdfile; do
    modified=false
    for pair in "${REWRITE_PAIRS[@]}"; do
      from="${pair%%|*}"
      to="${pair##*|}"
      # Escape slashes and dots for sed
      from_escaped="$(printf '%s' "$from" | sed 's/[.[\/*^$]/\\&/g')"
      to_escaped="$(printf '%s' "$to" | sed 's/[&/\]/\\&/g')"
      if grep -q "$from" "$mdfile" 2>/dev/null; then
        sed_inplace "s|${from}|${to}|g" "$mdfile"
        modified=true
      fi
    done
    if [[ "$modified" == true ]]; then
      (( ++rewrite_count ))
    fi
  done < <(find "$TARGET_DIR" -name '*.md' -type f -print0)

  echo "  REWRITE   $rewrite_count files updated with runtime path references"
fi

# ── Config-driven placeholder substitution ───────────────────────────────────
# Read provider config.yml (with providers-local/ override) and substitute
# {{KEY}} placeholders in all projected .md files.
CONFIG_FILE="$REPO_ROOT/providers-local/$PROVIDER/config.yml"
if [[ ! -f "$CONFIG_FILE" ]]; then
  CONFIG_FILE="$SOURCE_DIR/config.yml"
fi

if [[ -f "$CONFIG_FILE" ]]; then
  # Parse defaults section: extract key-value pairs under 'defaults:'
  declare -A CONFIG_VALUES
  in_defaults=false
  while IFS= read -r line; do
    if [[ "$line" =~ ^[[:space:]]*defaults:[[:space:]]*$ ]]; then
      in_defaults=true
      continue
    fi
    if [[ "$in_defaults" == true && "$line" =~ ^[^[:space:]] ]]; then
      in_defaults=false
    fi
    if [[ "$in_defaults" == true && "$line" =~ ^[[:space:]]+([a-zA-Z_]+):[[:space:]]*\"?([^\"]+)\"?[[:space:]]*$ ]]; then
      key="${BASH_REMATCH[1]^^}"  # uppercase
      value="${BASH_REMATCH[2]}"
      CONFIG_VALUES["{{DEFAULT_${key}}}"]="$value"
    fi
  done < "$CONFIG_FILE"

  if [[ ${#CONFIG_VALUES[@]} -gt 0 ]]; then
    subst_count=0
    while IFS= read -r -d '' mdfile; do
      modified=false
      for placeholder in "${!CONFIG_VALUES[@]}"; do
        value="${CONFIG_VALUES[$placeholder]}"
        if grep -qF "$placeholder" "$mdfile" 2>/dev/null; then
          # Escape sed special chars in value
          escaped_value="$(printf '%s' "$value" | sed 's/[&/\]/\\&/g')"
          escaped_placeholder="$(printf '%s' "$placeholder" | sed 's/[{}\[\].*^$]/\\&/g')"
          sed_inplace "s|${escaped_placeholder}|${escaped_value}|g" "$mdfile"
          modified=true
        fi
      done
      if [[ "$modified" == true ]]; then
        (( ++subst_count ))
      fi
    done < <(find "$TARGET_DIR" -name '*.md' -type f -print0)
    echo "  CONFIG  $subst_count files updated with provider config substitutions (${#CONFIG_VALUES[@]} keys)"
  fi
else
  echo "  SKIP  config — no provider config.yml found"
fi

# ── Refresh hub catalog ─────────────────────────────────────────────────────
echo ""
CATALOG_SCRIPT="$REPO_ROOT/.apm/scripts/powershell/refresh-hub-catalog.ps1"
if [[ -f "$CATALOG_SCRIPT" ]]; then
  if command -v pwsh &>/dev/null; then
    pwsh -NoProfile -File "$CATALOG_SCRIPT"
  else
    echo "  SKIP  hub-catalog — pwsh not available (install PowerShell to run refresh-hub-catalog.ps1)"
  fi
else
  echo "  SKIP  hub-catalog — refresh-hub-catalog.ps1 not found"
fi

echo ""
echo "Projection complete. Runtime assets projected to ${TARGET_DIR#"$REPO_ROOT"/}/"
