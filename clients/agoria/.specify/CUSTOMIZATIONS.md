# Spec-Kit Customizations for Agoria XY-Tool

**Project**: Agoria XY-Tool  
**Version**: 1.1.0  
**Date**: 2025-10-10

## Overview

This document describes all customizations made to vanilla Spec-Kit for the Agoria XY-Tool project. These changes integrate Jira workflow, handle Dutch prototype translation, and organize specs by epic structure.

## Customizations Summary

### 1. Jira Integration (`/speckit.specify`)

**File**: `.github/prompts/speckit.specify.prompt.md`

**Changes**: Added Jira Issue Import Mode section that:
- Detects patterns: `from-jira XY-123`, `jira:XY-123`, `jira XY-123`
- Retrieves issue via Atlassian MCP (`mcp_atlassian_atl_getJiraIssue`)
- Detects Epic parent and creates folder structure
- Uses Jira-based naming: `specs/[EPIC-KEY-epic-name/]ISSUE-KEY-issue-title/`
- Maps Jira fields to spec sections (Summary→Name, Description→Overview, Comments→Clarifications)

**Usage**: `/speckit.specify from-jira XY-123`

### 2. Prototype Comparison + Dutch Translation (`/speckit.clarify`)

**File**: `.github/prompts/speckit.clarify.prompt.md`

**Changes**: Added Prototype Comparison Phase that:
- Runs `compare-with-prototype.ps1` to analyze prototype structure
- Uses semantic search to find relevant prototype files
- Maps spec requirements to prototype coverage (✅Exists/⚠️Partial/❌Missing/🔄Different)
- Creates Dutch→English translation mapping table for production code
- Posts results to Jira via `mcp_atlassian_atl_addCommentToJiraIssue`
- Adds "Prototype Reference" section with translation mappings

**Key Features**:
- Handles Dutch prototype names → English production code
- Common mappings: gebruikersnaam→username, bedrijfsnaam→companyName
- Posts structured results to originating Jira issue

### 3. Constitutional Enforcement

**File**: `.specify/memory/constitution.md`

**Changes**: Enhanced Principle IX (Prototype-Driven Design) with:
- Mandatory Dutch-to-English translation requirements
- Implementation must reference prototype patterns
- Added Spec-Kit workflow to Development Workflow section

### 4. Supporting Scripts

**File**: `.specify/scripts/powershell/get-jira-feature.ps1`
- Validates Jira issue key format
- Outputs MCP instructions and naming conventions
- Supports Epic organization structure

**File**: `.specify/scripts/powershell/compare-with-prototype.ps1`  
- Scans prototype directory structure
- Detects patterns from package.json (routing, styling, state management)
- Outputs JSON with prototype analysis

## Integration Workflow

```
Jira Issue XY-123 "Gebruikersbeheer" (Epic: XY-100 "Beheermodule")
    ↓
/speckit.specify from-jira XY-123
    ↓ (creates specs/XY-100-beheermodule/XY-123-gebruikersbeheer/)
/speckit.clarify  
    ↓ (compares prototype, maps Dutch→English, posts to Jira)
Implementation with English names following prototype patterns
```

## Key Benefits

- **Single Source of Truth**: Jira remains authoritative
- **Automatic Translation**: Dutch prototype → English production code
- **Team Visibility**: Results posted back to Jira
- **Logical Organization**: Epic-based folder structure
- **Consistency**: Prototype patterns enforced constitutionally

## Dutch-English Translation Examples

| Dutch (Prototype) | English (Production) | Context |
|-------------------|---------------------|---------|
| gebruikersnaam | username | Form field |
| bedrijfsnaam | companyName | Entity property |
| e-mail | email | Form field |
| toevoegen | add | Action button |
| bewerken | edit | Action button |
| verwijderen | delete | Action button |
| overzicht | overview | Page title |
| beheer | management | Module name |
| instellingen | settings | Configuration |
| wachtwoord | password | Security field |

## File Structure Examples

**With Epic**:
```
specs/
├── XY-100-beheermodule/
│   ├── XY-101-gebruikersbeheer/
│   │   ├── spec.md
│   │   └── plan.md
│   └── XY-102-rolbeheer/
└── XY-200-rapportage/
    └── XY-201-maandrapport/
```

**Without Epic**:
```
specs/
├── XY-150-bug-fix-login/
│   └── spec.md
└── XY-151-performance-update/
    └── spec.md
```

## Testing

**Jira Integration**:
- Valid issue keys: XY-123, PROJ-456
- Epic detection and folder creation
- Jira comment posting

**Prototype Comparison**:
- Dutch name extraction from prototype files
- Translation mapping table generation
- Pattern detection (routing, styling, state management)

**Epic Organization**:
- Epic parent detection in Jira issues
- Proper folder hierarchy creation
- Standalone issue handling

## Limitations

- Manual review needed for complex Dutch translations
- Epic folder not auto-renamed if Jira epic title changes
- Only supports one Epic level (not nested epics)
- Requires Atlassian MCP access for Jira integration

## All Changes Marked

Every customization is marked with:
```markdown
<!-- CUSTOMIZATION: Agoria XY-Tool - [Description] -->
[Custom content]
<!-- END CUSTOMIZATION -->
```

**Files Modified**: 4 (constitution, 2 prompts, 1 script)  
**Scripts Added**: 2 (get-jira-feature.ps1, compare-with-prototype.ps1)  
**Version**: 1.1.0 (Dutch translation + Epic organization)