---
name: file-output
description: 'Mandate that document-producing agents write deliverables to disk as actual files, not just chat output.'
applyTo: '.apm/agents/**,.apm/skills/**'
---

# File Output Instructions

## Rule

Every deliverable specified in a skill's `## Output` section **must be written to disk** as an actual file. Do not merely display the content in chat.

## How to create files

1. Use the `edit/editFiles` tool (or `create_file` equivalent) to write each deliverable.
2. Create parent directories if they do not already exist.
3. Write the full content to the exact path specified by the skill (e.g., `outputs/specs/features/<feature>/spec.md`).
4. Include YAML front matter with artifact identifiers where the skill specifies them (e.g., `[VIS-001]`).

## Verification

After writing each file, confirm it was created by briefly stating the output path. Example:

> Created `outputs/docs/1-prd/1-scoping/vis-001-product-vision.md`

## Anti-pattern

Do **not**:
- Display the entire deliverable in chat and stop
- Ask the user to copy-paste content into files
- Skip file creation because tools seem unavailable — the agent has `edit/editFiles` granted
