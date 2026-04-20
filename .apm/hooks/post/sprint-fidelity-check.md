# Post-Hook: Sprint Fidelity Check

> **Applies to:** `tech-impl-plan` station
> **Severity:** blocker
> **Trigger:** after IMP-001 is produced, before gate evaluation

## Purpose

Verify that the implementation plan (IMP-001) is consistent with the sprint planning (PLAN-001). Detect missing items, silent sprint reallocations, and filtered infrastructure enablers.

## Checks

### CHECK-SF-01: Item coverage

For each sprint in scope, extract enabler IDs (`ENB-*`) and feature IDs (`FT-*`) from PLAN-001's `scope_items` (or equivalent sprint breakdown).

- **PASS**: every ID from PLAN-001 for the sprint(s) in scope appears in IMP-001.
- **FAIL**: one or more IDs are absent from IMP-001 → list the missing IDs.

### CHECK-SF-02: Sprint allocation fidelity

For each item present in both PLAN-001 and IMP-001, verify the sprint assignment matches.

- **PASS**: item is in the same sprint as PLAN-001, or a `## Deviations from sprint plan` section documents the reallocation with a rationale.
- **FAIL**: item is in a different sprint with no documented justification.

### CHECK-SF-03: Infrastructure wave presence

Verify that IMP-001 contains at least one wave or sub-wave categorized as infrastructure/IaC (type: `enabler` with sub-type `iac`, `helm`, `pb_scenario`, or `devops`), when PLAN-001 includes infrastructure enablers for the sprint.

- **PASS**: infrastructure items from PLAN-001 are present as waves in IMP-001.
- **FAIL**: infrastructure enablers from PLAN-001 are absent — likely filtered by "code-only" bias.

## Verdict

| Result | Action |
|--------|--------|
| All checks PASS | Proceed to gate evaluation |
| Any check FAIL | **STOP** — agent must revise IMP-001 to include missing items or document deviations before gate evaluation |
