---
id: EXF-001
title: "Functional Requirements Catalogue — [Project Name]"
phase: 1-scoping
type: functional-requirements
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-requirements
reviewers: []
dependencies: ["VIS-001", "GLO-001", "ACT-001"]
r4j_synced: false
r4j_mapping_file: r4j-mapping.json
confluence_id:
confluence_sync_hash:
---

# [EXF-001] Functional Requirements Catalogue

## Summary

| Indicator | Value |
|-----------|-------|
| **Total number of requirements** | X |
| **Must Have** | X |
| **Should Have** | X |
| **Could Have** | X |
| **Won't Have** | X |
| **Critical requirements** | X |
| **Identified functional domains** | X |

---

## Requirement categories

| Category | Description |
|----------|-------------|
| **Functional** | Direct business capability exposed to an actor |
| **Data** | Data management, quality and lifecycle |
| **Access rights** | Permissions and action scope control |
| **Interoperability** | Functional exchanges with third-party systems |
| **Cross-cutting** | Constraints applying to the entire system |

---

## Functional domain: [Domain 1 Name]

> _Corresponds to functional block X of the scope. Prefigures Epic [EP-xxx] (to be created in System 2)._

### [EX-001] Requirement title

| Property | Value |
|----------|-------|
| **Category** | Functional |
| **MoSCoW priority** | Must / Should / Could / Won't |
| **Criticality** | Critical / High / Standard |
| **Concerned actor(s)** | [ACT-Hxxx] Role name |
| **Source** | Section "X" of source document / [VIS-001] §X |
| **Depends on** | — |
| **Jira R4J** | _(to be filled after sync: PROJ-xxx)_ |

**Description:**
The system must allow [description of the capability in 2-4 sentences, no technical detail, business-value oriented].

**Usage context:**
> [Specify the context in which this requirement applies, if necessary]

**Downstream traceability:** _(completed as phases progress)_

| Component | Identifiers |
|-----------|------------|
| Epics / Features | [EP-xxx], [FT-xxx] ← _to complete in System 2_ |
| User Stories | [US-xxx] ← _to complete in System 3_ |
| Test scenarios | [TS-xxx] ← _to complete in System 3_ |

---

### [EX-002] Requirement title

| Property | Value |
|----------|-------|
| **Category** | Functional |
| **MoSCoW priority** | Must / Should / Could / Won't |
| **Criticality** | Critical / High / Standard |
| **Concerned actor(s)** | [ACT-Hxxx] |
| **Source** | |
| **Depends on** | [EX-001] |
| **Jira R4J** | _(to be filled after sync)_ |

**Description:**
The system must allow [...]

**Downstream traceability:**

| Component | Identifiers |
|-----------|------------|
| Epics / Features | ← _to complete_ |
| User Stories | ← _to complete_ |
| Test scenarios | ← _to complete_ |

---

## Functional domain: [Domain 2 Name]

> _Corresponds to functional block Y of the scope. Prefigures Epic [EP-yyy]._

### [EX-010] Requirement title

| Property | Value |
|----------|-------|
| **Category** | Access rights |
| **MoSCoW priority** | Must |
| **Criticality** | Critical |
| **Concerned actor(s)** | [ACT-Hxxx], [ACT-Hyyy] |
| **Source** | [ACT-001] Permissions matrix |
| **Depends on** | — |
| **Jira R4J** | _(to be filled after sync)_ |

**Description:**
The system must restrict [...]

**Downstream traceability:**

| Component | Identifiers |
|-----------|------------|
| Epics / Features | ← _to complete_ |
| User Stories | ← _to complete_ |
| Test scenarios | ← _to complete_ |

---

## Cross-cutting requirements

> _These requirements apply to all domains. They generate cross-cutting business rules and acceptance criteria in subsequent phases._

### [EX-T001] Functional security and action traceability

| Property | Value |
|----------|-------|
| **Category** | Cross-cutting |
| **MoSCoW priority** | Must |
| **Criticality** | Critical |
| **Concerned actor(s)** | All |
| **Source** | [VIS-001] Constraints |
| **Depends on** | — |
| **Jira R4J** | _(to be filled after sync)_ |

**Description:**
The system must authenticate each user before any access and record an audit log of sensitive actions (creations, modifications, deletions, validations). Every action must be timestamped and attributed to the logged-in user.

**Downstream traceability:**

| Component | Identifiers |
|-----------|------------|
| Epics / Features | ← _to complete_ |
| User Stories | ← _to complete_ |
| Test scenarios | ← _to complete_ |

---

### [EX-T002] Cross-cutting requirement 2 title

| Property | Value |
|----------|-------|
| **Category** | Cross-cutting |
| **MoSCoW priority** | |
| **Criticality** | |
| **Concerned actor(s)** | |
| **Source** | |
| **Depends on** | |
| **Jira R4J** | _(to be filled after sync)_ |

**Description:**
[...]

**Downstream traceability:**

| Component | Identifiers |
|-----------|------------|
| Epics / Features | ← _to complete_ |
| User Stories | ← _to complete_ |
| Test scenarios | ← _to complete_ |

---

## Coverage matrix: domains × actors

> _Verifies that each human actor is covered by at least one requirement in their main domain._

| Functional domain | [ACT-H001] | [ACT-H002] | [ACT-H003] | … |
|-------------------|-----------|-----------|-----------|---|
| Domain 1 | EX-001, EX-002 | EX-003 | — | |
| Domain 2 | — | EX-010 | EX-011 | |
| Cross-cutting | EX-T001 | EX-T001 | EX-T001 | |

---

## Coverage matrix: requirements × vision

> _Verifies that each element of the IN scope from the vision is covered._

| IN scope element ([VIS-001]) | Requirements covering this element | Covered? |
|------------------------------|------------------------------------|----------|
| [Element 1] | EX-001, EX-002 | ✅ |
| [Element 2] | EX-010 | ✅ |
| [Element 3] | (none) | ❌ |

---

## Attention Points

> _Uncertain, implicit requirements or those requiring a stakeholder decision._

| # | Requirement | Nature of the attention point | Decision expected from |
|---|-------------|-------------------------------|------------------------|
| 1 | EX-xxx | [Description of the uncertainty] | [Stakeholder] |

---

## Version history

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | agent-requirements | Initial version |
