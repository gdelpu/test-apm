---
name: sdlc-tech-3-impl
mode: agent
description: 'Run Tech System T3 — Implementation (5 stations, iterative per sprint).'
---

# /sdlc-tech-3-impl

Run the Tech implementation pipeline per sprint.

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-task-resolution` through `tech-wave-gate`.
2. Load sprint scope from [IMP-001] and `wave-state.json`.
3. For each item in dependency order: resolve context (T3.1) → generate code (T3.2) → implement tests (T3.3) → validate (T3.4).
4. If all wave items completed, evaluate wave gate (T3.5).
5. Write sprint summary.
6. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/docs/2-tech/3-implementation/`. Do not merely display content in chat.
7. Track state via `wave-state.json`.
