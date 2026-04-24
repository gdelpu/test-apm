---
id: DELTA-001
title: "Functional Delta Analysis — [Project Name]"
phase: 0-audit
type: delta-analysis
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-0.2-delta-analyse
reviewers: []
dependencies: ["ASIS-001"]
---

# [DELTA-001] Functional Delta Analysis

## 1. Executive summary

**Nature of the evolution:** <!-- Additive (mostly NEW) / Transformative (mostly MODIFIED) / Simplifying (mostly DEPRECATED) -->

**Scope of the evolution:** <!-- 2-3 sentence synthetic description of what changes -->

**Summary table:**

| Category | NOUVEAU | MODIFIÉ | PRÉSERVÉ | DÉPRÉCIÉ | Total |
|----------|---------|---------|---------|---------|-------|
| Entities / Concepts | | | | | |
| Features | | | | | |
| Business rules | | | | | |
| Actors / Roles | | | | | |
| Integrations | | | | | |

**Main risks:**
- <!-- Risk 1 -->
- <!-- Risk 2 -->

---

## 2. Delta — Business entities and concepts

| ASIS ID | Concept name | Status | Delta description | DELTA ID |
|---------|--------------|--------|-------------------|---------|
| [ASIS-GLO-001] | | PRÉSERVÉ | No modification | — |
| [ASIS-GLO-002] | | MODIFIÉ | <!-- What changes precisely --> | [DELTA-ENT-001] |
| — | | NOUVEAU | <!-- Description of the new concept --> | [DELTA-ENT-010] |
| [ASIS-GLO-005] | | DÉPRÉCIÉ | <!-- Deprecation plan --> | — |

### Detail of MODIFIÉ entities

#### [DELTA-ENT-001] — [Entity name]

**ASIS reference:** [ASIS-GLO-xxx]

| Aspect | Current state | Target state | Nature of change |
|--------|---------------|--------------|-----------------|
| Attributes | | | Add / Remove / Modify |
| Lifecycle | | | |
| Relations | | | |
| Rules | | | |

---

## 3. Delta — Features

| ASIS ID | Feature name | Status | Delta description | DELTA ID |
|---------|--------------|--------|-------------------|---------|
| [ASIS-FT-001] | | PRÉSERVÉ | | — |
| [ASIS-FT-002] | | MODIFIÉ | | [DELTA-FT-001] |
| — | | NOUVEAU | | [DELTA-FT-010] |
| [ASIS-FT-005] | | DÉPRÉCIÉ | | — |

---

## 4. Delta — Business rules

| ASIS ID | Rule | Status | Old formulation | New formulation | DELTA ID |
|---------|------|--------|----------------|----------------|---------|
| [ASIS-BR-001] | | PRÉSERVÉ | — | — | — |
| [ASIS-BR-002] | | MODIFIÉ | IF ... THEN ... | IF ... THEN ... | [DELTA-BR-001] |
| — | | NOUVEAU | — | IF ... THEN ... | [DELTA-BR-010] |

**Potential conflicts between existing rules and new rules:**
- <!-- Conflict 1: [ASIS-BR-xxx] vs [DELTA-BR-xxx] — to be resolved in workshop -->

---

## 5. Delta — Actors and roles

| ASIS ID | Actor / Role | Status | Delta description | DELTA ID |
|---------|--------------|--------|-------------------|---------|
| [ASIS-ACT-001] | | PRÉSERVÉ | | — |
| [ASIS-ROL-001] | | MODIFIÉ | New rights: ... / Removed rights: ... | [DELTA-ROL-001] |
| — | | NOUVEAU | | [DELTA-ACT-010] |
| [ASIS-ACT-003] | | DÉPRÉCIÉ | Migration to [ASIS-ROL-xxx] | — |

---

## 6. Delta — External integrations

| ASIS ID | External system | Status | Delta description | DELTA ID |
|---------|----------------|--------|-------------------|---------|
| [ASIS-INT-001] | | PRÉSERVÉ | | — |
| [ASIS-INT-002] | | MODIFIÉ | | [DELTA-INT-001] |
| — | | NOUVEAU | | [DELTA-INT-010] |

---

## 7. Impact zone map

| Functional domain | Affected elements | Impact level | Potential side effects |
|-------------------|------------------|--------------|------------------------|
| | | Major / Moderate / Minor | |

---

## 8. Evolution risks

| ID | Risk | Level | Description | Mitigation |
|----|------|-------|-------------|------------|
| [RSK-001] | | High / Moderate / Low | | |

---

## 9. Traceability

| Downstream deliverable | Consumed elements |
|------------------------|-------------------|
| [VIS-001] | Scope of evolution, constraints |
| [DOM-001] | NOUVEAU and MODIFIÉ entities → `[DELTA-ENT-xxx]` |
| [BRL-001] | NOUVEAU and MODIFIÉ rules → `[DELTA-BR-xxx]` |
| [GAP-001] | All DELTA elements for the technical gap |

---

## Attention Points

> ⚠️ **[PA-001]** <!-- PRÉSERVÉ status not explicitly confirmed — to be validated in workshop -->
