"""
Audit tracing and data anonymisation hook framework.

Pre-hooks run before model/tool interactions to classify context,
scan/redact PII, detect prompt injection, and authorize tools.

Post-hooks run after interactions to scan outputs, score risk,
and emit structured audit traces.
"""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any

from .config import HookConfig, load_config
from .context_classifier import classify_context
from .injection_detector import detect_injection
from .pii_scanner import scan_pii, redact_pii
from .policy_authorizer import authorize
from .risk_scorer import score_risk
from .trace_emitter import emit_trace

__all__ = [
    "run_pre_hooks",
    "run_post_hooks",
    "generate_trace_id",
    "generate_span_id",
]


def generate_trace_id() -> str:
    """Generate a correlation ID for a workflow run."""
    return str(uuid.uuid4())


def generate_span_id() -> str:
    """Generate a unique span ID for a single hook/station invocation."""
    return str(uuid.uuid4())


def _content_hash(content: str) -> str:
    """SHA-256 hash of content — never store raw content in traces."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def run_pre_hooks(
    *,
    content: str,
    trace_id: str,
    parent_span_id: str | None = None,
    workflow: str = "",
    station: str = "",
    agent: str = "",
    skill: str = "",
    provider: str = "cli",
    config_path: str | None = None,
    extra_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Execute the pre-hook chain (context → PII scan → injection → policy).

    Returns a dict with:
      - content: the (possibly redacted) content
      - blocked: True if any hook blocked execution
      - block_reason: reason for block (if any)
      - context: assembled context metadata
      - pii_findings: PII scan results
      - injection_findings: injection scan results
      - policy_findings: policy check results
      - spans: list of trace spans emitted
    """
    cfg = load_config(config_path)
    spans: list[dict[str, Any]] = []
    result: dict[str, Any] = {
        "content": content,
        "blocked": False,
        "block_reason": None,
        "context": {},
        "pii_findings": {},
        "injection_findings": {},
        "policy_findings": {},
        "spans": spans,
    }

    if not cfg.enabled:
        return result

    now = datetime.now(timezone.utc).isoformat()

    # --- Hook 1: Context classification ---
    span_id = generate_span_id()
    ctx = classify_context(
        workflow=workflow,
        station=station,
        agent=agent,
        skill=skill,
        provider=provider,
        extra=extra_context or {},
        config=cfg,
    )
    result["context"] = ctx
    spans.append({
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_span_id": parent_span_id,
        "timestamp": now,
        "hook_phase": "pre",
        "hook_name": "context-classification",
        "workflow": workflow,
        "station": station,
        "agent": agent,
        "skill": skill,
    })

    # --- Hook 2: PII / sensitive-data scan ---
    if cfg.pii_scan_enabled:
        span_id = generate_span_id()
        pii_result = scan_pii(content, config=cfg)
        result["pii_findings"] = pii_result

        if pii_result["found"] and cfg.redaction_mode != "tag":
            content = redact_pii(content, config=cfg)
            result["content"] = content

        spans.append({
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hook_phase": "pre",
            "hook_name": "pii-scan",
            "sensitivity": {
                "pii_types": pii_result.get("types", []),
                "redaction_applied": pii_result["found"] and cfg.redaction_mode != "tag",
                "patterns_matched": pii_result.get("count", 0),
            },
            "input_hash": _content_hash(content),
        })

    # --- Hook 3: Prompt-injection detection ---
    if cfg.injection_detection_enabled:
        span_id = generate_span_id()
        inj_result = detect_injection(content)
        result["injection_findings"] = inj_result

        if inj_result["blocked"]:
            result["blocked"] = True
            result["block_reason"] = f"Prompt injection detected: {inj_result['patterns']}"

        spans.append({
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hook_phase": "pre",
            "hook_name": "injection-detection",
            "blocked": inj_result["blocked"],
            "patterns": inj_result.get("patterns", []),
        })

    # --- Hook 4: Policy / tool authorization ---
    if cfg.policy_check_enabled:
        span_id = generate_span_id()
        pol_result = authorize(
            agent=agent,
            skill=skill,
            tools=ctx.get("tools", []),
            config=cfg,
        )
        result["policy_findings"] = pol_result

        if pol_result.get("blocked"):
            result["blocked"] = True
            result["block_reason"] = (
                result.get("block_reason", "") or ""
            ) + f" Policy violation: {pol_result['violations']}"

        spans.append({
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hook_phase": "pre",
            "hook_name": "policy-authorization",
            "blocked": pol_result.get("blocked", False),
            "violations": pol_result.get("violations", []),
        })

    return result


