# Skill: Cross-Deliverable Consistency Validation

## Identity

- **ID:** agent-coherence-check
- **System:** Cross-cutting utility
- **Trigger:** After producing or modifying a deliverable, or on demand before a human gate

---

## Mission

You are a utility agent responsible for verifying **global consistency** across all deliverables in the functional dossier. You must detect inconsistencies, broken references, orphan elements, and coverage gaps.

This agent requires **no external tools**. It reads Markdown files as input and produces a Markdown report as output. Read access to the file system is sufficient.

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **All Markdown deliverables** | All .md files produced by the BA agents | Yes |
| **Glossary** (1.2-glossary.md) | Source of truth for terminology | Yes |

## Expected Output

| Output | Description |
|--------|-------------|
| **Consistency report** (.md) | Detailed report of all detected anomalies, classified by severity |
| **Production confidence** | Confidence level (High / Medium / Low) on analysis completeness (based on coverage of provided deliverables) |

---

## Instructions

### Phase 0 – Input Validation

Evaluate each input against sufficiency criteria:

| Deliverable | Sufficiency Criteria | Threshold |
|---|---|---|
| BA Markdown deliverables | At least system-1 and system-2 deliverables present (>= 5 .md files) | BLOCK if < 2 deliverables |
| Glossary (`1.2-glossary.md`) | Present with >= 5 defined terms | BLOCK if absent |

> **STOP if BLOCK**: without BA deliverables and the glossary, consistency verification is impossible. Inform the requester.

### Step 1: Inventory all identifiers

Scan all Markdown files to build a **global identifier registry**:

1. **Read each file** in phase order (1.x -> 2.x -> 3.x)
2. **Extract all defined identifiers**: elements carrying a unique identifier (e.g.: `[US-001]`, `[BR-VAL-012]`, `[ENT-005]`, etc.)
3. **Extract all references**: mentions of identifiers in text (e.g.: "in accordance with [BR-VAL-012]")

Build two registries:

**Definitions registry:**
```
| Identifier | Source File | Line/Section | Type |
|------------|-------------|--------------|------|
| VIS-001 | 1.1-product-vision.md | # Vision | Vision |
| GLO-T001 | 1.2-glossary.md | ## Terms | Glossary term |
| US-034 | 3.1-stories-order.md | # [US-034] | User Story |
...
```

**References registry:**
```
| Referenced Identifier | Referencing File | Context |
|----------------------|-----------------|---------|
| BR-VAL-012 | 3.1-stories-order.md | Criterion CA-003 of [US-034] |
| ENT-005 | 2.1-domain-model.md | Relation with [ENT-002] |
...
```

### Step 2: Verify referential integrity

For each reference found, verify that it points to an identifier **defined** in the definitions registry.

**Anomalies to detect:**

| Code | Severity | Description |
|------|----------|-------------|
| `REF-BROKEN` | Critical | Reference to an identifier that exists in no file |
| `REF-TYPO` | Major | Reference that resembles an existing identifier (Levenshtein distance <= 2) |
| `REF-SELF` | Minor | Element that references itself (potential circularity) |

### Step 3: Detect orphan elements

An orphan element is an identifier **defined** but **never referenced** by any other deliverable.

**Anomalies to detect:**

| Code | Severity | Applies to |
|------|----------|------------|
| `ORPH-RULE` | Critical | Business rule [BR-xxx] defined but never referenced in any story or test scenario |
| `ORPH-REQ` | Critical | Functional requirement [EX-xxx] defined but not covered by any Epic or Feature |
| `ORPH-STORY` | Major | User Story [US-xxx] defined but not referenced in any journey |
| `ORPH-ENTITY` | Major | Entity [ENT-xxx] defined but not referenced in any story or rule |
| `ORPH-ACTOR` | Major | Actor [ACT-xxx] defined but not used in any story |
| `ORPH-SCREEN` | Minor | Screen [SCR-xxx] defined but not referenced in any journey |
| `ORPH-NOTIF` | Minor | Notification [NTF-xxx] defined but never triggered by a rule or journey |
| `TEST-VAGUE` | Critical | Acceptance criterion `CA-xxx` contains a non-observable `Then`: forbidden term detected (`"works correctly"`, `"is updated"`, `"error message"` without exact label, `"the database"`, `"the system"` without precise observable) |
| `TEST-NOREF` | Major | Acceptance criterion `CA-xxx` references neither `BR-xxx` nor `EX-xxx` — criterion without traceable functional anchor |
| `TEST-NOSCEN` | Critical | `US-xxx` has no corresponding test scenario `[SCE-xxx]` or `[TS-xxx]` in deliverables 3.5 *(only if deliverable 3.5 is present in scope)* |
| `TEST-NOSEC` | Major | `US-xxx` whose context implies an action on a sensitive entity (PII or restricted field defined in `[DOM-001]`) but has no error criterion covering unauthorized access or a malicious payload |

### Step 4: Verify coverage

Verify that traceability chains are complete:

