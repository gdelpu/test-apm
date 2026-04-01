---
id: "BRL-{rule_type}"
title: "{rule_type_name} Rules Catalogue — [Project Name]"
phase: 2-specification
type: business-rules
rule_type: "{rule_type}"
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-rules
reviewers: []
dependencies: ["VIS-001", "GLO-001", "ACT-001"]
---

# [BRL-{rule_type}] {rule_type_name} Rules Catalogue

## Rule type

| Type | Description | Prefix |
|------|-------------|--------|
| {rule_type} | {rule_type_description} | BR-{rule_type} |

---

## Rules

### [BR-{rule_type}-001] Rule name

<!-- Repeat this block for each rule. Fields depend on the rule type: -->

<!-- === VAL (Validation) === -->
<!-- | Property | Value |
|----------|-------|
| **Description** | <!-- Description in natural language -->  |
| **Condition** | IF <!-- condition --> |
| **Consequence** | THEN <!-- what happens --> |
| **Error message** | "<!-- Exact message displayed to the user -->" |
| **Concerned entities** | [ENT-xxx] |
| **Concerned attributes** | attribute1, attribute2 |
| **Related features** | [FT-xxx] |
| **Severity** | Blocking / Warning |

**Example:**
> IF the order amount is less than 5.00€
> THEN block the validation and display "The minimum order amount is 5.00€" -->

<!-- === CAL (Calculation) === -->
<!-- | Property | Value |
|----------|-------|
| **Description** | |
| **Formula** | `result = operand1 × operand2 + operand3` |
| **Variables** | operand1 = [ENT-xxx].attribute, operand2 = ... |
| **Rounding** | <!-- Rounding rule if applicable --> |
| **Concerned entities** | [ENT-xxx] |
| **Related features** | [FT-xxx] |

**Numerical example:**
> Inputs: amountExcludingTax = 100.00€, vatRate = 20%
> Calculation: amountIncludingTax = 100.00 × (1 + 0.20) = 120.00€ -->

<!-- === TRG (Trigger) === -->
<!-- | Property | Value |
|----------|-------|
| **Triggering event** | <!-- When this rule activates --> |
| **Condition** | IF <!-- condition for the action to trigger --> |
| **Action** | THEN <!-- action(s) executed --> |
| **Concerned entities** | [ENT-xxx] |
| **Related features** | [FT-xxx] |
| **Related notification** | [NTF-xxx] (if applicable) | -->

<!-- === COH (Consistency) === -->
<!-- | Property | Value |
|----------|-------|
| **Invariant** | <!-- Condition that must ALWAYS be true --> |
| **Concerned entities** | [ENT-xxx], [ENT-yyy] |
| **Verification moment** | <!-- On creation / modification / deletion --> |
| **Action if violated** | <!-- Block / Auto-correct / Alert --> |
| **Related features** | [FT-xxx] | -->

<!-- === AUT (Authorisation) === -->
<!-- | Property | Value |
|----------|-------|
| **Controlled action** | <!-- Which action is subject to this rule --> |
| **Condition** | IF <!-- authorisation condition --> |
| **Authorised roles** | [ROL-xxx] |
| **Exception** | <!-- Cases where the rule does not apply --> |
| **Related features** | [FT-xxx] | -->

---

## Rules index by entity

| Entity | Associated rules |
|--------|-----------------|
| [ENT-001] | [BR-{rule_type}-001], [BR-{rule_type}-002] |

## Rules index by feature

| Feature | Associated rules |
|---------|-----------------|
| [FT-001] | [BR-{rule_type}-001] |

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-rules ({rule_type}) |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [VIS-001], [GLO-001], [ACT-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |
