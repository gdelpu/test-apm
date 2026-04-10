# Post-Hook: Confluence Push

> **Type:** post | **Scope:** agent + station | **Domain:** universal | **Severity:** warning | **never_block:** true
>
> **Config refs:** `tools.pandoc`, `tools.mmdc`, `tools.node`, `env_required.confluence`

## Objective

Executed **after the quality control hook**, as the last step before returning to the coordinator. Pushes the produced deliverable to Confluence by delegating to the `sdlc-confluence-sync` skill's publish tooling. All front matter updates (`confluence_id`, `confluence_sync_hash`, `status` changes) **must be written to disk** using the `edit/editFiles` tool.

**Principle:** Confluence push is best-effort. It must NEVER block deliverable production.

---

## Prerequisites

The agent checks prerequisites **by reading files on disk**, not by inspecting process environment variables (the publish script loads `.env` itself). Tool paths are resolved from `.apm/hooks/config/tool-paths.yml`.

### Checklist

1. **`docs/project.yml`** — read the `confluence_enabled` field:
   - `false` → skip this hook immediately (user explicitly disabled Confluence at scaffold time)
   - `true` → proceed to credential checks below
   - **field absent** → treat as `true` (Confluence is enabled by default when credentials are present) — do NOT skip the push on the sole basis that the field is missing
2. **`.env` at project root** — must exist and contain non-empty values for all variables listed in `tool-paths.yml` → `env_required.confluence`.
3. **`tools/confluence-config.yaml`** — must exist with `instance_url` and `space_key` set.
4. **Pandoc** — resolved via `${PANDOC_PATH:-pandoc}` from `tool-paths.yml`. Must be available on PATH or at the configured location.
5. **`mmdc` (mermaid-cli)** — resolved via `${MMDC_PATH:-mmdc}`. Optional. If absent, Mermaid diagrams will not render but the push proceeds.

### Decision

| Condition | Action |
|-----------|--------|
| `confluence_enabled: false` in `docs/project.yml` | SKIP silently — no WARN needed |
| `.env` missing or credentials incomplete | WARN — skip push, suggest running `/scaffold` to configure |
| `confluence-config.yaml` missing | WARN — skip push, suggest running `/scaffold` |
| Pandoc not found at configured path | WARN — skip push for this deliverable |
| All prerequisites met | **PROCEED** to push |

---

## Process

### Step 1: Determine Push Mode

Read the deliverable's front matter:

| Condition | Mode | Status rule |
|-----------|------|-------------|
| `confluence_id` is null | **CREATE** | Status stays as-is (`draft`) |
| `confluence_id` exists and content hash differs from `confluence_sync_hash` | **UPDATE** | If current status is `validated` or `review` → reset to `draft` |
| `confluence_id` exists and content hash matches `confluence_sync_hash` | **SKIP** | No change needed |

### Step 2: Push

Delegate to the `sdlc-confluence-sync` skill's publish script:

```bash
${NODE_PATH:-node} tools/confluence-publish.js --file <deliverable-path>
```

> The script loads `.env` automatically — no need to export environment variables before calling it.

### Step 3: Confirm

After the script returns:
- Verify that `confluence_id` is now set in the front matter (non-null)
- Verify that `confluence_sync_hash` is updated
- If the script failed: log a WARN, do NOT block the agent — the deliverable itself is valid

---

## Section Page Title Uniqueness

When the publish script creates parent section pages (e.g. `user-stories/`, `journeys/`, `tests/`), it qualifies the title with the parent feature slug to ensure space-wide uniqueness:

> `"User Stories — ft-008-authenticate-users — {PROJECT_NAME}"`

This prevents Confluence 400 errors caused by identically-named section pages across different features. The logic is implemented in `tools/confluence-publish.js` and is transparent — no action required from the agent.

---

## Error Handling

| Error | Action |
|-------|--------|
| Confluence API unreachable | WARN — skip push, deliverable remains valid |
| Authentication failure | WARN — skip push, suggest checking env variables |
| Mermaid rendering failure | WARN — push page without diagrams |
| Pandoc conversion failure | WARN — skip push for this deliverable |

All errors produce WARN only — this hook has `never_block: true`.
