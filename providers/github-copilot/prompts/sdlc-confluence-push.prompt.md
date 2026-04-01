---
name: sdlc-confluence-push
mode: agent
description: 'Push a SDLC deliverable to Confluence (create or update).'
---

# /sdlc-confluence-push

Push a Markdown deliverable to Confluence.

1. Read YAML front matter from the target file.
2. Execute `.apm/skills/sdlc-confluence-sync/tools/confluence-publish.js`.
3. Handles Mermaid rendering, Markdown→Confluence conversion, status labels, and ID write-back.
