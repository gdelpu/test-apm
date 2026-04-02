# /sdlc-confluence-push

Push a **single Markdown deliverable** to Confluence (create or update).

$ARGUMENTS = path to the deliverable file (e.g., "docs/1-prd/1-scoping/glo-001-glossary.md")

## Steps

1. Read the deliverable's YAML front matter.
2. Read `.apm/skills/sdlc-confluence-sync/tools/confluence-config.yaml`.
3. Execute the publish script:
   ```bash
   node .apm/skills/sdlc-confluence-sync/tools/confluence-publish.js --file <path>
   ```
4. The script handles:
   - Mermaid diagram rendering to PNG (via `mmdc`).
   - Markdown to Confluence storage format conversion (via Pandoc).
   - Page creation (if `confluence_id` is null) or update (if exists).
   - Parent page creation (derived from file path).
   - Status label synchronization (`status-draft`, `status-review`, `status-validated`).
   - Write-back of `confluence_id` and `confluence_sync_hash` to front matter.
5. If status was `validated`/`review` and content changed: status resets to `draft`.
6. Display confirmation with Confluence page URL.
