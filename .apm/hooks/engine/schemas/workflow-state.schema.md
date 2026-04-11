# Workflow State File Format (Fallback Schema)

When the canonical state tracker (`python -m engine --state`) is **unavailable**
(e.g. `runCommands` blocked in Copilot), agents MUST write `workflow-state.md`
directly using `edit/editFiles` following this **exact format**.

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
