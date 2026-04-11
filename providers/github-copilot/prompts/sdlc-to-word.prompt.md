---
name: sdlc-to-word
mode: agent
description: 'Convert Markdown deliverable to Word via Pandoc.'
---

# /sdlc-to-word

Convert a SDLC deliverable to Word format.

1. Load conversion skill from `.apm/skills/sdlc-confluence-sync/docs/sk-word-conversion.md`.
2. Apply corporate template from `.apm/skills/sdlc-confluence-sync/docs/template-corporate.docx`.
3. Output Word file to `output/word/`.

## Alternative: Direct DOCX creation

For advanced Word document creation, editing, or manipulation (tracked changes, comments, XML-level edits), use the `docx` skill (`.apm/skills/docx/SKILL.md`) with shared utilities from `office-common`.
