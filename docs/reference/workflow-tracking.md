# Workflow Tracking

> Provider-independent execution tracking for workflows, stations, tools, MCP invocations, and skill lifecycle events. Produces a Markdown state file for human readability and a JSONL audit trace for observability tooling.

Engine: `.apm/hooks/engine/state_tracker.py`, `.apm/hooks/engine/tool_tracker.py`.
Schema: `.apm/hooks/engine/schemas/workflow-state.schema.md`.

---

## Overview

Every workflow run creates a **run directory** under `outputs/runs/` containing:

- `workflow-state.md` — Markdown table tracking station progress (human-readable)
- `audit-trace.jsonl` — structured spans for every workflow, station, tool, and skill event

The state tracker is a Python CLI (`python -m engine --state ...`) that all three providers call identically. No external dependencies — stdlib only (Python 3.10+).

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  CLI (bash)  │   │   Copilot    │   │  Claude Code │
│ run-workflow │   │ runCommands  │   │  bash blocks │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
              ┌───────────▼───────────┐
              │  python -m engine     │
              │  --state / --tool /   │
              │  --skill-event        │
              │  (stdlib-only Python) │
              └───────────┬───────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
    ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼──────┐
    │ workflow-   │ │  audit-   │ │   run-     │
    │ state.md    │ │ trace.jsonl│ │ manifest.json│
    └─────────────┘ └───────────┘ └────────────┘
```

### Copilot fallback

When `runCommands` is unavailable in Copilot, agents write `outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-feature-implementation-login.md`) directly using `edit/editFiles` following the format in `.apm/hooks/engine/schemas/workflow-state.schema.md`. The state file must always be written to the **root** of `outputs/` with the workflow and feature name as suffix — never inside a workflow's `output_dir` subfolder. The `<workflow>-<feature>` suffix prevents conflicts when multiple workflows or the same workflow for different features run concurrently. A post-hook validator auto-corrects malformed entries.

## Run directory layout

```
outputs/runs/
├── run-manifest.json                              # Append-only index of all runs
├── feature-implementation/
│   ├── latest → 20260412-143000-login-a1b2c3d4/   # Symlink to most recent
│   ├── 20260412-143000-login-a1b2c3d4/
│   │   ├── workflow-state.md
│   │   └── audit-trace.jsonl
│   └── 20260411-091500-signup-e5f6a7b8/
│       ├── workflow-state.md
│       └── audit-trace.jsonl
├── spec-kit/
│   ├── latest → ...
│   └── ...
```

### Directory naming

Format: `<YYYYMMDD-HHMMSS>-<name>-<short-tid>`

| Segment | Source | Example |
|---------|--------|---------|
| `YYYYMMDD-HHMMSS` | UTC timestamp at init | `20260412-143000` |
| `name` | Feature/workflow name, kebab-case slug | `login` |
| `short-tid` | First 8 chars of trace ID (UUID) | `a1b2c3d4` |

### `latest` symlink

Updated on every `--state init`. Used by `--state query/update/resume` to auto-discover the active run when `--state-file` is not given. On Windows, requires Developer Mode or elevated privileges — fails silently with lexicographic fallback.

### `run-manifest.json`

Append-only JSON array at `outputs/runs/run-manifest.json`. Each entry records `trace_id`, `workflow`, `feature`, `run_dir`, `started`, `status`. Status is updated to `passed` or `failed` when all stations resolve.

---

## CLI Reference

All commands run from the hooks directory:

```bash
cd .apm/hooks
```

### Initialise a workflow

```bash
python -m engine --state init \
  --workflow <name> --feature <feature> \
  --stations "station1,station2,station3"
```

Returns JSON with `trace_id`, `state_file`, `run_dir`, `created`. Auto-creates the run directory, `workflow-state.md`, `audit-trace.jsonl`, `latest` symlink, and manifest entry.

If the state file already exists (resume case), returns the existing `trace_id` without overwriting.

### Update a station

```bash
python -m engine --state update \
  --station <id> --status running \
  --trace-id <tid> --workflow <name>
