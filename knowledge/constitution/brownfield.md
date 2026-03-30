# Brownfield Constitution

Rules for changes to existing systems.

## Start with a reverse brief

- Document the current state before proposing changes.
- Identify affected modules, dependencies, and stakeholders.
- Map existing tests and coverage.

## Rules

- Backward compatibility is the default unless explicitly scoped out.
- Minimal blast radius: change only what is necessary.
- Coexistence strategy: old and new must run side by side during migration.
- Regression testing is mandatory for every change.
- Document what you found, not just what you changed.
