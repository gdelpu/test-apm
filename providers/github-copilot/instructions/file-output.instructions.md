---
name: file-output
description: 'Mandate that document-producing agents write deliverables to disk as actual files, not just chat output.'
applyTo: '**'
---

# File Output Instructions

## Rule

Every deliverable specified in a skill's `## Output` section or an agent's `## Required outputs` section **must be written to disk** as an actual file. Displaying content in chat is **never** a substitute for writing the file. If you produce a deliverable, you **must** call a file-writing tool.

## How to create files

1. **Always use the `edit/editFiles` tool** (or `create_file` equivalent) to write each deliverable to the file system. This is mandatory — not optional, not best-effort.
2. Create parent directories if they do not already exist.
3. Write the full content to the exact path specified by the skill or agent (e.g., `outputs/specs/features/<feature>/spec.md`).
4. Include YAML front matter with artifact identifiers where the skill specifies them (e.g., `[VIS-001]`).
5. Include the **output document metadata** defined in `output-metadata` instruction (see `knowledge/governance/schemas/output-metadata.schema.json`). Every `outputs/` file must have `workflow`, `trigger`, `date`, `status`, `inputDocuments`, `changeHistory`, `holisticQualityRating`, and `overallStatus` fields.

## Verification

After writing each file, confirm it was created by briefly stating the output path. Example:

> Created `outputs/docs/1-prd/1-scoping/vis-001-product-vision.md`

## Anti-patterns

Do **not**:
- Display the entire deliverable in chat and stop — this is the most common failure mode
- Ask the user to copy-paste content into files
- Skip file creation because tools seem unavailable — the agent has `edit/editFiles` granted
- Use phrases like "here is the content" or "the output is:" without also writing the file to disk
- Assume that outputting content in the conversation counts as "writing" — it does not

## Enforcement

When orchestrating workflows or delegating to station agents:
- Verify that each station's declared outputs were **actually created on disk** (not just displayed)
- If a station agent produces content only in chat, treat it as an incomplete station and retry with explicit file-creation instruction
- Workflow orchestrators must check file existence after each station completes