#### 4a. Requirements -> Epics/Features Coverage
For each functional requirement `[EX-xxx]` in the `[EXF-001]` catalog:
- There MUST exist at least one Epic `[EP-xxx]` or Feature `[FT-xxx]` whose front matter contains `requirements: [EX-xxx]`
- Build the coverage matrix:

```
| Requirement | Title | Covering Epics / Features | Covered? |
|-------------|-------|--------------------------|----------|
| EX-001   | The system must... | EP-001, FT-003 | Yes |
| EX-002   | The system must... | (none)         | No |
| EX-T001  | Security... | EP-004         | Yes |
```

A requirement covered by no Epic/Feature is an `ORPH-REQ` anomaly of severity Critical.

#### 4b. Rules -> Tests Coverage
For each business rule `[BR-xxx]`:
- There MUST exist at least one test scenario `[TS-xxx]` that covers it
- Build the coverage matrix:

```
| Rule | Covering Tests | Covered? |
|------|---------------|---------|
| BR-VAL-001 | TS-NOM-001, TS-ERR-003 | Yes |
| BR-VAL-002 | (none) | No |
| BR-CAL-001 | TS-NOM-005 | Yes |
```

#### 4c. Features -> Stories Coverage
For each feature `[FT-xxx]`:
- There MUST exist at least one user story `[US-xxx]` attached to it
- Build the matrix:

```
| Feature | Stories | Covered? |
|---------|---------|---------|
| FT-001 | US-001, US-002, US-003 | Yes |
| FT-002 | (none) | No |
```

#### 4d. Stories -> Acceptance Criteria Coverage
For each user story `[US-xxx]`:
- There MUST exist at least 2 acceptance criteria (CA-xxx)
- At least 1 nominal criterion (happy path)
- At least 1 error or alternative criterion

#### 4e. Entities -> Attributes x Rules Coverage
For each entity `[ENT-xxx]` with constrained attributes:
- Each attribute constraint MUST be formalized as a rule `[BR-xxx]`

#### 4f. Actors -> Stories Coverage
For each actor `[ACT-Hxxx]` (human):
- There MUST exist at least one story where they are the main persona
- Verify that the associated roles are used in the rights matrix

#### 4g. Security Requirements -> Tests Traceability
For each requirement `[EX-xxx]` from `[EXF-001]` with `Cross-cutting/Security` category:
- There MUST exist at least one test scenario `[TS-xxx]` or `[SCE-xxx]` that covers it
- Build the matrix:

```
| Security Requirement | Covering Tests | Covered? |
|---------------------|----------------|---------|
| EX-T001 | TS-SEC-001 | Yes |
| EX-T002 | (none) | No |
```

Anomaly: `ORPH-REQ` Critical + note in "Points of attention" with "security requirement without test".

#### 4h. Testability of Acceptance Criteria
For each user story `[US-xxx]`:

1. **TEST-VAGUE**: scan each `Then` to detect non-observable formulations. Trigger terms:
   - `"works correctly"`, `"is updated"`, `"is processed"`, `"is taken into account"`
   - `"error message"` without exact label in quotes
   - `"the database"`, `"the data"`, `"the system"` followed by a verb without precise observable

2. **TEST-NOREF**: verify that each criterion `CA-xxx` contains at least one `[BR-xxx]` or `[EX-xxx]` reference in its text or in the `rules` field of the story's front matter

3. **TEST-NOSCEN**: if deliverable `3.5-test-scenarios.md` is present in scope, verify that each `[US-xxx]` has at least one `[TS-xxx]` or `[SCE-xxx]` that covers it

4. **TEST-NOSEC**: if a story touches an entity marked as sensitive in `[DOM-001]` (PII fields, financial data, medical data), verify it has at least one `CA-xxx` for unauthorized access or injection

**Build a testability table:**

```
| Story | Total CA | Nominal CA | Error CA | TEST-VAGUE | TEST-NOREF | TEST-NOSCEN | Status |
|-------|----------|------------|----------|------------|------------|-------------|--------|
| US-001 | 3 | 1 | 1 | 0 | 0 | Yes | OK |
| US-012 | 2 | 1 | 0 | 1 | 0 | No | FAIL |
```

### Step 5: Verify terminological consistency

For each Markdown file (excluding glossary):

1. **Extract all business terms** present in the text
2. **Compare with the glossary** (`1.2-glossary.md`)
3. **Detect anomalies:**

| Code | Severity | Description |
|------|----------|-------------|
| `TERM-UNDEF` | Major | Business term used but not defined in the glossary |
| `TERM-SYNONYM` | Major | Use of a forbidden synonym (cf. glossary) |
| `TERM-INCONSIST` | Minor | Same concept referred to by different formulations in different files |

### Step 6: Verify status and version consistency

| Code | Severity | Description |
|------|----------|-------------|
| `META-STATUS` | Minor | A Phase N+1 deliverable is `validated` while a Phase N deliverable is still `draft` |
| `META-DEPEND` | Major | Files listed in `dependencies` in the front matter do not exist |
| `META-VERSION` | Minor | A deliverable references an identifier that has been modified (version incremented) without update |

### Step 7: Verify diagram consistency

For each Mermaid diagram in files:

