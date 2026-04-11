---
name: m365-data-query
description: 'Query Microsoft 365 data via Work-iq MCP — emails, meetings, Teams messages, OneDrive documents, and people directory.'
triggers:
  - microsoft 365
  - m365 data
  - outlook emails
  - teams messages
  - onedrive documents
  - work-iq
  - meeting notes
---

# Skill: m365-data-query

## Goal

Query Microsoft 365 data via the Work-iq MCP server to enrich SDLC workflows with organisational context: meeting notes, email threads, Teams discussions, document references, and people information.

## MCP Server

- **Registry ID**: `work-iq-mcp`
- **Repository**: https://github.com/microsoft/work-iq
- **Auth**: Entra tenant admin consent required
- **Install**: `npx -y @microsoft/workiq mcp`

## Prerequisites

> **Important**: Work-iq requires Microsoft Entra tenant admin consent to access M365 data. See the [Tenant Administrator Enablement Guide](https://github.com/microsoft/work-iq/blob/main/ADMIN-INSTRUCTIONS.md) for setup instructions.

## When to use

- Pulling meeting notes from Teams/Outlook for steering governance (COPIL)
- Searching email threads for project decisions and context
- Checking team calendar for sprint planning and availability
- Finding documents in OneDrive/SharePoint related to the project
- Looking up people and organisational structure

## When NOT to use

- For Jira/Confluence (use `atlassian-ops` skill)
- When M365 tenant admin consent has not been granted
- For production data analysis (PII risk too high without explicit approval)

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `work-iq-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute query

Based on the user's request:
- **Emails**: Search emails by sender, subject, date range, or keywords
- **Meetings**: List upcoming meetings, retrieve meeting notes and agendas
- **Teams messages**: Search Teams channels for project-related discussions
- **Documents**: Find documents in OneDrive/SharePoint by name or content
- **People**: Look up team members, reporting structure, skills

### Step 3 — PII redaction (MANDATORY)

**Before including any M365 data in outputs**, run the `data-anonymisation` skill:
- Replace all email addresses with `[REDACTED:email]`
- Replace phone numbers with `[REDACTED:phone]`
- Replace names of external parties with `[REDACTED:name]`
- Internal project team names may be kept if non-sensitive

### Step 4 — Format results

Write redacted results to the appropriate output file.

### Fallback (without MCP)

If `work-iq-mcp` is unavailable:
1. Ask the user to provide meeting notes, email summaries, or decisions manually
2. Accept pasted content and process it through the workflow
3. Warn that automatic M365 integration is unavailable
4. Document gaps where M365 data would have enriched the deliverable

## Output

Integrates into the calling workflow's output files. For standalone use:
`outputs/specs/features/<feature>/m365-context.md`

## Security

- **Mandatory PII redaction** on ALL M365 data before inclusion in any output
- Never cache or persist raw M365 data — process and redact immediately
- Respect Microsoft's data residency requirements
- All M365 queries are logged in audit trace with `[M365-ACCESS]` tag
- Sensitivity classification: **confidential** (derived from customer/business data)
