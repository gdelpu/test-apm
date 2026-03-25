---
name: fa-communication-templates
description: 'Professional communication document templates for functional analysis: discovery questionnaires, meeting preparation and summary documents, status reports, Word/PDF export with branding, and semantic versioning for all FA deliverables.'
triggers: ['questionnaire', 'meeting preparation', 'meeting summary', 'status report', 'client communication', 'document template', 'Word document', 'PDF export', 'document versioning']
version: '1.0.0'
author: 'soprasteria'
---

# Skill: FA Communication Templates

## Purpose

Provides standardised templates for all client and team communication documents in functional analysis projects. Covers questionnaires, meeting documents, status reports, and document conversion to Word/PDF with professional branding.

## When to Apply

Use this skill when:
- Creating discovery questionnaires for stakeholders
- Preparing meeting agendas and materials
- Writing meeting summaries with action items
- Generating project status reports
- Converting deliverables to Word or PDF format
- Applying document versioning standards

---

## Professional Standards

- No emojis or unicode symbols in any professional documents
- Use plain text status indicators (e.g., "COMPLETE" not checkmarks)
- All dates in dd/mm/YYYY format
- Maintain consistent formatting throughout
- For client-facing branding, invoke the existing `brand-styler` or `soprasteria-brand-*` skills

---

## Document Naming Convention

Format: `[PROJECT-CODE]-[DOCTYPE]-[VERSION]-[STATUS].[ext]`

Examples:
- `FUNDHUB-FA-COMPLETE-v2.0.0-APPROVED.docx`
- `AQUA-QUESTIONNAIRE-v1.0.0-DRAFT.pdf`
- `JCA-MEETING-NOTES-2025-12-09.md`

---

## Semantic Versioning for Documents

- **Major (X.0.0):** Complete restructure or final approved version
- **Minor (X.Y.0):** Significant content additions or updates
- **Patch (X.Y.Z):** Corrections, clarifications, minor edits

### Version History Table (include in all documents)

```
## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | [dd/mm/YYYY] | [Name] | Initial release |
| 1.1.0 | [dd/mm/YYYY] | [Name] | Added [section], updated [section] |
```

---

## Template 1: Discovery Questionnaire

```markdown
# [Project Name] - Discovery Questionnaire

## Document Information

| Field | Value |
|-------|-------|
| Project | [Project Name] |
| Document Type | Discovery Questionnaire |
| Version | [X.Y.Z] |
| Date | [dd/mm/YYYY] |
| Prepared By | [Name] |
| Target Audience | [Stakeholder Groups] |
| Response Deadline | [dd/mm/YYYY] |

## Purpose

This questionnaire gathers detailed information about [topic/system/project]
to support the functional analysis process.

## Instructions

1. Answer each question as thoroughly as possible
2. Provide specific examples where requested
3. Mark questions you cannot answer as "TBD" rather than leaving blank
4. Flag questions needing clarification

Timeline: Return by [date]. Expected time: [X hours].
Contact: [Name] at [email]

## Part 1: [Category Name] ([N] Questions)

Purpose: [Why these questions matter]

### Q1. [Question Title]
[Detailed question text]

Please provide:
- [Specific item 1]
- [Specific item 2]

## Additional Information (Optional)

If available, please share:
- [Supporting documents]
- [Data or reports]
- [Screenshots or examples]

## Next Steps

1. Review all responses (allow [X days])
2. Prepare clarification questions if needed
3. Schedule [meeting type] to discuss findings

## Confidentiality

All information will be treated as confidential and used solely
for this functional analysis project.
```

---

## Template 2: Meeting Preparation

