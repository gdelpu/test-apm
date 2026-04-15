#!/usr/bin/env python3
"""Static CI gate: validate coding-agent-briefing.md structural schema.

Runs BEFORE provider bootstrap to ensure the briefing file produced by
sdlc-tech-architect contains only permitted sections and no injection
patterns.  Exit code 0 = pass, 1 = fail.

Checks enforced:
  1. Only permitted top-level ## sections are present.
  2. No shell command patterns (backtick-wrapped or bare).
  3. No second-person imperative sentences outside Implementation Tasks.
  4. No non-project URLs.
  5. No YAML agent keys (tools:, allowedFilePaths:, etc.).
"""

import re
import sys
from pathlib import Path

PERMITTED_SECTIONS = {
    "Project Overview",
    "Architecture References",
    "Stack Conventions",
    "File Structure",
    "Coding Standards",
    "Implementation Tasks",
    "Test Strategy",
}

# Shell / command patterns (backtick-wrapped or bare)
SHELL_PATTERNS = re.compile(
    r"(?:^|\s)(?:`[^`]*(?:sh\b|bash\b|exec|rm\s|curl\s|wget\s|docker\s|npm\s|npx\s"
    r"|pip\s|helm\s|kubectl\s|mvn\s|gradle\s|make\s|powershell|pwsh|cmd\s)[^`]*`"
    r"|(?:&&|\|\||;\s*(?:rm|curl|wget|docker|exec))\b)",
    re.IGNORECASE | re.MULTILINE,
)

# Agent / system-prompt YAML keys
AGENT_YAML_KEYS = re.compile(
    r"^(?:tools|allowedFilePaths|allowedFilePathsReadOnly|deniedReadPaths"
    r"|commandAllowlist|allowedNetworkDomains|handoffs|model):",
    re.MULTILINE,
)

# Role-reassignment / instruction-override phrases
ROLE_OVERRIDE = re.compile(
    r"(?:you are now|ignore (?:all |previous )?instructions|forget (?:all |your )"
    r"|system prompt|your new role|act as|disregard (?:the |all )?(?:above|previous))",
    re.IGNORECASE,
)

# Non-project URLs (allow relative paths and anchors, block http(s) to non-project hosts)
EXTERNAL_URL = re.compile(r"https?://(?!github\.com/|localhost[:/]|127\.0\.0\.1[:/])\S+", re.IGNORECASE)

# Second-person imperative addressed to an agent (outside permitted task descriptions)
AGENT_IMPERATIVE = re.compile(
    r"(?:^|\.\s+)(?:You must|You should|You will|Always run|Never allow|Ensure you)",
    re.MULTILINE,
)


def validate(filepath: Path) -> list[dict]:
    findings: list[dict] = []
    if not filepath.exists():
        # Not an error — file may not exist yet in this pipeline stage
        return findings

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    # --- Check 1: Only permitted sections ---
    for i, line in enumerate(lines, 1):
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            section = m.group(1).strip()
            if section not in PERMITTED_SECTIONS:
                findings.append({
                    "check": "BRF-01",
                    "severity": "high",
                    "line": i,
                    "message": f"Unpermitted section '## {section}'. Allowed: {', '.join(sorted(PERMITTED_SECTIONS))}",
                })

    # --- Check 2: Shell command patterns ---
    for m in SHELL_PATTERNS.finditer(content):
        lineno = content[:m.start()].count("\n") + 1
        findings.append({
            "check": "BRF-02",
            "severity": "high",
            "line": lineno,
            "message": f"Shell command pattern detected: {m.group().strip()[:80]}",
        })

    # --- Check 3: Agent YAML keys ---
    for m in AGENT_YAML_KEYS.finditer(content):
        lineno = content[:m.start()].count("\n") + 1
        findings.append({
            "check": "BRF-03",
            "severity": "high",
            "line": lineno,
            "message": f"Agent YAML key detected: {m.group().strip()}",
        })

    # --- Check 4: Role-override phrases ---
    for m in ROLE_OVERRIDE.finditer(content):
        lineno = content[:m.start()].count("\n") + 1
        findings.append({
            "check": "BRF-04",
            "severity": "critical",
            "line": lineno,
            "message": f"Role-override phrase detected: {m.group().strip()[:80]}",
        })

    # --- Check 5: External URLs ---
    for m in EXTERNAL_URL.finditer(content):
        lineno = content[:m.start()].count("\n") + 1
        findings.append({
            "check": "BRF-05",
            "severity": "medium",
            "line": lineno,
            "message": f"Non-project URL detected: {m.group().strip()[:100]}",
        })

    # --- Check 6: Agent imperative sentences (outside Implementation Tasks) ---
    current_section = ""
    for i, line in enumerate(lines, 1):
        sec = re.match(r"^##\s+(.+)$", line)
        if sec:
            current_section = sec.group(1).strip()
            continue
        if current_section == "Implementation Tasks":
            continue  # Task descriptions may use imperative voice
        imp = AGENT_IMPERATIVE.search(line)
        if imp:
            findings.append({
                "check": "BRF-06",
                "severity": "medium",
                "line": i,
                "message": f"Agent-addressed imperative in '## {current_section}': {imp.group().strip()[:80]}",
            })

    return findings


def main() -> int:
    briefing = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("coding-agent-briefing.md")
    findings = validate(briefing)

    if not findings:
        print(f"validate_briefing: PASS — {briefing}")
        return 0

    max_sev = max(f["severity"] for f in findings)
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        print(f"  [{f['severity'].upper()}] L{f['line']}: {f['message']}")

    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    print(f"validate_briefing: FAIL — {summary}")

    # Only block on high/critical
    if any(f["severity"] in ("high", "critical") for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
