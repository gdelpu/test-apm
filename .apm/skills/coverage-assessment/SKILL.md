# Skill: coverage-assessment

## Goal

Measure test coverage and evaluate whether it meets configured thresholds. Select the appropriate coverage tool based on the project's language and test framework.

## Adapters

| Adapter | Language | Tool |
|---------|----------|------|
| `jacoco-adapter.md` | Java | JaCoCo |
| `istanbul-adapter.md` | JavaScript, TypeScript | Istanbul / nyc |
| `coveragepy-adapter.md` | Python | Coverage.py |

## Procedure

1. Detect project language
2. Select the matching coverage adapter
3. Run tests with coverage instrumentation
4. Parse coverage report for line/branch percentages
5. Compare against threshold (configurable, default: 80%)
6. Produce `coverage-report.md`

## Gate criteria

- **Pass**: Coverage percentage meets or exceeds configured threshold
- **Fail**: Coverage below threshold
- **Skip**: Coverage tool not installed or no tests found

## Configuration

Coverage thresholds can be set via environment variable or project config:
- `COVERAGE_THRESHOLD` environment variable (default: 80)
- Or project-specific configuration (e.g., `.nycrc`, `pytest.ini`, `pom.xml`)

## Output

`coverage-report.md` following the quality-validator report format.
