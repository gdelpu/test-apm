---
name: quality-report
description: 'Aggregate results from all quality validation stations into a single, comprehensive quality report.'
triggers: ['quality report', 'quality aggregation', 'validation summary']
---

# Skill: quality-report

## Goal

Aggregate results from all quality validation stations into a single, comprehensive quality report with an overall pass/fail assessment.

## When to use

- As the final station in the quality-validation workflow
- When all individual quality stations have completed

## Procedure

1. Read all station reports from the output directory:
   - `lint-report.md`
   - `static-analysis-report.md`
   - `sast-report.md`
   - `dependency-report.md`
   - `coverage-report.md`
   - `dast-report.md` (if present)
2. Extract status (passed/failed/skipped) from each report
3. Aggregate into a summary table
4. Determine overall status: passed only if all non-skipped stations passed
5. Write `quality-report.md`

## Gate criteria

- **Pass**: All non-skipped stations passed
- **Fail**: One or more stations failed

## Output format

    # Quality Report

    **Feature**: <feature name>
    **Date**: <timestamp>
    **Overall status**: passed | failed

    ## Station summary

    | Station | Tool | Status | Key findings |
    |---------|------|--------|-------------|
    | Lint | <tool> | passed/failed/skipped | <summary> |
    | Static Analysis | <tool> | passed/failed/skipped | <summary> |
    | SAST | <tool> | passed/failed/skipped | <summary> |
    | Dependency Audit | <tool> | passed/failed/skipped | <summary> |
    | Coverage | <tool> | passed/failed/skipped | <summary> |
    | DAST | <tool> | passed/failed/skipped | <summary> |

    ## Details

    <per-station detail sections>

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/quality-report-template.md` | Quality report output template |
