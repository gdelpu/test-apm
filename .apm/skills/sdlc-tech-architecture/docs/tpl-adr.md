---
id: ADR-001
title: "[Architecture decision title]"
system: t1-architecture
type: adr
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-t1.2-architecture-decisions
reviewers: []
dependencies: ["CTX-001"]
ba_dependencies: ["VIS-001", "DOM-001", "BRL-001"]
---

# [ADR-001] Architecture decision title

## Status

Proposed

<!-- Proposed | Accepted | Superseded by [ADR-yyy] -->

---

## Context

<!-- 
What is the architectural problem or force that motivates this decision?
What is the business and technical context?
Include relevant constraints from [CTX-001].
-->

---

## Addressed NFRs

<!-- Which non-functional requirements does this decision satisfy? -->

| NFR | Description | Target | BA Source |
|-----|-------------|--------|-----------|
| Performance | <!-- E.g. API response time --> | <!-- E.g. < 200ms p95 --> | [VIS-001] §Constraints |
| Scalability | <!-- E.g. Number of concurrent users --> | <!-- E.g. 1000 concurrent --> | [VIS-001] §Constraints |
| Availability | <!-- E.g. Uptime --> | <!-- E.g. 99.9% --> | |
| Security | <!-- E.g. GDPR compliance --> | <!-- E.g. Encryption at rest + in transit --> | [VIS-001] §Regulatory constraints |
| Maintainability | <!-- E.g. Module independence --> | <!-- E.g. Independent deployment per module --> | |

---

## Evaluated options

### Option A: <!-- Option name -->

<!-- Description of the option -->

**Advantages:**
- <!-- Advantage 1 -->
- <!-- Advantage 2 -->

**Disadvantages:**
- <!-- Disadvantage 1 -->
- <!-- Disadvantage 2 -->

### Option B: <!-- Option name -->

<!-- Description of the option -->

**Advantages:**
- <!-- Advantage 1 -->
- <!-- Advantage 2 -->

**Disadvantages:**
- <!-- Disadvantage 1 -->
- <!-- Disadvantage 2 -->

### Option C: <!-- Option name (optional) -->

<!-- Same structure -->

### Comparison matrix

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Performance | <!-- 1-5 --> | <!-- Score /5 --> | | |
| Complexity | | | | |
| Infrastructure cost | | | | |
| Team skills | | | | |
| Evolvability | | | | |
| **Weighted total** | | **X** | **X** | **X** |

---

## Decision

<!-- 
Which option was chosen and why?
Be explicit: "We choose Option X because..."
-->

---

## Consequences

### Positive
- <!-- Positive consequence 1 -->
- <!-- Positive consequence 2 -->

### Negative
- <!-- Negative consequence 1 (accepted technical debt, added complexity...) -->
- <!-- Negative consequence 2 -->

### Required enablers
<!-- Which technical enablers does this decision require? -->
- <!-- E.g. [ENB-001] Multi-environment CI/CD setup -->
- <!-- E.g. [ENB-002] OAuth2 authentication configuration -->

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| <!-- Risk 1 --> | High / Medium / Low | High / Medium / Low | <!-- Mitigation strategy --> |
| <!-- Risk 2 --> | | | |

---

## Traceability

### Technical traceability
| Element | Detail |
|---------|--------|
| **Produced by** | agent-t1.2-architecture-decisions |
| **Production date** | YYYY-MM-DD |
| **Technical inputs** | [CTX-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |

### BA traceability
| BA Deliverable | Traced elements |
|----------------|-----------------|
| [VIS-001] | Business constraints motivating the NFRs |
| [DOM-001] | Domain complexity influencing the architecture style |
| [BRL-001] | Business rules influencing the data strategy |