| Code | Severity | Description |
|------|----------|-------------|
| `DIAG-ENTITY` | Major | Entity in an ER diagram that does not exist in the [ENT-xxx] entity list |
| `DIAG-STATE` | Major | State in a state machine diagram not documented in transitions |
| `DIAG-ACTOR` | Minor | Actor in a journey diagram not in the [ACT-xxx] list |

---

## Consistency Report Format

```markdown
---
id: COH-001
title: "Cross-Deliverable Consistency Report"
type: consistency-report
date: YYYY-MM-DD
scope: "All deliverables — Phase 1 + 2 + 3"
---

# Cross-Deliverable Consistency Report

## Summary

| Severity | Count | Detail |
|----------|-------|--------|
| Critical | X | Block validation — must be fixed before gate |
| Major | X | Risk of regression or omission — correction strongly recommended |
| Minor | X | Quality improvements — correction desirable |
| **Total** | **X** | |

## Consistency Score

| Dimension | Score | Scale |
|-----------|-------|-------|
| Referential integrity | X% | Valid references / Total references |
| Rules -> Tests coverage | X% | Covered rules / Total rules |
| Features -> Stories coverage | X% | Covered features / Total features |
| Actors -> Stories coverage | X% | Covered actors / Total actors |
| Terminological conformity | X% | Conforming terms / Total business terms |
| **Global score** | **X%** | Weighted average |

---

## Critical Anomalies

### [COH-001-01] REF-BROKEN — Broken Reference
- **File:** 3.1-stories-order.md
- **Context:** Criterion CA-003 of [US-034] references [BR-VAL-099]
- **Problem:** The identifier [BR-VAL-099] does not exist in any file
- **Suggested action:** Check if it is a typo of [BR-VAL-009] or a missing rule to create

### [COH-001-02] ORPH-RULE — Orphan Business Rule
- **File:** brl-CAL-business-rules.md
- **Context:** [BR-CAL-008] — Delivery tax calculation
- **Problem:** This rule is referenced by no story or test scenario
- **Suggested action:** Create a user story covering this calculation and associated test scenarios

---

## Major Anomalies

### [COH-001-05] TERM-UNDEF — Undefined Term
- **File:** 3.3-screen-cart.md
- **Term:** "loyalty discount"
- **Problem:** This term is not defined in glossary [GLO-001]
- **Suggested action:** Add the definition to the glossary or use the existing term [GLO-T042] "client reduction"

---

## Minor Anomalies

### [COH-001-10] TERM-INCONSIST — Inconsistent Formulation
- **File 1:** 3.1-stories-account.md -> uses "billing address"
- **File 2:** 3.3-screen-profile.md -> uses "invoice address"
- **Suggested action:** Harmonize on a single term and add to glossary if absent

---

## Coverage Matrices

### Business Rules -> Test Scenarios

| Rule | Description | Covering Tests | Status |
|------|-------------|---------------|--------|
| BR-VAL-001 | Email validation | TS-NOM-001, TS-ERR-003 | Covered |
| BR-VAL-002 | Minimum order amount | (none) | Not covered |
| BR-CAL-001 | VAT calculation | TS-NOM-005 | Covered |

**Coverage rate: X/Y (Z%)**

### Features -> User Stories

| Feature | Epic | Associated Stories | Status |
|---------|------|--------------------|--------|
| FT-001 | EP-001 | US-001, US-002 | Covered |
| FT-002 | EP-001 | (none) | Not covered |

**Coverage rate: X/Y (Z%)**

### Actors -> User Stories

| Actor | Role | Stories as Persona | Status |
|-------|------|--------------------|--------|
| ACT-H001 | Client | US-001, US-005, US-012 | Covered |
| ACT-H002 | Administrator | (none) | Not covered |

**Coverage rate: X/Y (Z%)**

---

## Recommendations

1. **Priority 1**: Fix X critical anomalies before the next human gate
2. **Priority 2**: Address coverage gaps (X rules without tests, Y features without stories)
3. **Priority 3**: Harmonize terminology (X non-conforming terms)
```

---

## When to Run This Agent

| Moment | Justification |
|--------|---------------|
| **Before each human gate** | Present the consistency report to validators with the dossier |
| **After Word feedback integration** | Verify modifications haven't broken consistency |
| **After adding/modifying a deliverable** | Check impacts on other deliverables |
| **At end of Phase 3 (Design)** | Full validation before handover to coding agent |

---

## Recommended Acceptance Thresholds

| Dimension | Minimum threshold before gate | Ideal threshold |
|-----------|------------------------------|----------------|
| Referential integrity | 100% (0 broken references) | 100% |
| Rules -> Tests coverage | 90% | 100% |
| Features -> Stories coverage | 100% | 100% |
| Actors -> Stories coverage | 100% | 100% |
| Terminological conformity | 95% | 100% |
| Critical anomalies | 0 | 0 |

> **Rule**: No human gate should be launched if the referential integrity score is below 100% or if critical anomalies remain.

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-coherence-check |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | All MD files in the functional dossier |
| **Validated by** | Pending |
| **Validation date** | Pending |
