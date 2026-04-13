"""
Tool and MCP invocation tracker.

Logs tool/MCP calls and skill lifecycle events as individual spans
in audit-trace.jsonl with ``span_type`` of ``tool`` or ``skill``.
"""

from __future__ import annotations

from typing import Any

from . import generate_span_id
from .state_tracker import _now_utc
from .trace_emitter import emit_trace


def log_tool_call(
    *,
    trace_id: str,
    tool: str,
    mcp_server: str | None = None,
    mcp_method: str | None = None,
    duration_ms: int | None = None,
    workflow: str = "",
    station: str = "",
    agent: str = "",
    skill: str = "",
    trace_file: str | None = None,
) -> dict[str, Any]:
    """
    Emit a ``span_type: tool`` record to audit-trace.jsonl.

    Args:
        trace_id: Correlation ID for the workflow run.
        tool: Tool name (e.g. ``codebase``, ``fetch``, ``runCommands``).
        mcp_server: MCP server ID if this is an MCP call.
        mcp_method: MCP method name.
        duration_ms: Call duration in milliseconds.
        workflow/station/agent/skill: Execution context.
        trace_file: Path to audit-trace.jsonl.

    Returns:
        The emitted trace record.
    """
    record: dict[str, Any] = {
        "trace_id": trace_id,
        "span_id": generate_span_id(),
        "parent_span_id": None,
        "timestamp": _now_utc(),
        "span_type": "tool",
        "workflow": workflow,
        "station": station,
        "agent": agent,
        "skill": skill,
        "tool_invoked": tool,
    }

    if mcp_server:
        record["mcp"] = {
            "server_id": mcp_server,
            "method": mcp_method or "",
            "external": True,
            "duration_ms": duration_ms,
        }
    elif duration_ms is not None:
        record["duration_ms"] = duration_ms

    emit_trace(record, trace_file=trace_file)
    return record


def log_skill_event(
    *,
    trace_id: str,
    skill: str,
    event: str,
    workflow: str = "",
    station: str = "",
    agent: str = "",
    trace_file: str | None = None,
) -> dict[str, Any]:
    """
    Emit a ``span_type: skill`` record for skill lifecycle events.

    Args:
        trace_id: Correlation ID for the workflow run.
        skill: Skill name.
        event: ``start`` or ``end``.
        workflow/station/agent: Execution context.
        trace_file: Path to audit-trace.jsonl.

    Returns:
        The emitted trace record.
    """
    record: dict[str, Any] = {
        "trace_id": trace_id,
        "span_id": generate_span_id(),
        "parent_span_id": None,
        "timestamp": _now_utc(),
        "span_type": "skill",
        "workflow": workflow,
        "station": station,
        "agent": agent,
        "skill": skill,
        "event": f"skill-{event}",
    }

    emit_trace(record, trace_file=trace_file)
    return record
