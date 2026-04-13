#!/usr/bin/env python3
"""
Station A0 — Intake (deterministic replacement for LLM-based intake).

Classifies changed files by artefact type, computes risk hints from the diff,
determines PR scope, and writes outputs/station_out/a0_result.json.

Usage:
    python3 a0_intake.py \
        --changed-files outputs/station_out/changed_files.txt \
        --diff outputs/station_out/diff.patch \
        --out outputs/station_out/a0_result.json \
        [--mr-iid 42]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── File-type classification by path pattern ──────────────────────────────
TYPE_PATTERNS: list[tuple[str, str]] = [
    (r"agents/.*\.agent\.md$", "agent"),
    (r"skills/.*/SKILL\.md$", "skill"),
    (r"prompts/.*\.prompt\.md$", "prompt"),
    (r"instructions/.*\.instructions\.md$", "instruction"),
    (r"\.github/workflows/.*\.yml$", "workflow"),
]

# ── Risk-hint patterns (applied to the full diff) ─────────────────────────
RISK_PATTERNS: list[tuple[str, str]] = [
    (r"tools:\s*\[.*runCommands", "exec-tool"),
    (r"tools:.*runCommands", "exec-tool"),
    (r"(?<!allowed)NetworkDomains.*\*", "unconstrained-network"),
    (r"allowedFilePaths.*(\*\*|/\*)", "unconstrained-files"),
    (r"(curl|wget|bash|sh)\s.*\|", "shell-pipe"),
    (r"eval\s*\(", "eval-usage"),
]

CHANGE_MAP = {"A": "added", "M": "modified", "D": "deleted"}


def classify_file(path: str) -> str:
    """Return the artefact type for a file path."""
    for pattern, file_type in TYPE_PATTERNS:
        if re.search(pattern, path):
            return file_type
    return "other"


def parse_changed_files(text: str) -> list[dict]:
    """Parse git diff --name-status output into structured entries."""
    entries = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        status_code, path = parts[0][0], parts[-1]
        entries.append({
            "path": path,
            "type": classify_file(path),
            "change": CHANGE_MAP.get(status_code, "modified"),
        })
    return entries


def compute_risk_hints(diff_text: str, changed_files: list[dict]) -> list[str]:
    """Scan the diff for risk indicators."""
    hints: set[str] = set()
    for pattern, hint in RISK_PATTERNS:
        if re.search(pattern, diff_text, re.IGNORECASE):
            hints.add(hint)

    # Check for allowedNetworkDomains absent when fetch is in tools
    if re.search(r"tools:.*fetch", diff_text, re.IGNORECASE):
        if not re.search(r"allowedNetworkDomains:", diff_text):
            hints.add("unconstrained-network")

    # Check for allowedFilePaths absent or wildcard
    if not re.search(r"allowedFilePaths:", diff_text):
        pass  # only flag if file-ops tools are present (handled at higher level)

    # Deleted agents
    for f in changed_files:
        if f["type"] == "agent" and f["change"] == "deleted":
            hints.add("agent-removed")

    return sorted(hints)


def determine_scope(changed_files: list[dict]) -> str:
    """Return 'agent-change' if any agent/skill/prompt/instruction changed."""
    agent_types = {"agent", "skill", "prompt", "instruction"}
    if any(f["type"] in agent_types for f in changed_files):
        return "agent-change"
    return "non-agent"


def build_diff_summary(changed_files: list[dict], risk_hints: list[str]) -> str:
    """Build a one-line summary of the changes."""
    type_counts: dict[str, int] = {}
    for f in changed_files:
        type_counts[f["type"]] = type_counts.get(f["type"], 0) + 1
    parts = [f"{count} {ftype}" for ftype, count in sorted(type_counts.items())]
    summary = f"Changed files: {', '.join(parts)}."
    if risk_hints:
        summary += f" Risk hints: {', '.join(risk_hints)}."
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="A0 Intake — deterministic PR classifier")
    parser.add_argument("--changed-files", required=True, help="Path to changed_files.txt")
    parser.add_argument("--diff", required=True, help="Path to diff.patch")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--mr-iid", default=os.environ.get("CI_MERGE_REQUEST_IID", "0"))
    args = parser.parse_args()

    # Read inputs
    changed_text = Path(args.changed_files).read_text(encoding="utf-8", errors="replace") if Path(args.changed_files).exists() else ""
    diff_text = Path(args.diff).read_text(encoding="utf-8", errors="replace") if Path(args.diff).exists() else ""

    changed_files = parse_changed_files(changed_text)
    risk_hints = compute_risk_hints(diff_text, changed_files)
    scope = determine_scope(changed_files)

    result = {
        "station": "A0",
        "status": "pass",
        "pr_number": int(args.mr_iid) if str(args.mr_iid).isdigit() else 0,
        "scope": scope,
        "changed_files": changed_files,
        "risk_hints": risk_hints,
        "diff_summary": build_diff_summary(changed_files, risk_hints),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"  → A0 intake complete: scope={scope}, {len(changed_files)} files, {len(risk_hints)} risk hints")


if __name__ == "__main__":
    main()