def run_post_hooks(
    *,
    output: str,
    pre_result: dict[str, Any],
    trace_id: str,
    parent_span_id: str | None = None,
    workflow: str = "",
    station: str = "",
    agent: str = "",
    skill: str = "",
    provider: str = "cli",
    tool_invoked: str = "",
    model_name: str = "",
    tokens_in: int | None = None,
    tokens_out: int | None = None,
    cost_usd: float | None = None,
    latency_ms: int | None = None,
    config_path: str | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """
    Execute the post-hook chain (output scan → risk scoring → audit trace).

    Returns a dict with:
      - output: the (possibly redacted) output
      - risk: risk assessment result
      - trace_record: the full audit trace record
      - human_review_required: whether human review is needed
    """
    cfg = load_config(config_path)
    result: dict[str, Any] = {
        "output": output,
        "risk": {},
        "trace_record": {},
        "human_review_required": False,
    }

    if not cfg.enabled:
        return result

    ctx = pre_result.get("context", {})

    # --- Hook 5: Output secret/PII scan ---
    output_pii = {"found": False, "types": [], "count": 0}
    if cfg.pii_scan_enabled:
        output_pii = scan_pii(output, config=cfg)
        if output_pii["found"] and cfg.redaction_mode != "tag":
            output = redact_pii(output, config=cfg)
            result["output"] = output

    # --- Hook 6: Risk scoring ---
    risk = score_risk(
        pre_findings=pre_result,
        output_pii=output_pii,
        context=ctx,
        config=cfg,
    )
    result["risk"] = risk
    result["human_review_required"] = risk.get("human_review_required", False)

    # --- Hook 7: Structured audit trace ---
    input_content = pre_result.get("content", "")
    trace_record = {
        "trace_id": trace_id,
        "span_id": generate_span_id(),
        "parent_span_id": parent_span_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workflow": workflow,
        "station": station,
        "agent": agent,
        "skill": skill,
        "tool_invoked": tool_invoked,
        "input_hash": _content_hash(input_content),
        "output_hash": _content_hash(output),
        "sensitivity": {
            "level": ctx.get("sensitivity_level", "internal"),
            "tags": ctx.get("sensitivity_tags", []),
            "pii_types": list(
                set(
                    pre_result.get("pii_findings", {}).get("types", [])
                    + output_pii.get("types", [])
                )
            ),
            "redaction_applied": (
                pre_result.get("pii_findings", {}).get("found", False)
                or output_pii.get("found", False)
            )
            and cfg.redaction_mode != "tag",
        },
        "risk": {
            "score": risk.get("score", 0),
            "level": risk.get("level", "low"),
            "factors": risk.get("factors", []),
            "human_review_required": risk.get("human_review_required", False),
            "human_review_reason": risk.get("human_review_reason", ""),
        },
        "model": {
            "provider": provider,
            "name": model_name or None,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_usd": cost_usd,
            "latency_ms": latency_ms,
        },
        "redaction": {
            "status": _redaction_status(pre_result, output_pii, cfg),
            "patterns_matched": (
                pre_result.get("pii_findings", {}).get("count", 0)
                + output_pii.get("count", 0)
            ),
            "types_redacted": list(
                set(
                    pre_result.get("pii_findings", {}).get("types", [])
                    + output_pii.get("types", [])
                )
            ),
        },
    }
    result["trace_record"] = trace_record

    emit_trace(trace_record, trace_file=trace_file, config=cfg)

    return result


def _redaction_status(
    pre_result: dict[str, Any],
    output_pii: dict[str, Any],
    cfg: HookConfig,
) -> str:
    """Determine redaction status label."""
    had_pii = (
        pre_result.get("pii_findings", {}).get("found", False)
        or output_pii.get("found", False)
    )
    if not had_pii:
        return "not-required"
    if cfg.redaction_mode == "tag":
        return "skipped"
    return "applied"
