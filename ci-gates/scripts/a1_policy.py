#!/usr/bin/env python3
"""
Station A1 — Policy & Structure Validation (deterministic).

Validates YAML frontmatter of changed agent/skill files against policy rules
P-01 through P-06.  Writes station_out/a1_result.json.

Usage:
    python3 a1_policy.py \
        --work-order station_out/a0_result.json \
        --out station_out/a1_result.json \
        [--repo-root .]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Allowed tool names (P-02) ────────────────────────────────────────────
ALLOWED_TOOLS = frozenset({
    "codebase", "search", "edit/editFiles", "problems",
    "runCommands", "github", "terminal", "fetch", "vscode",
})


def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from a markdown file.

    Returns parsed dict or None if no frontmatter found.
    Uses a simple parser to avoid PyYAML dependency in CI containers that
    may not have it pre-installed (though it's typically available).
    """
    try:
        import yaml  # noqa: F811
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return None
        return yaml.safe_load(match.group(1))
    except ImportError:
        # Fallback: minimal key-value parser for flat frontmatter
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return None
        return _parse_frontmatter_fallback(match.group(1))


def _parse_frontmatter_fallback(raw: str) -> dict:
    """Minimal YAML-like parser for flat frontmatter (no nested structures)."""
    result: dict = {}
    current_key = None
    current_list: list[str] | None = None

    for line in raw.splitlines():
        # List item under current key
        list_match = re.match(r"^\s+-\s+(.*)", line)
        if list_match and current_key is not None:
            if current_list is None:
                current_list = []
            val = list_match.group(1).strip().strip("'\"")
            current_list.append(val)
            result[current_key] = current_list
            continue

        # New key
        kv_match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv_match:
            # Flush previous list
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip().strip("'\"")
            current_list = None
            if value.startswith("[") and value.endswith("]"):
                # Inline array: [a, b, c]
                items = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
                result[current_key] = items
                current_list = items
            elif value:
                result[current_key] = value
            else:
                result[current_key] = None
                current_list = []
                result[current_key] = current_list
            continue

    return result


def validate_agent(path: str, fm: dict, body: str) -> list[dict]:
    """Apply P-01 through P-06 for an agent file."""
    findings: list[dict] = []

    # P-01: Required frontmatter fields
    for field in ("name", "description", "tools"):
        if field not in fm or fm[field] is None or fm[field] == "":
            findings.append({
                "rule": "P-01",
                "severity": "critical",
                "file": path,
                "message": f"Missing required frontmatter field: '{field}'",
            })

    tools = fm.get("tools", [])
    if not isinstance(tools, list):
        tools = []

    # P-02: Tool allowlist
    for tool in tools:
        if tool not in ALLOWED_TOOLS:
            findings.append({
                "rule": "P-02",
                "severity": "critical",
                "file": path,
                "message": f"Unknown tool '{tool}' not in workspace allowlist",
            })

    # P-03: No wildcard exec — runCommands requires commandAllowlist
    if "runCommands" in tools:
        cal = fm.get("commandAllowlist")
        if not cal or (isinstance(cal, list) and len(cal) == 0):
            findings.append({
                "rule": "P-03",
                "severity": "critical",
                "file": path,
                "message": "runCommands declared without commandAllowlist",
            })

    # P-04: Network safety — fetch requires allowedNetworkDomains
    if "fetch" in tools:
        and_val = fm.get("allowedNetworkDomains")
        if not and_val or (isinstance(and_val, list) and len(and_val) == 0):
            findings.append({
                "rule": "P-04",
                "severity": "high",
                "file": path,
                "message": "fetch declared without allowedNetworkDomains",
            })
        elif isinstance(and_val, list) and "*" in and_val:
            findings.append({
                "rule": "P-04",
                "severity": "high",
                "file": path,
                "message": "allowedNetworkDomains contains wildcard '*'",
            })

    # P-05: Description quality
    desc = fm.get("description", "")
    if isinstance(desc, str) and 0 < len(desc) < 20:
        findings.append({
            "rule": "P-05",
            "severity": "low",
            "file": path,
            "message": f"Description is {len(desc)} characters — consider expanding (minimum 20)",
        })

    return findings


def validate_skill(path: str, fm: dict) -> list[dict]:
    """Apply P-01 and P-05 for a skill file."""
    findings: list[dict] = []

    # P-01: Required fields
    for field in ("name", "description", "triggers"):
        if field not in fm or fm[field] is None or fm[field] == "":
            findings.append({
                "rule": "P-01",
                "severity": "critical",
                "file": path,
                "message": f"Missing required frontmatter field: '{field}'",
            })

    # triggers must be non-empty array
    triggers = fm.get("triggers")
    if isinstance(triggers, list) and len(triggers) == 0:
        findings.append({
            "rule": "P-01",
            "severity": "critical",
            "file": path,
            "message": "triggers array is empty — at least one trigger required",
        })

    # P-05: Description quality
    desc = fm.get("description", "")
    if isinstance(desc, str) and 0 < len(desc) < 20:
        findings.append({
            "rule": "P-05",
            "severity": "low",
            "file": path,
            "message": f"Description is {len(desc)} characters — consider expanding (minimum 20)",
        })

    return findings


def summarise(findings: list[dict]) -> str:
    """Return e.g. '1 critical, 0 high, 0 medium, 0 low'."""
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity", "low")
        if sev in counts:
            counts[sev] += 1
    return ", ".join(f"{v} {k}" for k, v in counts.items())


def main() -> None:
    parser = argparse.ArgumentParser(description="A1 Policy Validation — deterministic")
    parser.add_argument("--work-order", required=True, help="Path to a0_result.json")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    # Load work order
    wo_path = Path(args.work_order)
    if not wo_path.exists():
        print(f"  ⚠ Work order not found: {wo_path}", file=sys.stderr)
        sys.exit(1)
    work_order = json.loads(wo_path.read_text(encoding="utf-8"))

    # Skip if non-agent scope
    if work_order.get("scope") == "non-agent":
        result = {
            "station": "A1",
            "status": "skipped",
            "findings": [],
            "summary": "No user-authored agent/skill files changed.",
        }
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("  → A1 skipped: non-agent scope")
        return

    repo = Path(args.repo_root)
    findings: list[dict] = []

    for cf in work_order.get("changed_files", []):
        ftype = cf.get("type")
        fpath = cf.get("path", "")

        # Exclude ci-gates/stations/ and deleted files
        if fpath.startswith("ci-gates/stations/"):
            continue
        if cf.get("change") == "deleted":
            # P-06: deleted agent without issue reference (needs PR body — skip for now)
            continue

        if ftype not in ("agent", "skill"):
            continue

        full_path = repo / fpath
        if not full_path.exists():
            continue

        text = full_path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if fm is None:
            findings.append({
                "rule": "P-01",
                "severity": "critical",
                "file": fpath,
                "message": "No YAML frontmatter found",
            })
            continue

        if ftype == "agent":
            findings.extend(validate_agent(fpath, fm, text))
        elif ftype == "skill":
            findings.extend(validate_skill(fpath, fm))

    # Determine status
    has_critical = any(f["severity"] == "critical" for f in findings)
    has_high = any(f["severity"] == "high" for f in findings)
    status = "fail" if (has_critical or has_high) else "pass"

    result = {
        "station": "A1",
        "status": status,
        "findings": findings,
        "summary": summarise(findings),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"  → A1 policy validation: {status} ({summarise(findings)})")


if __name__ == "__main__":
    main()
