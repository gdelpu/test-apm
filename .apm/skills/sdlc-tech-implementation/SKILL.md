---
name: sdlc-tech-implementation
description: 'Execute the implementation plan wave-by-wave per sprint, producing code with full T0-T2 context injection, BA-traced tests, and wave gate validation.'
triggers: ['implementation', 'code generation', 'wave execution', 'sprint implementation']
---

# Skill: sdlc-tech-implementation

## Goal

Execute the implementation plan [IMP-001] wave-by-wave, producing production code
and tests with full technical context (ADRs, stack conventions, data model, API
contracts, test strategy) and BA traceability (business rules, test scenarios).

The system is designed for **iterative per-sprint execution**: each sprint selects
a subset of items from the current wave, executes them through the T3 pipeline,
and validates them at the wave gate. A wave may span multiple sprints; the wave
gate fires only when all wave items are completed.

## When to use

- After T2 Design is complete and validated
- As System T3 in the `sdlc-tech` workflow
- Runs per sprint scope, per wave
- Can be invoked iteratively: one sprint at a time or in a continuous loop

## Sprint-iterative execution model

```
Sprint N scope (from IMP-001 + sprint planning):
│
│  For each item in sprint scope (dependency order):
│  ┌─────────────────────────────────────────────────┐
│  │ T3.1 Task Resolution   → current-task.md        │
│  │ T3.2 Code Generation   → impl-log.md + code     │
│  │ T3.3 Test Implementation → test-log.md + tests   │
│  │ T3.4 Validation        → validation-report.md    │
│  └─────────────────────────────────────────────────┘
│         (loop per item)
│
├─ If all items in current wave are now completed:
│  └─ T3.5 Wave Gate → wave-report.md → advance to next wave
│
└─ If wave has remaining items:
   └─ Sprint complete → update wave-state.json → resume next sprint
```

## Inputs — full T0-T2 context

### Mandatory inputs (must exist before execution)

| Input | ID | From system | Used by phase |
|-------|----|-------------|---------------|
| Implementation Plan | [IMP-001] | T2 Design | T3.1 Task Resolution |
| Stack Conventions | [STK-001] | T1 Architecture | T3.2 Code Generation |
| Data Model | [DAT-001] | T2 Design | T3.2 Code Generation |
| API Contracts | [API-xxx] | T2 Design | T3.2 Code Generation |
| Test Strategy | [TST-001] | T2 Design | T3.3 Test Implementation |
| Enabler Index | [ENB-000] | T1 Architecture | T3.1 Task Resolution |

### Contextual inputs (loaded on-demand per item)

| Input | ID | From system | Used when |
|-------|----|-------------|-----------|
| ADRs | [ADR-001] to [ADR-nnn] | T1 Architecture | Code touches the ADR's scope |
| System Context | [CTX-001] | T1 Architecture | Integration-related tasks |
| BA Domain Model | [DOM-001] | BA Specification | Entity/JPA tasks |
| Business Rules | [BRL-*] | BA Specification | Service-layer logic |
| Test Scenarios | [SCE-xxx] | BA Tests | E2E and integration tests |
| User Stories | [US-xxx] | BA Specification | Feature tasks |

### Sprint-level inputs

Each sprint execution also reads:
- The **wave state file** (`wave-state.json`) to know which items are completed
- The **sprint scope** — item IDs selected for this sprint from [IMP-001]
- The **gate criteria** from [IMP-001] for the current wave
- The **dependency graph** (JSON queue in IMP-001 §4) to determine item ordering

## Procedure

### Phase T3.1 — Task Resolution

**Purpose:** Select the next implementable item from the sprint scope, resolve its
full context, and produce a self-contained task description.

