#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# dispatch-rules-to-features.sh
#
# Reads all deduplicated business rules from _rules-staging/
# and dispatches them into per-feature business-rules.md files.
#
# Sources:
#   _rules-staging/{TYPE}/_base.md          (domain + epic rules)
#   _rules-staging/{TYPE}/rules-from-ep-*.md (feature-level rules)
#
# Output per feature:
#   outputs/docs/1-prd/3-epics/{epic}/{feature}/business-rules.md
#
# Logic:
#   - Rules with "Related features | [FT-xxx]" → dispatched to FT-xxx
#   - Rules with "Related features | --" (domain rules) → dispatched to
#     ALL features that reference the same entity (inclusion large)
#   - Rules are grouped by type (VAL, CAL, TRG, COH, AUT) in the output
# ─────────────────────────────────────────────────────────────

set -euo pipefail

DOCS_ROOT="outputs/1-prd"
STAGING="$DOCS_ROOT/2-specification/_rules-staging"
EPICS_DIR="$DOCS_ROOT/3-epics"

# ── Step 0: Build entity→features mapping ──────────────────
# Read each feature spec to know which entities it references
declare -A ENTITY_TO_FEATURES  # entity → "FT-001 FT-002 ..."

echo "Building entity → features mapping..."
for ft_file in "$EPICS_DIR"/ep-*/ft-*/ft-*.md; do
  [ -f "$ft_file" ] || continue
  ft_id=$(grep -oE 'id:[[:space:]]*FT-[0-9]+' "$ft_file" | head -1 | grep -oE 'FT-[0-9]+' || true)
  [ -z "$ft_id" ] && continue

  # Extract entity references [ENT-xxx] from the file
  entities=$(grep -oE '\[ENT-[0-9]+\]' "$ft_file" | sort -u | tr '\n' ' ' || true)
  for ent in $entities; do
    ent_clean=$(echo "$ent" | tr -d '[]')
    ENTITY_TO_FEATURES[$ent_clean]="${ENTITY_TO_FEATURES[$ent_clean]:-} $ft_id"
  done
done

# ── Step 1: Build feature→directory mapping ─────────────────
declare -A FT_DIR  # FT-001 → outputs/docs/1-prd/3-epics/ep-001-.../ft-001-.../

echo "Building feature → directory mapping..."
for ft_dir in "$EPICS_DIR"/ep-*/ft-*/; do
  [ -d "$ft_dir" ] || continue
  ft_id=$(basename "$ft_dir" | grep -oE 'ft-[0-9]+' | sed 's/ft-/FT-/' || true)
  [ -z "$ft_id" ] && continue
  FT_DIR[$ft_id]="$ft_dir"
done

echo "Found ${#FT_DIR[@]} feature directories."

# ── Step 2: Parse rules and dispatch ────────────────────────
# Temporary directory for collecting rules per feature per type
TMP_DISPATCH=$(mktemp -d)
trap "rm -rf $TMP_DISPATCH" EXIT

