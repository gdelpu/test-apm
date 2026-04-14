---
id: SCR-001
title: "[Screen name]"
phase: 3-design
type: screen-spec
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-screens
reviewers: []
dependencies: ["DOM-001", "BRL-001"]
stories: ["US-001"]
confluence_id:
confluence_sync_hash:
---

# [SCR-001] Screen Name

## Summary

| Property | Value |
|----------|-------|
| **Screen type** | Form / List / Dashboard / Detail / Modal |
| **Actors** | [ACT-Hxxx] |
| **Authorised roles** | [ROL-xxx] |
| **Main story** | [US-xxx] |
| **Displayed/edited entities** | [ENT-xxx] |
| **Journey** | [UF-xxx] - Step X |

---

## 1. Displayed information (read-only)

| Element | Source (entity.attribute) | Display format | Display condition |
|---------|--------------------------|----------------|-------------------|
| | [ENT-xxx].attribute | | Always / If condition |
| | | | |

---

## 2. Input fields

| Field | Type | Mandatory | Default value | Constraints | Business rule |
|-------|------|-----------|---------------|-------------|---------------|
| Name | Text | Yes | - | Max 100 chars | - |
| Email | Email | Yes | - | Valid email format | [BR-VAL-xxx] |
| Amount | Decimal | Yes | 0.00 | > 0, 2 decimal places | [BR-VAL-xxx] |
| Type | Dropdown | Yes | First element | See [REF-xxx] | - |
| Date | Date picker | No | Today | ≤ today | - |
| Comment | Text area | No | - | Max 500 chars | - |
| Active | Checkbox | - | Checked | - | - |

---

## 3. Dynamic behaviours

### 3.1 Conditional display

| Condition | Elements shown/hidden | Detail |
|-----------|----------------------|--------|
| If Type = "Professional" | Show "Company number" field | Company number field becomes mandatory |
| If Amount > 1000€ | Show alert | "Amount subject to manager validation" |

### 3.2 Dependent fields

| Trigger field | Impacted field | Behaviour |
|---------------|---------------|-----------|
| Country | Region | Reloads the list of regions for the selected country |
| | | |

### 3.3 Real-time calculations

| Calculated field | Formula | Trigger |
|-----------------|---------|---------|
| Amount incl. VAT | Amount excl. VAT × (1 + VAT Rate) | Modification of the pre-tax amount or the VAT rate |

---

## 4. Actions (Buttons)

| Button | Type | Activation condition | Behaviour | Confirmation required |
|--------|------|---------------------|-----------|----------------------|
| Save | Primary | Form valid | Save and return to list | No |
| Validate | Primary | Form valid + status = Draft | Changes status to "Validated" | Yes: "Do you confirm the validation?" |
| Cancel | Secondary | Always | Return to previous page without saving | Yes if unsaved changes |
| Delete | Danger | Role [ROL-xxx] required | Deletion after confirmation | Yes: "This action is irreversible" |

---

## 5. Tables / Lists

### Table: Table name

| Column | Source | Sortable | Filterable | Format |
|--------|--------|---------|-----------|--------|
| ID | [ENT-xxx].id | Yes | No | Clickable link |
| Name | [ENT-xxx].name | Yes | Yes (text) | Text |
| Status | [ENT-xxx].status | Yes | Yes (list) | Colour badge |
| Date | [ENT-xxx].date | Yes | Yes (range) | DD/MM/YYYY |
| Amount | [ENT-xxx].amount | Yes | Yes (range) | #,###.##€ |

**Pagination:** Yes, 20 items per page
**Default sort:** Date descending
**Row actions:** View / Edit / Delete (by role)

---

## 6. User messages

| Event | Type | Message |
|-------|------|---------|
| Successful save | Success | "The record has been saved successfully" |
| Validation error | Error | See rule [BR-VAL-xxx] |
| Deletion confirmation | Confirmation | "Are you sure you want to delete this item?" |
| No results | Information | "No results match your search criteria" |

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-screens |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [US-xxx], [DOM-001], [BRL-001], [UF-xxx] |
| **Validated by** | Pending |
| **Validation date** | Pending |
