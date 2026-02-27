# Agoria XY-Tool Spec-Kit Workflow

**Project**: Agoria XY-Tool  
**Updated**: October 2025  
**Status**: Active

## Overview

This project uses a customized Spec-Kit workflow that integrates with Jira and leverages our Dutch prototype for consistent development. The workflow ensures all features are properly specified, validated against the prototype, and implemented according to our design standards.

## Prerequisites

- **Jira Access**: You need access to the Agoria Jira instance with the XY project
- **Atlassian MCP**: Configured for Jira integration (see IT setup guide)
- **Prototype Access**: The Dutch prototype is available in the `prototype/` directory
- **PowerShell**: Required for running Spec-Kit scripts

## Core Workflow

### 1. Specify: Create Specification from Jira

**Command**: `/speckit.specify from-jira XY-123`

**What it does**:
- Retrieves the Jira issue (story, task, or bug)
- Imports issue details (summary, description, acceptance criteria)
- Checks if the issue belongs to an Epic for proper organization
- Creates a comprehensive specification document
- Names and organizes the spec according to Jira structure

**Output**:
- Spec folder: `specs/XY-123-issue-title/` (or `specs/EPIC-KEY/XY-123-issue-title/` if part of an Epic)
- Complete specification with requirements, user stories, and technical details
- Properly structured for development handoff

**Alternative syntaxes**:
```powershell
/speckit.specify jira:XY-123
/speckit.specify XY-123
```

### 2. Clarify: Validate Against Prototype

**Command**: `/speckit.clarify XY-123`

**What it does**:
- Analyzes the prototype to understand existing patterns and structures
- Compares the specification against prototype implementation
- Identifies gaps, inconsistencies, or missing elements
- Creates Dutch-to-English translation mapping for development
- Generates clarification report with actionable findings
- Posts results back to the original Jira issue as a comment

**Output**:
- Updated specification with prototype reference section
- Dutch-English translation table for developers
- Gap analysis and recommendations
- Jira comment with summary of findings and next steps

### 3. Plan: Development Strategy

**Command**: `/speckit.plan XY-123`

**What it does**:
- Creates implementation roadmap based on clarified specification
- Ensures adherence to prototype design patterns
- Plans feature implementation to match existing prototype structure
- Considers Dutch naming conventions and English code requirements

**Output**:
- Development plan with clear phases
- Technical approach aligned with prototype
- Resource and timeline estimates

### 4. Tasks: Break Down Work

**Command**: `/speckit.tasks XY-123`

**What it does**:
- Converts the plan into actionable development tasks
- Creates detailed task list with clear acceptance criteria
- Ensures each task maintains prototype consistency
- Provides implementation guidance for Dutch-English translation

**Output**:
- Detailed task breakdown
- Clear acceptance criteria for each task
- Implementation notes referencing prototype patterns

### 5. Implement: Execute Development

**Command**: `/speckit.implement XY-123`

**What it does**:
- Guides implementation of the planned tasks
- Ensures code matches prototype design exactly (unless overruled by spec)
- Enforces English naming in production code
- Maintains consistency with existing codebase patterns

**Output**:
- Production-ready code implementation
- Code that visually matches the prototype
- Proper English naming conventions
- Integration with existing project structure

## Key Features

### Jira Integration
- **Automatic Import**: Pull requirements directly from Jira issues
- **Epic Organization**: Specs organized by Epic when applicable
- **Feedback Loop**: Clarification results posted back to Jira
- **Traceability**: Clear connection between specs and Jira issues

### Prototype Alignment
- **Visual Consistency**: Implementation must match prototype appearance
- **Pattern Reuse**: Leverage existing prototype components and patterns
- **Gap Detection**: Identify missing elements in specifications
- **Design Validation**: Ensure specifications reflect actual prototype behavior

### Dutch-English Translation
- **Business Language**: Dutch names preserved in UI and documentation
- **Code Language**: English names required in all production code
- **Translation Mapping**: Automatic generation of name translation tables
- **Consistency**: Standardized translation patterns across the project

### Epic-Based Organization
- **Logical Grouping**: Specs organized under Epic folders when applicable
- **Hierarchical Structure**: `specs/EPIC-KEY/ISSUE-KEY/` for related work
- **Standalone Support**: `specs/ISSUE-KEY/` for non-Epic issues
- **Clear Navigation**: Easy to find related specifications

## Example Workflow

```powershell
# 1. Start with a Jira issue
/speckit.specify from-jira XY-145

# 2. Validate against prototype and post to Jira
/speckit.clarify XY-145

# 3. Create implementation plan
/speckit.plan XY-145

# 4. Break down into tasks
/speckit.tasks XY-145

# 5. Implement the feature
/speckit.implement XY-145
```

This creates:
- `specs/XY-100-beheermodule/XY-145-gebruikersbeheer/` (if XY-145 belongs to Epic XY-100)
- Complete specification validated against prototype
- Jira comment with clarification results
- Implementation plan and tasks
- Production code matching prototype design with English naming

## File Structure

```
.specify/
 README.md                    # This workflow guide
 CUSTOMIZATIONS.md            # Technical customization details
 memory/
    constitution.md         # Project governance principles
 scripts/powershell/
    get-jira-feature.ps1   # Jira validation and Epic handling
    compare-with-prototype.ps1  # Prototype analysis
 templates/                  # Spec-Kit templates

specs/
 XY-100-beheermodule/        # Epic folder
    XY-145-gebruikersbeheer/    # Issue spec
 XY-200-standalone-feature/  # Standalone issue spec
```

## Best Practices

1. **Always start with Jira**: Use `/speckit.specify from-jira XY-###` to ensure traceability
2. **Include ticket number in all steps**: Each workflow command requires the Jira ticket number (XY-###)
3. **Run clarify immediately**: Validate against prototype before planning
4. **Check Jira comments**: Review clarification feedback posted to the issue
5. **Follow Epic structure**: Organize related specs under Epic folders
6. **Respect prototype design**: Implementation should visually match prototype
7. **Use English in code**: Production code must use English naming conventions
8. **Preserve Dutch context**: Keep Dutch names in UI text and folder names

## Troubleshooting

- **Jira connection issues**: Check Atlassian MCP configuration
- **Epic not detected**: Verify issue has Epic link in Jira
- **Prototype comparison fails**: Ensure prototype directory is accessible
- **Translation mapping empty**: Check for Dutch text patterns in prototype files

For technical details about customizations, see `CUSTOMIZATIONS.md`.
