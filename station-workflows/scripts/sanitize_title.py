#!/usr/bin/env python3
"""
Reads a string from stdin, applies NFKC unicode normalization to defeat
encoding-based injection tricks, strips control/format characters, and
outputs the first 200 characters to stdout.

Usage:
    printf '%s' "$MR_TITLE" | python3 sanitize_title.py
"""

import sys
import unicodedata

text = sys.stdin.read()
text = unicodedata.normalize("NFKC", text)
text = "".join(
    ch for ch in text if unicodedata.category(ch) not in ("Cc", "Cf")
)
sys.stdout.write(text[:200])
