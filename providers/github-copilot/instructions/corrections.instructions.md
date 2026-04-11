---
name: corrections
description: 'Accumulated corrections from user feedback. Agents append lessons here automatically when corrected during conversations.'
applyTo: '**'
---

# Corrections Memory

Lessons learned from user corrections — applied automatically to prevent repeated mistakes.

## C-01 · Agent file-write capability (2026-04-11)

**Problem**: Document-producing agents kept regressing to read-only in consumer repos.
Three interacting causes:
1. Overly narrow `allowedFilePaths` (e.g. only `outputs/**`) prevented writing to consumer project directories (`src/**`, `tests/**`, `docs/**`, `specs/**`).
2. "Out of Scope" body text ("Direct source-code modification outside `outputs/`") caused the LLM to refuse file writes even when tools allowed it.
3. No CI gate validated write capability, so regressions were invisible.

**Fix applied**:
- Expanded `allowedFilePaths` in both canonical (`.apm/agents/`) and provider (`providers/github-copilot/agents/`) layers for 12 agents.
- Removed "Direct source-code modification outside `outputs/`" from Out of Scope in 5 agents.
- Added policy rule **P-07** (a/b/c) to `a1_policy.py` and `a1-policy-validation.prompt.md`:
  - **P-07a**: ALL agents must have `edit/editFiles` in tools (opt out with `readOnly: true` in frontmatter).
  - **P-07b**: Agents with `allowedFilePathsReadOnly` must ALSO have `allowedFilePaths`.
  - **P-07c**: `allowedFilePaths` when present must be a non-empty array.
- This ensures MRs cannot silently remove write capability, guaranteeing consumer bundles always include writable agents.

**Rule for agents**: When creating or editing agent definitions:
- ALL agents that produce deliverables (code, docs, tests, specs) MUST have `edit/editFiles` in `tools:` AND `allowedFilePaths` entries covering their output directories.
- `allowedFilePathsReadOnly` is for ADDITIONAL read-access paths — it must never be the ONLY path restriction on agents that need to write.
- Never add "Direct code modification or file writes" to Out of Scope for agents that produce deliverables.
- Consumer-facing agents should include `src/**`, `tests/**`, `docs/**`, `specs/**`, `outputs/**` in `allowedFilePaths` unless there's a specific security reason to restrict.
