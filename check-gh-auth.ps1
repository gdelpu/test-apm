# check-gh-auth.ps1 - Verify GH_TOKEN from .env is valid for GitHub Copilot
# USAGE:  .\check-gh-auth.ps1 [-EnvFile .env]
#
# Checks performed:
#   1. .env file exists and contains GH_TOKEN
#   2. Token format is plausible (ghp_*, github_pat_*, or fine-grained)
#   3. Token authenticates against GitHub API (GET /user)
#   4. Token has required scopes (read:user, copilot)
#   5. Copilot seat is active for the authenticated user

param(
    [string]$EnvFile = ".env"
)

$ErrorActionPreference = "Stop"

# -- Helpers ---------------------------------------------------------------
function Write-Check  { param([string]$Msg) Write-Host "  [CHECK] $Msg" -ForegroundColor Cyan }
function Write-Pass   { param([string]$Msg) Write-Host "  [PASS]  $Msg" -ForegroundColor Green }
function Write-Fail   { param([string]$Msg) Write-Host "  [FAIL]  $Msg" -ForegroundColor Red }
function Write-Warn   { param([string]$Msg) Write-Host "  [WARN]  $Msg" -ForegroundColor Yellow }
function Write-Detail { param([string]$Msg) Write-Host "          $Msg" -ForegroundColor Gray }

$failCount = 0

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  GitHub Copilot Authentication Check" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# -- 1. Load GH_TOKEN from .env -------------------------------------------
Write-Check "Loading GH_TOKEN from $EnvFile"

if (-not (Test-Path $EnvFile)) {
    Write-Fail "$EnvFile not found."
    Write-Detail "Copy .env.example to .env and add your GitHub PAT."
    exit 1
}

$ghToken = ""
Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -match "^GH_TOKEN=(.+)$") {
        $ghToken = $Matches[1].Trim().Trim('"').Trim("'")
    }
}

if (-not $ghToken) {
    Write-Fail "GH_TOKEN not found in $EnvFile."
    Write-Detail "Add a line: GH_TOKEN=ghp_your_token_here"
    exit 1
}

$masked = $ghToken.Substring(0, [Math]::Min(7, $ghToken.Length)) + "***"
Write-Pass "Token loaded: $masked"

# -- 2. Token format validation --------------------------------------------
Write-Check "Validating token format"

$validPrefixes = @("ghp_", "github_pat_", "gho_", "ghu_", "ghs_")
$hasValidPrefix = $false
foreach ($prefix in $validPrefixes) {
    if ($ghToken.StartsWith($prefix)) {
        $hasValidPrefix = $true
        break
    }
}

if (-not $hasValidPrefix) {
    Write-Warn "Token does not start with a known GitHub prefix."
    Write-Detail "Fine-grained PATs may use different prefixes - continuing anyway."
} else {
    Write-Pass "Token prefix is valid"
}

$tokenLen = $ghToken.Length
if ($tokenLen -lt 30) {
    Write-Fail "Token seems too short at $tokenLen chars. Expected 40+."
    $failCount++
} else {
    Write-Pass "Token length OK at $tokenLen chars"
}

# -- 3. Authenticate against GitHub API ------------------------------------
Write-Check "Authenticating against GitHub API - GET /user"

$headers = @{
    "Authorization"        = "Bearer $ghToken"
    "Accept"               = "application/vnd.github+json"
    "User-Agent"           = "check-gh-auth/1.0"
    "X-GitHub-Api-Version" = "2022-11-28"
}

