---
id: ENB-001
title: "[Technical enabler title]"
system: t2-design
type: enabler
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-t1.4-enabler-extraction
dependencies: ["CTX-001", "STK-001"]
ba_dependencies: []
adr_reference: ADR-xxx
priority: Must
wave: 0
---

# [ENB-001] Technical enabler title

## Description

<!-- What cross-cutting need does this enabler address?
     Why is it necessary before the stories are implemented? -->

---

## Context

| Property | Value |
|----------|-------|
| **Motivating ADR** | [ADR-xxx] — <!-- ADR title --> |
| **Category** | Infrastructure / Security / Observability / Cross-cutting / DevOps |
| **Priority** | Must / Should / Could |
| **Implementation wave** | <!-- Wave 0 (setup) / Wave 1 (foundation) / Wave 2 (application) --> |
| **Enabler dependencies** | [ENB-xxx] <!-- Other prerequisite enablers --> |
| **Unlocked stories** | [US-xxx], [US-xxx] <!-- Stories that require this enabler --> |

---

## Specification

### Scope

**Included:**
- <!-- Element 1 -->
- <!-- Element 2 -->

**Excluded:**
- <!-- Excluded element with justification -->

### Required configuration

<!-- Only list parameters that are specific to this enabler.
     Omit this section if no configuration is needed. -->

| Parameter | Value | Secret |
|-----------|-------|--------|
| <!-- E.g. DATABASE_URL --> | <!-- E.g. postgresql://... --> | No |

### Architecture

<!-- Diagram or description of the enabler architecture.
     Optional — include only if it clarifies the implementation. -->

```mermaid
graph LR
    A[Client] --> B[API Gateway]
    B --> C[Auth Middleware]
    C --> D[Service]
```

---

## Acceptance criteria

### AC-001: <!-- Criterion name (nominal case) -->

- **Given** <!-- initial context with concrete values -->
- **When** <!-- triggering action -->
- **Then** <!-- expected verifiable result -->

### AC-002: <!-- Criterion name (error case) -->

- **Given** <!-- context with error situation -->
- **When** <!-- action -->
- **Then** <!-- expected behaviour on error -->

---

## Validation tests

<!-- Concise list of how to verify this enabler works. -->

| Type | Description |
|------|-------------|
| Unit | <!-- E.g. Test of the authentication service in isolation --> |
| Integration | <!-- E.g. Test with a real database --> |
| Smoke test | <!-- E.g. Health check verification in deployed env --> |

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-t1.4-enabler-extraction |
| **Production date** | YYYY-MM-DD |
| **Technical inputs** | [CTX-001], [ADR-xxx], [STK-001] |
| **BA inputs** | <!-- [ACT-001], [VIS-001] if applicable --> |
| **Validated by** | Pending |
