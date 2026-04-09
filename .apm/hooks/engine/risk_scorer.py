"""
Hook 6: Risk scoring.

Extends the canonical risk-scoring skill formula with context-aware
risk factors (regulated client, external MCP, production data,
destructive actions, autonomous execution, high token cost).

Human-review threshold is configurable (default ≥ 30).
"""

from __future__ import annotations

from typing import Any

from .config import HookConfig

# ---------------------------------------------------------------------------
# Severity weights (from .apm/skills/risk-scoring/SKILL.md)
# ---------------------------------------------------------------------------
_SEVERITY_WEIGHTS: dict[str, int] = {
    "critical": 10,
    "high": 7,
    "medium": 4,
    "low": 1,
}

# Category multipliers (base set from risk-scoring skill)
_CATEGORY_MULTIPLIERS: dict[str, float] = {
    "security": 1.5,
    "pii": 1.3,
}


def score_risk(
    *,
    pre_findings: dict[str, Any],
    output_pii: dict[str, Any],
    context: dict[str, Any],
    config: HookConfig,
) -> dict[str, Any]:
    """
    Compute weighted risk score from pre-hook findings, output PII scan,
    and context classification.

    Returns:
        {
            "score": int,
            "level": "low" | "medium" | "high" | "critical",
            "factors": list of contributing factor labels,
            "human_review_required": bool,
            "human_review_reason": str,
            "breakdown": {factor: points},
        }
    """
    score = 0.0
    factors: list[str] = []
    breakdown: dict[str, float] = {}

    # --- Score from injection findings ---
    inj = pre_findings.get("injection_findings", {})
    for finding in inj.get("findings", []):
        severity = finding.get("severity", "medium")
        weight = _SEVERITY_WEIGHTS.get(severity, 4)
        points = weight * _CATEGORY_MULTIPLIERS["security"]
        score += points
        label = f"injection:{finding.get('check', 'unknown')}"
        factors.append(label)
        breakdown[label] = points

    # --- Score from policy violations ---
    pol = pre_findings.get("policy_findings", {})
    for violation in pol.get("violations", []):
        # Advisory violations score lower
        if "advisory" in violation:
            points = _SEVERITY_WEIGHTS["low"] * _CATEGORY_MULTIPLIERS["security"]
        else:
            points = _SEVERITY_WEIGHTS["high"] * _CATEGORY_MULTIPLIERS["security"]
        score += points
        label = f"policy:{violation.split(':')[0]}"
        factors.append(label)
        breakdown[label] = breakdown.get(label, 0) + points

    # --- Score from input PII findings ---
    input_pii = pre_findings.get("pii_findings", {})
    if input_pii.get("found"):
        count = input_pii.get("count", 0)
        pii_types = input_pii.get("types", [])
        points = min(count * _SEVERITY_WEIGHTS["medium"], 40) * _CATEGORY_MULTIPLIERS["pii"]
        score += points
        factors.append("input-pii")
        breakdown["input-pii"] = points
        # Secrets in input are critical
        if any(t in ("secret-key", "aws-secret", "github-pat", "openai-key", "pem-key")
               for t in pii_types):
            secret_points = _SEVERITY_WEIGHTS["critical"] * _CATEGORY_MULTIPLIERS["security"]
            score += secret_points
            factors.append("input-secrets")
            breakdown["input-secrets"] = secret_points

    # --- Score from output PII findings ---
    if output_pii.get("found"):
        count = output_pii.get("count", 0)
        points = min(count * _SEVERITY_WEIGHTS["medium"], 40) * _CATEGORY_MULTIPLIERS["pii"]
        score += points
        factors.append("output-pii")
        breakdown["output-pii"] = points

    # --- Context-based risk factors ---
    risk_factors = context.get("risk_factors", [])
    factor_weights = config.risk_factor_weights

    for factor in risk_factors:
        if factor in factor_weights:
            # Context factors add a base score multiplied by their weight
            base = _SEVERITY_WEIGHTS["medium"]
            multiplier = factor_weights[factor]
            points = base * multiplier
            score += points
            factors.append(factor)
            breakdown[factor] = points

    # --- Classify ---
    score_int = int(round(score))
    level = _classify(score_int)

    # --- Human review decision ---
    human_review = score_int >= config.risk_threshold
    review_reasons: list[str] = []

    if score_int >= config.risk_threshold:
        review_reasons.append(f"risk score {score_int} >= threshold {config.risk_threshold}")
    if "regulated_client" in risk_factors:
        human_review = True
        review_reasons.append("regulated client")
    if "destructive_action" in risk_factors:
        human_review = True
        review_reasons.append("destructive action flagged")
    if "production_data" in risk_factors:
        human_review = True
        review_reasons.append("production data exposure")

    return {
        "score": score_int,
        "level": level,
        "factors": sorted(set(factors)),
        "human_review_required": human_review,
        "human_review_reason": "; ".join(review_reasons) if review_reasons else "",
        "breakdown": breakdown,
    }


def _classify(score: int) -> str:
    """Map numeric score to risk level."""
    if score <= 10:
        return "low"
    if score <= 30:
        return "medium"
    if score <= 60:
        return "high"
    return "critical"