1. Load [IMP-001] §4 JSON implementation queue
2. Load `wave-state.json` — identify current wave and completed items
3. Select the next item in sprint scope whose `deps` are all completed
4. For the selected item, resolve context:
   a. Which [ADR-xxx] applies? (from `story_ref` or `enb_or_story_ref`)
   b. Which [DAT-001] tables are impacted? (from `title` and `deliverable`)
   c. Which [API-xxx] endpoints are relevant? (from `story_ref`)
   d. Which [TST-001] test IDs should be implemented? (from `story_ref`)
   e. Which [BRL-*] business rules apply?
5. Write `outputs/docs/2-tech/3-implementation/current-task-{item_id}.md` containing:
   - Item metadata (id, title, type, wave, estimate, deps, sprint)
   - Resolved context (relevant ADR excerpts, DAT columns, API contract, test IDs)
   - Acceptance criteria (from [IMP-001] deliverable column + relevant gate criteria)
   - Naming conventions (from [STK-001] §4)

**Gate criteria:**
- Task prerequisites (deps) are verified as completed
- Context resolution produced at least one relevant upstream reference
- Task scope is bounded (estimated ≤ 8h)

### Phase T3.2 — Code Generation

**Purpose:** Produce or modify source code for the resolved task, following all
project conventions and upstream specifications.

1. Read resolved task from `current-task-{item_id}.md`
2. Read [STK-001] for naming conventions, patterns, and project structure
3. For **database tasks** (Flyway migrations, JPA entities):
   a. Read [DAT-001] — exact column definitions, types, constraints, indexes
   b. Generate migration SQL matching DAT-001 DDL exactly
   c. Generate JPA entity with column mappings matching DAT-001
4. For **API controller tasks**:
   a. Read [API-xxx] — endpoint URL, method, DTOs, error codes, RBAC
   b. Generate controller matching API contract exactly (no deviation)
   c. Generate DTOs matching API-xxx field definitions
   d. Generate service interface matching sequence diagram
5. For **frontend tasks**:
   a. Read [API-xxx] — expected request/response shapes
   b. Read [STK-001] — frontend integration rules, component patterns
   c. Generate components following project conventions
6. For **enabler tasks** (ENB-Cxx):
   a. Read relevant [ADR-xxx] for decision details
   b. Read [ENB-000] for enabler scope and included tasks
7. After code generation, run build command (per project conventions)
8. Write implementation log: `outputs/docs/2-tech/3-implementation/impl-log-{item_id}.md`

**Gate criteria:**
- Code compiles without errors
- Generated code adheres to [STK-001] naming conventions
- Database migrations match [DAT-001] column definitions exactly
- API controllers match [API-xxx] contracts (URL, method, DTOs, error codes)
- No files modified outside the task scope

### Phase T3.3 — Test Implementation

**Purpose:** Generate tests traceable to BA test scenarios and the TST-001 catalogue.

1. Read resolved task from `current-task-{item_id}.md`
2. Read [TST-001] — identify which test IDs correspond to this item
3. For each test type (unit, integration, frontend, E2E, security):
   a. Read the test description from the relevant TST-001 section
   b. Generate test file following TST-001 naming conventions
   c. Include BA traceability comment (e.g. `// Implements: [BR-xxx], [US-xxx]`)
4. Run test suite
5. Write test log: `outputs/docs/2-tech/3-implementation/test-log-{item_id}.md`

**Gate criteria:**
- Every test ID from [TST-001] mapped to this item has a corresponding test file
- Tests pass (build green)
- Each test contains a BA traceability comment
- Test naming follows [TST-001] conventions

### Phase T3.4 — Validation

**Purpose:** Run full build, test, and coverage validation for the item.

1. Run full build (backend + frontend as applicable)
2. Check coverage against project thresholds
3. Run lint checks
4. Run security checks (secret scan, SAST on changed files)
5. Verify ADR compliance (cross-module imports, security headers if applicable)
6. Write validation report: `outputs/docs/2-tech/3-implementation/validation-{item_id}.md`

