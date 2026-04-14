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
import os
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
_RUN_DIR_PATTERN = re.compile(
    r"^(\d{8}-\d{6})-(.+)-([0-9a-f]{8})$"
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_run_dir(
    *,
    repo_root: Path,
    workflow: str,
    name: str,
    trace_id: str,
) -> Path:
    """
    Build the canonical run directory path::

        outputs/runs/<workflow>/<YYYYMMDD-HHMMSS>-<name>-<short-tid>/

    Returns the absolute ``Path``.
    """
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short_tid = trace_id[:8]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "run"
    dir_name = f"{ts}-{slug}-{short_tid}"
    return repo_root / "outputs" / "runs" / workflow / dir_name


def find_latest_run(
    *,
    repo_root: Path,
    workflow: str | None = None,
) -> Path | None:
    """
    Return the ``workflow-state.md`` inside the latest run directory.

    If *workflow* is given, scopes to ``outputs/runs/<workflow>/``.
    Otherwise, searches across all workflow directories under ``outputs/runs/``.

    Uses the ``latest`` symlink when available, falling back to
    lexicographic sort of directory names (timestamp prefix ensures order).
    """
    runs_root = repo_root / "outputs" / "runs"
    if not runs_root.exists():
        return None

    search_dirs: list[Path] = []
    if workflow:
        wf_dir = runs_root / workflow
        if wf_dir.exists():
            search_dirs = [wf_dir]
    else:
        search_dirs = [d for d in runs_root.iterdir() if d.is_dir()]

    latest_state: Path | None = None
    for wf_dir in search_dirs:
        # Prefer symlink
        link = wf_dir / "latest"
        if link.exists():
            candidate = link / "workflow-state.md"
            if candidate.exists():
                if latest_state is None or str(candidate) > str(latest_state):
                    latest_state = candidate
                continue
        # Fallback: lexicographic sort
        run_dirs = sorted(
            (d for d in wf_dir.iterdir()
             if d.is_dir() and _RUN_DIR_PATTERN.match(d.name)),
            key=lambda d: d.name,
            reverse=True,
        )
        for rd in run_dirs:
            candidate = rd / "workflow-state.md"
            if candidate.exists():
                if latest_state is None or str(candidate) > str(latest_state):
                    latest_state = candidate
                break

    return latest_state


def init_workflow(
    *,
    state_file: str | None = None,
    workflow: str,
    feature: str,
    stations: list[str],
    trace_id: str | None = None,
    trace_file: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """
    Create the workflow-state.md file and emit a ``span_type: workflow``
    root span to audit-trace.jsonl.

    If *state_file* is omitted and *repo_root* is provided, the run
    directory is auto-resolved to::

        outputs/runs/<workflow>/<YYYYMMDD-HHMMSS>-<feature>-<short-tid>/

    If the state file already exists (resume case), returns the existing
    trace_id without overwriting.

    Returns:
        dict with ``trace_id``, ``state_file``, ``run_dir``, ``created``.
    """
    tid = trace_id or generate_trace_id()

    # Resolve path
    if state_file:
        path = Path(state_file)
    elif repo_root:
        run_dir = resolve_run_dir(
            repo_root=repo_root,
            workflow=workflow,
            name=feature or workflow,
            trace_id=tid,
        )
        path = run_dir / "workflow-state.md"
    else:
        raise ValueError(
            "Either --state-file or repo_root must be provided for init"
        )

    # Resume guard — don't overwrite existing state
    if path.exists():
        existing_tid = _read_trace_id(path)
        return {
            "trace_id": existing_tid or tid,
            "state_file": str(path),
            "run_dir": str(path.parent),
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

    # Auto-derive trace file as sibling
    if not trace_file:
        trace_file = str(path.parent / "audit-trace.jsonl")

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

    # Write YAML companion (best-effort, non-fatal)
    try:
        _write_yaml_companion(path)
    except Exception:
        pass

    # Symlink + manifest (best-effort, non-fatal)
    if repo_root:
        _update_latest_symlink(path.parent)
        _update_manifest(
            repo_root=repo_root,
            workflow=workflow,
            feature=feature,
            trace_id=tid,
            run_dir=path.parent,
        )

    return {
        "trace_id": tid,
        "state_file": str(path),
        "run_dir": str(path.parent),
        "created": True,
    }


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
    repo_root: Path | None = None,
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
        repo_root: Repository root (for manifest update on completion).

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
    workflow_completed = False
    if _all_resolved(content):
        overall = "passed" if "| failed |" not in content else "failed"
        content = re.sub(
            r"\*\*Status\*\*: in-progress",
            f"**Status**: {overall}",
            content,
        )
        workflow_completed = True

    path.write_text(content, encoding="utf-8")

    # Write YAML companion (best-effort, non-fatal)
    try:
        _write_yaml_companion(path)
    except Exception:
        pass

    # Auto-derive trace file as sibling if not provided
    if not trace_file:
        trace_file = str(path.parent / "audit-trace.jsonl")

    # Update manifest on workflow completion
    if workflow_completed and repo_root:
        _update_manifest_status(
            repo_root=repo_root,
            run_dir=path.parent,
            status=overall,
        )

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
    wf_started = _extract_header_field(content, "Started")
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
        "started": wf_started,
        "status": status,
        "trace_id": trace_id,
        "stations": stations,
        "current_station": current_station,
        "run_dir": str(path.parent),
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


def _update_latest_symlink(run_dir: Path) -> None:
    """Create or replace a ``latest`` symlink in the workflow directory."""
    link = run_dir.parent / "latest"
    try:
        if link.is_symlink() or link.exists():
            link.unlink()
        # Use relative target so the symlink is portable
        link.symlink_to(run_dir.name, target_is_directory=True)
    except OSError:
        # Symlinks may require elevated privileges on Windows — best-effort
        pass


def _update_manifest(
    *,
    repo_root: Path,
    workflow: str,
    feature: str,
    trace_id: str,
    run_dir: Path,
) -> None:
    """Append an entry to ``outputs/runs/run-manifest.json``."""
    manifest_path = repo_root / "outputs" / "runs" / "run-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    if manifest_path.exists():
        try:
            entries = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            entries = []

    entries.append({
        "trace_id": trace_id,
        "workflow": workflow,
        "feature": feature,
        "run_dir": str(run_dir.relative_to(repo_root)),
        "started": _now_utc(),
        "status": "in-progress",
    })

    manifest_path.write_text(
        json.dumps(entries, indent=2) + "\n", encoding="utf-8"
    )


def _write_yaml_companion(md_path: Path) -> None:
    """
    Write a ``workflow-state.yml`` alongside the given ``workflow-state.md``.

    Emits a machine-friendly YAML representation of the same state data.
    Uses a minimal hand-written serialiser (no PyYAML dependency) since the
    structure is simple: scalars + a list of flat dicts.
    """
    state = query_state(state_file=str(md_path))
    yml_path = md_path.with_suffix(".yml")

    lines = [
        f"workflow: {_yaml_scalar(state['workflow'])}",
        f"feature: {_yaml_scalar(state['feature'])}",
        f"started: {_yaml_scalar(state.get('started', ''))}",
        f"status: {_yaml_scalar(state['status'])}",
        f"trace_id: {_yaml_scalar(state['trace_id'])}",
        f"current_station: {_yaml_scalar(state.get('current_station') or '')}",
        "stations:",
    ]
    for s in state["stations"]:
        lines.append(f"  - id: {_yaml_scalar(s['id'])}")
        lines.append(f"    status: {_yaml_scalar(s['status'])}")
        lines.append(f"    started: {_yaml_scalar(s['started'])}")
        lines.append(f"    completed: {_yaml_scalar(s['completed'])}")
        lines.append(f"    gate: {_yaml_scalar(s['gate'])}")

    yml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _yaml_scalar(value: str) -> str:
    """Quote a YAML scalar value when necessary."""
    if not value:
        return '""'
    # Quote if it contains YAML-special chars, looks like a boolean/null, or starts with special chars
    if (
        any(c in value for c in ":#{}[]|>&*!%@`,")
        or value.lower() in ("true", "false", "null", "yes", "no", "on", "off")
        or value.startswith(("-", "?", " "))
        or value != value.strip()
    ):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


def _update_manifest_status(
    *,
    repo_root: Path,
    run_dir: Path,
    status: str,
) -> None:
    """Update the status of an existing manifest entry on completion."""
    manifest_path = repo_root / "outputs" / "runs" / "run-manifest.json"
    if not manifest_path.exists():
        return

    try:
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return

    rel_dir = str(run_dir.relative_to(repo_root))
    for entry in entries:
        if entry.get("run_dir") == rel_dir:
            entry["status"] = status
            entry["completed"] = _now_utc()
            break

    manifest_path.write_text(
        json.dumps(entries, indent=2) + "\n", encoding="utf-8"
    )
