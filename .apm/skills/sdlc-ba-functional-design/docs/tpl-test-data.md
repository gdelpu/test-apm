---
id: DAT-TEST-001
title: "Seed Catalogue for Integration & E2E Tests — [Project Name]"
system: system-3-design
type: test-data-catalog
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-3.6-donnees-test
reviewers: []
dependencies: ["DOM-001", "BRL-001", "ACT-001", "SCE-XXX"]
---

# [DAT-TEST-001] Seed Catalogue for Integration & E2E Tests

---

## 1. Entity dependency graph

> *This section establishes the topological insertion order for entities, derived from the referential dependencies of the domain model `[DOM-001]`. This order is mandatory to avoid FK constraint violations.*

```
Insertion order:
1. <!-- Entity A (root entity, no outgoing FK) -->
2. <!-- Entity B → FK: b.a_id → Entity A -->
3. <!-- Entity C → FK: c.a_id → Entity A -->
4. <!-- Entity D → FK: d.b_id → Entity B, d.c_id → Entity C -->
```

| Entity | Depends on | Note |
|--------|-----------|------|
| <!-- E.g.: User --> | <!-- Role --> | <!-- FK: user.role_id --> |
| <!-- E.g.: Product --> | <!-- Category --> | <!-- FK: product.category_id --> |
| <!-- E.g.: Order --> | <!-- User --> | <!-- FK: order.client_id --> |
| <!-- E.g.: OrderLine --> | <!-- Order, Product --> | <!-- Composite FK --> |

### Identified cycles

<!-- List any FK cycles here and the chosen resolution strategy. -->
<!-- Example: -->
<!--
| Cycle | Resolution strategy |
|-------|---------------------|
| Order ↔ ProformaInvoice | Create Order with `invoice_id = NULL`, create ProformaInvoice with `order_id`, then UPDATE Order.invoice_id |
-->
*(No cycle detected)*

---

## 2. Shared dataset — Reference data

> *These entities are loaded once before the entire test suite. They form the common foundation available to all scenarios.*

### 2.1 Users by role

| Stable ID | Role | First name | Last name | Email | Status | Note |
|-----------|------|-----------|----------|-------|--------|------|
| <!-- user-admin-001 --> | <!-- ADMIN --> | <!-- System --> | <!-- Admin --> | <!-- admin@test-project.com --> | <!-- ACTIVE --> | <!-- Role [ACT-001]: Administrator --> |
| <!-- user-client-001 --> | <!-- CLIENT --> | <!-- Mary --> | <!-- Smith --> | <!-- mary.smith@test-project.com --> | <!-- ACTIVE --> | <!-- Role [ACT-001]: Standard client --> |
| <!-- user-manager-001 --> | <!-- MANAGER --> | <!-- Sophie --> | <!-- Martin --> | <!-- sophie.martin@test-project.com --> | <!-- ACTIVE --> | <!-- Role [ACT-001]: Manager --> |

### 2.2 Reference entities

<!-- For each configuration entity or reference list -->

#### <!-- Product categories -->

| Stable ID | <!-- Name --> | <!-- Code --> | <!-- Status --> | Note |
|-----------|--------------|--------------|----------------|------|
| <!-- cat-electronics-001 --> | <!-- Electronics --> | <!-- ELEC --> | <!-- ACTIVE --> | <!-- Base category --> |
| <!-- cat-services-001 --> | <!-- Services --> | <!-- SRV --> | <!-- ACTIVE --> | <!-- Base category --> |

### 2.3 Neutral entities

> *Entities that exist in the shared dataset and must not interfere with scenario assertions.*

| Stable ID | Type | Value / Description | Why "neutral" |
|-----------|------|---------------------|--------------|
| <!-- order-neutral-001 --> | <!-- Order --> | <!-- Closed order, client user-client-001 --> | <!-- Final irreversible status: triggers no calculation or notification --> |

---

## 3. Datasets per scenario

> *Each subsection below corresponds to a group of scenarios sharing common preconditions. Entities here are added to the shared dataset (section 2) — do not re-declare shared entities unless explicitly overriding them.*

---

### SCE-001 — <!-- Scenario title -->

**Type:** Nominal | Boundary | Error | Rights *(choose)*
**Preconditions (`Given`):** *Reproduce the scenario Given here*

#### Specific entities

**<!-- Main entity: Order -->**

| Field | Value | Justification |
|-------|-------|---------------|
| id | `SEED-SCE-001-order-001` | Stable identifier for assertions |
| client_id | `user-client-001` | Reference to shared dataset |
| <!-- status --> | <!-- DRAFT --> | <!-- State required by the Given --> |
| <!-- total --> | <!-- 150.00 € --> | <!-- [BR-CAL-001]: amount > 10.00€ minimum --> |
| <!-- created_at --> | <!-- 2026-01-15T10:00:00Z --> | <!-- Fixed date for reproducibility --> |

**<!-- Dependent entities: OrderLines -->**

| id | product_id | quantity | unit_price | Justification |
|----|-----------|----------|------------|---------------|
| `SEED-SCE-001-line-001` | `SEED-SCE-001-product-001` | 2 | 50.00 € | 2 lines × 50€ = 100€ of total |
| `SEED-SCE-001-line-002` | `SEED-SCE-001-product-002` | 1 | 50.00 € | 1 line × 50€ = 50€ of total |