**Gate criteria:**
- Build passes
- All tests pass
- Coverage thresholds met
- 0 secrets detected
- 0 critical SAST findings
- No ADR violations detected

### Phase T3.5 — Wave Gate

**Purpose:** After all items in a wave are completed (possibly across multiple sprints),
evaluate the wave gate criteria from [IMP-001] and decide whether to proceed.

1. Read [IMP-001] — wave gate criteria for the current wave
2. Aggregate all validation reports for items in this wave
3. Check cumulative metrics:
   - All items marked completed in wave state
   - All item-level gates passed
   - Wave-specific criteria met (from [IMP-001] §6)
4. If gate passes:
   a. Mark wave as COMPLETED in `wave-state.json`
   b. Write wave report: `outputs/docs/2-tech/3-implementation/wave-{wave_id}-report.md`
   c. Trigger T4 Quality — drift detection on newly implemented code
5. If gate fails:
   a. Write failure report with specific blocking items
   b. Stop and await manual resolution

**Gate criteria:**
- All items in wave completed and validated
- Wave-specific DoD from [IMP-001] met
- No blocker issues pending

## Output

| Output | ID | Location |
|--------|----|----------|
| Resolved task (per item) | — | `outputs/docs/2-tech/3-implementation/current-task-{item_id}.md` |
| Implementation log (per item) | — | `outputs/docs/2-tech/3-implementation/impl-log-{item_id}.md` |
| Test log (per item) | — | `outputs/docs/2-tech/3-implementation/test-log-{item_id}.md` |
| Validation report (per item) | — | `outputs/docs/2-tech/3-implementation/validation-{item_id}.md` |
| Wave completion report | — | `outputs/docs/2-tech/3-implementation/wave-{wave_id}-report.md` |
| Sprint summary | — | `outputs/docs/2-tech/3-implementation/sprint-{sprint_id}-summary.md` |
| Wave state file | — | `outputs/docs/2-tech/3-implementation/wave-state.json` |
| Source code | — | `src/` (project source tree) |

## Rules

1. **Phases are sequential per item:** T3.1 → T3.2 → T3.3 → T3.4 (loop per item within a sprint)
2. **T3.5 runs once per wave** after all items in that wave are completed (may span multiple sprints)
3. **Wave ordering is strict:** W0 → W1 → W2 → ... → WNFR. No wave starts until the previous wave's gate passes.
4. **Sprint scoping is flexible:** A sprint may contain items from a single wave only. The sprint scope is the intersection of the wave backlog and the sprint planning selection.
5. **Context injection is mandatory:** T3.2 must NOT generate code without first reading the relevant upstream documents (DAT, API, STK, ADRs)
6. **Traceability is mandatory:** every test must have a BA traceability comment
7. **No deviation from specs:** generated code must match DAT-001 columns, API-xxx contracts, and STK-001 conventions exactly
8. **Incremental state:** `wave-state.json` tracks completed items and sprint boundaries, allowing resume after interruption
9. **Scope discipline:** each item generates only what its [IMP-001] entry specifies — no scope creep
10. **Sprint summary:** at the end of each sprint invocation, write a sprint summary listing completed items, remaining wave backlog, and blockers

## Context management

AI coding agents have finite context windows. The T3 pipeline applies the following rules to prevent context overflow during wave execution:

### Per-item context isolation

Each T3.1→T3.4 cycle operates on a **single item**. At the start of each item:

