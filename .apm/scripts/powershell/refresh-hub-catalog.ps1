#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Generates the hub-catalog.yaml index from canonical agent and workflow metadata.

.DESCRIPTION
    Scans .apm/agents/*.md (YAML frontmatter) and .apm/workflows/*.yml + *.md
    to produce a machine-readable catalog index at .apm/contexts/hub-catalog.yaml.

    The hub-orchestrator agent reads this catalog for fast intent classification.
    New agents or workflows added to .apm/ are automatically discovered on the
    next run. Hooked into project-copilot.ps1 for automatic refresh.

.EXAMPLE
    .\.apm\scripts\powershell\refresh-hub-catalog.ps1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path

$agentsDir    = Join-Path $repoRoot '.apm/agents'
$workflowsDir = Join-Path $repoRoot '.apm/workflows'
$outputFile   = Join-Path $repoRoot '.apm/contexts/hub-catalog.yaml'

# ── Helper: extract YAML frontmatter from a markdown file ──────────────

function Get-YamlFrontmatter {
    param([string]$Path)

    $lines = Get-Content $Path -Encoding utf8
    $result = @{}

    if ($lines.Count -lt 2 -or $lines[0].Trim() -ne '---') {
        return $result
    }

    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Trim() -eq '---') { break }

        $line = $lines[$i]
        if ($line -match '^\s*(\w[\w-]*):\s*(.+)$') {
            $key   = $Matches[1]
            $value = $Matches[2].Trim().Trim("'").Trim('"')
            $result[$key] = $value
        }
    }

    return $result
}

# ── Helper: extract "When to use" bullets from workflow .md companion ──

function Get-WhenToUse {
    param([string]$Path)

    if (-not (Test-Path $Path)) { return @() }

    $lines   = Get-Content $Path -Encoding utf8
    $bullets = @()
    $inSection = $false

    foreach ($line in $lines) {
        if ($line -match '^##\s+When to use') {
            $inSection = $true
            continue
        }
        if ($inSection -and $line -match '^##\s') {
            break
        }
        if ($inSection -and $line -match '^\s*-\s+(.+)$') {
            $bullets += $Matches[1].Trim()
        }
    }

    return $bullets
}

# ── Helper: count stations in a workflow YAML ──────────────────────────

function Get-StationCount {
    param([string]$Path)

    $count = 0
    $lines = Get-Content $Path -Encoding utf8
    foreach ($line in $lines) {
        if ($line -match '^\s+-\s+id:\s+') { $count++ }
    }
    return $count
}

# ── Helper: extract top-level scalar field from YAML ───────────────────

function Get-YamlField {
    param([string]$Path, [string]$Field)

    $lines = Get-Content $Path -Encoding utf8
    foreach ($line in $lines) {
        if ($line -match "^${Field}:\s+(.+)$") {
            return $Matches[1].Trim().Trim("'").Trim('"')
        }
    }
    return $null
}

# ── Helper: escape a YAML string value ─────────────────────────────────

function Format-YamlString {
    param([string]$Value)

    if ($Value -match '[:#\[\]{}&*!|>''"%@`]' -or $Value -match '^\s' -or $Value -match '\s$') {
        $escaped = $Value -replace "'", "''"
        return "'$escaped'"
    }
    return $Value
}

# ── Build agent catalog ────────────────────────────────────────────────

$agentEntries = @()

if (Test-Path $agentsDir) {
    $agentFiles = Get-ChildItem $agentsDir -Filter '*.md' | Where-Object { $_.Name -ne '_schema.md' } | Sort-Object Name
    foreach ($file in $agentFiles) {
        $fm = Get-YamlFrontmatter $file.FullName
        if (-not $fm['name']) { continue }

        $entry = "  - name: $(Format-YamlString $fm['name'])`n"
        $entry += "    description: $(Format-YamlString $(if ($fm['description']) { $fm['description'] } else { '' }))`n"

        # Parse tools array
        if ($fm['tools']) {
            $toolsRaw = $fm['tools'] -replace '[\[\]]', ''
            $tools = @(($toolsRaw -split ',') | ForEach-Object { $_.Trim().Trim("'").Trim('"') } | Where-Object { $_ })
            if ($tools.Count -gt 0) {
                $entry += "    tools: [$($tools -join ', ')]`n"
            } else {
                $entry += "    tools: []`n"
            }
        } else {
            $entry += "    tools: []`n"
        }

        $agentEntries += $entry
    }
}

# ── Build workflow catalog ─────────────────────────────────────────────

$workflowEntries = @()

if (Test-Path $workflowsDir) {
    $ymlFiles = Get-ChildItem $workflowsDir -Filter '*.yml' | Where-Object { $_.Name -ne '_schema.yml' } | Sort-Object Name
    foreach ($file in $ymlFiles) {
        $name        = Get-YamlField $file.FullName 'name'
        $description = Get-YamlField $file.FullName 'description'
        $type        = Get-YamlField $file.FullName 'type'
        $stations    = Get-StationCount $file.FullName

        if (-not $name) { continue }

        $entry = "  - name: $(Format-YamlString $name)`n"
        $entry += "    description: $(Format-YamlString $(if ($description) { $description } else { '' }))`n"
        $entry += "    type: $(if ($type) { $type } else { 'delivery' })`n"
        $entry += "    stations: $stations`n"

        # Extract "When to use" from companion .md
        $mdPath  = Join-Path $workflowsDir ($file.BaseName + '.md')
        $bullets = Get-WhenToUse $mdPath
        if ($bullets.Count -gt 0) {
            $entry += "    when_to_use:`n"
            foreach ($b in $bullets) {
                $entry += "      - $(Format-YamlString $b)`n"
            }
        }

        $workflowEntries += $entry
    }
}

# ── Write hub-catalog.yaml ─────────────────────────────────────────────

$timestamp = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')

$output = @"
# Hub Catalog — Auto-generated by refresh-hub-catalog.ps1
# Do not edit manually. Re-run the script to refresh.
# Generated: $timestamp

workflows:
$($workflowEntries -join "`n")
agents:
$($agentEntries -join "`n")
"@

$outputDir = Split-Path $outputFile -Parent
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Set-Content -Path $outputFile -Value $output -Encoding utf8 -NoNewline
Write-Host "  CATALOG  $($ymlFiles.Count) workflows + $($agentFiles.Count) agents -> $outputFile"
