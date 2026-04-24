---
id: ACT-001
title: "Actors, Roles and Permissions — [Project Name]"
phase: 1-scoping
type: acteurs
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-actors
reviewers: []
dependencies: ["VIS-001", "GLO-001"]
confluence_id:
confluence_sync_hash:
---

# [ACT-001] Actors, Roles and Permissions

## 1. Actors

### 1.1 Human actors

#### [ACT-H001] ActorName

| Property | Value |
|----------|-------|
| **Description** | <!-- Who this person is in the organisation --> |
| **Primary objective** | <!-- What they seek to accomplish with the system --> |
| **Usage frequency** | <!-- Daily / Weekly / Occasional --> |
| **Technical level** | <!-- Novice / Intermediate / Expert --> |

---

### 1.2 System actors (external systems)

#### [ACT-S001] SystemName

| Property | Value |
|----------|-------|
| **Description** | <!-- Nature of the external system --> |
| **Interaction type** | <!-- Data send / Receive / Bidirectional --> |
| **Frequency** | <!-- Real-time / Batch / Event-driven --> |

---

## 2. Roles

| ID | Role | Description | Associated actors |
|----|------|-------------|-------------------|
| [ROL-001] | | | [ACT-H001] |
| [ROL-002] | | | [ACT-H001], [ACT-H002] |

### Role hierarchy
<!-- Does a role inherit rights from another? -->

```
ROL-ADMIN
  └── ROL-MANAGER
        └── ROL-USER
```

---

## 3. Permissions matrix

### 3.1 Role × Entity matrix (CRUD)

| Entity / Role | [ROL-001] | [ROL-002] | [ROL-003] |
|---------------|-----------|-----------|-----------|
| [ENT-001] Entity1 | CRUD | R | - |
| [ENT-002] Entity2 | CRUD | CRU | R |
| [ENT-003] Entity3 | CRUD | CR | R |

**Legend:** C = Create, R = Read, U = Update, D = Delete, - = No access

### 3.2 Role × Feature matrix

| Feature / Role | [ROL-001] | [ROL-002] | [ROL-003] |
|----------------|-----------|-----------|-----------|
| Feature 1 | ✅ | ✅ | ❌ |
| Feature 2 | ✅ | ❌ | ❌ |

---

## 4. Delegation and escalation rules

| Rule | Description |
|------|-------------|
| <!-- E.g.: Validation delegation --> | <!-- A manager can delegate their validation right to another manager --> |

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-actors |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [VIS-001], [GLO-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |
