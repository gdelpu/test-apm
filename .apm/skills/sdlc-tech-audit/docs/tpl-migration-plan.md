---
id: GAP-001
title: "Technical Gap & Migration Plan — [Project Name]"
phase: t0-audit
type: technical-gap-analysis
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-t0.2-gap-technique
reviewers: []
dependencies: ["TECH-ASIS-001", "DELTA-001"]
---

# [GAP-001] Technical Gap & Migration Plan

## 1. Executive summary

**Gap magnitude:** Low / Moderate / High / Critical

**Indicative migration effort:** <!-- Rough estimate in days/sprint -->

**Summary table:**

| Category | CREATE | ALTER | DROP/DEPRECATE | REMEDIATION | Total |
|----------|--------|-------|----------------|-------------|-------|
| Tables (GAP-DAT) | | | | — | |
| API Endpoints (GAP-API) | | | | — | |
| Architecture modules (GAP-ARCH) | | | | — | |
| Remediations (GAP-REM) | — | — | — | | |

**Critical risks:**
- <!-- Critical risk 1 -->
- <!-- Critical risk 2 -->

---

## 2. Data schema gap

| ID | Table | Status | Description | FK Dependencies | BA Traceability |
|----|-------|--------|-------------|----------------|-----------------|
| [GAP-DAT-001] | | CREATE | | | [DELTA-ENT-xxx] |
| [GAP-DAT-002] | | ALTER | | | [DELTA-ENT-xxx] |
| [GAP-DAT-003] | | DROP | | | [DELTA-ENT-xxx] |
| [GAP-DAT-004] | | DEPRECATE | | | [DELTA-ENT-xxx] |

### Alteration details (ALTER)

#### [GAP-DAT-xxx] — Table `[table_name]`

**Columns to add:**

| Column | SQL Type | Nullable | Default | Strategy |
|--------|----------|----------|---------|----------|
| | | Yes (nullable-first) | | Nullable then backfill then NOT NULL |

**Columns to modify:**

| Column | Current type | Target type | Data compatibility | Strategy |
|--------|-------------|------------|-------------------|----------|
| | | | Yes / No / To verify | |

**Columns to remove:**

| Column | Data to migrate | Deprecation strategy |
|--------|----------------|---------------------|
| | Yes / No | deprecated_at then DROP after [date] |

**Constraints to add:**

| Type | Definition | Impact on existing data |
|------|-----------|------------------------|
| UNIQUE | | |
| CHECK | | |
| FK | | |

---

## 3. API gap

| ID | Endpoint | Status | Description | Breaking Change | BA Traceability |
|----|----------|--------|-------------|----------------|-----------------|
| [GAP-API-001] | POST /xxx | CREATE | | N/A | [DELTA-FT-xxx] |
| [GAP-API-002] | GET /xxx/{id} | VERSION → /v2 | | Yes | [DELTA-FT-xxx] |
| [GAP-API-003] | DELETE /xxx | DEPRECATE | | Yes | [DELTA-FT-xxx] |
| [GAP-API-004] | PUT /xxx | MODIFY | | No | [DELTA-FT-xxx] |

**Identified external consumers:**

| Impacted endpoint | Consumer | Type | Deprecation window |
|-------------------|----------|------|--------------------|
| | | Internal system / External | |

---

## 4. Architecture gap

| ID | Module / Component | Status | Description | Dependencies | BA Traceability |
|----|-------------------|--------|-------------|-------------|-----------------|
| [GAP-ARCH-001] | | CREATE | | | [DELTA-FT-xxx] |
| [GAP-ARCH-002] | | REFACTOR | | | [DELTA-ENT-xxx] |

---

## 5. Technical remediations

| ID | Deviation | Priority | Scope | Estimated effort | Justification |
|----|-----------|---------|-------|------------------|---------------|
| [GAP-REM-001] | | BLOCKING | | | Blocks evolution [GAP-DAT-xxx] |
| [GAP-REM-002] | | OPTIONAL | | | Technical debt — plan separately |

---

## 6. Data migration plan

### Migration order (respects FK constraints)

| Step | Gap ID | SQL action | Table(s) | Zero-downtime | Rollback possible | Estimated duration |
|------|--------|-----------|----------|---------------|-------------------|--------------------|
| 1 | [GAP-DAT-xxx] | ADD COLUMN ... NULLABLE | | Yes | Yes | |
| 2 | [GAP-DAT-xxx] | UPDATE (backfill) | | Yes (batch) | Yes | |
| 3 | [GAP-DAT-xxx] | ALTER COLUMN SET NOT NULL | | No | No | |
| 4 | [GAP-DAT-xxx] | CREATE TABLE | | Yes | Yes | |
| 5 | [GAP-DAT-xxx] | CREATE INDEX CONCURRENTLY | | Yes | Yes | |

**Data to migrate:**

| Source table | Target table | Estimated volume | Transformation required | Migration script |
|-------------|-------------|-----------------|------------------------|-----------------|
| | | | Yes / No | |

**Irreversible migrations:**
> ⚠️ The following operations are irreversible once executed in production:
> - <!-- Example: DROP COLUMN `old_status` on table `orders` -->

---

## 7. Coexistence strategy (if applicable)

> *Complete if the evolution is progressive (strangler-fig, feature flags)*

**Retained pattern:** Feature flags / Anti-corruption layer / Strangler-fig / None

**Coexistence boundary:**

| Component | Legacy system | New system | Activation |
|-----------|--------------|------------|-----------|
| | Continues to function | Takes over | Feature flag / Date / % traffic |

**End-of-coexistence criteria:** <!-- When can legacy code be removed? -->

---

## 8. Technical risks

| ID | Risk | Criticality | Description | Mitigation |
|----|------|-------------|-------------|------------|
| [RSK-T-001] | | Critical / High / Moderate / Low | | |

---

## 9. Traceability

| Downstream deliverable | Consumed elements |
|-----------------------|-------------------|
| [ADR-xxx] brownfield | Existing non-negotiable constraints |
| [DAT-001] | GAP-DAT → ALTER + CREATE migrations |
| [ENB-xxx] brownfield | Wave 0 BF: BLOCKING remediations + evolution setup |
| T-3.1 initial gap report | All GAP-xxx as baseline |

---

## Attention Points

> ⚠️ **[PA-001]** <!-- Blocking gap or unmitigated risk -->
