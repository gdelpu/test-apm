#!/usr/bin/env pwsh
<#
.SYNOPSIS
Extract feature description from a Jira issue using Atlassian MCP

.DESCRIPTION
This script helps retrieve Jira issue data and format it for the specify workflow.
It outputs structured information that can be used by the AI agent.

.PARAMETER IssueKey
The Jira issue key (e.g., XY-123)

.PARAMETER CloudId
The Atlassian Cloud ID (optional, can be retrieved from environment or MCP)

.PARAMETER Json
Output in JSON format for agent consumption

.EXAMPLE
./get-jira-feature.ps1 -IssueKey XY-123 -Json

.NOTES
This script serves as a bridge between the specify workflow and Jira.
The actual MCP calls must be made by the AI agent with Atlassian MCP access.
This script validates the issue key format and outputs the request structure.
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$IssueKey,
    
    [Parameter(Mandatory=$false)]
    [string]$CloudId,
    
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Err {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Validate-IssueKey {
    param([string]$Key)
    # Jira key format: PROJECT-NUMBER (e.g., XY-123)
    # Project key: 1-10 uppercase letters, optionally followed by uppercase letters or numbers
    # Issue number: 1 or more digits
    if ($Key -match '^[A-Z][A-Z0-9]+-\d+$') {
        return $true
    }
    return $false
}

function Get-CloudIdFromEnvironment {
    # Check if CloudId is in environment variable
    if ($env:ATLASSIAN_CLOUD_ID) {
        return $env:ATLASSIAN_CLOUD_ID
    }
    return $null
}

# Validate issue key format
if (-not (Validate-IssueKey -Key $IssueKey)) {
    Write-Err "Invalid Jira issue key format: $IssueKey"
    Write-Host "Expected format: PROJECT-123 (e.g., XY-1, ABC-456)" -ForegroundColor Yellow
    Write-Host "  - Project key: 1-10 uppercase letters/numbers (must start with letter)" -ForegroundColor Yellow
    Write-Host "  - Hyphen: -" -ForegroundColor Yellow
    Write-Host "  - Issue number: one or more digits" -ForegroundColor Yellow
    exit 1
}

# Try to get CloudId
if (-not $CloudId) {
    $CloudId = Get-CloudIdFromEnvironment
}

# Output results
if ($Json) {
    $result = @{
        issueKey = $IssueKey
        cloudId = if ($CloudId) { $CloudId } else { "NEEDS_LOOKUP" }
        status = "READY_FOR_MCP_CALL"
        instructions = @(
            "Use mcp_atlassian_atl_getJiraIssue to retrieve issue details",
            "Use mcp_atlassian_atl_getJiraIssueRemoteIssueLinks for related Confluence pages",
            "Check if issue has parent Epic - if so, retrieve Epic details for folder organization",
            "Transform Jira data to feature description format",
            "Use issue key and summary for spec naming: XY-123-issue-title",
            "Organize spec in epic subfolder if Epic parent exists: specs/EPIC-KEY-epic-name/XY-123-issue-title/",
            "Continue with standard specify workflow"
        )
        mcpTools = @{
            getIssue = "mcp_atlassian_atl_getJiraIssue"
            getLinks = "mcp_atlassian_atl_getJiraIssueRemoteIssueLinks"
            searchJira = "mcp_atlassian_atl_search"
        }
        namingConvention = @{
            format = "ISSUE-KEY-issue-title"
            example = "XY-123-user-authentication"
            rules = @(
                "Use full issue key (e.g., XY-123)",
                "Append normalized issue summary (lowercase, hyphens)",
                "Keep original language (Dutch titles remain Dutch)",
                "Remove special characters except hyphens"
            )
        }
        folderOrganization = @{
            withEpic = "specs/EPIC-KEY-epic-name/ISSUE-KEY-issue-title/"
            withoutEpic = "specs/ISSUE-KEY-issue-title/"
            rule = "If issue has Epic parent, create subfolder under epic folder"
        }
    }
    $result | ConvertTo-Json -Depth 5
} else {
    Write-Info "Jira Issue Key: $IssueKey"
    if ($CloudId) {
        Write-Info "CloudId: $CloudId"
    } else {
        Write-Host "[WARN] CloudId not provided. Agent must look it up." -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Ready for MCP integration" -ForegroundColor Green
    Write-Host ""
    Write-Host "Agent workflow:" -ForegroundColor Cyan
    Write-Host "  1. Get CloudId (if not provided) using mcp_atlassian_atl_getAccessibleAtlassianResources" -ForegroundColor White
    Write-Host "  2. Call mcp_atlassian_atl_getJiraIssue(cloudId, '$IssueKey')" -ForegroundColor White
    Write-Host "  3. Check if issue has Epic parent field" -ForegroundColor White
    Write-Host "  4. If Epic exists, retrieve Epic details for folder name" -ForegroundColor White
    Write-Host "  5. Call mcp_atlassian_atl_getJiraIssueRemoteIssueLinks(cloudId, '$IssueKey')" -ForegroundColor White
    Write-Host "  6. Transform Jira data to feature description" -ForegroundColor White
    Write-Host "  7. Create spec folder: specs/[EPIC-KEY-name/]$IssueKey-issue-title/" -ForegroundColor White
    Write-Host "  8. Continue with standard specify workflow" -ForegroundColor White
    Write-Host ""
    Write-Host "Naming Convention:" -ForegroundColor Yellow
    Write-Host "  Format: ISSUE-KEY-issue-title (e.g., XY-123-gebruikersbeheer)" -ForegroundColor White
    Write-Host "  Keep original language (Dutch titles remain Dutch)" -ForegroundColor White
    Write-Host ""
    Write-Host "Folder Organization:" -ForegroundColor Yellow
    Write-Host "  With Epic: specs/XY-100-epic-name/XY-123-issue-title/" -ForegroundColor White
    Write-Host "  Without Epic: specs/XY-123-issue-title/" -ForegroundColor White
    Write-Host ""
    Write-Host "Tip: Set ATLASSIAN_CLOUD_ID environment variable to skip CloudId lookup" -ForegroundColor Yellow
}

exit 0
