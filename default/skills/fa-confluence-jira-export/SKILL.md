---
name: fa-confluence-jira-export
description: 'Converts FA deliverables to platform-ready formats: Confluence wiki markup pages with proper hierarchy, metadata, and macros; Jira-ready epics and stories with Gherkin acceptance criteria in CSV and JSON export formats.'
triggers: ['prepare for Confluence', 'Confluence export', 'wiki markup', 'prepare for Jira', 'Jira export', 'Jira import', 'epic structure Jira', 'story export', 'Confluence page']
version: '1.0.0'
author: 'soprasteria'
---

# Skill: FA Confluence & Jira Export

## Purpose

Transforms FA deliverables into platform-specific formats for Confluence and Jira. Produces Confluence wiki markup pages (not Markdown) and Jira-ready CSV/JSON exports with standardised naming, labels, and acceptance criteria.

## When to Apply

Use this skill when:
- Preparing deliverables for Confluence upload
- Exporting user stories and epics for Jira import
- Converting Markdown requirements to Confluence wiki markup
- Generating CSV or JSON for Jira bulk import
---

## Confluence Standards

### Output Format Rule

All files in `confluence-export/` MUST use **Confluence wiki markup**, not Markdown. File extension remains `.md` for editor compatibility; content is wiki markup.

### Wiki Markup Quick Reference

| Element | Wiki Markup | Example |
|---------|-------------|---------|
| Heading 1 | `h1. Title` | `h1. Project Overview` |
| Heading 2 | `h2. Section` | `h2. Business Requirements` |
| Heading 3 | `h3. Subsection` | `h3. MUST HAVE` |
| Bold | `*text*` | `*MUST HAVE*` |
| Italic | `_text_` | `_Draft_` |
| Bullet list | `* item` | `* First` then `* Second` |
| Numbered list | `# item` | `# Step one` |
| Table header | header cells between double bars | `|| col1 || col2 ||` |
| Table data | data cells between single bars | then data rows |
| Horizontal rule | `----` | Four hyphens |
| Info panel | `{info:title=Title}...{info}` | Informational callout |
| Warning panel | `{warning:title=Title}...{warning}` | Critical callout |
| Note panel | `{note:title=Title}...{note}` | Advisory callout |
| TOC macro | `{toc:printable=true}` | Table of contents |
| Expandable | `{expand:title=Title}...{expand}` | Collapsible section |
| Link | `[display text or page-title-or-url]` | Internal/external link |

### Page Hierarchy

```
[PROJECT] - Functional Analysis (Space Home)
+-- 1. Project Overview
+-- 2. Stakeholder Analysis
+-- 3. Discovery & Elicitation
+-- 4. Current State Analysis
+-- 5. Requirements
|   +-- 5.1 Business Requirements
|   +-- 5.2 Functional Requirements
|   +-- 5.3 Non-Functional Requirements
|   +-- 5.4 Traceability Matrix
|   +-- 5.5 MoSCoW Prioritisation
+-- 6. User Stories & Epics
+-- 7. Process Models & Diagrams
+-- 8. Solution Design
+-- 9. Meetings & Workshops
+-- 10. Appendices
```

### Page Metadata (Every Page)

Include an info panel at the top of every Confluence page:

```
{info:title=Document Information}
Project: [Project Name]
Version: [X.Y.Z]
Status: [Draft / Review / Approved / Final]
Author: [Name]
Last Updated: [dd/mm/YYYY]
{info}
```

### Cross-Linking

- Link overview pages to detail pages
- Link requirements to user stories
- Link user stories to epics
- Link decisions to supporting rationale

### Labels (Apply Consistently)

- Project identifier: `[project-name]`
- Phase: `discovery`, `analysis`, `design`, `validation`
- Type: `requirements`, `user-stories`, `diagrams`, `decisions`
- Priority: `must-have`, `should-have`, `could-have`
- Status: `draft`, `review`, `approved`

### Output Location

`Projects/[project]/deliverables/.../FA/confluence-export/`
---

## Jira Standards

### Naming Conventions

**Project Key:** Uppercase, 3-6 characters (e.g., `FUNDHUB`, `JCA`)
**Epics:** `EPIC-[NN]: [Descriptive Name]` (max 60 chars)
**Stories:** `US-[NNN]: [Action-Oriented Title]` (max 80 chars, start with verb)
**Tasks:** `[EPIC-NN] [Brief Description]`

### Epic Fields for Jira

- Summary: One-line, max 255 chars
- Description: Business context, scope, out-of-scope
- Priority: Critical / High / Medium / Low
- Labels: [project-code], [feature-area]
- Fix Version: [Release X.Y]
- Story Points (Total): Sum of child stories

### Story Fields for Jira

- Summary: One-line, max 255 chars
- Issue Type: Story
- Epic Link: EPIC-[NN]
- Description: Persona-driven As a / I want / So that
- Acceptance Criteria: Gherkin (GIVEN/WHEN/THEN)
- Priority: MoSCoW (Must / Should / Could / Won't)
- Story Points: Fibonacci (1/2/3/5/8/13/21)
- Labels: [project], [epic-name], [feature]
- Components: [Component name]

### Acceptance Criteria Standard (Gherkin)

```
GIVEN [precondition/context]
  AND [additional context if needed]
WHEN [action/trigger]
  AND [additional action if needed]
THEN [expected outcome]
  AND [additional outcome if needed]
```

Quality: Specific, measurable, testable, achievable, complete (happy path + alternatives + errors), independent of implementation, written from user perspective.

### CSV Export Format

Headers:
```
Summary,Issue Type,Epic Link,Description,Priority,Labels,Story Points,Acceptance Criteria
```

### JSON Export Format

```json
{
  "projects": [{
    "key": "[PROJECT-KEY]",
    "issues": [
      {
        "issueType": "Epic",
        "summary": "[Title]",
        "description": "[Description]",
        "priority": "[Priority]",
        "labels": ["label1"]
      },
      {
        "issueType": "Story",
        "summary": "[Title]",
        "epicLink": "EPIC-NN",
        "description": "[Story description]",
        "acceptanceCriteria": "[Gherkin AC]",
        "storyPoints": 5,
        "priority": "[Priority]"
      }
    ]
  }]
}
```