---
name: readme
description: 'Rules for maintaining the root README.md as canonical repo documentation.'
applyTo: README.md
---

# README Maintenance Instructions

The root README.md is the canonical documentation for this repository.
It must reflect the actual state of the repo at all times.

## Self-maintenance rules

1. **When adding an agent**: update the Agents heading count, Agents table (new row), Asset summary table, Architecture diagram counts, and Repository Layout counts.
2. **When adding a skill**: update the Skills heading count, Skills table (new row in correct category), and Asset summary table.
3. **When adding a workflow**: update the Workflows heading count, add a detailed station table under the correct workflow category (Delivery / Specification / Validation / Assessment), update the Table of Contents, and update the Asset summary table.
4. **When adding a prompt**: update the Prompts heading count, Prompts table (new row), and Asset summary table.
5. **When adding an instruction**: update the Asset summary table and Repository Layout counts.
6. **When changing directory structure**: update the Repository Layout table.
7. **When changing provider projections**: update the Provider Setup section and Architecture diagram counts.
8. **When adding or renaming a doc in `docs/`**: update `docs/README.md` (the Documentation Hub) — add or update the row in the appropriate audience table (Consumers, Reference, Contributors, Shared).
9. **After any change**: run `python scripts/validate_all.py` to verify cross-layer consistency.

## Counts to keep in sync

These locations all contain counts that must match the actual file counts:

- **Asset summary table** (top of README)
- **Architecture diagram** (ASCII art counts in the canonical layer box)
- **Repository Layout table** (parenthetical counts per path)
- **Section headings** — e.g., `## Agents (17)`, `## Workflows (15)`
- **Workflow sub-headings** — station counts, e.g., `#### feature-implementation (10 stations)`

## Style

- Use Markdown tables for structured lists.
- Keep the architecture diagram current.
- Do not duplicate content from `.apm/` — reference it.
- Section heading counts must match actual file counts.
- Each workflow gets its own sub-section with a detailed station table (columns: #, Station, Agent, Skills, Outputs, Gate Severity).
- Group workflows by type: Delivery, Specification, Validation, Assessment.
