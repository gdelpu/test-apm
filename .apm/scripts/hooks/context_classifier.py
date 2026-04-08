"""Hook 1: Context classification — assemble metadata for downstream hooks."""

from __future__ import annotations

from typing import Any

from .config import HookConfig


def classify_context(
    *,
    workflow: str,
    station: str,
    agent: str,
    skill: str,
    provider: str,
    extra: dict[str, Any],
    config: HookConfig,
) -> dict[str, Any]:
    """
    Build context metadata from workflow/station/agent/skill identifiers,
    client profile, and execution-mode indicators.

    Returns a dict consumed by downstream hooks (PII scanner sensitivity,
    risk scorer factor activation, trace emitter fields).
    """
    sensitivity_level = config.sensitivity_default
    sensitivity_tags: list[str] = []
    risk_factors: list[str] = list(config.risk_factors_active)
    tools: list[str] = extra.get("tools", [])

    # --- Derive sensitivity from station/skill names ---
    if _contains_any(station, ("pii", "compliance", "governance")):
        sensitivity_tags.append("compliance-context")

    if _contains_any(skill, ("security", "injection", "red-team")):
        sensitivity_tags.append("security-context")

    # --- Client profile escalation ---
    if config.client_profile:
        sensitivity_tags.append(f"client:{config.client_profile}")
        # Regulated clients get higher sensitivity
        if "regulated_client" not in risk_factors:
            risk_factors.append("regulated_client")
        sensitivity_level = "confidential"

    # --- Execution-mode indicators from extra context ---
    if extra.get("autonomous"):
        risk_factors.append("autonomous_execution")
    if extra.get("destructive"):
        risk_factors.append("destructive_action")
    if extra.get("production_data"):
        risk_factors.append("production_data")
        sensitivity_level = "restricted"
        sensitivity_tags.append("production-data")
    if extra.get("external_mcp"):
        risk_factors.append("external_mcp")
        sensitivity_tags.append("external-mcp")

    # --- Tool-based escalation ---
    if "runCommands" in tools:
        sensitivity_tags.append("exec-tool")
    if "fetch" in tools:
        sensitivity_tags.append("network-access")

    return {
        "workflow": workflow,
        "station": station,
        "agent": agent,
        "skill": skill,
        "provider": provider,
        "sensitivity_level": sensitivity_level,
        "sensitivity_tags": list(set(sensitivity_tags)),
        "risk_factors": list(set(risk_factors)),
        "tools": tools,
        "client_profile": config.client_profile,
        "extra": extra,
    }


def _contains_any(value: str, terms: tuple[str, ...]) -> bool:
    """Case-insensitive substring match against multiple terms."""
    lower = value.lower()
    return any(t in lower for t in terms)
