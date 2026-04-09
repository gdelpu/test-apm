"""
Hook 2 + 5: PII / sensitive-data scanner and redactor.

Regex-based detection for common PII patterns.  Supports three redaction
modes: mask, hash, tag.  Zero external dependencies (stdlib only).
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

from .config import HookConfig

# ---------------------------------------------------------------------------
# Pattern registry — each entry is (label, compiled regex)
# ---------------------------------------------------------------------------

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Email
    ("email", re.compile(
        r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
    )),
    # Phone (international, with optional leading +)
    ("phone", re.compile(
        r"(?<!\d)(?:\+?\d{1,3}[\s\-.]?)?\(?\d{1,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{2,4}(?!\d)"
    )),
    # SSN (US)
    ("ssn", re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b"
    )),
    # Credit card (Visa, MC, Amex — basic Luhn-length check)
    ("credit-card", re.compile(
        r"\b(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2})[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{3,4}\b"
    )),
    # IPv4
    ("ipv4", re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b"
    )),
    # IBAN (2-letter country code + 2 check digits + up to 30 alphanumeric)
    ("iban", re.compile(
        r"\b[A-Z]{2}\d{2}[\s]?[\dA-Z]{4}[\s]?(?:[\dA-Z]{4}[\s]?){1,7}[\dA-Z]{1,4}\b"
    )),
    # Belgian national number (rijksregisternummer: YY.MM.DD-SSS.CC)
    ("belgian-rrn", re.compile(
        r"\b\d{2}\.\d{2}\.\d{2}-\d{3}\.\d{2}\b"
    )),
    # Date of birth (patterns: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
    ("date-of-birth", re.compile(
        r"\b(?:\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))\b"
        r"|\b(?:(?:0[1-9]|[12]\d|3[01])[/\-](?:0[1-9]|1[0-2])[/\-]\d{4})\b"
    )),
    # High-entropy secrets (API keys, tokens — 20+ hex or base64-ish chars)
    ("secret-key", re.compile(
        r"\b(?:ghp_[A-Za-z0-9]{36})\b"               # GitHub PAT
        r"|\b(?:sk-[A-Za-z0-9]{32,})\b"               # OpenAI key
        r"|\b(?:AKIA[A-Z0-9]{16})\b"                  # AWS access key
        r"|-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"   # PEM private key
    )),
]

# Placeholder when scanning for specific content types
_SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws-secret", re.compile(r"\b(?:AKIA[A-Z0-9]{16})\b")),
    ("github-pat", re.compile(r"\b(?:ghp_[A-Za-z0-9]{36})\b")),
    ("openai-key", re.compile(r"\b(?:sk-[A-Za-z0-9]{32,})\b")),
    ("pem-key", re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
    ("generic-token", re.compile(
        r"(?i)\b(?:token|api[_\-]?key|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{20,}['\"]?"
    )),
]


def scan_pii(content: str, *, config: HookConfig | None = None) -> dict[str, Any]:
    """
    Scan content for PII and sensitive data patterns.

    Returns:
        {
            "found": bool,
            "count": total match count,
            "types": list of matched PII type labels,
            "matches": {type: [{"start": int, "end": int, "value": "<masked>"}]},
        }
    """
    all_patterns = list(_PATTERNS) + list(_SECRET_PATTERNS)

    # Append any extra patterns from config
    if config and config.pii_patterns_extra:
        for i, pat_str in enumerate(config.pii_patterns_extra):
            all_patterns.append((f"custom-{i}", re.compile(pat_str)))

    types_found: list[str] = []
    matches: dict[str, list[dict[str, Any]]] = {}
    total_count = 0

    for label, pattern in all_patterns:
        hits = list(pattern.finditer(content))
        if hits:
            if label not in types_found:
                types_found.append(label)
            match_list = []
            for m in hits:
                # Never include the full value — just position + masked preview
                val = m.group()
                masked = val[:2] + "***" + val[-2:] if len(val) > 4 else "***"
                match_list.append({
                    "start": m.start(),
                    "end": m.end(),
                    "preview": masked,
                })
            matches[label] = matches.get(label, []) + match_list
            total_count += len(hits)

    return {
        "found": total_count > 0,
        "count": total_count,
        "types": types_found,
        "matches": matches,
    }


def redact_pii(content: str, *, config: HookConfig | None = None) -> str:
    """
    Redact PII in content using the configured redaction mode.

    Modes:
      - mask:  replace with ``[REDACTED:<type>]``
      - hash:  replace with deterministic token ``[HASH:<hex8>]``
      - tag:   no modification (scan-only)
    """
    mode = "mask"
    if config:
        mode = config.redaction_mode

    if mode == "tag":
        return content

    all_patterns = list(_PATTERNS) + list(_SECRET_PATTERNS)
    if config and config.pii_patterns_extra:
        for i, pat_str in enumerate(config.pii_patterns_extra):
            all_patterns.append((f"custom-{i}", re.compile(pat_str)))

    # Collect all match spans with their labels, sort by position descending
    # to replace from end to start (preserving earlier offsets)
    spans: list[tuple[int, int, str, str]] = []
    for label, pattern in all_patterns:
        for m in pattern.finditer(content):
            spans.append((m.start(), m.end(), label, m.group()))

    # Sort descending by start position
    spans.sort(key=lambda s: s[0], reverse=True)

    # Remove overlapping spans (keep the first one found)
    filtered: list[tuple[int, int, str, str]] = []
    occupied_end = len(content) + 1
    for start, end, label, value in spans:
        if end <= occupied_end:
            filtered.append((start, end, label, value))
            occupied_end = start

    for start, end, label, value in filtered:
        if mode == "hash":
            token = hashlib.sha256(value.encode()).hexdigest()[:8]
            replacement = f"[HASH:{token}]"
        else:
            replacement = f"[REDACTED:{label}]"
        content = content[:start] + replacement + content[end:]

    return content


def scan_retroactive(file_path: str, *, config: HookConfig | None = None) -> dict[str, Any]:
    """
    Scan an existing file for PII (retroactive mode).

    Returns scan results without modifying the file.
    """
    from pathlib import Path

    text = Path(file_path).read_text(encoding="utf-8")
    return scan_pii(text, config=config)
