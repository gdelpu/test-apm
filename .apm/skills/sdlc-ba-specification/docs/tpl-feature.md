---
id: FT-001
title: "[Feature Name]"
phase: 2-specification
type: feature
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-features
reviewers: []
epic: EP-001                          # Parent epic identifier
dependencies: ["EP-001", "GLO-001", "BRL-001"]
requirements: ["EX-xxx"]             # EX-xxx requirements covered by this feature (R4J traceability)
---

# [FT-001] Feature Name

## Description

<!-- What this feature enables the user to do. One clear paragraph, business language only. -->

---

## Feature details

| Property | Value |
|----------|-------|
| **Parent epic** | [EP-001] Epic Name |
| **Main actor** | [ACT-Hxxx] Actor Name |
| **Secondary actors** | [ACT-Hxxx], [ACT-Sxxx] *(if any)* |
| **Priority** | Must / Should / Could / Won't (MoSCoW) |
| **Estimated complexity** | Low / Medium / High |
| **Covered requirements** | [EX-xxx], [EX-yyy] |
| **Dependencies** | [FT-xxx] *(other features that must exist first)* |
| **Concerned entities** | [ENT-xxx], [ENT-xxx] |

---

## Associated business rules

<!-- Business rules that specifically apply to this feature.
     Cross-cutting rules are in brl-*-business-rules.md (one file per rule type).
     Feature-scoped rules are in brl-ft-xxx.md alongside this file. -->

| Rule ID | Description | Type |
|---------|-------------|------|
| [BR-xxx] | <!-- Rule summary --> | BR-VAL / BR-CAL / BR-TRG / BR-AUT |

---

## Acceptance criteria

<!-- Macroscopic criteria that validate this feature works as an integrated capability.
     These are NOT User Story criteria — they test what emerges when the stories
     of this feature are combined (concurrency, performance at volume, cross-story flows).
     Each criterion feeds the E2E test plan and functional test scenarios. -->

### FAC-001: <!-- Criterion name — integrated capability -->

- **Given** <!-- realistic context with representative volumes -->
- **When** <!-- action that exercises the feature as a whole -->
- **Then** <!-- observable result proving the capability works end-to-end -->

### FAC-002: <!-- Criterion name — edge case or non-functional -->

- **Given** <!-- boundary or concurrent context -->
- **When** <!-- action that stresses the feature -->
- **Then** <!-- expected behaviour under stress or edge conditions -->

<!-- Add one FAC per key capability this feature must deliver.
     Typical: 2-5 criteria per feature. Use FAC- prefix (Feature Acceptance Criterion). -->

---

## Definition of Ready

- [ ] All user stories [US-xxx] of this feature have status `validated`
- [ ] All US-level acceptance criteria are covered by test scenarios [SCE-xxx]
- [ ] Feature-level acceptance criteria (FAC-xxx) are covered by E2E scenarios
- [ ] All referenced business rules [BR-xxx] are covered by test scenarios
- [ ] Screen specifications validated (if applicable)
- [ ] No BLOCK in validation reports for this feature

---

## User stories

> Populated by `agent-3.1-user-stories.md`. Listed here for traceability.

| Story ID | Title | Priority |
|----------|-------|----------|
| [US-xxx] | *(to be created)* | Must |

---

## Functional boundaries

**In scope:**
- <!-- What is explicitly covered -->

**Out of scope:**
- <!-- What is explicitly excluded, including Won't items -->

---

## Points of attention

<!-- Known constraints, ambiguities, or risks to flag for story writing and design -->

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-features |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [EP-001], [GLO-001], [BRL-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |
