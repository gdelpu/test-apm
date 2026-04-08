<#
.SYNOPSIS
    APM Bundle Installer (Windows)

.DESCRIPTION
    Downloads and installs an APM bundle from the GitLab Generic Package Registry.

.PARAMETER Version
    Semantic version to install (required). Example: 1.2.0

.PARAMETER Target
    Target bundle: copilot, claude, all (default: all)

.PARAMETER Destination
    Destination directory (default: .\.apm-dist)

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
    .\install-apm-bundle.ps1 -Version 2.0.0 -Target copilot -ProjectId 12345

.EXAMPLE
    .\install-apm-bundle.ps1 -Version 1.0.0 `
        -RegistryUrl https://gitlab.example.com/api/v4/projects/42/packages/generic
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [ValidateSet('copilot', 'claude', 'all')]
    [string]$Target = 'all',

    [string]$Destination = '.\.apm-dist',

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

# --- Strip leading 'v' ---
$Version = $Version -replace '^v', ''

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

# --- Summary ---
Write-Step 'Installation Complete'
Write-Ok "$PackageName v$Version ($Target) installed to $Destination"
Get-ChildItem -Path $Destination | Format-Table Name, Length, LastWriteTime -AutoSize
