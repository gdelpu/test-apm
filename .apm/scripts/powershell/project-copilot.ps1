#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Projects provider runtime files from the adapter layer into the runtime
    folder that the target tool discovers (e.g. .github/ for GitHub Copilot).

.DESCRIPTION
    Provider-agnostic projection script.  Reads apm.yml at the repo root to
    resolve the adapter (source) and runtime (target) paths for the selected
    provider, then copies all asset-type subdirectories from source to target.

    When -Full is specified the script additionally copies canonical content
    (.apm/skills, .apm/workflows, .apm/contexts, .apm/templates, .apm/knowledge/)
    into the runtime tree and rewrites .apm/ path references
    inside every .md file so they point to their new runtime locations.

    After the main provider copy, files under providers-local/ (if it exists)
    are overlaid on top, allowing per-repo overrides without editing upstream.

    .github/copilot-instructions.md is NOT managed by this script -- it lives
    directly in .github/ as the hub context file.

.PARAMETER Clean
    Remove the target directories before copying (default: $false).
    Useful to ensure deleted source files are also removed from the projection.

.PARAMETER Full
    Additionally copy canonical content (.apm/skills, .apm/workflows, etc.)
    into the runtime tree and rewrite path references in .md files.

.PARAMETER Provider
    Provider key as defined in apm.yml (default: github-copilot).

.EXAMPLE
    .\.apm\scripts\powershell\project-copilot.ps1
    .\.apm\scripts\powershell\project-copilot.ps1 -Clean
    .\.apm\scripts\powershell\project-copilot.ps1 -Full -Provider github-copilot
