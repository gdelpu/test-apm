---
id: TST-001
title: "Functional Test Scenarios — [Project Name]"
phase: 3-design
type: test-scenarios
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-tests
reviewers: []
dependencies: ["DOM-001", "BRL-001"]
confluence_id:
confluence_sync_hash:
---

# [TST-001] Functional Test Scenarios

## Coverage

### Coverage matrix: Business rules → Scenarios

| Business rule | Scenarios | Covered |
|--------------|-----------|---------|
| [BR-VAL-001] | [TS-001], [TS-002] | ✅ |
| [BR-CAL-001] | [TS-003] | ✅ |
| [BR-TRG-001] | [TS-004], [TS-005] | ✅ |
| [BR-COH-001] | None | ❌ To complete |

### Coverage matrix: User Stories → Scenarios

| User Story | Scenarios | Covered |
|-----------|-----------|---------|
| [US-001] | [TS-001], [TS-002], [TS-003] | ✅ |
| [US-002] | [TS-004] | ✅ |

---

## Nominal scenarios

### [TS-001] Nominal scenario name

| Property | Value |
|----------|-------|
| **Type** | Nominal |
| **Story / Enabler** | [US-xxx] or [EN-xxx] |
| **Tested rules** | [BR-xxx] |
| **Actor** | [ACT-Hxxx] with role [ROL-xxx] |

**Preconditions:**
- <!-- Required initial state of the system -->
- <!-- Pre-existing data necessary -->

**Test data:**

| Data | Value |
|------|-------|
| Name | "Martin Dupont" |
| Email | "martin.dupont@example.com" |
| Amount | 150.00€ |

**Scenario:**

- **Given** an authenticated user with the "Manager" role and order #1234 in "Draft" status with an amount of 150.00€
- **When** the user clicks "Validate the order"
- **Then** order #1234 moves to "Validated" status
- **And** a confirmation email is sent to martin.dupont@example.com
- **And** the validation date is recorded as today's date

---

## Boundary scenarios

### [TS-010] Boundary scenario name

| Property | Value |
|----------|-------|
| **Type** | Boundary |
| **Story / Enabler** | [US-xxx] or [EN-xxx] |
| **Tested rules** | [BR-xxx] |
| **What is tested** | <!-- E.g.: minimum value, empty list, maximum volume --> |

**Test data:**

| Data | Value | Particularity |
|------|-------|---------------|
| Amount | 5.00€ | Minimum allowed value |

**Scenario:**

- **Given** <!-- context with boundary value -->
- **When** <!-- action -->
- **Then** <!-- expected result: the boundary value is accepted -->

---

## Error scenarios

### [TS-020] Error scenario name

| Property | Value |
|----------|-------|
| **Type** | Error |
| **Story / Enabler** | [US-xxx] or [EN-xxx] |
| **Tested rules** | [BR-VAL-xxx] |
| **What is tested** | <!-- E.g.: invalid data, insufficient rights --> |

**Test data:**

| Data | Value | Particularity |
|------|-------|---------------|
| Amount | -10.00€ | Negative value (forbidden) |

**Scenario:**

- **Given** <!-- context with invalid data -->
- **When** <!-- action -->
- **Then** the system displays the error message "<!-- exact message -->"
- **And** <!-- system state: no modification made -->

---

## Access rights scenarios

### [TS-030] Rights scenario name

| Property | Value |
|----------|-------|
| **Type** | Authorisation |
| **Tested rules** | [BR-AUT-xxx] |
| **What is tested** | <!-- E.g.: access denied for an unauthorised role --> |

**Scenario:**

- **Given** an authenticated user with the "Reader" role
- **When** the user attempts to delete order #1234
- **Then** the system displays "You do not have the rights to perform this action"
- **And** order #1234 is not modified

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-tests |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [US-xxx], [DOM-001], [BRL-001], [UF-xxx] |
| **Validated by** | Pending |
| **Validation date** | Pending |
