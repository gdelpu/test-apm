"""
Provider-independent workflow state tracker.

Replaces the bash-only state-manager.sh with a Python implementation
that all three providers (CLI, Copilot, Claude Code) can call.

State is persisted as a Markdown table in workflow-state.md (same format
as the original bash implementation) and workflow-level spans are emitted
to audit-trace.jsonl for full observability.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import generate_span_id, generate_trace_id
from .trace_emitter import emit_trace

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_STATUS_VALUES = {"pending", "running", "passed", "failed", "skipped"}
_GATE_VALUES = {"pass", "fail", "warning", "blocked-by-hook", "—"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def init_workflow(
    *,
    state_file: str,
    workflow: str,
    feature: str,
    stations: list[str],
    trace_id: str | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """
    Create the workflow-state.md file and emit a ``span_type: workflow``
    root span to audit-trace.jsonl.

    If the state file already exists (resume case), returns the existing
    trace_id without overwriting.

    Returns:
        dict with ``trace_id``, ``state_file``, ``created`` (bool).
    """
    path = Path(state_file)
    tid = trace_id or generate_trace_id()

    # Resume guard — don't overwrite existing state
    if path.exists():
        existing_tid = _read_trace_id(path)
        return {
            "trace_id": existing_tid or tid,
            "state_file": str(path),
            "created": False,
        }

    now = _now_utc()
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Workflow State: {workflow}",
        "",
        f"**Feature**: {feature}",
        f"**Started**: {now}",
        "**Status**: in-progress",
        f"**Trace ID**: {tid}",
        "",
        "| Station | Status | Started | Completed | Gate |",
        "|---------|--------|---------|-----------|------|",
    ]
    for sid in stations:
        lines.append(f"| {sid} | pending | — | — | — |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Emit workflow root span
    _emit_span(
        trace_id=tid,
        trace_file=trace_file,
        span_type="workflow",
        workflow=workflow,
        station="",
        event="workflow-init",
        metadata={"feature": feature, "stations": stations},
    )

    return {"trace_id": tid, "state_file": str(path), "created": True}


def update_station(
    *,
    state_file: str,
    station_id: str,
    status: str,
    gate: str = "—",
    trace_id: str | None = None,
    trace_file: str | None = None,
    workflow: str = "",
    agent: str = "",
    skill: str = "",
) -> dict[str, Any]:
    """
    Update a station row in workflow-state.md and emit a station span.

    Args:
        state_file: Path to workflow-state.md.
        station_id: Station ID to update.
        status: New status (pending|running|passed|failed|skipped).
        gate: Gate result (pass|fail|warning|blocked-by-hook|—).
        trace_id: Correlation ID (reads from state file if omitted).
        trace_file: Path to audit-trace.jsonl.
        workflow: Workflow name (for trace record).
        agent: Agent name (for trace record).
        skill: Skill name (for trace record).

    Returns:
        dict with ``station_id``, ``status``, ``gate``, ``timestamp``.
    """
    if status not in _STATUS_VALUES:
        raise ValueError(f"Invalid status '{status}'; must be one of {_STATUS_VALUES}")

    path = Path(state_file)
    if not path.exists():
        raise FileNotFoundError(f"State file not found: {state_file}")

    now = _now_utc()
    content = path.read_text(encoding="utf-8")
    tid = trace_id or _read_trace_id(path) or ""

    # Build replacement row
    completed = now if status in ("passed", "failed", "skipped") else "—"
    new_row = f"| {station_id} | {status} | {now} | {completed} | {gate} |"

    # Match existing row for this station (preserve started time for non-initial updates)
    pattern = re.compile(
        rf"^\| {re.escape(station_id)} \|[^\n]*$", re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        raise ValueError(f"Station '{station_id}' not found in state file")

    # Preserve original started timestamp if transitioning from running→passed/failed
    old_row = match.group(0)
    old_started = _extract_field(old_row, 2)
    if old_started != "—" and status != "running":
        new_row = f"| {station_id} | {status} | {old_started} | {completed} | {gate} |"

    content = pattern.sub(new_row, content, count=1)

    # Update overall workflow status if all stations resolved
    if _all_resolved(content):
        overall = "passed" if "| failed |" not in content else "failed"
        content = re.sub(
            r"\*\*Status\*\*: in-progress",
            f"**Status**: {overall}",
            content,
        )

    path.write_text(content, encoding="utf-8")

    # Emit station span
    _emit_span(
        trace_id=tid,
        trace_file=trace_file,
        span_type="station",
        workflow=workflow,
        station=station_id,
        event=f"station-{status}",
        metadata={"gate": gate, "agent": agent, "skill": skill},
    )

    return {
        "station_id": station_id,
        "status": status,
        "gate": gate,
        "timestamp": now,
    }


def query_state(
    *,
    state_file: str,
) -> dict[str, Any]:
    """
    Parse workflow-state.md and return structured JSON.

    Returns:
        dict with ``workflow``, ``feature``, ``status``, ``trace_id``,
        ``stations`` (list of dicts), ``current_station`` (first non-passed).
    """
    path = Path(state_file)
    if not path.exists():
        raise FileNotFoundError(f"State file not found: {state_file}")

    content = path.read_text(encoding="utf-8")

    # Parse header fields
    workflow = _extract_header(content, "Workflow State")
    feature = _extract_header_field(content, "Feature")
    status = _extract_header_field(content, "Status")
    trace_id = _extract_header_field(content, "Trace ID")

    # Parse station table rows
    stations: list[dict[str, str]] = []
    current_station: str | None = None
    for m in re.finditer(
        r"^\| (\S+) \| (\S+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
        content,
        re.MULTILINE,
    ):
        sid, st, started, completed, gate = (
            m.group(i).strip() for i in range(1, 6)
        )
        # Skip the header row and separator row
        if sid.startswith("-") or sid == "Station":
            continue
        stations.append({
            "id": sid,
            "status": st,
            "started": started,
            "completed": completed,
            "gate": gate,
        })
        if current_station is None and st not in ("passed", "skipped"):
            current_station = sid

    return {
        "workflow": workflow,
        "feature": feature,
        "status": status,
        "trace_id": trace_id,
        "stations": stations,
        "current_station": current_station,
    }


def get_resume_index(
    *,
    state_file: str,
) -> int:
    """
    Return the 0-based index of the first station that is not ``passed``.
    Used by ``--resume`` mode.
    """
    state = query_state(state_file=state_file)
    for i, s in enumerate(state["stations"]):
        if s["status"] != "passed":
            return i
    return len(state["stations"])


def inherit_trace_id(
    *,
    state_file: str,
) -> str | None:
    """
    Read the trace ID from an existing workflow-state.md.

    Returns None if the file doesn't exist or has no trace ID.
    Used by cross-provider trace correlation.
    """
    path = Path(state_file)
    if not path.exists():
        return None
    return _read_trace_id(path)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_trace_id(path: Path) -> str | None:
    content = path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Trace ID\*\*: (\S+)", content)
    return m.group(1) if m and m.group(1) != "unset" else None


def _extract_header(content: str, prefix: str) -> str:
    m = re.search(rf"^# {re.escape(prefix)}: (.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_header_field(content: str, field: str) -> str:
    m = re.search(rf"\*\*{re.escape(field)}\*\*: (.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_field(row: str, index: int) -> str:
    """Extract the Nth pipe-delimited field from a Markdown table row."""
    parts = [p.strip() for p in row.split("|")]
    # parts[0] is empty (before first |), so fields start at index 1
    if index + 1 < len(parts):
        return parts[index + 1]
    return "—"


def _all_resolved(content: str) -> bool:
    """Check if all stations are in a terminal state."""
    for m in re.finditer(
        r"^\| (\S+) \| (\S+) \|", content, re.MULTILINE
    ):
        sid, st = m.group(1), m.group(2)
        if sid.startswith("-") or sid == "Station":
            continue
        if st in ("pending", "running"):
            return False
    return True


def _emit_span(
    *,
    trace_id: str,
    trace_file: str | None,
    span_type: str,
    workflow: str,
    station: str,
    event: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Emit a structured span to audit-trace.jsonl."""
    record: dict[str, Any] = {
        "trace_id": trace_id,
        "span_id": generate_span_id(),
        "parent_span_id": None,
        "timestamp": _now_utc(),
        "span_type": span_type,
        "workflow": workflow,
        "station": station,
        "event": event,
    }
    if metadata:
        record.update(metadata)

    emit_trace(record, trace_file=trace_file)
