#!/usr/bin/env bash
# tools/assemble-rules.sh — Assemble deduplicated business rules into final catalogue
#
# Usage:  bash tools/assemble-rules.sh <RULE_TYPE>
# Example: bash tools/assemble-rules.sh CAL
#
# Prerequisites: Step 0–2 completed (all staging files have dedup_done: true)
# Input:  docs/1-prd/2-specification/_rules-staging/<RULE_TYPE>/
# Output: docs/1-prd/2-specification/brl-<RULE_TYPE>-business-rules.md
# Stdout: summary (total rules, duplicates, conflicts)

set -euo pipefail

RULE_TYPE="${1:?Usage: assemble-rules.sh <RULE_TYPE>}"
STAGING_DIR="docs/1-prd/2-specification/_rules-staging/$RULE_TYPE"
OUTPUT="docs/1-prd/2-specification/brl-${RULE_TYPE}-business-rules.md"
TODAY=$(date +%Y-%m-%d)

# ── Validate prerequisites ───────────────────────────────────────────

if [[ ! -d "$STAGING_DIR" ]]; then
  echo "ERROR: staging directory not found: $STAGING_DIR" >&2; exit 1
fi

BASE_FILE="$STAGING_DIR/_base.md"
if [[ ! -f "$BASE_FILE" ]]; then
  echo "ERROR: _base.md not found in $STAGING_DIR" >&2; exit 1
fi

if [[ ! -f docs/project.yml ]]; then
  echo "ERROR: docs/project.yml not found" >&2; exit 1
fi

# ── Read project metadata ────────────────────────────────────────────

PROJECT_NAME=$(grep 'project_name:' docs/project.yml | head -1 | sed 's/.*: *//')
LANG=$(grep 'lang:' docs/project.yml | head -1 | sed 's/.*: *//')

# Rule type display names
case "$RULE_TYPE" in
  VAL) TYPE_NAME="Validation"   ;;
  CAL) TYPE_NAME="Calculation"  ;;
  TRG) TYPE_NAME="Trigger"      ;;
  COH) TYPE_NAME="Consistency"  ;;
  AUT) TYPE_NAME="Authorisation";;
  *)   TYPE_NAME="$RULE_TYPE"   ;;
esac

# ── Collect source files in order ────────────────────────────────────

FEATURE_FILES=()
while IFS= read -r f; do
  FEATURE_FILES+=("$f")
done < <(ls "$STAGING_DIR"/rules-from-ep-*.md 2>/dev/null | sort)

# ── extract_rules: strip front matter, H1/H2, Production confidence ─

extract_rules() {
  awk '
    NR==1 && /^---$/ { in_yaml=1; next }
    in_yaml && /^---$/ { in_yaml=0; skip=1; next }
    in_yaml { next }
    /^## Production confidence/ { exit }
    /^### \[BR-/ { skip=0 }
    /^# /  { next }
    /^## / { next }
    !skip  { print }
  ' "$1"
}

# ── Assemble rule blocks into temp file ──────────────────────────────

RULES_TMP=$(mktemp)
trap 'rm -f "$RULES_TMP"' EXIT

extract_rules "$BASE_FILE" > "$RULES_TMP"

for f in "${FEATURE_FILES[@]}"; do
  content=$(extract_rules "$f")
  # Skip files where all rules were duplicates
  if [[ -n "$content" ]] && ! echo "$content" | grep -q "All rules from this source were duplicates"; then
    echo "" >> "$RULES_TMP"
    echo "$content" >> "$RULES_TMP"
  fi
done

TOTAL_RULES=$(grep -c '^### \[BR-' "$RULES_TMP" || true)

# ── Build entity index ───────────────────────────────────────────────

ENTITY_INDEX=$(awk '
/^### \[BR-/ {
  match($0, /\[BR-[A-Z]+-[0-9]+\]/)
  rule = substr($0, RSTART, RLENGTH)
}
rule != "" {
  line = $0
  while (match(line, /\[ENT-[0-9]+\]/)) {
    ent = substr(line, RSTART, RLENGTH)
    key = ent SUBSEP rule
    if (!(key in seen)) {
      entities[ent] = (ent in entities) ? entities[ent] ", " rule : rule
      seen[key] = 1
    }
    line = substr(line, RSTART + RLENGTH)
  }
}
END {
  for (ent in entities) print "| " ent " | " entities[ent] " |"
}
' "$RULES_TMP" | sort -t'-' -k2 -n)

# ── Build feature index ──────────────────────────────────────────────

FEATURE_INDEX=$(awk '
/^### \[BR-/ {
  match($0, /\[BR-[A-Z]+-[0-9]+\]/)
  rule = substr($0, RSTART, RLENGTH)
}
rule != "" {
  line = $0
  while (match(line, /\[FT-[0-9]+\]/)) {
    ft = substr(line, RSTART, RLENGTH)
    key = ft SUBSEP rule
    if (!(key in seen)) {
      features[ft] = (ft in features) ? features[ft] ", " rule : rule
      seen[key] = 1
    }
    line = substr(line, RSTART + RLENGTH)
  }
}
END {
  for (ft in features) print "| " ft " | " features[ft] " |"
}
' "$RULES_TMP" | sort -t'-' -k2 -n)

