<#
.SYNOPSIS
    APM Bundle Installer (Windows)

.DESCRIPTION
    Downloads and installs an APM bundle from the GitLab Generic Package Registry.
    Supports two install modes:
      - standard   — projects runtime-only files (e.g. .github/) for consumers.
      - expandable — extracts full source and scaffolds providers-local/ for
                     customisation.

.PARAMETER Version
    Semantic version to install (required). Example: 1.2.0

.PARAMETER Target
    Target bundle: copilot, claude, all (default: copilot)

.PARAMETER Destination
    Destination directory (default: .\.apm-dist)

.PARAMETER Mode
    Install mode: standard (runtime projection only) or expandable (full source
    with local override scaffolding). Default: standard.

.PARAMETER Provider
    Provider adapter key as defined in apm.yml. Default: github-copilot.

.PARAMETER RegistryUrl
    Full Generic Package Registry URL.
    Alternative: provide ProjectId + GitLabUrl.

.PARAMETER ProjectId
    GitLab project ID (used to construct registry URL).

.PARAMETER GitLabUrl
    GitLab instance base URL (default: https://gitlab.com).

.PARAMETER Token
    Private or job token for authentication.
    Falls back to $env:GITLAB_TOKEN.

.PARAMETER NoVerify
    Skip SHA-256 checksum verification.

.EXAMPLE
    .\install-apm-bundle.ps1 -Version 1.2.0 -ProjectId 12345 -Token $env:GITLAB_TOKEN

.EXAMPLE
    .\install-apm-bundle.ps1 -Version 2.0.0 -Target copilot -Mode expandable -ProjectId 12345

.EXAMPLE
    .\install-apm-bundle.ps1 -Version 1.0.0 `
        -RegistryUrl https://gitlab.example.com/api/v4/projects/42/packages/generic
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [ValidateSet('copilot', 'claude', 'all')]
    [string]$Target = 'copilot',

    [string]$Destination = '.\.apm-dist',

    [ValidateSet('standard', 'expandable')]
    [string]$Mode = 'standard',

    [string]$Provider = 'github-copilot',

    [string]$RegistryUrl = $env:APM_REGISTRY_URL,

    [string]$ProjectId = $env:APM_PROJECT_ID,

    [string]$GitLabUrl = $(if ($env:APM_GITLAB_URL) { $env:APM_GITLAB_URL } else { 'https://gitlab.com' }),

    [string]$Token = $env:GITLAB_TOKEN,

    [switch]$NoVerify
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$PackageName = 'ssg-ai-backbone'

# --- Helpers ---
function Write-Step  { param([string]$msg) Write-Host "`n── $msg ──" -ForegroundColor Cyan }
function Write-Ok    { param([string]$msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Info  { param([string]$msg) Write-Host "ℹ️  $msg" }
function Write-Err   { param([string]$msg) Write-Host "❌ $msg" -ForegroundColor Red }

# --- Dot-source lock file helper ---
. (Join-Path $PSScriptRoot 'lib/apm-lock.ps1')

# --- Strip leading 'v' ---
$Version = $Version -replace '^v', ''

# --- Initialise checksum (may be set later by verification step) ---
$actualHash = ''

# --- Validate semver ---
if ($Version -notmatch '^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$') {
    Write-Err "Invalid semver: '$Version'"
    exit 1
}

# --- Resolve registry URL ---
if (-not $RegistryUrl) {
    if (-not $ProjectId) {
        Write-Err 'Provide -RegistryUrl or -ProjectId'
        exit 1
    }
    $RegistryUrl = "$GitLabUrl/api/v4/projects/$ProjectId/packages/generic"
}

# --- Prepare headers ---
$headers = @{}
if ($Token) {
    $headers['PRIVATE-TOKEN'] = $Token
}

# --- Prepare destination ---
Write-Step "Installing $PackageName v$Version (target: $Target)"
New-Item -ItemType Directory -Path $Destination -Force | Out-Null

$BaseUrl = "$RegistryUrl/$PackageName/$Version"
$ArchiveName = "$PackageName-$Target.tar.gz"
$DownloadUrl = "$BaseUrl/$ArchiveName"
$ArchivePath = Join-Path $Destination $ArchiveName

# --- Download ---
Write-Info "Downloading: $ArchiveName"
try {
    Invoke-WebRequest -Uri $DownloadUrl -Headers $headers -OutFile $ArchivePath -UseBasicParsing
    Write-Ok "Downloaded: $ArchiveName"
}
catch {
    Write-Err "Download failed: $DownloadUrl"
    Write-Err $_.Exception.Message
    exit 1
}

# --- Verify checksum ---
if (-not $NoVerify) {
    Write-Info 'Downloading checksums'
    $ChecksumUrl = "$BaseUrl/SHA256SUMS"
    $ChecksumPath = Join-Path $Destination 'SHA256SUMS'

    try {
        Invoke-WebRequest -Uri $ChecksumUrl -Headers $headers -OutFile $ChecksumPath -UseBasicParsing
        $checksumLine = Get-Content $ChecksumPath | Where-Object { $_ -match [regex]::Escape($ArchiveName) }
        if ($checksumLine) {
            $expectedHash = ($checksumLine -split '\s+')[0]
            $actualHash = (Get-FileHash -Path $ArchivePath -Algorithm SHA256).Hash.ToLower()
            if ($actualHash -eq $expectedHash) {
                Write-Ok 'Checksum verified'
            }
            else {
                Write-Err "Checksum mismatch: expected $expectedHash, got $actualHash"
                exit 1
            }
        }
        else {
            Write-Info "No checksum entry for $ArchiveName — skipping"
        }
    }
    catch {
        Write-Info 'Checksums not available — skipping verification'
    }
}

# --- Extract ---
Write-Step "Extracting to $Destination"
tar -xzf $ArchivePath -C $Destination
Write-Ok "Extracted: $ArchiveName"

# --- Check for existing lock file ---
$existingLock = Read-ApmLock -Path $Destination
if ($existingLock) {
    Write-Info "Existing install detected: v$($existingLock['version']) ($($existingLock['mode']) mode)"
}

# --- Helper: parse runtime path from apm.yml in extracted content ---
function Get-ApmRuntime {
    param([string]$ApmRoot, [string]$ProviderKey)
    $apmCfg = Join-Path $ApmRoot 'apm.yml'
    if (-not (Test-Path $apmCfg)) { return $null }
    $lines = Get-Content $apmCfg -Encoding UTF8
    $inProviders = $false
    $inTarget = $false
    foreach ($l in $lines) {
        if ($l -match '^providers:\s*$')                                   { $inProviders = $true; continue }
        if ($inProviders -and $l -match '^\S' -and $l -notmatch '^providers:') { $inProviders = $false; $inTarget = $false; continue }
        if (-not $inProviders) { continue }
        if ($l -match "^  ${ProviderKey}:\s*$")                             { $inTarget = $true; continue }
        if ($inTarget -and $l -match '^\s{2}\S' -and $l -notmatch "^  ${ProviderKey}:") { break }
        if (-not $inTarget) { continue }
        if ($l -match '^\s{4}runtime:\s*(.+)$') { return $Matches[1].Trim() }
    }
    return $null
}

# --- Install mode logic ---
Write-Step "Applying install mode: $Mode"

if ($Mode -eq 'standard') {
    # ── Standard mode: project runtime-only files ──────────────────────

    # If updating, remove old runtime directory
    if ($existingLock) {
        $oldRuntime = Get-ApmRuntime -ApmRoot $Destination -ProviderKey $Provider
        if ($oldRuntime) {
            $oldRuntimePath = Join-Path $Destination $oldRuntime
            if (Test-Path $oldRuntimePath) {
                Remove-Item $oldRuntimePath -Recurse -Force
                Write-Info "Removed previous runtime directory: $oldRuntime"
            }
        }
    }

    # Create temp working directory alongside destination
    $tempDir = Join-Path (Split-Path $Destination -Parent) ".apm-install-tmp-$(Get-Date -Format 'yyyyMMddHHmmss')"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    Write-Info "Temp working directory: $tempDir"

    try {
        # Move extracted content to temp dir
        Get-ChildItem -Path $Destination -Force | Where-Object { $_.FullName -ne (Resolve-Path $ArchivePath -ErrorAction SilentlyContinue).Path } | ForEach-Object {
            $destItem = Join-Path $tempDir $_.Name
            Move-Item $_.FullName -Destination $destItem -Force
        }

        # Locate and run projection script
        $projectionScript = Join-Path $tempDir '.apm/scripts/powershell/project-copilot.ps1'
        if (-not (Test-Path $projectionScript)) {
            Write-Err "Projection script not found at $projectionScript"
            exit 1
        }

        Write-Info "Running projection (-Full -Clean) from extracted content"
        & $projectionScript -Provider $Provider -Full -Clean

        # Resolve runtime path from apm.yml
        $runtimeDir = Get-ApmRuntime -ApmRoot $tempDir -ProviderKey $Provider
        if (-not $runtimeDir) {
            Write-Err "Could not resolve runtime path for provider '$Provider' from apm.yml"
            exit 1
        }
        Write-Info "Runtime directory: $runtimeDir"

        $runtimeSrc = Join-Path $tempDir $runtimeDir
        if (-not (Test-Path $runtimeSrc)) {
            Write-Err "Projected runtime directory not found: $runtimeSrc"
            exit 1
        }

        # Copy runtime directory to destination
        $runtimeDst = Join-Path $Destination $runtimeDir
        Copy-Item $runtimeSrc -Destination $runtimeDst -Recurse -Force
        Write-Ok "Copied runtime: $runtimeDir"

        # Write lock file
        Write-ApmLock -Path $Destination -Version $Version -Mode 'standard' -Provider $Provider -Archive $ArchiveName -Checksum $actualHash
        Write-Ok 'Lock file written'
    }
    finally {
        # Clean up temp directory
        if (Test-Path $tempDir) {
            Remove-Item $tempDir -Recurse -Force
            Write-Info 'Cleaned up temp directory'
        }
    }
}
elseif ($Mode -eq 'expandable') {
    # ── Expandable mode: full source with local override scaffolding ───

    # If updating, preserve providers-local, remove upstream, re-extract, re-project
    if ($existingLock) {
        $providersLocalPath = Join-Path $Destination "providers-local"
        $savedLocalPath = $null

        if (Test-Path $providersLocalPath) {
            $savedLocalPath = Join-Path (Split-Path $Destination -Parent) ".apm-providers-local-bak-$(Get-Date -Format 'yyyyMMddHHmmss')"
            Move-Item $providersLocalPath -Destination $savedLocalPath -Force
            Write-Info "Preserved providers-local/ for update"
        }

        # Remove upstream content (keep archive)
        Get-ChildItem -Path $Destination -Force | Where-Object {
            $_.Name -ne $ArchiveName -and $_.Name -ne (Split-Path $ArchivePath -Leaf)
        } | ForEach-Object {
            Remove-Item $_.FullName -Recurse -Force
        }

        # Re-extract
        tar -xzf $ArchivePath -C $Destination
        Write-Info 'Re-extracted archive for update'

        # Restore providers-local
        if ($savedLocalPath -and (Test-Path $savedLocalPath)) {
            Move-Item $savedLocalPath -Destination $providersLocalPath -Force
            Write-Info 'Restored providers-local/'
        }
    }

    # Scaffold providers-local if it doesn't exist
    $localBase = Join-Path $Destination "providers-local/$Provider"
    $scaffoldDirs = @('agents', 'prompts', 'instructions')

    foreach ($dir in $scaffoldDirs) {
        $dirPath = Join-Path $localBase $dir
        if (-not (Test-Path $dirPath)) {
            New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        }
    }

    $readmePath = Join-Path $localBase 'README.md'
    if (-not (Test-Path $readmePath)) {
        $readmeContent = @"
# providers-local

Local overrides for the APM provider layer.

Files placed here will be overlaid on top of upstream provider assets during projection.
To override an upstream file, place a file with the same name in the matching subdirectory.

## Structure

``````
providers-local/<provider>/
  agents/       # Custom or overridden agent definitions
  prompts/      # Custom or overridden prompt definitions
  instructions/ # Custom or overridden instruction files
``````

## Re-projecting

After adding or modifying local files, re-run the projection script:

``````powershell
.\.apm\scripts\powershell\project-copilot.ps1 -Provider <provider> -Clean
``````

Or on Linux/macOS:

``````bash
./scripts/project-copilot.sh --provider <provider> --clean
``````
"@
        Set-Content -Path $readmePath -Value $readmeContent -Encoding UTF8
    }

    Write-Ok "Scaffolded providers-local/$Provider/"

    # Run projection (no -Full for expandable)
    $projectionScript = Join-Path $Destination '.apm/scripts/powershell/project-copilot.ps1'
    if (-not (Test-Path $projectionScript)) {
        Write-Err "Projection script not found at $projectionScript"
        exit 1
    }

    Write-Info 'Running projection (-Clean) for expandable mode'
    & $projectionScript -Provider $Provider -Clean

    # Write lock file
    Write-ApmLock -Path $Destination -Version $Version -Mode 'expandable' -Provider $Provider -Archive $ArchiveName -Checksum $actualHash
    Write-Ok 'Lock file written'

    # Generate .gitignore with runtime paths
    $runtimeDir = Get-ApmRuntime -ApmRoot $Destination -ProviderKey $Provider
    if ($runtimeDir) {
        $gitignorePath = Join-Path $Destination '.gitignore'
        $gitignoreContent = @"
# APM generated runtime content — do not edit manually
# Re-generated by project-copilot.ps1 during projection
$runtimeDir/agents/
$runtimeDir/prompts/
$runtimeDir/instructions/
"@
        Set-Content -Path $gitignorePath -Value $gitignoreContent -Encoding UTF8
        Write-Ok "Generated .gitignore for runtime directory: $runtimeDir"
    }
}

# --- Summary ---
Write-Step 'Installation Complete'
Write-Ok "$PackageName v$Version ($Target, $Mode mode) installed to $Destination"
Get-ChildItem -Path $Destination | Format-Table Name, Length, LastWriteTime -AutoSize