1. **Reload only the upstream documents relevant to this item** (per [Context resolution rules](#context-resolution-rules) below). Do NOT carry forward the full context of all previous items.
2. **Read `wave-state.json`** for current progress — this is a lightweight file (IDs + statuses only).
3. **Do NOT accumulate previous items' impl-log, test-log, or validation reports** in the active context. They are written to disk and not needed for subsequent items.

### Mandatory context pruning between items

After completing T3.4 for an item:

1. **Drop from active context:** `current-task-{prev_id}.md`, `impl-log-{prev_id}.md`, `test-log-{prev_id}.md`, `validation-{prev_id}.md`.
2. **Retain in context:** `wave-state.json` (updated), [STK-001] (conventions are cross-cutting), and active sprint scope.
3. **Reload on demand** for the next item: the relevant upstream docs are re-resolved in T3.1.

### Wave size and sub-batching

- Waves are capped at **12 items** by the upstream [IMP-001] plan (enforced in T2.5).
- If a wave exceeds 12 items (legacy plan), the T3 executor **sub-batches** automatically: process 10 items, write a checkpoint to `wave-state.json`, and start a fresh context for the remaining items.
- The **wave gate (T3.5) runs once** after all sub-batches complete — it reads validation reports from disk, not from context.

### What stays loaded vs. what is reloaded per item

| Document | Loaded once per sprint | Reloaded per item |
|----------|----------------------|-------------------|
| [STK-001] Stack conventions | ✅ | |
| [IMP-001] §4 JSON queue | ✅ | |
| `wave-state.json` | ✅ (updated in-place) | |
| [DAT-001] Data model | | ✅ if item touches DB |
| [API-xxx] API contracts | | ✅ if item touches endpoints |
| [ADR-xxx] Decisions | | ✅ matching ADR only |
| [TST-001] Test strategy | | ✅ relevant section only |
| [BRL-*] Business rules | | ✅ matching rules only |
| Previous item artifacts | ❌ never | ❌ never |

## Context resolution rules

| Item characteristic | Documents to load |
|--------------------|-------------------|
| `type: "enabler"` and `story_ref: "ENB-Cxx"` | [ENB-000] enabler details, relevant [ADR-xxx] |
| Title contains migration/schema terms | [DAT-001] full table definitions |
| Title contains entity/repository terms | [DAT-001] table + [STK-001] naming |
| Title contains controller/endpoint terms | [API-xxx] endpoint contract + sequence diagram |
| Title contains frontend/component terms | [API-xxx] DTOs + [STK-001] frontend conventions |
| Title contains E2E/Playwright terms | [TST-001] E2E scenarios + [SCE-xxx] |
| Title contains security/RBAC/JWT terms | Security ADRs, [TST-001] SEC tests |
| Title contains batch/CronJob terms | Async/batch ADRs |
| Title contains Docker/Helm/CI terms | Infrastructure ADRs |
| Title contains observability terms | Observability ADRs |
| `story_ref` starts with "US-" | [US-xxx] user story + [BRL-*] associated rules |
| `story_ref` starts with "FT-" | All US under that feature + [SCE-xxx] scenarios |

## Error handling and recovery

| Scenario | Behaviour |
|----------|-----------|
| Build fails in T3.2 | Log error, retry once with fix attempt. If still failing, mark item as `failed` and stop. |
| Test fails in T3.3 | If test is wrong, fix test. If code is wrong, return to T3.2. Max 2 retries per item. |
| Coverage below threshold in T3.4 | Return to T3.3 to add missing tests. |
| Wave gate fails in T3.5 | Write failure report. Stop execution. Await human decision. |
| Item dependency not met | Skip item, process next eligible. Return when dependency completes. |
| Session interrupted | `wave-state.json` preserves progress. Resume from last incomplete item. |

## Resources

| Resource | Purpose |
|----------|---------|
| `resources/tpl-wave-report.md` | Wave completion report template |
| `resources/tpl-impl-log.md` | Per-item implementation log template |
| `resources/tpl-sprint-summary.md` | Sprint summary template |
| `docs/sk-t3.1-task-resolution.md` | Task resolution procedure |
| `docs/sk-t3.2-code-generation.md` | Code generation procedure |
| `docs/sk-t3.3-test-implementation.md` | Test implementation procedure |
| `docs/sk-t3.4-validation.md` | Validation procedure |
| `docs/sk-t3.5-wave-gate.md` | Wave gate procedure |