try {
    $resp = Invoke-WebRequest -Uri "https://api.github.com/user" `
        -Headers $headers -UseBasicParsing -ErrorAction Stop

    $user = $resp.Content | ConvertFrom-Json
    Write-Pass "Authenticated as: $($user.login) - $($user.name)"
    Write-Detail "User ID: $($user.id)  |  Type: $($user.type)"
} catch {
    $status = $null
    if ($_.Exception.Response) {
        $status = [int]$_.Exception.Response.StatusCode
    }
    if ($status -eq 401) {
        Write-Fail "Token is invalid or expired - HTTP 401."
        Write-Detail "Generate a new PAT at https://github.com/settings/tokens"
    } elseif ($status -eq 403) {
        Write-Fail "Token is forbidden - HTTP 403. It may lack permissions."
    } else {
        Write-Fail "GitHub API error: $($_.Exception.Message)"
    }
    exit 1
}

# -- 4. Check token scopes ------------------------------------------------
Write-Check "Checking token scopes"

$scopeHeader = $resp.Headers["X-OAuth-Scopes"]
if ($scopeHeader) {
    $scopeStr = if ($scopeHeader -is [array]) { $scopeHeader -join "," } else { $scopeHeader }
    $scopes = $scopeStr -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    Write-Detail "Scopes granted: $($scopes -join ', ')"

    $requiredScopes = @("read:user", "copilot")
    foreach ($req in $requiredScopes) {
        $parentScope = ($req -split ":") | Select-Object -Last 1
        $found = $scopes | Where-Object { $_ -eq $req -or $_ -eq $parentScope }
        if ($found) {
            Write-Pass "Required scope present: $req"
        } else {
            Write-Fail "Missing required scope: $req"
            Write-Detail "Re-create your PAT with scope: $req"
            $failCount++
        }
    }
} else {
    Write-Warn "No X-OAuth-Scopes header returned."
    Write-Detail "Fine-grained PATs do not expose scopes via headers."
    Write-Detail "Copilot access will be checked directly in the next step."
}

# -- 5. Verify Copilot access ---------------------------------------------
Write-Check "Verifying Copilot seat status"

try {
    $copilotResp = Invoke-WebRequest -Uri "https://api.github.com/copilot/user" `
        -Headers $headers -UseBasicParsing -ErrorAction Stop

    $copilotStatus = $copilotResp.StatusCode
    Write-Pass "Copilot API responded - HTTP $copilotStatus"

    try {
        $copilotData = $copilotResp.Content | ConvertFrom-Json
        if ($copilotData.seat_management_setting) {
            Write-Detail "Seat management: $($copilotData.seat_management_setting)"
        }
    } catch {
        Write-Detail "Copilot endpoint returned non-JSON or unexpected format."
    }
} catch {
    $status = $null
    if ($_.Exception.Response) {
        $status = [int]$_.Exception.Response.StatusCode
    }
    if ($status -eq 401 -or $status -eq 403) {
        Write-Fail "No Copilot access with this token - HTTP $status."
        Write-Detail "Ensure your PAT has the 'copilot' scope and you have an active subscription."
        $failCount++
    } elseif ($status -eq 404) {
        Write-Warn "Copilot user endpoint returned 404."
        Write-Detail "This may mean the endpoint has changed, or Copilot is not enabled."
        Write-Detail "The token may still work for Copilot CLI."
    } else {
        Write-Warn "Copilot API check returned HTTP $status."
    }
}

# -- 6. Quick Copilot CLI check -------------------------------------------
Write-Check "Checking for GitHub Copilot CLI - gh copilot"

$ghCli = Get-Command gh -ErrorAction SilentlyContinue
if ($ghCli) {
    Write-Pass "gh CLI found at: $($ghCli.Source)"
    try {
        $env:GH_TOKEN = $ghToken
        $copilotVersion = & gh copilot --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Pass "gh copilot extension installed: $copilotVersion"
        } else {
            Write-Warn "gh copilot extension not installed."
            Write-Detail "Install with: gh extension install github/gh-copilot"
        }
    } catch {
        Write-Warn "Could not run gh copilot --version"
    } finally {
        Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    }
} else {
    Write-Warn "gh CLI not found in PATH."
    Write-Detail "Install from: https://cli.github.com/"
    Write-Detail "Container-based pipelines install it automatically."
}

# -- Summary ---------------------------------------------------------------
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
if ($failCount -eq 0) {
    Write-Host "  RESULT: All checks passed" -ForegroundColor Green
    Write-Host "  Your GH_TOKEN is ready for the Agent Factory pipeline." -ForegroundColor Green
} else {
    Write-Host "  RESULT: $failCount check(s) failed" -ForegroundColor Red
    Write-Host "  Fix the issues above, then re-run this script." -ForegroundColor Red
}
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

exit $failCount
