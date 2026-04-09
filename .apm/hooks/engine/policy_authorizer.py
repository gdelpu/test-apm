"""
Hook 4: Policy / tool authorization.

Runtime policy checks derived from scripts/check_policy.py (P-01–P-06).
Verifies agent has permission for requested tools, files, and network access.
"""

from __future__ import annotations

from typing import Any

from .config import HookConfig


def authorize(
    *,
    agent: str,
    skill: str,
    tools: list[str],
    config: HookConfig,
) -> dict[str, Any]:
    """
    Verify that an agent's requested tools are within the allowed set
    and that required constraints (commandAllowlist, allowedNetworkDomains)
    are declared.

    This is a runtime check complementing the static P-01–P-06 validation
    in ``scripts/check_policy.py``.

    Returns:
        {
            "blocked": True if critical violations found,
            "violations": list of violation descriptions,
            "checks_passed": list of passed check IDs,
        }
    """
    violations: list[str] = []
    passed: list[str] = []

    # P-02: Tool allowlist
    for tool in tools:
        if tool not in config.allowed_tools:
            violations.append(f"P-02: unknown tool '{tool}' for agent '{agent}'")

    if not violations or all("P-02" not in v for v in violations):
        passed.append("P-02")

    # P-03: runCommands requires commandAllowlist
    # At runtime we flag if runCommands is requested without prior static check
    if "runCommands" in tools:
        # This is a warning — the static check (check_policy.py) should have
        # caught missing commandAllowlist at PR time.  At runtime we flag it
        # for the risk scorer.
        violations.append(
            f"P-03-advisory: agent '{agent}' uses runCommands — "
            "ensure commandAllowlist is declared in agent manifest"
        )
    else:
        passed.append("P-03")

    # P-04: fetch requires allowedNetworkDomains
    if "fetch" in tools:
        violations.append(
            f"P-04-advisory: agent '{agent}' uses fetch — "
            "ensure allowedNetworkDomains is declared in agent manifest"
        )
    else:
        passed.append("P-04")

    # Determine if any violation is blocking (only hard P-02 violations block)
    hard_violations = [v for v in violations if not v.endswith("-advisory")]
    blocked = len(hard_violations) > 0

    return {
        "blocked": blocked,
        "violations": violations,
        "checks_passed": passed,
    }
