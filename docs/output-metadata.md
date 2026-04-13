# Output File Metadata

> How agents and workflows tag every file they produce under `outputs/` with structured, machine-readable YAML frontmatter.

---

## Table of Contents

- [Overview](#overview)
- [Required Frontmatter](#required-frontmatter)
- [Field Reference](#field-reference)
  - [workflow](#workflow)
  - [trigger](#trigger)
  - [date](#date)
  - [status](#status)
  - [inputDocuments](#inputdocuments)
  - [changeHistory](#changehistory)
  - [holisticQualityRating](#holisticqualityrating)
  - [overallStatus](#overallstatus)
- [Lifecycle](#lifecycle)
  - [On File Creation](#on-file-creation)
  - [On File Update](#on-file-update)
- [Ownership Rules](#ownership-rules)
- [Schema](#schema)
- [Compatibility with BA Conventions](#compatibility-with-ba-conventions)
- [Examples](#examples)

---

## Overview

Every file written under `outputs/` by an agent or workflow **must** include YAML frontmatter that records:

- **Provenance** — which workflow produced it and what triggered the execution
- **Lineage** — which input documents were consumed
- **Lifecycle** — current document status and full change history
- **Quality** — holistic quality rating and overall health verdict after review

This metadata makes output artifacts traceable, auditable, and machine-consumable across the entire SDLC pipeline.

---

## Required Frontmatter

```yaml
---
workflow: <workflow name>
trigger: <trigger source>
date: '<YYYY-MM-DD>'
status: <draft | review | validated | superseded | archived>
inputDocuments:
  - <relative path to source document>
changeHistory:
  - date: '<YYYY-MM-DD>'
    description: '<summary>'
    changes:
      - '<individual change>'
holisticQualityRating: <excellent | good | adequate | poor | insufficient | not-rated>
overallStatus: <good | warning | critical | not-reviewed>
---
```

---

## Field Reference

### `workflow`

Name of the workflow that created the file. Use the canonical workflow ID from `.apm/workflows/` (e.g., `spec-kit`, `feature-implementation`, `quality-validation`, `bug-fixing`).

### `trigger`

What initiated the workflow execution. Examples:

| Value | Meaning |
|-------|---------|
| `user` | End user invoked directly |
| `hub-orchestrator` | Dispatched by the Hub Orchestrator |
| `spec-kit/station-3` | Triggered by another workflow station |
| `pr-validation` | Triggered by a PR event |

### `date`

ISO 8601 date (`YYYY-MM-DD`) of the initial file creation. Do **not** update this on subsequent edits — use `changeHistory` instead.

### `status`

Document lifecycle state. **Closed list**:

| Value | Meaning | Set by | When |
|-------|---------|--------|------|
| `draft` | Initial creation — default for all new files | Producing agent | Automatically on file creation |
| `review` | Submitted for review by a human or agent | Producing agent or orchestrator | When submitting for human/agent review |
| `validated` | Approved and accepted | Reviewing agent or human | After approval at a quality gate |
| `superseded` | Replaced by a newer version | Any agent | When a newer version of this document is created |
| `archived` | Retired — no longer active | Any agent or human | When the document is retired |

### `inputDocuments`

Array of relative paths (from repo root) listing all documents used as input. Use an empty array `[]` if the workflow consumed no documents.

### `changeHistory`

Chronological log of every modification. The first entry records initial creation. Each entry contains:

| Sub-field | Type | Description |
|-----------|------|-------------|
| `date` | `YYYY-MM-DD` | When the change was made |
| `description` | string | One-line human-readable summary |
| `changes` | string[] | List of specific modifications made by agents |

### `holisticQualityRating`

Content quality rating after agent review. **Closed list**:

| Value | Meaning |
|-------|---------|
| `excellent` | Exceeds expectations — no gaps |
| `good` | Meets expectations — minor observations only |
| `adequate` | Acceptable with minor gaps |
| `poor` | Below expectations — needs improvement |
| `insufficient` | Does not meet minimum standards — requires rework |
| `not-rated` | Not yet evaluated (default for new files) |

### `overallStatus`

Overall health verdict after review. **Closed list**:

| Value | Meaning |
|-------|---------|
| `good` | No issues — document is fit for purpose |
| `warning` | Minor issues — acceptable with documented caveats |
| `critical` | Significant issues — requires rework before use |
| `not-reviewed` | Not yet reviewed (default for new files) |

---

## Lifecycle

### On File Creation

Producing agents set defaults:

| Field | Default |
|-------|---------|
| `status` | `draft` |
| `holisticQualityRating` | `not-rated` |
| `overallStatus` | `not-reviewed` |
| `changeHistory` | One entry recording the creation |

### On File Update

When modifying an existing output file:

1. **Append** a new entry to `changeHistory` — never overwrite previous entries.
2. Update `status` if the lifecycle state changed (e.g., `draft` → `review`).
3. Update `holisticQualityRating` and `overallStatus` if a review was performed.
4. Do **not** change the `date` field (it records original creation).

---

## Ownership Rules

| Field | Owner | Rule |
|-------|-------|------|
| `status` (`draft` → `review`) | Producing agent | Transitions when submitting for review |
| `status` (`review` → `validated`) | Reviewing agent or human | Transitions after approval at a quality gate |
| `holisticQualityRating` | Reviewing agent only | Never set by the producing agent |
| `overallStatus` | Reviewing agent only | Never set by the producing agent |

> **Key principle**: the agent that *produces* a document never rates its own quality. Quality and overall status are always set by a *different* agent during a review station or quality gate.

---

## Schema

The formal JSON Schema is at:

```
.apm/knowledge/governance/schemas/output-metadata.schema.json
```

The instruction enforcing this metadata is at:

```
.apm/instructions/output-metadata.md              (canonical)
providers/github-copilot/instructions/output-metadata.instructions.md  (Copilot adapter)
```

---

## Compatibility with BA Conventions

This metadata is **additive** to the existing BA markdown frontmatter (`id`, `title`, `phase`, `type`, `version`, `author`, `reviewers`, `dependencies` — defined in `.apm/contexts/sdlc-conventions/cv-ba-markdown.md`). Both sets of fields coexist in the same YAML frontmatter block:

```yaml
---
# BA fields
id: FT-003
title: User Authentication
type: feature
version: '1.0'
author: sdlc-ba-analyst

# Output metadata fields
workflow: sdlc-ba
trigger: hub-orchestrator
date: '2026-04-10'
status: draft
inputDocuments:
  - outputs/ba/vis-001-product-vision.md
  - outputs/ba/ep-001-epics.md
changeHistory:
  - date: '2026-04-10'
    description: 'Initial creation by SDLC BA Analyst'
    changes:
      - 'Generated feature specification from epic EP-001'
holisticQualityRating: not-rated
overallStatus: not-reviewed
---
```

---

## Examples

### Newly created specification

```yaml
---
workflow: spec-kit
trigger: user
date: '2026-04-10'
status: draft
inputDocuments:
  - .apm/knowledge/constitution/speckit-constitution.md
changeHistory:
  - date: '2026-04-10'
    description: 'Initial creation by Spec Orchestrator'
    changes:
      - 'Generated feature specification from product vision'
holisticQualityRating: not-rated
overallStatus: not-reviewed
---
```

### After quality review

```yaml
---
workflow: spec-kit
trigger: user
date: '2026-04-10'
status: review
inputDocuments:
  - .apm/knowledge/constitution/speckit-constitution.md
changeHistory:
  - date: '2026-04-10'
    description: 'Initial creation by Spec Orchestrator'
    changes:
      - 'Generated feature specification from product vision'
  - date: '2026-04-11'
    description: 'Quality review by Architecture Governance'
    changes:
      - 'Validated against architecture principles'
      - 'Added NFR traceability references'
holisticQualityRating: good
overallStatus: good
---
```

### After human validation

```yaml
---
workflow: spec-kit
trigger: user
date: '2026-04-10'
status: validated
inputDocuments:
  - .apm/knowledge/constitution/speckit-constitution.md
changeHistory:
  - date: '2026-04-10'
    description: 'Initial creation by Spec Orchestrator'
    changes:
      - 'Generated feature specification from product vision'
  - date: '2026-04-11'
    description: 'Quality review by Architecture Governance'
    changes:
      - 'Validated against architecture principles'
      - 'Added NFR traceability references'
  - date: '2026-04-12'
    description: 'Validated by product owner'
    changes:
      - 'Approved for implementation'
holisticQualityRating: good
overallStatus: good
---
```