**<!-- Support entities: Products -->**

| id | name | price | stock | Justification |
|----|------|-------|-------|---------------|
| `SEED-SCE-001-product-001` | <!-- Standard Widget --> | 50.00 € | 10 | Stock > ordered quantity |
| `SEED-SCE-001-product-002` | <!-- Premium Widget --> | 50.00 € | 5 | Stock > ordered quantity |

**Insertion order for this scenario:**
1. SEED-SCE-001-product-001, SEED-SCE-001-product-002
2. SEED-SCE-001-order-001
3. SEED-SCE-001-line-001, SEED-SCE-001-line-002

---

### SCE-010 — <!-- Boundary scenario: amount below minimum -->

**Type:** Boundary
**Preconditions (`Given`):** *Reproduce the Given here*

#### Specific entities

**Order with invalid amount**

| Field | Value | Justification |
|-------|-------|---------------|
| id | `SEED-SCE-010-order-001` | |
| client_id | `user-client-001` | Reference to shared dataset |
| total | `9.99 €` | **[BR-VAL-001]: Minimum amount = 10.00€. Value = min - 0.01€ to trigger rejection.** |
| status | `DRAFT` | Only status where amount validation applies |

> ⚠️ **Destructive / error scenario:** inserting this order may be refused if validation constraints are applied at the database level. In that case, inject via API `POST /orders?bypass_validation=true` (if available) or directly in the database with an explicit comment in the test.

---

### SCE-020 — <!-- Access rights denied scenario -->

**Type:** Rights
**Preconditions (`Given`):** *Reproduce the Given here*

#### Specific entities

**Order belonging to another user**

| Field | Value | Justification |
|-------|-------|---------------|
| id | `SEED-SCE-020-order-001` | |
| client_id | `user-client-001` | Order belongs to CLIENT — the MANAGER cannot modify it |
| status | `PENDING_VALIDATION` | Status on which the MANAGER's access attempt is made |

**Test context:** The actor attempting access is `user-manager-001` (shared dataset) on an order belonging to `user-client-001`.

---

<!-- Add one section per scenario or group of scenarios sharing the same preconditions -->

---

## 4. Coverage matrix

> *Cross-view: for each scenario, the datasets that cover it.*

| Scenario | Type | Shared dataset used | Specific datasets |
|----------|------|---------------------|-------------------|
| [SCE-001] <!-- Create nominal order --> | Nominal | `user-client-001` | `SEED-SCE-001-*` (4 entities) |
| [SCE-010] <!-- Amount below minimum --> | Boundary | `user-client-001` | `SEED-SCE-010-order-001` |
| [SCE-020] <!-- Manager access denied --> | Rights | `user-manager-001`, `user-client-001` | `SEED-SCE-020-order-001` |
| <!-- ... --> | | | |

---

## 5. Destructive scenarios — isolation required

> *These scenarios modify or delete data irreversibly. They must be executed with an isolation strategy (transaction rollback or full reset before the test).*

| Scenario | Destructive action | Recommended strategy |
|----------|--------------------|---------------------|
| [SCE-xxx] <!-- Delete an order --> | Order deletion | Clean dataset per test — do not reuse shared dataset entities |
| [SCE-xxx] <!-- Archive a user --> | Irreversible status change | Transaction rollback or entity reset after the test |

---

## 6. Instructions for Claude Code

> *This section is a direct instruction to Claude Code for generating and using these seeds.*

### Loading order

```
1. Load the shared dataset (section 2): Roles → Users → Reference entities → Neutral entities
2. For each scenario, load its specific dataset (section 3) in the indicated insertion order
```

### Reset strategy between tests

| Test level | Strategy |
|------------|----------|
| API integration tests | Reset before each `describe` (suite) — reload shared dataset + scenario dataset |
| E2E tests (Phase 0) | Full reset before each Playwright scenario — truncate business tables in reverse FK order, then full reload |
| Destructive scenarios | Transactional scope or targeted reset of touched entities |

### Naming conventions to preserve

Stable IDs from the shared dataset (e.g.: `user-client-001`, `cat-electronics-001`) must be the same in TypeScript/Python factories and in SQL seeds. This allows test assertions to reference these IDs directly without collision risk.

### Recommended injection method

| Entity type | Preferred method | Reason |
|-------------|-----------------|--------|
| Reference entities (roles, categories) | Direct INSERT or test SQL migration | No expected business side effects |
| Application entities (users, orders) | Via setup API or application factory | To trigger business side effects (notifications, calculations, indexing) |
| Entities in abnormal states | Direct INSERT with explicit comment | APIs may refuse inserting invalid entities |

---

## Traceability

| BA Deliverable | Traced elements |
|----------------|-----------------|
| [DOM-001] | Entities and FK dependencies → Insertion graph (section 1) |
| [BRL-001] | Validation rules → Boundary values (section 3) |
| [ACT-001] | Roles → Shared dataset users (section 2.1) |
| [SCE-xxx] | `Given` preconditions → Datasets per scenario (section 3) |
