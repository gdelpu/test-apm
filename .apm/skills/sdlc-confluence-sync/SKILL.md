---
name: sdlc-confluence-sync
description: 'Synchronize SDLC deliverables with Confluence: push markdown to Confluence pages, pull status labels and review comments, and manage the review cycle.'
---

# Skill: sdlc-confluence-sync

## Goal

Synchronize SDLC deliverables with Confluence: push markdown to Confluence pages (with Mermaid→PNG conversion), pull status labels and review comments, and manage the review cycle.

## When to use

- After any agent produces a deliverable (invoked via post-confluence-push hook)
- On-demand via `/confluence-push`, `/confluence-pull`, `/confluence-comments` commands
- During the review cycle to capture human feedback

## Procedure

### Push to Confluence
1. Read the deliverable markdown file
2. Convert Mermaid diagrams to PNG images
3. Create or update the Confluence page (using page mapping from `confluence-mapping.md`)
4. Apply status label (draft/review/validated)
5. Write sync hash to prevent duplicate pushes

### Pull from Confluence
1. Read current status labels from Confluence pages
2. Pull review comments as plain text
3. Update local deliverable YAML front matter with Confluence status
4. Make comments available for `/impact` change analysis

## Output

- Updated Confluence pages
- Synced status labels
- Extracted comments for impact analysis

## Rules

- Push is idempotent — sync hash prevents duplicate updates
- Status labels must match the lifecycle: draft → review → validated
- Confluence is the review interface; Git is the source of truth
- Mermaid diagrams must be converted to PNG for Confluence rendering

## Resources

| Resource | Purpose |
|----------|---------|
| `tools/confluence-publish.js` | Node.js publish script |
| `tools/confluence-pull.js` | Node.js pull script |
| `tools/confluence-config.yaml` | Confluence API configuration |
| `tools/confluence-mapping.md` | Page ID mapping reference |
