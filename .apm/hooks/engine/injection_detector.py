"""
Hook 3: Prompt-injection detection.

Deterministic regex scan implementing PI-01 through PI-06 checks.
Refactored from ci-gates/scripts/check_injection.py and
ci-gates/stations/a3-prompt-injection.prompt.md patterns.
"""

from __future__ import annotations

import re
from typing import Any

# ---------------------------------------------------------------------------
# PI-01: Jailbreak / instruction-override phrases
# ---------------------------------------------------------------------------
_PI01_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ignore\s+(previous|above|all)", re.I),
    re.compile(r"disregard\s+(previous|all)", re.I),
    re.compile(r"forget\s+(previous|all|everything)", re.I),
    re.compile(r"you\s+are\s+now", re.I),
    re.compile(r"pretend\s+(you|to)", re.I),
    re.compile(r"developer\s+mode", re.I),
    re.compile(r"\[SYSTEM\]|\[INST\]", re.I),
    re.compile(r"system\s*:", re.I),
    re.compile(r"override\s*:", re.I),
    re.compile(r"jailbreak", re.I),
    re.compile(r"\bact\s+as\b", re.I),
    re.compile(r"new\s+instructions?", re.I),
]

# ---------------------------------------------------------------------------
# PI-02: Missing refusal anchors (checked at agent-definition level, not content)
# Included here for completeness but scored as info, not block.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# PI-03: Unconstrained input markers
# ---------------------------------------------------------------------------
_PI03_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\{\{?\s*user[_\s]*input\s*\}?\}", re.I),
    re.compile(r"\$\{user[_\s]*input\}", re.I),
    re.compile(r"<user[_\-]?input>", re.I),
]

# ---------------------------------------------------------------------------
# PI-04: Exfiltration vectors
# ---------------------------------------------------------------------------
_PI04_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"curl\s+.*\|\s*(?:bash|sh)", re.I),
    re.compile(r"wget\s+.*\|\s*(?:bash|sh)", re.I),
    re.compile(r"fetch\s*\(\s*['\"]https?://", re.I),
    re.compile(r"send\s+(?:to|data|results?)\s+(?:to\s+)?(?:http|external|remote)", re.I),
]

# ---------------------------------------------------------------------------
# PI-05: Resource exhaustion signals
# ---------------------------------------------------------------------------
_PI05_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:repeat|loop|iterate)\s+(?:forever|infinitely|until)", re.I),
    re.compile(r"no\s+(?:limit|bounds?|cap)", re.I),
]

# ---------------------------------------------------------------------------
# PI-06: Tool misuse (unscoped commands)
# ---------------------------------------------------------------------------
_PI06_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"eval\s*\(", re.I),
    re.compile(r"subprocess\.call\s*\(\s*.*shell\s*=\s*True", re.I),
    re.compile(r"rm\s+-rf\s+/", re.I),
    re.compile(r"chmod\s+777", re.I),
]


def detect_injection(content: str) -> dict[str, Any]:
    """
    Scan content for prompt-injection patterns (PI-01 through PI-06).

    Returns:
        {
            "blocked": True if critical patterns found,
            "patterns": list of matched pattern IDs,
            "findings": [
                {"check": "PI-01", "severity": "critical", "pattern": "<matched text>", ...},
            ],
        }
    """
    findings: list[dict[str, Any]] = []
    blocked = False

    # PI-01 — critical: jailbreak
    for pat in _PI01_PATTERNS:
        m = pat.search(content)
        if m:
            findings.append({
                "check": "PI-01",
                "severity": "critical",
                "label": "jailbreak",
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })
            blocked = True

    # PI-03 — high: unconstrained inputs
    for pat in _PI03_PATTERNS:
        m = pat.search(content)
        if m:
            findings.append({
                "check": "PI-03",
                "severity": "high",
                "label": "unconstrained-input",
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })

    # PI-04 — high: exfiltration
    for pat in _PI04_PATTERNS:
        m = pat.search(content)
        if m:
            findings.append({
                "check": "PI-04",
                "severity": "high",
                "label": "exfiltration",
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })
            blocked = True

    # PI-05 — medium: resource exhaustion
    for pat in _PI05_PATTERNS:
        m = pat.search(content)
        if m:
            findings.append({
                "check": "PI-05",
                "severity": "medium",
                "label": "resource-exhaustion",
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })

    # PI-06 — high: tool misuse
    for pat in _PI06_PATTERNS:
        m = pat.search(content)
        if m:
            findings.append({
                "check": "PI-06",
                "severity": "high",
                "label": "tool-misuse",
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })

    pattern_ids = sorted(set(f["check"] for f in findings))

    return {
        "blocked": blocked,
        "patterns": pattern_ids,
        "findings": findings,
    }
