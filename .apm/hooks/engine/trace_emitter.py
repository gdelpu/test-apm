"""
Hook 7: Structured audit trace emitter.

Writes trace records as JSON Lines to a per-workflow-run file.
Optionally exports to an OTLP endpoint when configured.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .config import HookConfig

logger = logging.getLogger(__name__)


def emit_trace(
    record: dict[str, Any],
    *,
    trace_file: str | None = None,
    config: HookConfig | None = None,
) -> None:
    """
    Append a trace record to the JSONL trace file and optionally
    export via OTLP.

    Args:
        record: The structured trace record dict (see schema).
        trace_file: Explicit path to the JSONL file.  Falls back to
                     ``specs/features/<feature>/audit-trace.jsonl``.
        config: Hook configuration (for OTLP settings).
    """
    # --- Local JSONL ---
    if trace_file:
        _write_jsonl(trace_file, record)
    else:
        logger.debug("No trace file specified — trace record not persisted locally")

    # --- Optional OTLP export ---
    if config and config.otlp_enabled and config.otlp_endpoint:
        _export_otlp(record, config)


def _write_jsonl(path: str, record: dict[str, Any]) -> None:
    """Append a single JSON object as one line to the trace file."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str, ensure_ascii=False))
        f.write("\n")


def _export_otlp(record: dict[str, Any], config: HookConfig) -> None:
    """
    Export trace record to an OTLP endpoint.

    Requires ``opentelemetry-api`` and ``opentelemetry-exporter-otlp-proto-http``
    as optional dependencies.  Silently skips if not installed.
    """
    try:
        from opentelemetry import trace as otel_trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
    except ImportError:
        logger.debug(
            "opentelemetry packages not installed — OTLP export skipped. "
            "Install with: pip install opentelemetry-api opentelemetry-sdk "
            "opentelemetry-exporter-otlp-proto-http"
        )
        return

    try:
        exporter = OTLPSpanExporter(
            endpoint=config.otlp_endpoint,
            headers=config.otlp_headers or {},
        )
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        tracer = provider.get_tracer("ssg-ai-hooks")

        with tracer.start_as_current_span(
            name=f"hook.{record.get('hook_name', 'audit-trace')}",
        ) as span:
            span.set_attribute("trace_id", record.get("trace_id", ""))
            span.set_attribute("workflow", record.get("workflow", ""))
            span.set_attribute("station", record.get("station", ""))
            span.set_attribute("agent", record.get("agent", ""))
            span.set_attribute("skill", record.get("skill", ""))
            span.set_attribute("risk.score", record.get("risk", {}).get("score", 0))
            span.set_attribute("risk.level", record.get("risk", {}).get("level", "low"))
            span.set_attribute(
                "sensitivity.level",
                record.get("sensitivity", {}).get("level", "internal"),
            )

        provider.shutdown()
    except Exception:
        logger.warning("OTLP export failed", exc_info=True)
