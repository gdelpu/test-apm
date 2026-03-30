#!/usr/bin/env python3
"""
HMAC-SHA256 sign or verify a file using a shared secret from the environment.

Usage:
    # Sign (writes <file>.hmac):
    python3 hmac_artifact.py sign gate_decision.json

    # Verify (reads <file>.hmac, exits non-zero on mismatch):
    python3 hmac_artifact.py verify gate_decision.json

Requires: ARTIFACT_HMAC_KEY env var (set as a CI/CD masked variable).
Falls back to SHA256 checksum if ARTIFACT_HMAC_KEY is not set (with a warning).
"""

import hashlib
import hmac
import os
import sys


def get_key() -> bytes | None:
    key = os.environ.get("ARTIFACT_HMAC_KEY", "")
    return key.encode() if key else None


def compute_hmac(filepath: str, key: bytes) -> str:
    h = hmac.new(key, digestmod=hashlib.sha256)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sign(filepath: str) -> None:
    key = get_key()
    if key:
        sig = compute_hmac(filepath, key)
        method = "hmac-sha256"
    else:
        sys.stderr.write(
            "WARNING: ARTIFACT_HMAC_KEY not set; falling back to SHA256 checksum.\n"
        )
        sig = compute_sha256(filepath)
        method = "sha256"

    sig_path = filepath + ".sig"
    with open(sig_path, "w") as f:
        f.write(f"{method}:{sig}\n")
    print(f"Signed {filepath} -> {sig_path} ({method})")


def verify(filepath: str) -> None:
    sig_path = filepath + ".sig"
    if not os.path.exists(sig_path):
        sys.stderr.write(f"WARNING: No signature file {sig_path}; skipping verification.\n")
        return

    with open(sig_path) as f:
        line = f.read().strip()

    if ":" not in line:
        sys.stderr.write(f"ERROR: Malformed signature file {sig_path}\n")
        sys.exit(1)

    method, expected = line.split(":", 1)
    key = get_key()

    if method == "hmac-sha256":
        if not key:
            sys.stderr.write("ERROR: Signature requires ARTIFACT_HMAC_KEY but it is not set.\n")
            sys.exit(1)
        actual = compute_hmac(filepath, key)
    elif method == "sha256":
        actual = compute_sha256(filepath)
    else:
        sys.stderr.write(f"ERROR: Unknown signature method '{method}'\n")
        sys.exit(1)

    if not hmac.compare_digest(actual, expected):
        sys.stderr.write(f"ERROR: {filepath} integrity check FAILED ({method} mismatch)\n")
        sys.exit(1)

    print(f"Verified {filepath} ({method})")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("sign", "verify"):
        sys.stderr.write("Usage: hmac_artifact.py sign|verify <file>\n")
        sys.exit(1)
    action, path = sys.argv[1], sys.argv[2]
    if action == "sign":
        sign(path)
    else:
        verify(path)
