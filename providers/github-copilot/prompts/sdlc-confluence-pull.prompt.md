---
name: sdlc-confluence-pull
mode: agent
description: 'Pull status and comments from Confluence into local deliverables.'
---

# /sdlc-confluence-pull

Pull Confluence status changes and comments.

1. Execute `.apm/skills/sdlc-confluence-sync/tools/confluence-pull.js`.
2. Sync status (promotes if Confluence is ahead, never downgrades).
3. Extract comments as plain text — feed into `/sdlc-impact` for change analysis.