# ── Build production confidence from YAML front matter ───────────────

BASE_COUNT=$(grep -m1 'rules_count:' "$BASE_FILE" | awk '{print $2}' || true)
BASE_DEDUP=$(grep -m1 'duplicates_removed:' "$BASE_FILE" | awk '{print $2}' || true)
BASE_COUNT=${BASE_COUNT:-0}
BASE_DEDUP=${BASE_DEDUP:-0}

INVENTORY="| _base.md (domain + epics) | ${BASE_COUNT} | ${BASE_DEDUP} |"
TOTAL_DEDUP=$BASE_DEDUP

for f in "${FEATURE_FILES[@]}"; do
  fname=$(basename "$f")
  dedup=$(awk '/^duplicates_removed:/{print $2; exit}' "$f" || true)
  dedup=${dedup:-0}
  remaining=$(grep -c '^### \[BR-' "$f" || true)
  INVENTORY="$INVENTORY
| $fname | $remaining | $dedup |"
  TOTAL_DEDUP=$((TOTAL_DEDUP + dedup))
done

# ── Detect cross-epic near-duplicate formulas ────────────────────────

CONFLICTS=$(awk '
/^### \[BR-/ {
  match($0, /\[BR-[A-Z]+-[0-9]+\]/)
  rule = substr($0, RSTART, RLENGTH)
}
rule != "" && /^\| \*\*Formula\*\*/ {
  formula = $0
  gsub(/^\| \*\*Formula\*\* \| /, "", formula)
  gsub(/ \|[[:space:]]*$/, "", formula)
  # Normalize whitespace for comparison
  gsub(/[[:space:]]+/, " ", formula)
  if (formula in seen_formulas) {
    print "| " rule " | " seen_formulas[formula] " | Similar formula |"
  }
  seen_formulas[formula] = rule
}
' "$RULES_TMP")

CONFLICT_COUNT=0
if [[ -n "$CONFLICTS" ]]; then
  CONFLICT_COUNT=$(echo "$CONFLICTS" | wc -l | tr -d ' ')
fi

# ── Write final output file ──────────────────────────────────────────

cat > "$OUTPUT" <<EOF
---
id: "BRL-${RULE_TYPE}"
title: "${TYPE_NAME} Rules Catalogue — ${PROJECT_NAME}"
phase: 2-specification
type: business-rules
rule_type: "${RULE_TYPE}"
status: draft
version: "1.0"
last_updated: ${TODAY}
author: agent-rules
reviewers: []
dependencies: ["VIS-001", "GLO-001", "ACT-001"]
---

# [BRL-${RULE_TYPE}] ${TYPE_NAME} Rules Catalogue

## Rule type

| Type | Description | Prefix |
|------|-------------|--------|
| ${RULE_TYPE} | ${TYPE_NAME} rules | BR-${RULE_TYPE} |

---

## Rules

EOF

cat "$RULES_TMP" >> "$OUTPUT"

# Attention Points (only if conflicts)
if [[ -n "$CONFLICTS" ]]; then
  cat >> "$OUTPUT" <<EOF

---

## Attention Points

> [PA-001] Cross-epic near-duplicate formulas detected. These were not caught by the fold/reduce algorithm (which only compares each feature file against _base.md, not against other feature files). Review and merge manually if appropriate.

| Rule | Near-duplicate of | Detail |
|------|-------------------|--------|
${CONFLICTS}

EOF
fi

cat >> "$OUTPUT" <<EOF

---

## Rules index by entity

| Entity | Associated rules |
|--------|-----------------|
${ENTITY_INDEX}

## Rules index by feature

| Feature | Associated rules |
|---------|-----------------|
${FEATURE_INDEX}

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-rules (${RULE_TYPE}) |
| **Production date** | ${TODAY} |
| **Inputs used** | [VIS-001], [GLO-001], [ACT-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |

## Production confidence

### Source inventory

| Source file | Rules kept | Duplicates removed |
|-------------|-----------|-------------------|
${INVENTORY}

### Summary

| Dimension | Value |
|-----------|-------|
| **Total rules in catalogue** | ${TOTAL_RULES} |
| **Total duplicates removed (all steps)** | ${TOTAL_DEDUP} |
| **Cross-epic near-duplicates flagged** | ${CONFLICT_COUNT} |
| **Global score** | 3/3 CONFIDENT — Mechanical assembly from pre-deduplicated staging files |
EOF

# ── Stdout summary ───────────────────────────────────────────────────

echo "=== assemble-rules.sh: ${RULE_TYPE} ==="
echo "Output:    ${OUTPUT}"
echo "Rules:     ${TOTAL_RULES}"
echo "Dedup:     ${TOTAL_DEDUP}"
echo "Conflicts: ${CONFLICT_COUNT}"
echo "Done."