parse_and_dispatch() {
  local file="$1"
  local rule_type="$2"

  # Split file into individual rule blocks (delimiter: ### [BR-)
  # Each block starts with ### [BR-xxx] and ends before the next ### [BR- or EOF
  local current_block=""
  local current_rule_id=""

  while IFS= read -r line; do
    # Detect new rule block
    if [[ "$line" =~ ^###[[:space:]]+\[BR- ]]; then
      # Flush previous block
      if [ -n "$current_rule_id" ] && [ -n "$current_block" ]; then
        dispatch_rule "$current_block" "$rule_type" "$file"
      fi
      current_rule_id=$(echo "$line" | grep -oE '\[BR-[A-Z]+-[A-Z]?[0-9]+\]' || echo "$line")
      current_block="$line"$'\n'
    elif [[ "$line" =~ ^##[[:space:]] ]] && [[ ! "$line" =~ ^### ]]; then
      # Section header (## FT-xxx) — flush and skip
      if [ -n "$current_rule_id" ] && [ -n "$current_block" ]; then
        dispatch_rule "$current_block" "$rule_type" "$file"
      fi
      current_rule_id=""
      current_block=""
    elif [ -n "$current_rule_id" ]; then
      current_block+="$line"$'\n'
    fi
  done < "$file"

  # Flush last block
  if [ -n "$current_rule_id" ] && [ -n "$current_block" ]; then
    dispatch_rule "$current_block" "$rule_type" "$file"
  fi
}

dispatch_rule() {
  local block="$1"
  local rule_type="$2"
  local source_file="$3"

  # Extract related features
  local related
  related=$(echo "$block" | grep 'Related features' | sed 's/.*|[[:space:]]*//' | head -1 | tr -d ' ' || true)

  if [[ "$related" == "--" ]] || [[ -z "$related" ]]; then
    # Domain rule: no specific feature — dispatch to all features sharing the entity
    local entities
    entities=$(echo "$block" | grep -oE '\[ENT-[0-9]+\]' | sort -u || true)
    local target_features=""
    for ent in $entities; do
      ent_clean=$(echo "$ent" | tr -d '[]')
      target_features+=" ${ENTITY_TO_FEATURES[$ent_clean]:-}"
    done
    # Deduplicate
    target_features=$(echo "$target_features" | tr ' ' '\n' | sort -u | tr '\n' ' ')
  else
    # Feature-specific rule: parse [FT-xxx], [FT-yyy]
    target_features=$(echo "$related" | grep -oE 'FT-[0-9]+' | sort -u | tr '\n' ' ')
  fi

  # Dispatch to each target feature
  for ft_id in $target_features; do
    [ -z "$ft_id" ] && continue
    local ft_dir="${FT_DIR[$ft_id]:-}"
    [ -z "$ft_dir" ] && continue

    # Append to temp file for this feature+type
    local tmp_file="$TMP_DISPATCH/${ft_id}___${rule_type}"
    echo "$block" >> "$tmp_file"
    echo "---" >> "$tmp_file"
    echo "" >> "$tmp_file"
  done
}

# Process all staging files
echo "Parsing rules..."
for type_dir in "$STAGING"/*/; do
  [ -d "$type_dir" ] || continue
  rule_type=$(basename "$type_dir")

  # Process _base.md (domain + epic rules)
  base_file="$STAGING/${rule_type}/_base.md"
  if [ -f "$base_file" ]; then
    echo "  Processing $base_file"
    parse_and_dispatch "$base_file" "$rule_type"
  fi

  # Process per-epic files (feature-level rules)
  for ep_file in "$type_dir"/rules-from-ep-*.md; do
    [ -f "$ep_file" ] || continue
    echo "  Processing $ep_file"
    parse_and_dispatch "$ep_file" "$rule_type"
  done
done

# ── Step 3: Assemble per-feature business-rules.md ──────────
echo "Assembling per-feature files..."
assembled=0

for ft_id in "${!FT_DIR[@]}"; do
  ft_dir="${FT_DIR[$ft_id]}"
  output="$ft_dir/business-rules.md"

  # Check if any type files exist for this feature
  has_rules=false
  for tf in "$TMP_DISPATCH/${ft_id}"___*; do
    [ -f "$tf" ] && has_rules=true && break
  done

  $has_rules || continue

  # Write header
  ft_name=$(basename "$ft_dir")
  cat > "$output" << EOF
---
type: business-rules
feature: $ft_id
generated_by: dispatch-rules-to-features.sh
date: $(date +%Y-%m-%d)
---

# Business Rules — $ft_id

EOF

  # Append each type section
  for tf in "$TMP_DISPATCH/${ft_id}"___*; do
    [ -f "$tf" ] || continue
    rule_type=$(echo "$tf" | sed "s/.*___//")
    echo "## $rule_type Rules" >> "$output"
    echo "" >> "$output"
    cat "$tf" >> "$output"
    echo "" >> "$output"
  done

  assembled=$((assembled + 1))
done

echo ""
echo "Done. Dispatched rules to $assembled feature directories."
echo "Output: {feature-dir}/business-rules.md"

# ── Step 4: Remove staging directory ────────────────────────
echo ""
echo "Cleaning up staging directory..."
rm -rf "$STAGING"
echo "Removed: $STAGING"
