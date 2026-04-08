<#
.SYNOPSIS
    One-liner APM bootstrap for consumer repos (Windows).

.DESCRIPTION
    THIS IS THE ONLY FILE YOU NEED TO DOWNLOAD.

    Downloads the multi-part installer and its dependencies into a hidden temp
    directory, runs the full install, then removes all temp files automatically.
    End result: .github/ (Copilot runtime) and .apm.lock.yaml — nothing else.

    Steps performed internally:
      1. Downloads scripts/install-apm-bundle.ps1  (the full installer)
      2. Downloads scripts/lib/apm-lock.ps1        (lock-file helper)
      3. Runs the installer against the chosen version + target
      4. Deletes the temp directory

.PARAMETER Version
    Semantic version to install (default: 0.0.1). Use "latest" to fetch the
    latest tag from the source project.

.PARAMETER ProjectId
    GitLab numeric project ID of the ai-sdlc-foundation source repo (required).

.PARAMETER GitLabUrl
    GitLab instance base URL (default: https://innersource.soprasteria.com).

.PARAMETER Token
    Private access token for authentication.
    Falls back to $env:GITLAB_TOKEN.

.PARAMETER Mode
    Install mode: standard (runtime projection only) or expandable
    (full source with local override support). Default: standard.

.PARAMETER Target
    Target bundle: copilot, claude, all (default: copilot).

.PARAMETER Ref
    Git ref to download installer scripts from (default: main).

.EXAMPLE
    # Minimal — relies on GITLAB_TOKEN env var
    .\bootstrap-apm.ps1 -ProjectId 12345

.EXAMPLE
    # Explicit version and token
    .\bootstrap-apm.ps1 -Version 0.0.1 -ProjectId 12345 -Token "glpat-xxx"

.EXAMPLE
    # Expandable mode for customization
    .\bootstrap-apm.ps1 -Version 0.0.1 -ProjectId 12345 -Mode expandable
#>
[CmdletBinding()]
param(
    [string]$Version = '0.0.1',

    [string]$ProjectId = '545119',

    [string]$GitLabUrl = $(if ($env:APM_GITLAB_URL) { $env:APM_GITLAB_URL } else { 'https://innersource.soprasteria.com' }),

    [string]$Token = $env:GITLAB_TOKEN,

    [ValidateSet('standard', 'expandable')]
    [string]$Mode = 'standard',

    [ValidateSet('copilot', 'claude', 'all')]
    [string]$Target = 'copilot',

    [string]$Ref = 'main'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Helpers ---
function Write-Step  { param([string]$msg) Write-Host "`n── $msg ──" -ForegroundColor Cyan }
function Write-Ok    { param([string]$msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Info  { param([string]$msg) Write-Host "ℹ️  $msg" }
function Write-Err   { param([string]$msg) Write-Host "❌ $msg" -ForegroundColor Red }

# --- Validate token ---
if (-not $Token) {
    Write-Err 'No token provided. Set -Token or $env:GITLAB_TOKEN'
    exit 1
}

$headers = @{ 'PRIVATE-TOKEN' = $Token }
$apiBase = "$GitLabUrl/api/v4/projects/$ProjectId"

# --- Resolve "latest" version ---
if ($Version -eq 'latest') {
    Write-Step 'Resolving latest version'
    try {
        $tags = Invoke-RestMethod -Uri "$apiBase/repository/tags?order_by=version&sort=desc&per_page=1" `
            -Headers $headers -UseBasicParsing
        if ($tags -and $tags.Count -gt 0) {
            $Version = $tags[0].name -replace '^v', ''
            Write-Info "Latest version: $Version"
        }
        else {
            Write-Err 'No tags found in source project. Publish a version first.'
            exit 1
        }
    }
    catch {
        Write-Err "Failed to resolve latest version: $($_.Exception.Message)"
        exit 1
    }
}

Write-Step "Bootstrapping AI SDLC Foundation v$Version ($Mode mode, target: $Target)"
Write-Info "Source: $GitLabUrl (project $ProjectId)"

# --- Create temp directory for installer scripts ---
$tempDir = Join-Path $PWD ".apm-bootstrap-tmp"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tempDir 'lib') -Force | Out-Null

try {
    # --- Download installer files from source repo ---
    $filesToDownload = @(
        @{ Remote = 'scripts%2Finstall-apm-bundle.ps1'; Local = 'install-apm-bundle.ps1' }
        @{ Remote = 'scripts%2Flib%2Fapm-lock.ps1';     Local = 'lib/apm-lock.ps1' }
    )

    foreach ($file in $filesToDownload) {
        $url  = "$apiBase/repository/files/$($file.Remote)/raw?ref=$Ref"
        $dest = Join-Path $tempDir $file.Local
        Write-Info "Downloading $($file.Local)..."
        Invoke-WebRequest -Uri $url -Headers $headers -OutFile $dest -UseBasicParsing
    }
    Write-Ok 'Installer scripts downloaded'

    # --- Run the installer ---
    Write-Step "Running installer"
    $installerPath = Join-Path $tempDir 'install-apm-bundle.ps1'

    $installArgs = @{
        Version  = $Version
        Target   = $Target
        Mode     = $Mode
        ProjectId = $ProjectId
        GitLabUrl = $GitLabUrl
        Token    = $Token
    }

    & $installerPath @installArgs
}
finally {
    # --- Clean up temp files ---
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force
        Write-Info 'Cleaned up bootstrap temp files'
    }
}

# --- Summary ---
Write-Host ''
Write-Step 'Done!'
Write-Host ''
if ($Mode -eq 'standard') {
    Write-Host '  Next steps:' -ForegroundColor Yellow
    Write-Host '    git add .github/ .apm.lock.yaml'
    Write-Host "    git commit -m `"feat: install AI SDLC Foundation v$Version`""
    Write-Host '    git push'
    Write-Host ''
    Write-Host '  Copilot will auto-discover agents and prompts from .github/' -ForegroundColor Gray
    Write-Host '  Try: @hub-orchestrator or /workflow-feature' -ForegroundColor Gray
}
else {
    Write-Host '  Next steps:' -ForegroundColor Yellow
    Write-Host '    git add .apm/ providers/ knowledge/ providers-local/ .apm.lock.yaml apm.yml'
    Write-Host "    git commit -m `"feat: install AI SDLC Foundation v$Version (expandable)`""
    Write-Host '    git push'
    Write-Host ''
    Write-Host '  Customize via providers-local/<provider>/ — then re-project.' -ForegroundColor Gray
}
Write-Host ''
