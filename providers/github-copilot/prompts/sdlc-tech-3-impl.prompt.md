---
name: sdlc-tech-3-impl
mode: agent
description: 'Run Tech System T3 — Implementation (5 stations, iterative per sprint).'
---

# /sdlc-tech-3-impl

Run the Tech implementation pipeline per sprint.

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-task-resolution` through `tech-wave-gate`.
2. Load sprint scope from [IMP-001] and `wave-state.json`.
3. Create feature branch for the current wave: `git checkout -b feat/W{id}-{slug} main`.
4. For each item in dependency order: resolve context (T3.1) → generate code (T3.2) → implement tests (T3.3) → validate + commit (T3.4).
5. If all wave items completed:
   a. Evaluate wave gate (T3.5)
   b. Run T4.1 drift detection on the branch
   c. Push branch: `git push origin feat/W{id}-{slug}`
   d. Verify CI pipeline passes (T3.6)
   e. Create MR to main (T3.7)
6. Write sprint summary.
7. After last wave gate of sprint: run T4.3 E2E campaign generation with testability filter.
8. **Use `edit/editFiles` or `create_file` to write every artifact as an actual file on disk** under `outputs/docs/2-tech/3-implementation/`. Do not merely display content in chat.
9. Track state via `wave-state.json`.
