---
id: US-001
title: "[User Story Title]"
phase: 3-design
type: user-story
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-stories
reviewers: []
dependencies: ["DOM-001", "EP-001", "BRL-001"]
epic: EP-001
feature: FT-001
priority: Must
---

# [US-001] User Story Title

## Story

**As a** [ACT-Hxxx] (actor name),
**I want** <!-- action the user wants to perform -->,
**so that** <!-- expected business benefit -->.

---

## Context

| Property | Value |
|----------|-------|
| **Epic** | [EP-001] Epic name |
| **Feature** | [FT-001] Feature name |
| **Actor** | [ACT-Hxxx] Actor name |
| **Required role** | [ROL-xxx] |
| **Impacted entities** | [ENT-xxx], [ENT-xxx] |
| **Business rules** | [BR-xxx], [BR-xxx] |
| **Associated screen(s)** | [SCR-xxx] |
| **Priority** | Must / Should / Could |

---

## Acceptance criteria

### CA-001: Criterion name (nominal case)

- **Given** <!-- initial context with concrete values -->
- **When** <!-- trigger action -->
- **Then** <!-- verifiable expected result -->
- **And** <!-- additional result (optional) -->

### CA-002: Criterion name (alternative case)

- **Given** <!-- initial context -->
- **When** <!-- trigger action -->
- **Then** <!-- expected result -->

### CA-003: Criterion name (error case)

- **Given** <!-- initial context with invalid data -->
- **When** <!-- trigger action -->
- **Then** <!-- exact error message -->
- **And** <!-- system state after the error -->

---

## Preconditions

- <!-- Condition that must be true before the story can be executed -->
- <!-- E.g.: The user is authenticated with role [ROL-xxx] -->

## Postconditions

- <!-- State of the system after successful story execution -->
- <!-- E.g.: Entity [ENT-xxx] is created with status "Draft" -->

---

## Dependencies

| Type | Element | Description |
|------|---------|-------------|
| Required story | [US-xxx] | <!-- Why this story is needed before --> |
| Related story | [US-xxx] | <!-- Functional link without order dependency --> |

---

## Definition of Ready

- [ ] All acceptance criteria (CA-xxx) are in Given/When/Then format with concrete values
- [ ] All referenced business rules [BR-xxx] exist in the business rules catalogue
- [ ] Associated screen specification [SCR-xxx] is available (if UI story)
- [ ] Preconditions are verifiable (no vague state descriptions)
- [ ] No open question in Points of attention blocks the implementation

---

## Functional notes

<!-- Additional information, clarifications, justified functional choices -->

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-stories |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [DOM-001], [EP-001], [FT-001], [BRL-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |
