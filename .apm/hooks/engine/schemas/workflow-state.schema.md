# Workflow State File Format (Fallback Schema)

When the canonical state tracker (`python -m engine --state`) is **unavailable**
(e.g. `runCommands` blocked in Copilot), agents MUST write
`outputs/workflow-state-<workflow>-<feature>.md` (e.g. `outputs/workflow-state-feature-implementation-login.md`)
directly using `edit/editFiles` following this **exact format**.

> **Important**: Always write the state file to `outputs/workflow-state-<workflow>-<feature>.md`
> (the **root** of the `outputs/` directory, with the workflow name and
> feature/project name as suffix). Never write it inside a workflow’s
> `output_dir` subfolder (e.g. not
> `outputs/specs/features/<feature>/workflow-state.md` or
> `outputs/docs/1-prd/workflow-state.md`). The `<workflow>-<feature>` suffix
> ensures concurrent workflows and repeated runs for different features do not
> overwrite each other’s state.

## Required structure

```markdown
# Workflow State: <workflow-name>

**Feature**: <feature-name>
**Started**: <ISO-8601-UTC>
**Status**: in-progress
**Trace ID**: <UUID-v4>

| Station | Status | Started | Completed | Gate |
|---------|--------|---------|-----------|------|
| <id> | pending | — | — | — |
```

## Field rules

### Header fields

| Field | Format | Mutability |
|-------|--------|------------|
| `Workflow State` | `# Workflow State: <name>` — must be line 1 | Immutable |
| `Feature` | `**Feature**: <name>` | Immutable |
| `Started` | `**Started**: <ISO 8601 UTC>` e.g. `2026-04-12T14:30:00Z` | Immutable |
| `Status` | `**Status**: in-progress \| passed \| failed` | Updated when all stations resolve |
| `Trace ID` | `**Trace ID**: <UUID>` — must be valid UUID v4 | Immutable |

### Station table rows

Each station is a pipe-delimited row. Fields:

| Column | Values | Rules |
|--------|--------|-------|
| Station | Station ID (kebab-case) | Immutable — set at init |
| Status | `pending` \| `running` \| `passed` \| `failed` \| `skipped` | See transitions |
| Started | ISO 8601 UTC or `—` | Set once when status → `running` |
| Completed | ISO 8601 UTC or `—` | Set when status → `passed`/`failed`/`skipped` |
| Gate | `pass` \| `fail` \| `warning` \| `blocked-by-hook` \| `—` | Set with completion |

### Valid status transitions

```
pending → running → passed
pending → running → failed
pending → skipped
```

Do **not** transition backwards (e.g. `passed` → `running`).

## Validation

The hook framework's post-hook validator checks:
1. Header fields are present and correctly formatted
2. All station IDs match the workflow YAML definition
3. Status values are valid enum members
4. Timestamps are ISO 8601
5. Trace ID is a valid UUID

Malformed entries are auto-corrected where possible and flagged in
`audit-trace.jsonl` with `event: "state-validation-fix"`.

## Run directory layout

All workflow runs are stored under a centralized `outputs/runs/` tree:

```
outputs/runs/
├── run-manifest.json               # Append-only index of all runs
├── feature-implementation/
│   ├── latest → 20260412-143000-login-a1b2c3d4/
│   ├── 20260412-143000-login-a1b2c3d4/
│   │   ├── workflow-state.md
│   │   ├── workflow-state.yml   # Machine-readable YAML companion
│   │   └── audit-trace.jsonl
│   └── 20260411-091500-signup-e5f6a7b8/
│       ├── workflow-state.md
│       ├── workflow-state.yml
│       └── audit-trace.jsonl
├── spec-kit/
│   ├── latest → 20260412-150000-payments-c9d0e1f2/
│   └── ...
```

### Directory naming

Format: `<YYYYMMDD-HHMMSS>-<name>-<short-tid>`

| Segment | Source | Example |
|---------|--------|---------|
| `YYYYMMDD-HHMMSS` | UTC timestamp at init | `20260412-143000` |
| `name` | Feature name or workflow name (kebab-case slug) | `login` |
| `short-tid` | First 8 chars of trace ID | `a1b2c3d4` |

### `latest` symlink

Each `outputs/runs/<workflow>/latest` is a symlink pointing to the most
recent run directory. Updated automatically by `--state init`. Used by
`--state query/update/resume` to auto-discover state when `--state-file`
is not explicitly provided.

### `run-manifest.json`

Append-only JSON array at `outputs/runs/run-manifest.json`:

```json
[
  {
    "trace_id": "a1b2c3d4-...",
    "workflow": "feature-implementation",
    "feature": "login",
    "run_dir": "outputs/runs/feature-implementation/20260412-143000-login-a1b2c3d4",
    "started": "2026-04-12T14:30:00Z",
    "status": "in-progress"
  }
]
```

The `status` field is updated to `passed` or `failed` when all stations resolve.

### Auto-derived trace file

When `--trace-file` is not explicitly provided, `audit-trace.jsonl` is
automatically created as a sibling of `workflow-state.md` in the run directory.

### YAML companion file

Every `workflow-state.md` is accompanied by a `workflow-state.yml` in the same
directory. This YAML file contains the same state data in a machine-friendly
format suitable for CI pipelines, dashboards, and scripts that need to parse
workflow progress without reading Markdown tables.

The YAML companion is automatically generated and updated by the state tracker
on every `init` and `update` operation. Example:

```yaml
workflow: feature-implementation
feature: login
started: "2026-04-12T14:30:00Z"
status: in-progress
trace_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
current_station: implement
stations:
  - id: spec
    status: passed
    started: "2026-04-12T14:30:05Z"
    completed: "2026-04-12T14:35:00Z"
    gate: pass
  - id: implement
    status: running
    started: "2026-04-12T14:35:05Z"
    completed: "—"
    gate: "—"
```
