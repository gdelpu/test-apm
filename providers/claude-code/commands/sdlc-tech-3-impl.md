# /sdlc-tech-3-impl

Execute the **Tech System T3 — Implementation** pipeline.

## Steps

1. Read `.apm/workflows/sdlc-tech.yml` — stations `tech-task-resolution` through `tech-wave-gate`.
2. Read `.apm/contexts/sdlc-agent-registry.yaml` — agent compositions for tech-t3.1 through tech-t3.5.
3. Load sprint scope — determine which items from [IMP-001] are in scope for this sprint.
4. Load `wave-state.json` — determine current wave and completed items.
4b. Create feature branch for the current wave: `git checkout -b feat/W{id}-{slug} main`
5. For each item in sprint scope (dependency order):
   - T3.1: Resolve task context from T0-T2 deliverables
   - T3.2: Generate code following STK-001, DAT-001, API-xxx specs
   - T3.3: Generate tests with BA traceability (TST-001 mapping)
   - T3.4: Validate (build, test, coverage, SAST)
6. If all wave items are now completed:
   a. Run T3.5 wave gate
   b. Run T4.1 drift detection on the branch
   c. Push branch: `git push origin feat/W{id}-{slug}`
   d. Verify CI pipeline passes (T3.6)
   e. Create MR to main (T3.7)
7. Write sprint summary.
7b. After last wave gate of sprint: run T4.3 E2E campaign generation with testability filter
8. **Write every artifact as an actual file on disk** under `outputs/docs/2-tech/3-implementation/`. Do not merely display content in chat — use file-writing tools to create each file.

This pipeline runs **iteratively per sprint**. A wave may span multiple sprints.

## Prerequisites

T2 deliverables must exist: [IMP-001], [STK-001], [DAT-001], [API-xxx], [TST-001].

## Outputs

- `current-task-{item_id}.md` — resolved task with full upstream context
- `impl-log-{item_id}.md` — implementation log per item
- `test-log-{item_id}.md` — test log per item
- `validation-{item_id}.md` — validation report per item
- `wave-{wave_id}-report.md` — wave completion report (when wave gate passes)
- `sprint-{sprint_id}-summary.md` — sprint summary
- `wave-state.json` — progress tracking across sprints
