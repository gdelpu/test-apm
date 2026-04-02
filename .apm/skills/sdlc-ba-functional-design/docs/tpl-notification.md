---
id: NTF-001
title: "[Notification name]"
phase: 3-design
type: notification
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-notifications
reviewers: []
dependencies: ["DOM-001", "BRL-001"]
stories: ["US-001"]
---

# [NTF-001] Notification Name

## Summary

| Property | Value |
|----------|-------|
| **Triggering event** | <!-- Which business event triggers this notification --> |
| **Trigger rule** | [BR-TRG-xxx] |
| **Channel** | Email / In-app / SMS / Push |
| **Related story** | [US-xxx] |

---

## Recipients

| Recipient | Condition | Channel |
|-----------|-----------|---------|
| [ACT-Hxxx] Entity creator | Always | Email + In-app |
| [ACT-Hxxx] Manager | If amount > 1000€ | Email |
| <!-- Role or actor --> | <!-- Contextual condition --> | <!-- Channel --> |

---

## Message content

### Subject (if email)
```
[ApplicationName] - {{entity.type}} #{{entity.id}}: {{action_performed}}
```

### Message body

```
Hello {{recipient.firstName}},

{{description_of_the_event}}.

**Details:**
- **Reference:** {{entity.id}}
- **Date:** {{event.date | format "DD/MM/YYYY at HH:mm"}}
- **Performed by:** {{actor.name}}
- **Status:** {{entity.new_status}}

{{#if action_required}}
**Action required:** {{description_of_required_action}}
[Access the item]({{link_to_entity}})
{{/if}}

Best regards,
The {{application_name}} team
```

### Dynamic variables

| Variable | Source | Format |
|----------|--------|--------|
| `recipient.firstName` | [ENT-User].firstName | Text |
| `entity.id` | [ENT-xxx].id | Text |
| `event.date` | Current date/time | DD/MM/YYYY HH:mm |
| `actor.name` | User who triggered the action | Text |
| `entity.new_status` | [ENT-xxx].status | Enum label |

---

## Management rules

| Rule | Description |
|------|-------------|
| **Non-duplication** | <!-- E.g.: Do not send if same notification sent within 24 hours --> |
| **Grouping** | <!-- E.g.: Group same-type notifications into a daily digest --> |
| **Deactivation** | <!-- Can the user deactivate this notification? --> |
| **Language** | <!-- Recipient's language or default language --> |

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-notifications |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [US-xxx], [DOM-001], [BRL-001] |
| **Validated by** | Pending |
| **Validation date** | Pending |
