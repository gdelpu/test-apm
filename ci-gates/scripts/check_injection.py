#!/usr/bin/env python3
"""
Checks sys.argv[1] for known prompt-injection patterns.

Exits 0 (match found → block) if the title contains a pattern.
Exits 1 (no match → allow) otherwise.

Usage:
    python3 check_injection.py "$SAFE_TITLE"
    if [ $? -eq 0 ]; then echo "BLOCKED"; fi
"""

import re
import sys

PATTERNS = [
    r"system\s*:",
    r"ignore\s+(previous|above|all)",
    r"you\s+are\s+now",
    r"override\s*:",
    r"jailbreak",
    r"disregard\s+(previous|all)",
    r"forget\s+(previous|all|everything)",
    r"\bact\s+as\b",
    r"pretend\s+(you|to)",
    r"new\s+instructions?",
]

title = sys.argv[1].lower() if len(sys.argv) > 1 else ""
sys.exit(0 if any(re.search(p, title) for p in PATTERNS) else 1)
