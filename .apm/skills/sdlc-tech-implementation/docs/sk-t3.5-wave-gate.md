# Procedure: T3.5 — Wave Gate

## Purpose

After all items in a wave are completed (possibly across multiple sprints),
evaluate the wave gate criteria from [IMP-001] and decide whether to proceed
to the next wave.

## Pre-conditions

- All items in the current wave are marked `completed` in `wave-state.json`
- All item-level validation reports exist

## When does the wave gate fire?

The wave gate is **not tied to a single sprint**. It fires when:
1. The last item of the wave is completed and validated (T3.4 passes)
2. All items in the wave state are `completed`

This means a wave can span multiple sprints. The sprint-level output is a
sprint summary; the wave-level output is the wave gate report.

## Steps

### 1. Load wave gate criteria

Read [IMP-001] — extract the DoD criteria for the current wave:
- Wave-specific functional criteria (e.g. "docker compose up works" for W0)
- Quality thresholds
- Integration verification requirements

### 2. Aggregate validation reports

Collect all `W{wave_id}/validation-{item_id}.md` files for items in this wave:
- Compile cumulative build/test/coverage metrics
- Identify any items with warnings or non-critical findings

### 3. Evaluate gate criteria

For each wave DoD criterion from [IMP-001]:
1. Check if the criterion is met based on validation reports
2. Record PASS/FAIL with evidence reference
3. If any criterion fails → gate FAILS

### 4. Gate passes

If all criteria are met:
1. Mark wave as `completed` in `wave-state.json` with `completed_at` timestamp
2. Mark the next wave as `in-progress`
3. Write wave report: `outputs/docs/2-tech/3-implementation/W{wave_id}/wave-{wave_id}-report.md` using the `tpl-wave-report.md` template
4. Log that T4 Quality (drift detection) should be triggered on the wave's code

### 5. Gate fails

If any criterion is not met:
1. Write failure report with:
   - Which criteria failed
   - Which items are blocking
   - Suggested remediation actions
2. Do NOT advance to the next wave
3. Await human decision: fix and re-evaluate, or override gate

## Gate criteria

- [ ] All items in wave completed and validated
- [ ] Wave-specific DoD from [IMP-001] met
- [ ] No blocker issues pending
