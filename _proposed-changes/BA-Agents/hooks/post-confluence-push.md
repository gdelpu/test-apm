# Post-Hook: Confluence Push

## Objective

This hook is executed **after the quality control hook**, as the last step before returning to the coordinator. It pushes the produced deliverable to Confluence.

> For details on what the publish script does (conversion, page hierarchy, labels, locking), see the header comment in `tools/confluence-publish.js`.

---

## Prerequisites

The agent checks prerequisites **by reading files on disk**, not by inspecting process environment variables (the publish script loads `.env` itself).

### Checklist

1. **`docs/project.yml`** — read the `confluence_enabled` field:
   - `false` → skip this hook immediately (user explicitly disabled Confluence at scaffold time)
   - `true` → proceed to credential checks below
   - **field absent** → treat as `true` (Confluence is enabled by default when credentials are present) — do NOT skip the push on the sole basis that the field is missing
2. **`.env` at project root** — must exist and contain non-empty values for:
   - `CONFLUENCE_INSTANCE_URL`
   - `CONFLUENCE_USER_EMAIL`
   - `CONFLUENCE_API_TOKEN`
   - `CONFLUENCE_SPACE_KEY`
3. **`tools/confluence-config.yaml`** — must exist with `instance_url` and `space_key` set.
4. **Pandoc** — must be installed (check `tools.config.yml` or known path for this project: `C:/Users/vfady/AppData/Local/Pandoc/pandoc.exe`).
5. **`mmdc` (mermaid-cli)** — optional. If absent, Mermaid diagrams will not render but the push proceeds.

**Decision:**

| Condition | Action |
|-----------|--------|
| `confluence_enabled: false` in `docs/project.yml` | SKIP silently — no WARN needed |
| `.env` missing or credentials incomplete | WARN — skip push, suggest running `/scaffold` to configure |
| `confluence-config.yaml` missing | WARN — skip push, suggest running `/scaffold` |
| Pandoc missing | WARN — skip push for this deliverable |
| All prerequisites met | **PROCEED** to push |

---

## Process

### Step 1: Determine push mode

Read the deliverable's front matter:

| Condition | Mode | Status rule |
|-----------|------|-------------|
| `confluence_id` is null | **CREATE** | Status stays as-is (`draft`) |
| `confluence_id` exists and content hash differs from `confluence_sync_hash` | **UPDATE** | If current status is `validated` or `review` → reset to `draft` |
| `confluence_id` exists and content hash matches `confluence_sync_hash` | **SKIP** | No change needed |

### Step 2: Push

Run the publish script via bash:

```bash
node tools/confluence-publish.js --file <deliverable-path>
```

> The script loads `.env` automatically — no need to export environment variables before calling it.

### Step 3: Confirm

After the script returns:
- Verify that `confluence_id` is now set in the front matter (non-null)
- Verify that `confluence_sync_hash` is updated
- If the script failed: log a WARN, do NOT block the agent — the deliverable itself is valid

---

## Section page title uniqueness

When the publish script creates parent section pages (e.g. `user-stories/`, `journeys/`, `tests/`), it qualifies the title with the parent feature slug to ensure space-wide uniqueness:

> `"User Stories — ft-008-authenticate-users — {PROJECT_NAME}"`

This prevents Confluence 400 errors caused by identically-named section pages across different features (e.g. "User Stories — Activity tracking" existing under both FT-001 and FT-008). The logic is implemented in `tools/confluence-publish.js` and is transparent — no action required from the agent.

---

## Error handling

| Error | Action |
|-------|--------|
| Confluence API unreachable | WARN — skip push, deliverable remains valid |
| Authentication failure | WARN — skip push, suggest checking env variables |
| Mermaid rendering failure | WARN — push page without diagrams |
| Pandoc conversion failure | WARN — skip push for this deliverable |

**Principle:** Confluence push is best-effort. It must NEVER block deliverable production.
