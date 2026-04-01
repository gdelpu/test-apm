#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Projects GitHub Copilot runtime files from the provider adapter layer
    into the .github/ runtime folder that VS Code discovers.

.DESCRIPTION
    Source of truth: providers/github-copilot/{agents,prompts,instructions}
    Runtime target:  .github/{agents,prompts,instructions}

    This script copies files from the provider layer into .github/ so Copilot
    can discover them at runtime.  Run it after adding/removing/editing any
    Copilot asset, or call it from CI to keep the projection in sync.

    .github/copilot-instructions.md is NOT managed by this script — it lives
    directly in .github/ as the hub context file.

.PARAMETER Clean
    Remove the target directories before copying (default: $false).
    Useful to ensure deleted source files are also removed from the projection.

.EXAMPLE
    .\.apm\scripts\powershell\project-copilot.ps1
    .\.apm\scripts\powershell\project-copilot.ps1 -Clean
#>
param(
    [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve repo root
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path

$sourcePath = Join-Path $repoRoot 'providers/github-copilot'
$targetPath = Join-Path $repoRoot '.github'

$assetTypes = @('agents', 'prompts', 'instructions')

foreach ($type in $assetTypes) {
    $src = Join-Path $sourcePath $type
    $dst = Join-Path $targetPath $type

    if (-not (Test-Path $src)) {
        Write-Host "  SKIP  $type — source folder not found ($src)"
        continue
    }

    if ($Clean -and (Test-Path $dst)) {
        Remove-Item $dst -Recurse -Force
        Write-Host "  CLEAN $dst"
    }

    if (-not (Test-Path $dst)) {
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
    }

    $files = Get-ChildItem $src -File
    $count = 0
    foreach ($file in $files) {
        Copy-Item $file.FullName -Destination $dst -Force
        $count++
    }
    Write-Host "  COPY  $type — $count files -> $dst"
}

Write-Host "`nProjection complete. Copilot will discover assets in .github/."
