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
dependencies: ["VIS-001", "GLO-001", "ACT-001"]
confluence_id:
confluence_sync_hash:
---

# [BRL-{rule_type}] {rule_type_name} Rules Catalogue

## Rule type

| Type | Description | Prefix |
|------|-------------|--------|
| {rule_type} | {rule_type_description} | BR-{rule_type} |

---

## Rules

<!-- Repeat this block for each rule.
     Use the compact format below — one table per rule, adapted to the rule type.
     Keep each rule self-contained but concise: no variable tables, no entity/feature
     cross-references per rule (these are in the indices at the bottom). -->

### [BR-{rule_type}-001] Rule name

<!-- === VAL (Validation) === -->
| Property | Value |
|----------|-------|
| **Condition** | IF <!-- condition --> |
| **Consequence** | THEN <!-- what happens --> |
| **Error message** | "<!-- Exact message displayed to the user -->" |
| **Severity** | Blocking / Warning |

**Example:** <!-- One concrete example with realistic values -->

<!-- === CAL (Calculation) === -->
| Property | Value |
|----------|-------|
| **Formula** | <!-- Natural-language formula, e.g.: Row Total = sum of day allocations for working days --> |
| **Precision** | <!-- Rounding rule if applicable --> |

**Numerical example:** <!-- One concrete example with inputs → result -->

<!-- === TRG (Trigger) === -->
| Property | Value |
|----------|-------|
| **Event** | <!-- When this rule activates --> |
| **Condition** | IF <!-- condition --> |
| **Action** | THEN <!-- action(s) executed --> |

<!-- === COH (Consistency) === -->
| Property | Value |
|----------|-------|
| **Invariant** | <!-- Condition that must ALWAYS be true --> |
| **Verification** | <!-- On creation / modification / deletion --> |
| **Action if violated** | <!-- Block / Auto-correct / Alert --> |

<!-- === AUT (Authorisation) === -->
| Property | Value |
|----------|-------|
| **Controlled action** | <!-- Which action is subject to this rule --> |
| **Condition** | IF <!-- authorisation condition --> |
| **Authorised roles** | [ROL-xxx] |

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
