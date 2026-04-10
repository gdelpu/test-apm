#!/usr/bin/env python3
"""
Station A3 — Prompt Injection & Exfil Hardening Checks (deterministic).

Scans changed agent/skill/prompt files for jailbreak phrases, missing safety
constraints, unconstrained tool scope, exfiltration vectors, and indirect
injection patterns.  Writes outputs/station_out/a3_result.json.

Usage:
    python3 a3_injection.py \
        --work-order outputs/station_out/a0_result.json \
        --out outputs/station_out/a3_result.json \
        [--repo-root .]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── PI-01: Jailbreak / instruction-override phrases ──────────────────────
PI01_PATTERNS: list[tuple[str, str]] = [
    (r"ignore\s+(all|previous|above|prior)\s+instructions?", "Classic instruction override"),
    (r"disregard\s+(your|all)\s+(previous|prior)", "Instruction override variant"),
    (r"you\s+(are|were)\s+now\s+(a|an)\b", "Role reassignment"),
    (r"pretend\s+(you\s+are|to\s+be)", "Persona hijack"),
    (r"do\s+anything\s+now", "DAN jailbreak"),
    (r"\bDAN\b", "DAN jailbreak acronym"),
    (r"your\s+(new|real|true)\s+instructions", "System prompt override attempt"),
    (r"developer\s+mode", "Developer-mode jailbreak"),
    (r"\[SYSTEM\]", "Injected system-role delimiter"),
    (r"\[INST\]", "Injected instruction delimiter"),
]

# ── PI-02: Required non-negotiable constraints ──────────────────────────
PI02_REFUSE_PATTERNS = [
    r"(must\s+not|will\s+not|never)\s+.{0,30}(delete|modify|send|exfiltrate|bypass)",
    r"refuse\s+.{0,20}(request|instruction|attempt)",
    r"out\s+of\s+scope",
]

# ── PI-05: Exfiltration via fetch / URL construction ─────────────────────
PI05_PATTERNS: list[tuple[str, str, str]] = [
    (r"\$\{[^}]*\}\s*.*https?://", "Template variable in URL construction", "high"),
    (r"\{\{[^}]*\}\}\s*.*https?://", "Mustache template in URL construction", "high"),
    (r"https?://.*\$\{", "URL with template variable", "high"),
    (r"https?://.*\{\{", "URL with mustache template", "high"),
    (r"https?://(webhook|hook|exfil|ngrok|pipedream|requestbin)", "Suspicious webhook/data-sink URL", "medium"),
]

# ── PI-06: Indirect injection vectors ────────────────────────────────────
PI06_PATTERN = r"(read|process|execute|follow).{0,40}(file|document|webpage|url).{0,40}(instruct|step|direct)"


def is_in_safe_codeblock(text: str, match_start: int) -> bool:
    """Check if a match position is inside a fenced code block with a safety comment."""
    # Find all code blocks
    code_blocks = list(re.finditer(r"```[^\n]*\n(.*?)```", text, re.DOTALL))
    safety_comments = re.compile(
        r"#\s*(example|do\s+not\s+follow|do\s+not\s+interpret|detection\s+patterns)",
        re.IGNORECASE,
    )
    for block in code_blocks:
        if block.start() <= match_start <= block.end():
            if safety_comments.search(block.group(0)):
                return True
    return False


def scan_pi01(path: str, text: str) -> list[dict]:
    """PI-01: Jailbreak/instruction-override phrases."""
    findings = []
    lines = text.splitlines()
    for pattern, description in PI01_PATTERNS:
        for i, line in enumerate(lines, 1):
            m = re.search(pattern, line, re.IGNORECASE)
            if m and not is_in_safe_codeblock(text, text.find(line)):
                findings.append({
                    "check": "PI-01",
                    "severity": "critical" if "override" in description.lower() or "delimiter" in description.lower() else "high",
                    "file": path,
                    "line": i,
                    "match": m.group(0),
                    "message": f"Jailbreak pattern: {description}",
                })
    return findings


def scan_pi02(path: str, text: str, ftype: str) -> list[dict]:
    """PI-02: Required non-negotiable system constraints (agents only)."""
    if ftype != "agent":
        return []

    for pattern in PI02_REFUSE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return []  # At least one constraint found

    return [{
        "check": "PI-02",
        "severity": "high",
        "file": path,
        "line": None,
        "match": None,
        "message": "Agent body contains no non-negotiable refusal constraints (must not / will not / never / refuse / out of scope).",
    }]


def scan_pi03(path: str, fm: dict, ftype: str) -> list[dict]:
    """PI-03: Data access boundary declarations for skills with file tools."""
    if ftype != "skill":
        return []
    tools = fm.get("tools", [])
    if not isinstance(tools, list):
        return []

    file_tools = {"codebase", "edit/editFiles", "search"}
    if not any(t in file_tools for t in tools):
        return []

    afp = fm.get("allowedFilePaths")
    if not afp:
        return [{
            "check": "PI-03",
            "severity": "high",
            "file": path,
            "line": None,
            "match": None,
            "message": "Skill with file operation tools missing allowedFilePaths declaration.",
        }]

    if isinstance(afp, list):
        for p in afp:
            if p in ("**", "/*", "/**"):
                return [{
                    "check": "PI-03",
                    "severity": "high",
                    "file": path,
                    "line": None,
                    "match": p,
                    "message": f"allowedFilePaths contains wildcard '{p}'.",
                }]
    return []


def scan_pi04(path: str, fm: dict, ftype: str) -> list[dict]:
    """PI-04: Unconstrained tool scope."""
    findings = []
    tools = fm.get("tools", [])
    if not isinstance(tools, list):
        tools = []

    # tools: ["*"] or ["all"]
    if "*" in tools or "all" in tools:
        findings.append({
            "check": "PI-04",
            "severity": "critical",
            "file": path,
            "line": None,
            "match": str(tools),
            "message": "Tools contain wildcard — unrestricted tool access.",
        })

    if "runCommands" in tools:
        cal = fm.get("commandAllowlist")
        if not cal or (isinstance(cal, list) and len(cal) == 0):
            findings.append({
                "check": "PI-04",
                "severity": "high",
                "file": path,
                "line": None,
                "match": None,
                "message": "runCommands without commandAllowlist (prompt-security layer).",
            })

    if "fetch" in tools:
        and_val = fm.get("allowedNetworkDomains")
        if not and_val or (isinstance(and_val, list) and len(and_val) == 0):
            findings.append({
                "check": "PI-04",
                "severity": "high",
                "file": path,
                "line": None,
                "match": None,
                "message": "fetch without allowedNetworkDomains.",
            })

    return findings


def scan_pi05(path: str, text: str) -> list[dict]:
    """PI-05: Exfiltration via fetch / URL construction."""
    findings = []
    lines = text.splitlines()
    for pattern, description, severity in PI05_PATTERNS:
        for i, line in enumerate(lines, 1):
            m = re.search(pattern, line, re.IGNORECASE)
            if m and not is_in_safe_codeblock(text, text.find(line)):
                findings.append({
                    "check": "PI-05",
                    "severity": severity,
                    "file": path,
                    "line": i,
                    "match": m.group(0),
                    "message": f"Exfiltration vector: {description}",
                })
    return findings


def scan_pi06(path: str, text: str) -> list[dict]:
    """PI-06: Indirect injection vectors."""
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        m = re.search(PI06_PATTERN, line, re.IGNORECASE)
        if m and not is_in_safe_codeblock(text, text.find(line)):
            findings.append({
                "check": "PI-06",
                "severity": "critical",
                "file": path,
                "line": i,
                "match": m.group(0),
                "message": "Indirect injection: instruction to follow external content without sandboxing.",
            })
    return findings


def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from markdown."""
    try:
        import yaml
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return None
        return yaml.safe_load(match.group(1)) or {}
    except ImportError:
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return None
        return _parse_frontmatter_minimal(match.group(1))


def _parse_frontmatter_minimal(raw: str) -> dict:
    """Minimal fallback parser."""
    result: dict = {}
    current_key = None
    for line in raw.splitlines():
        list_match = re.match(r"^\s+-\s+(.*)", line)
        if list_match and current_key is not None:
            if not isinstance(result.get(current_key), list):
                result[current_key] = []
            result[current_key].append(list_match.group(1).strip().strip("'\""))
            continue
        kv_match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv_match:
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip().strip("'\"")
            if value.startswith("[") and value.endswith("]"):
                result[current_key] = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
            elif value:
                result[current_key] = value
            else:
                result[current_key] = []
    return result


def summarise(findings: list[dict]) -> str:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity", "low")
        if sev in counts:
            counts[sev] += 1
    return ", ".join(f"{v} {k}" for k, v in counts.items())


def main() -> None:
    parser = argparse.ArgumentParser(description="A3 Prompt Injection Checks — deterministic")
    parser.add_argument("--work-order", required=True, help="Path to a0_result.json")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    wo_path = Path(args.work_order)
    if not wo_path.exists():
        print(f"  ⚠ Work order not found: {wo_path}", file=sys.stderr)
        sys.exit(1)
    work_order = json.loads(wo_path.read_text(encoding="utf-8"))

    # Skip if non-agent scope
    if work_order.get("scope") == "non-agent":
        result = {
            "station": "A3",
            "status": "skipped",
            "red_team_ran": False,
            "findings": [],
            "summary": "No user-authored agent/skill/prompt files changed.",
        }
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("  → A3 skipped: non-agent scope")
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
            continue
        if ftype not in ("agent", "skill", "prompt"):
            continue

        full_path = repo / fpath
        if not full_path.exists():
            continue

        text = full_path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text) or {}

        findings.extend(scan_pi01(fpath, text))
        findings.extend(scan_pi02(fpath, text, ftype))
        findings.extend(scan_pi03(fpath, fm, ftype))
        findings.extend(scan_pi04(fpath, fm, ftype))
        findings.extend(scan_pi05(fpath, text))
        findings.extend(scan_pi06(fpath, text))

    has_critical = any(f["severity"] == "critical" for f in findings)
    has_high = any(f["severity"] == "high" for f in findings)
    status = "fail" if (has_critical or has_high) else "pass"

    result = {
        "station": "A3",
        "status": status,
        "red_team_ran": False,
        "findings": findings,
        "summary": summarise(findings),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"  → A3 prompt injection checks: {status} ({summarise(findings)})")


if __name__ == "__main__":
    main()
