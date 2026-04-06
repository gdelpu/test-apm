---
name: cv-dep-markdown
description: 'Convention defining formatting and structural rules for all deliverables produced by the DEP-Agents domain.'
triggers: ['DEP output format', 'DEP markdown convention', 'DEP deliverable structure']
---

# Convention: DEP Agents — Markdown & Output Format

## Purpose

This convention defines the formatting and structural rules for all deliverables produced by the DEP-Agents domain. It ensures consistency with the wider backBone harness while adapting to the specificity of DEP asset configuration outputs (YAML files, CI pipelines, workstation configs).

---

## 1. Deliverable structure

Every DEP deliverable is a Markdown document with YAML front matter, containing:
1. Context summary (why this configuration was chosen)
2. Asset-specific configuration (YAML code blocks)
3. Activation guide (how to use / deploy)
4. Customisation reference (variables and options)
5. Points of attention (assumptions, risks, open items)
6. Production confidence (filled by post-quality-control hook)

---

## 2. YAML front matter

All deliverables **must** include the following front matter:

```yaml
---
id: [ID]
title: "[Full title]"
type: dep-[asset]        # dep-ci | dep-mw | dep-iac
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-dep[N].[N]
tech_dependencies: []    # IDs of Tech-Agent deliverables used as inputs
---
```

---

## 3. Code blocks

- All YAML configuration blocks: fenced with ` ```yaml `
- All shell/CLI commands: fenced with ` ```bash `
- All `.gitlab-ci.yml` fragments: fenced with ` ```yaml ` and annotated with a comment header
- Never inline configuration values — always use code blocks

---

## 4. Tables

Use Markdown tables for:
- Module inventories (workstation)
- Job inventories (CI pipeline)
- Variable reference sheets
- Environment mapping (launchpad)

Column widths must be consistent. Use `—` for empty cells, never leave them blank.

---

## 5. Identifiers

DEP deliverable identifiers follow this pattern:

| Asset | Prefix | Example |
|-------|--------|---------|
| GitLab CI setup | `CI-` | `CI-001-gitlab-ci-setup` |
| Modern Workstation config | `MW-` | `MW-001-workstation-config` |
| DEP Launchpad IaC | `IAC-` | `IAC-001-launchpad-setup` |

Reference upstream Tech-Agent deliverables using their brackets: `[STK-001]`, `[CTX-001]`, `[IMP-001]`.

---

## 6. Points of attention

Any assumption, open question, or risk must be flagged in a dedicated section:

```markdown
## ⚠ Points of attention

| # | Type | Description | Action required |
|---|------|-------------|-----------------|
| 1 | Assumption | ... | Confirm with team |
| 2 | Risk | ... | Validate before merge |
| 3 | Open | ... | Decision pending |
```

Types: `Assumption` | `Risk` | `Open` | `Dependency`

---

## 7. Language

- All deliverables are written in **English**
- Variable names, keys, and file paths are verbatim (no translation)
- Comments inside YAML/CI blocks are in English