```

Valid statuses: `pending`, `running`, `passed`, `failed`, `skipped`.
Valid gates: `pass`, `fail`, `warning`, `blocked-by-hook`, `—`.

Transitions: `pending → running → passed|failed`, `pending → skipped`. No backward transitions.

When all stations reach a terminal state, the overall workflow status auto-updates to `passed` or `failed`, and the manifest entry is updated with `completed` timestamp.

### Query current state

```bash
python -m engine --state query --workflow <name> --json
```

Auto-discovers the latest run for the given workflow. Returns JSON with `workflow`, `feature`, `status`, `trace_id`, `stations[]`, `current_station`, `run_dir`.

Use `--state-file <path>` to target a specific run instead.

### Resume detection

```bash
python -m engine --state resume --workflow <name>
```

Returns `{"resume_index": N}` — the 0-based index of the first non-passed station.

### Trace ID inheritance

```bash
python -m engine --state inherit-trace --workflow <name>
```

Reads the trace ID from an existing run's `workflow-state.md`. Used for cross-provider trace correlation when resuming a workflow started by another provider.

### Tool / MCP invocation tracking

```bash
python -m engine --tool <tool-name> \
  --mcp-server <server-id> --mcp-method <method> \
  --trace-id <tid> --station <station> --workflow <name>
```

Emits a `span_type: "tool"` record to `audit-trace.jsonl`. Optional `--duration-ms` for call timing.

### Skill lifecycle tracking

```bash
python -m engine --skill-event start --skill <name> \
  --trace-id <tid> --station <station> --workflow <name>

python -m engine --skill-event end --skill <name> \
  --trace-id <tid> --station <station> --workflow <name>
```

Emits `span_type: "skill"` records with `event: "skill-start"` or `"skill-end"`.

### Explicit paths (override auto-discovery)

| Flag | Purpose |
|------|---------|
| `--state-file <path>` | Target a specific `workflow-state.md` instead of auto-discovering via `latest` symlink |
| `--trace-file <path>` | Target a specific `audit-trace.jsonl` instead of auto-deriving as sibling of state file |

---

## State file format

```markdown
# Workflow State: feature-implementation

**Feature**: login
**Started**: 2026-04-12T14:30:00Z
**Status**: in-progress
**Trace ID**: a1b2c3d4-e5f6-7890-abcd-ef1234567890

| Station | Status | Started | Completed | Gate |
|---------|--------|---------|-----------|------|
| constitution | passed | 2026-04-12T14:30:05Z | 2026-04-12T14:31:12Z | pass |
| specification | running | 2026-04-12T14:31:15Z | — | — |
| plan | pending | — | — | — |
```

Header fields (`Feature`, `Started`, `Trace ID`) are immutable after creation. `Status` auto-updates when all stations resolve. Full format spec: `.apm/hooks/engine/schemas/workflow-state.schema.md`.

## Audit trace format

Each line in `audit-trace.jsonl` is a JSON object:

```json
{
  "trace_id": "a1b2c3d4-...",
  "span_id": "unique-span-uuid",
  "parent_span_id": null,
  "timestamp": "2026-04-12T14:30:00Z",
  "span_type": "workflow|station|tool|skill",
  "workflow": "feature-implementation",
  "station": "specification",
  "event": "workflow-init|station-running|station-passed|skill-start|..."
}
```

| `span_type` | Emitted by | Fields |
|-------------|-----------|--------|
| `workflow` | `--state init` | `feature`, `stations[]` |
| `station` | `--state update` | `gate`, `agent`, `skill` |
| `tool` | `--tool` | `tool_invoked`, `mcp` object (`server_id`, `method`, `external`, `duration_ms`) |
| `skill` | `--skill-event` | `skill`, `event` (`skill-start` / `skill-end`) |

Schema: `.apm/hooks/engine/schemas/trace-record.schema.json`.

---

## Consumer setup

### Prerequisites

- **Python 3.10+** (stdlib only — no pip install needed)
- Hooks engine at `.apm/hooks/engine/` (shipped by the APM bundle installer in both standard and expandable modes)

### Bundle install

The `install-apm-bundle` script (`.ps1` / `.sh`) copies `.apm/hooks/` to the consumer repo alongside the runtime projection. No additional setup required.

### Windows notes

The `latest` symlink requires Developer Mode enabled or elevated privileges. Without it, the tracker degrades gracefully — `find_latest_run()` falls back to lexicographic sort of directory names (the timestamp prefix ensures correct ordering).

### Provider integration

| Provider | Primary method | Fallback |
|----------|---------------|----------|
| **CLI** | `python -m engine --state ...` in `run-workflow.sh` | — |
| **Copilot** | `runCommands` → same CLI | `edit/editFiles` with schema-compliant Markdown |
| **Claude Code** | Bash blocks in slash commands → same CLI | — |

### Verify installation

```bash
cd .apm/hooks && python -m engine --state init \
  --workflow test-run --feature smoke-test \
  --stations "step-a,step-b"
```

Should return JSON with `created: true` and create `outputs/runs/test-run/<timestamp>-smoke-test-<tid>/workflow-state.md`.
