#!/usr/bin/env bash
# push-docs.sh — Push docs/ to the Activity Tracking showcase repo
# Usage: bash tools/push-docs.sh ["commit message"]
#
# SAFE: uses a temporary GIT_INDEX_FILE — never touches the working tree,
# current branch, or .git/index. No checkout, no branch switch.

set -e

REMOTE="docs-origin"
MSG="${1:-chore: update deliverables}"

echo "Building docs-only commit (working tree untouched)..."

TEMP_INDEX=$(mktemp).gitindex
trap 'rm -f "$TEMP_INDEX"' EXIT

GIT_INDEX_FILE="$TEMP_INDEX" git add -f docs/
TREE=$(GIT_INDEX_FILE="$TEMP_INDEX" git write-tree)
COMMIT=$(git commit-tree "$TREE" -m "$MSG

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>")

echo "Force-pushing to $REMOTE/master..."
git push --force "$REMOTE" "$COMMIT:master"

echo "Done — docs/ pushed to $REMOTE (commit $COMMIT)"