```markdown
# Meeting Preparation - [Meeting Type] - [Project Name]

## Meeting Information

| Field | Value |
|-------|-------|
| Meeting Type | [Discovery / Workshop / Review / Validation] |
| Date and Time | [dd/mm/YYYY HH:MM - HH:MM] |
| Duration | [X hours] |
| Location | [Physical location or video link] |
| Facilitator | [Name] |

## Attendees

Required:
| Name | Role | Organisation |
|------|------|--------------|
| [Name] | [Role] | [Org] |

Optional:
| Name | Role | Organisation |
|------|------|--------------|
| [Name] | [Role] | [Org] |

## Objectives

By the end of this meeting, we will have:
1. [Objective 1 - specific, measurable]
2. [Objective 2]

## Agenda

| Time | Duration | Topic | Owner | Materials |
|------|----------|-------|-------|-----------|
| [HH:MM] | [X min] | Welcome and Objectives | [Name] | - |
| [HH:MM] | [X min] | [Topic 1] | [Name] | [Link] |
| [HH:MM] | [X min] | Next Steps and Close | [Name] | - |

## Pre-Meeting Materials

1. [Document Name] ([X pages], [X min read]) - [Brief description]

## Key Questions to Address

### Topic 1: [Topic Name]
1. [Question 1]
2. [Question 2]

## Expected Decisions

| # | Decision Required | Options | Stakeholder |
|---|-------------------|---------|-------------|
| 1 | [Decision topic] | A, B, or C | [Who decides] |

## Preparation Checklist

Facilitator:
- Agenda confirmed and distributed
- Materials prepared and shared
- Meeting room/link confirmed
- Note-taker identified

Attendees:
- Pre-reading completed
- Questions prepared
```

---

## Template 3: Meeting Summary

```markdown
# Meeting Summary - [Meeting Type] - [Project Name]

## Meeting Information

| Field | Value |
|-------|-------|
| Date | [dd/mm/YYYY] |
| Time | [HH:MM - HH:MM] ([X hours]) |
| Location | [Location] |
| Facilitator | [Name] |

## Attendees

Present:
- [Name] ([Role], [Organisation])

Absent:
- [Name] ([Role]) - [Reason]

## Objectives (Planned)
1. [Objective 1]
2. [Objective 2]

## Key Discussion Points

### Topic 1: [Topic Name]
Discussion: [Summary]
Decision: [What was decided]
Action Items:
- [Action] - Owner: [Name] - Due: [dd/mm/YYYY]

## Decisions Made

| # | Decision | Rationale | Impact |
|---|----------|-----------|--------|
| 1 | [Decision] | [Why] | [What it affects] |

## Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [Action] | [Name] | [dd/mm/YYYY] | Pending |

## Open Questions
1. [Question] - To be addressed by: [Name/Date]

## Next Meeting
- Date: [dd/mm/YYYY]
- Topics: [Planned topics]
```

---

## Template 4: Status Report

```markdown
# Project Status Report - [Project Name]

## Reporting Period
[dd/mm/YYYY] - [dd/mm/YYYY]

## Status Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| Overall | [On Track / At Risk / Delayed] | [Brief note] |
| Discovery | [Complete / In Progress / Not Started] | [Brief note] |
| Requirements | [Complete / In Progress / Not Started] | [Brief note] |
| Documentation | [Complete / In Progress / Not Started] | [Brief note] |

## Accomplishments This Period
1. [Accomplishment 1]
2. [Accomplishment 2]

## Planned Next Period
1. [Planned item 1]
2. [Planned item 2]

## Risks and Issues

| # | Type | Description | Mitigation | Status |
|---|------|-------------|------------|--------|
| 1 | Risk | [Description] | [Plan] | [Open/Mitigated] |

## Key Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Requirements Complete | [N] | [N] | [%] |

## Decisions Needed
1. [Decision needed with context]
```

---

## Word/PDF Export

### Word Document Structure

1. Cover Page (Project Name, Title, Version, Date, Client, Logo)
2. Document Control (Version History, Approvals, Distribution)
3. Table of Contents (auto-generated)
4. Executive Summary
5. Main Content Sections
6. Appendices
7. Footer (page numbers, document name, version, confidentiality)

### PDF Generation Workflow

1. Create/edit content in Markdown
2. Convert to Word using `python scripts/md_to_word.py document.md --pdf`
3. Branding applied automatically (fonts, colours, logo)

### For branded output

Invoke the existing `brand-styler` skill for Pandoc-based DOCX/PDF generation with brand fonts, colours, and templates.