#>
param(
    [switch]$Clean,
    [switch]$Full,
    [string]$Provider = 'github-copilot'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Resolve repo root ─────────────────────────────────────────────────
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path

# ── Parse apm.yml for provider config ─────────────────────────────────
$apmFile = Join-Path $repoRoot 'apm.yml'
if (-not (Test-Path $apmFile)) {
    Write-Error "apm.yml not found at $apmFile"
    exit 1
}

$apmLines = Get-Content $apmFile -Encoding UTF8

# Find the providers: section, then the specific provider block and its keys
$adapterValue = $null
$runtimeValue = $null
$inProviders = $false
$inTarget = $false

foreach ($line in $apmLines) {
    # Detect top-level 'providers:' key
    if ($line -match '^providers:\s*$') {
        $inProviders = $true
        continue
    }
    # Once inside providers, a non-indented line ends the section
    if ($inProviders -and $line -match '^\S' -and $line -notmatch '^providers:') {
        $inProviders = $false
        $inTarget = $false
        continue
    }
    if (-not $inProviders) { continue }

    # Detect provider sub-key (2-space indent)
    if ($line -match "^  ${Provider}:\s*$") {
        $inTarget = $true
        continue
    }
    # Another provider sub-key at 2-space indent ends our block
    if ($inTarget -and $line -match '^\s{2}\S' -and $line -notmatch "^  ${Provider}:") {
        break
    }
    if (-not $inTarget) { continue }

    # Extract adapter and runtime (4-space indent)
    if ($line -match '^\s{4}adapter:\s*(.+)$')  { $adapterValue = $Matches[1].Trim() }
    if ($line -match '^\s{4}runtime:\s*(.+)$')   { $runtimeValue = $Matches[1].Trim() }
}

if (-not $adapterValue) {
    Write-Error "Provider '$Provider' not found in apm.yml or has no adapter key."
    exit 1
}

$sourcePath = Join-Path $repoRoot $adapterValue
$targetPath = if ($runtimeValue) { Join-Path $repoRoot $runtimeValue } else { $sourcePath }

Write-Host "  PROVIDER  $Provider -- adapter: $adapterValue, runtime: $(if ($runtimeValue) { $runtimeValue } else { $adapterValue })"

# ── Discover asset types from source directory ─────────────────────────
if (-not (Test-Path $sourcePath)) {
    Write-Error "Source path not found: $sourcePath"
    exit 1
}

$assetTypes = (Get-ChildItem $sourcePath -Directory).Name

# ── Copy provider adapter files ────────────────────────────────────────
foreach ($type in $assetTypes) {
    $src = Join-Path $sourcePath $type
    $dst = Join-Path $targetPath $type

    if (-not (Test-Path $src)) {
        Write-Host "  SKIP  $type -- source folder not found ($src)"
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
    Write-Host "  COPY  $type -- $count files -> $dst"
}

# ── providers-local/ overlay ───────────────────────────────────────────
$localOverlay = Join-Path $repoRoot "providers-local/$Provider"
if (Test-Path $localOverlay) {
    $localDirs = Get-ChildItem $localOverlay -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $localDirs) {
        $dst = Join-Path $targetPath $dir.Name
        if (-not (Test-Path $dst)) {
            New-Item -ItemType Directory -Path $dst -Force | Out-Null
        }
        $files = Get-ChildItem $dir.FullName -File -Recurse
        $count = 0
        foreach ($file in $files) {
            $relativePath = $file.FullName.Substring($dir.FullName.Length + 1)
            $destFile = Join-Path $dst $relativePath
            $destDir = Split-Path $destFile -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item $file.FullName -Destination $destFile -Force
            $count++
        }
        Write-Host "  OVERLAY   $($dir.Name) -- $count files from providers-local/"
    }
}

# ── -Full: canonical content copy ──────────────────────────────────────
if ($Full) {
    $canonicalMappings = @(
        @{ Source = '.apm/skills';     Target = 'skills' }
        @{ Source = '.apm/workflows';  Target = 'workflows' }
        @{ Source = '.apm/contexts';   Target = 'contexts' }
        @{ Source = '.apm/templates';  Target = 'templates' }
        @{ Source = '.apm/knowledge';   Target = 'knowledge' }
        @{ Source = '.apm/hooks';        Target = 'hooks' }
    )

    foreach ($mapping in $canonicalMappings) {
        $src = Join-Path $repoRoot $mapping.Source
        $dst = Join-Path $targetPath $mapping.Target

        if (-not (Test-Path $src)) {
            Write-Host "  SKIP  $($mapping.Target) -- source folder not found ($src)"
            continue
        }

        if ($Clean -and (Test-Path $dst)) {
            Remove-Item $dst -Recurse -Force
            Write-Host "  CLEAN $dst"
        }

        Copy-Item $src -Destination $dst -Recurse -Force

        $count = @(Get-ChildItem $dst -File -Recurse).Count
        Write-Host "  FULL-COPY $($mapping.Target) -- $count files -> $dst"
    }

    # ── -Full: path rewrites in .md files ──────────────────────────────
    $runtimePrefix = if ($runtimeValue) { $runtimeValue } else { $adapterValue }

    # Build ordered rewrite pairs (more specific first); comma prefix prevents array flattening
    $rewritePairs = @(
        ,@('.apm/skills/',        "$runtimePrefix/skills/")
        ,@('.apm/workflows/',     "$runtimePrefix/workflows/")
        ,@('.apm/contexts/',      "$runtimePrefix/contexts/")
        ,@('.apm/templates/',     "$runtimePrefix/templates/")
        ,@('.apm/prompts/',       "$runtimePrefix/prompts/")
        ,@('.apm/instructions/',  "$runtimePrefix/instructions/")
        ,@('.apm/knowledge/',      "$runtimePrefix/knowledge/")
        ,@('.apm/hooks/',          "$runtimePrefix/hooks/")
        ,@('.apm/hooks',           "$runtimePrefix/hooks")
    )

    # Only rewrite .apm/agents/ if the runtime is different from the source
    if ($runtimePrefix -ne $adapterValue) {
        $rewritePairs += ,@('.apm/agents/', "$runtimePrefix/agents/")
    }

    # Provider-specific rewrites
    if ($Provider -eq 'github-copilot') {
        $rewritePairs += ,@('providers/github-copilot', $runtimePrefix)
    }

    $mdFiles = Get-ChildItem $targetPath -Filter '*.md' -Recurse -File
    $rewriteCount = 0

    foreach ($mdFile in $mdFiles) {
        $content = Get-Content $mdFile.FullName -Raw -Encoding UTF8
        $original = $content

        foreach ($pair in $rewritePairs) {
            $oldPath = $pair[0]
            $newPath = $pair[1]

            # Skip if old and new are identical
            if ($oldPath -eq $newPath) { continue }

            # Replace forward-slash variant
            $content = $content.Replace($oldPath, $newPath)

            # Replace backslash variant
            $oldBackslash = $oldPath.Replace('/', '\')
            $newBackslash = $newPath.Replace('/', '\')
            if ($oldBackslash -ne $oldPath) {
                $content = $content.Replace($oldBackslash, $newBackslash)
            }
        }

        if ($content -ne $original) {
            Set-Content -Path $mdFile.FullName -Value $content -NoNewline -Encoding UTF8
            $rewriteCount++
        }
    }

    Write-Host "  REWRITE   $rewriteCount files updated with runtime path references"
}

# ── Refresh hub catalog ────────────────────────────────────────────────

# ── Config-driven placeholder substitution ─────────────────────────────
# Read provider config.yml (with providers-local/ override) and substitute
# {{KEY}} placeholders in all projected .md files.
$configFile = Join-Path $repoRoot "providers-local/$Provider/config.yml"
if (-not (Test-Path $configFile)) {
    $configFile = Join-Path $sourcePath 'config.yml'
}
if (Test-Path $configFile) {
    $configLines  = Get-Content $configFile -Encoding UTF8
    $configValues = @{}
    $inDefaults   = $false

    foreach ($line in $configLines) {
        if ($line -match '^\s*defaults:\s*$') { $inDefaults = $true; continue }
        if ($inDefaults -and $line -match '^\S') { $inDefaults = $false }
        if ($inDefaults -and $line -match '^\s+(\w+):\s*"?(.+?)"?\s*$') {
            $key   = $Matches[1].ToUpper()
            $value = $Matches[2]
            $configValues["{{DEFAULT_$key}}"] = $value
        }
    }

    if ($configValues.Count -gt 0) {
        $mdFiles = Get-ChildItem $targetPath -Filter '*.md' -Recurse -File
        $substCount = 0
        foreach ($mdFile in $mdFiles) {
            $content  = Get-Content $mdFile.FullName -Raw -Encoding UTF8
            $original = $content
            foreach ($entry in $configValues.GetEnumerator()) {
                $content = $content.Replace($entry.Key, $entry.Value)
            }
            if ($content -ne $original) {
                Set-Content -Path $mdFile.FullName -Value $content -NoNewline -Encoding UTF8
                $substCount++
            }
        }
        Write-Host "  CONFIG  $substCount files updated with provider config substitutions ($($configValues.Count) keys)"
    }
} else {
    Write-Host "  SKIP  config -- no provider config.yml found"
}

# ── Refresh hub catalog ────────────────────────────────────────────────

$catalogScript = Join-Path $PSScriptRoot 'refresh-hub-catalog.ps1'
if (Test-Path $catalogScript) {
    Write-Host ""
    & $catalogScript
} else {
    Write-Host "`n  SKIP  hub-catalog -- refresh-hub-catalog.ps1 not found"
}

Write-Host "`nProjection complete. Runtime assets written to $targetPath."

# ── Parity check: canonical agents vs provider agents ─────────────────
$canonicalAgentDir = Join-Path $repoRoot '.apm/agents'
$providerAgentDir  = Join-Path $repoRoot "$adapterValue/agents"
if ((Test-Path $canonicalAgentDir) -and (Test-Path $providerAgentDir)) {
    $canonicalNames = (Get-ChildItem $canonicalAgentDir -Filter '*.md').BaseName
    $providerNames  = (Get-ChildItem $providerAgentDir -Filter '*.agent.md').BaseName | ForEach-Object { $_ -replace '\.agent$', '' }
    $missing = $canonicalNames | Where-Object { $_ -notin $providerNames }
    if ($missing) {
        Write-Host ""
        Write-Host "  ⚠️  PARITY WARNING -- canonical agents without provider projection:" -ForegroundColor Yellow
        foreach ($m in $missing) {
            Write-Host "      - $m  ->  add $adapterValue/agents/$m.agent.md" -ForegroundColor Yellow
        }
        Write-Host "  Run: python scripts/validate_copilot_assets.py  to confirm." -ForegroundColor Yellow
    }
}
