---
name: output-metadata
description: 'Mandate structured YAML frontmatter metadata on every file produced by agents and workflows under outputs/.'
applyTo: 'outputs/**'
---

# Output Document Metadata Instructions

## Rule

Every file written under `outputs/` by an agent or workflow **must** include YAML frontmatter conforming to the schema at `.apm/knowledge/governance/schemas/output-metadata.schema.json`.

## Required frontmatter

```yaml
---
workflow: <name of the workflow creating this file>
trigger: <what triggered the workflow — another workflow, an agent, or the end user>
date: '<YYYY-MM-DD>'
status: <draft | review | validated | superseded | archived>
inputDocuments:
  - <relative path to each source document used to produce this file>
changeHistory:
  - date: '<YYYY-MM-DD>'
    description: '<short summary of what happened>'
    changes:
      - '<individual change line>'
holisticQualityRating: <excellent | good | adequate | poor | insufficient | not-rated>
overallStatus: <good | warning | critical | not-reviewed>
---
```

## Field rules

### `workflow`
Name of the workflow that created the file. Use the canonical workflow ID from `.apm/workflows/` (e.g., `spec-kit`, `feature-implementation`, `quality-validation`, `bug-fixing`).

### `trigger`
What initiated this workflow execution. Examples:
- `user` — end user invoked directly
- `hub-orchestrator` — dispatched by the Hub Orchestrator
- `spec-kit/station-3` — triggered by another workflow station
- `pr-validation` — triggered by a PR event

### `date`
ISO 8601 date (`YYYY-MM-DD`) of the initial file creation. Do **not** update this on subsequent edits — use `changeHistory` instead.

### `status` (closed list)

| Value | Meaning | Set by | When |
|-------|--------|--------|------|
| `draft` | Initial creation — default for all new files | Producing agent | Automatically on file creation |
| `review` | Submitted for review by a human or agent | Producing agent or orchestrator | When submitting for human/agent review |
| `validated` | Approved and accepted | Reviewing agent or human | After approval at a quality gate |
| `superseded` | Replaced by a newer version of this document | Any agent | When a newer version of this document is created |
| `archived` | Retired — no longer active or relevant | Any agent or human | When the document is retired |

Lifecycle: `draft` → `review` → `validated` → (`superseded` | `archived`).

> **Ownership**: the producing agent is responsible for the `draft` → `review` transition. A reviewing agent or human gate is responsible for the `review` → `validated` transition.

### `inputDocuments`
Array of relative paths (from repo root) listing all documents used as input. If the workflow consumed no documents, use an empty array `[]`.

### `changeHistory`
Chronological log of every modification. The first entry records initial creation. Each entry has:
- `date` — when the change was made (`YYYY-MM-DD`)
- `description` — one-line human-readable summary
- `changes` — list of specific modifications made by agents

**On every update**, agents must append a new entry to `changeHistory` and update `status` if the lifecycle state changed.

### `holisticQualityRating` (closed list)

| Value | Meaning |
|-------|---------|
| `excellent` | Exceeds expectations — no gaps |
| `good` | Meets expectations — minor observations only |
| `adequate` | Acceptable with minor gaps |
| `poor` | Below expectations — needs improvement |
| `insufficient` | Does not meet minimum standards — requires rework |
| `not-rated` | Not yet evaluated (default for new files) |

> **Ownership**: set exclusively by a **reviewing agent** (e.g., Quality Validator, Architecture Governance) during a quality assessment or review station — never by the producing agent. Newly created files default to `not-rated`. Maps conceptually to the existing "Production confidence" pattern (`CONFIDENT` / `PARTIAL` / `INSUFFICIENT`) but with finer granularity.

### `overallStatus` (closed list)

| Value | Meaning |
|-------|---------|
| `good` | No issues — document is fit for purpose |
| `warning` | Minor issues — acceptable with documented caveats |
| `critical` | Significant issues — requires rework before use |
| `not-reviewed` | Not yet reviewed (default for new files) |

> **Ownership**: set exclusively by a **reviewing agent** during a review station or quality gate — never by the producing agent. This is the **go/no-go signal** for downstream consumers. Aligned with the existing severity model (`critical` / `high` / `medium` / `low`) but simplified to a traffic-light model for documents. Newly created files default to `not-reviewed`.

## On file creation

When creating a new output file, set:
- `status: draft`
- `holisticQualityRating: not-rated`
- `overallStatus: not-reviewed`
- `changeHistory` with one entry recording the creation

Example:

```yaml
---
workflow: spec-kit
trigger: user
date: '2026-04-10'
status: draft
inputDocuments:
  - outputs/docs/1-prd/1-scoping/vis-001-product-vision.md
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

## On file update

When modifying an existing output file:
1. **Append** a new entry to `changeHistory` — never overwrite previous entries.
2. Update `status` if the lifecycle state changed (e.g., `draft` → `review`).
3. Update `holisticQualityRating` and `overallStatus` if a review was performed.
4. Do **not** change the `date` field (it records original creation).

## Compatibility

This metadata is additive to any existing frontmatter fields (e.g., `id`, `title`, `type`, `version` from the BA markdown conventions). Both sets of fields can coexist in the same frontmatter block.
