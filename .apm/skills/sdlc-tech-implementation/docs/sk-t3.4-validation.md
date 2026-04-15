# Procedure: T3.4 — Validation

## Purpose

Run full build, test, and coverage validation for the item and verify
cumulative quality within the sprint.

## Pre-conditions

- Code generated (impl-log exists)
- Tests generated (test-log exists)
- Build and test commands are available

## Steps

### 1. Full build

Run the complete project build to verify end-to-end compilation:
- Backend build
- Frontend build (if applicable)
- Any additional module builds

### 2. Full test suite

Run all tests (not just the new ones) to detect regressions:
- Unit tests
- Integration tests
- Frontend tests
- E2E tests (if applicable for this stage)

### 3. Coverage check

Verify code coverage against project thresholds:
- Check coverage on modified modules
- Compare against project minimum thresholds
- Log coverage gaps if below threshold

### 4. Lint checks

Run project linting tools on changed files:
- Code style enforcement
- Static analysis rules
- Formatting verification

### 5. Security checks

Run security scans on changed files:
- Secret scan (e.g. gitleaks) on changed files
- SAST scan (e.g. Semgrep) on changed files
- Report any findings by severity

### 6. ADR compliance verification

For items touching architecture-sensitive areas:
- Verify cross-module import rules (if module boundaries changed)
- Verify security configuration (if security-related changes)
- Cross-reference against applicable ADRs

### 7. Write validation report

Create `outputs/docs/2-tech/3-implementation/validation-{item_id}.md` with:
- Build results (pass/fail per module)
- Test results (pass/fail with counts)
- Coverage metrics
- Lint findings
- Security scan results
- ADR compliance status

## Gate criteria

- [ ] Build passes (all modules)
- [ ] All tests pass
- [ ] Coverage thresholds met
- [ ] 0 secrets detected
- [ ] 0 critical SAST findings
- [ ] No ADR violations detected
