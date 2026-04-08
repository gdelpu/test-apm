"""Hook configuration — enable/disable hooks, set thresholds, configure OTLP."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class HookConfig:
    """Runtime configuration for the hook framework."""

    # Master switch
    enabled: bool = True

    # Individual hook toggles
    pii_scan_enabled: bool = True
    injection_detection_enabled: bool = True
    policy_check_enabled: bool = True

    # PII / redaction
    redaction_mode: str = "mask"  # "mask" | "hash" | "tag"
    pii_patterns_extra: list[str] = field(default_factory=list)

    # Risk scoring
    risk_threshold: int = 30  # score >= this → human review required
    risk_factor_weights: dict[str, float] = field(default_factory=lambda: {
        "regulated_client": 2.0,
        "external_mcp": 1.5,
        "production_data": 1.8,
        "destructive_action": 2.0,
        "autonomous_execution": 1.5,
    })
    token_cost_threshold: int = 50000  # tokens above this flag high cost

    # Context / client profile
    client_profile: str = ""  # e.g. "agoria"
    sensitivity_default: str = "internal"  # default sensitivity level
    risk_factors_active: list[str] = field(default_factory=list)

    # OTLP export (optional)
    otlp_enabled: bool = False
    otlp_endpoint: str = ""
    otlp_headers: dict[str, str] = field(default_factory=dict)

    # Policy
    allowed_tools: set[str] = field(default_factory=lambda: {
        "codebase", "search", "edit/editFiles", "problems",
        "runCommands", "github", "terminal", "fetch", "vscode",
    })


def load_config(config_path: str | None = None) -> HookConfig:
    """
    Load hook configuration from a YAML/JSON file.

    Resolution order:
    1. Explicit ``config_path`` argument
    2. ``HOOK_CONFIG_PATH`` environment variable
    3. ``<repo_root>/hook-config.json`` (auto-detected)
    4. Defaults
    """
    path = _resolve_path(config_path)
    if path is None or not path.exists():
        return HookConfig()

    raw = path.read_text(encoding="utf-8")
    data: dict[str, Any] = json.loads(raw)
    return _from_dict(data)


def _resolve_path(config_path: str | None) -> Path | None:
    if config_path:
        return Path(config_path)
    env = os.environ.get("HOOK_CONFIG_PATH")
    if env:
        return Path(env)
    # Walk up from this file to find repo root (contains apm.yml)
    current = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = current / "hook-config.json"
        if candidate.exists():
            return candidate
        if (current / "apm.yml").exists():
            return current / "hook-config.json"
        current = current.parent
    return None


def _from_dict(data: dict[str, Any]) -> HookConfig:
    cfg = HookConfig()
    for key, value in data.items():
        attr = key.replace("-", "_")
        if hasattr(cfg, attr):
            current = getattr(cfg, attr)
            # Convert list → set for set-typed fields
            if isinstance(current, set) and isinstance(value, list):
                setattr(cfg, attr, set(value))
            else:
                setattr(cfg, attr, value)
    return cfg
