# Procedure: T3.1 — Task Resolution

## Purpose

Select the next implementable item from the sprint scope, resolve its full
upstream context, and produce a self-contained task description that the
code-generation phase can execute without additional lookups.

## Pre-conditions

- [IMP-001] Implementation Plan exists and is validated
- `wave-state.json` exists (or will be initialized on first run)
- Sprint scope is defined (list of item IDs for this sprint)

## Steps

### 1. Load implementation queue

Read `[IMP-001]` §4 — the JSON implementation queue containing all items across all waves with their dependencies, estimates, types, and story references.

### 2. Determine current state

Load `wave-state.json`:
- Identify the current wave (e.g. W0, W1, W2, WNFR)
- List already-completed items
- If the file does not exist, initialize it with all waves in `not-started` status, marking W0 as `in-progress`

### 3. Select next item

From the sprint scope:
1. Filter items belonging to the current wave
2. Exclude items already marked `completed` or `failed` in wave state
3. From the remaining items, select the first one whose `deps` are all `completed`
4. If no item is eligible (all blocked), report `BLOCKED` and stop

### 3b. Sub-batch boundary check

If the wave contains more than 12 items (legacy plan without the wave size cap):
1. Track a `sub_batch_count` in wave state (defaults to 0)
2. After every 10 items completed within the same context session, write a checkpoint to `wave-state.json` and **signal a context reset** — the orchestrator must start a fresh context for the remaining items
3. On context restart, reload only: `wave-state.json`, [STK-001], [IMP-001] §4 queue, and sprint scope

### 4. Resolve context

For the selected item, determine which upstream documents are relevant using the context resolution rules from SKILL.md:

| Lookup | Action |
|--------|--------|
| ADR relevance | Match `story_ref` or item title against ADR scopes |
| Data model | Check if title implies database/entity work → load [DAT-001] |
| API contracts | Check if title implies controller/DTO work → load [API-xxx] |
| Test IDs | Match `story_ref` against [TST-001] to find mapped test IDs |
| Business rules | Match `story_ref` against BA [BRL-*] catalogue |
| Enabler details | If `type: enabler`, load [ENB-000] for enabler scope |

### 5. Write resolved task

Create `outputs/docs/2-tech/3-implementation/W{wave_id}/current-task-{item_id}.md` with:

```markdown
# Resolved Task — {item_id}

## Metadata
- **ID:** {item_id}
- **Title:** {title}
- **Type:** {type}
- **Wave:** {wave}
- **Sprint:** {sprint_id}
- **Estimate:** {estimate}h
- **Dependencies:** {deps} (all completed ✓)

## Resolved context
### ADRs
{relevant ADR excerpts}

### Data model
{relevant DAT-001 table definitions}

### API contract
{relevant API-xxx endpoint definition}

### Test IDs
{list of TST-001 test IDs to implement}

### Business rules
{relevant BRL-* rules}

## Acceptance criteria
{from IMP-001 deliverable column + wave gate criteria}

## Naming conventions
{from STK-001 §4}
```

### 6. Update wave state

Mark the item as `in-progress` in `wave-state.json` with `started_at` timestamp.

## Gate criteria

- [ ] Task prerequisites (deps) are verified as completed
- [ ] Context resolution produced at least one relevant upstream reference
- [ ] Task scope is bounded (estimated ≤ 8h)
- [ ] Previous item artifacts (`current-task-{prev_id}`, `impl-log-{prev_id}`, etc.) are NOT in active context
