---
name: test-strategy
description: 'Define a risk-aligned test strategy covering scope, approach, coverage expectations, and test types for a feature or project.'
triggers: ['test strategy', 'test plan', 'testing approach', 'test coverage', 'quality assurance plan']
---

# Skill: test-strategy

## Goal

Define a risk-aligned test strategy that specifies what to test, how to test it, and what coverage is expected — enabling implementation teams to build the right tests at the right level.

## When to use

- After spec and task breakdown are complete (spec-kit, feature-implementation workflows)
- As a station in incident-resolution to ensure regression coverage
- When release-readiness requires documented test approach
- When spec-to-execution needs a testing plan before implementation

## Procedure

1. Load the specification, tasks, and any existing clarifications for context.
2. Identify risk areas from the spec (security-critical paths, data integrity, edge cases).
3. Define test types needed:
   - Unit tests (component isolation)
   - Integration tests (cross-component contracts)
   - E2E tests (user journey validation)
   - Performance tests (if NFRs specify thresholds)
   - Security tests (if security NFRs exist)
4. Map acceptance criteria to test cases — every AC should be testable.
5. Define coverage expectations per module/component.
6. Identify test data requirements and environment needs.
7. Write the test strategy document.

## Output

`outputs/specs/features/<feature>/test-strategy.md`

## Gate criteria

- **Pass**: All acceptance criteria mapped to tests, coverage targets defined, risk areas addressed
- **Fail**: Unmapped acceptance criteria, no coverage targets, or security-critical paths untested
- **Conditional**: Minor gaps with documented assumptions

## Rules

- Every acceptance criterion must map to at least one test case.
- Security-critical paths require explicit test coverage.
- Performance NFRs must have corresponding load/stress test plans.
- Prefer testing at the lowest feasible level (unit > integration > E2E).
