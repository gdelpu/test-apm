---
name: lint-analysis
description: 'Run language-specific linters to detect code style violations, syntax errors, and potential bugs.'
triggers: ['linting', 'code style', 'syntax errors', 'lint rules']
---

# Skill: lint-analysis

## Goal

Run language-specific linters to detect code style violations, syntax errors, and potential bugs. Select the appropriate linter based on the project's language and stack.

## Adapters

| Adapter | Language | Tool |
|---------|----------|------|
| `eslint-adapter.md` | JavaScript, TypeScript | ESLint |
| `pylint-adapter.md` | Python | Pylint |
| `clippy-adapter.md` | Rust | Clippy |

## Procedure

1. Detect project language from file extensions and build configuration
2. Select the matching adapter(s)
3. Check that the linter is installed (use adapter's `check_command`)
4. Run the linter (use adapter's `run_command`)
5. Parse output for error and warning counts
6. Produce `lint-report.md`

## Gate criteria

- **Pass**: Zero errors (warnings are acceptable)
- **Fail**: One or more errors detected
- **Skip**: Linter not installed (report as skipped, not failed)

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/lint-report.md`
