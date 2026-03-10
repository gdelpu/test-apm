# Agent Factory pipeline - local Podman runner
# Mirrors .gitlab-ci.yml using debian:bookworm-slim + GitHub Copilot CLI
#
# USAGE:   .\run-pipeline-podman.ps1 [-Station <name>] [-Help]
# PREREQS: Podman Desktop running; .env with GH_TOKEN=ghp_xxx (scopes: read:user, copilot)

param(
    [Parameter(Position=0)]
    [string]$Station = "",
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host ""
    Write-Host "USAGE:"
    Write-Host "  .\run-pipeline-podman.ps1 [-Station <name>] [-Help]"
    Write-Host ""
    Write-Host "STATIONS:"
    Write-Host "  A0-intake              Extract MR context       -> station_out/work_order.json"
    Write-Host "  A1-policy-validation   Validate manifests       -> station_out/policy_report.json"
    Write-Host "  A2-security-static     Scan secrets/patterns    -> station_out/security_report.json"
    Write-Host "  A3-prompt-injection    Detect injection vulns   -> station_out/promptsec_report.json"
    Write-Host "  A4-sandbox-simulation  Simulate agent behavior  -> station_out/sim_report.json"
    Write-Host "  A5-policy-gate         Aggregate and gate       -> station_out/gate_decision.json"
    Write-Host "  (A6-github-update skipped locally - requires live GitLab API)"
    Write-Host ""
    Write-Host "EXAMPLES:"
    Write-Host "  .\run-pipeline-podman.ps1                      # Run full pipeline"
    Write-Host "  .\run-pipeline-podman.ps1 -Station A0-intake   # Run single station"
    Write-Host "  .\run-pipeline-podman.ps1 -Help"
    Write-Host ""
    exit 0
}

# --------------------------------------------------------------------------
# Load GH_TOKEN from .env
# --------------------------------------------------------------------------
$ghToken = ""
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -match "^GH_TOKEN=(.+)$") {
            $val = $Matches[1].Trim()
            # Strip inline comments (e.g. GH_TOKEN=ghp_xxx # my token)
            if ($val -match "^([^#]+)#") { $val = $Matches[1].Trim() }
            # Strip surrounding quotes (e.g. GH_TOKEN="ghp_xxx" or GH_TOKEN='ghp_xxx')
            $ghToken = $val.Trim('"').Trim("'")
        }
    }
}
if (-not $ghToken) {
    Write-Error "GH_TOKEN not found in .env. Add: GH_TOKEN=ghp_..."
    exit 1
}

# --------------------------------------------------------------------------
# Pre-flight checks
# --------------------------------------------------------------------------
if (-not (Get-Command podman -ErrorAction SilentlyContinue)) {
    Write-Error "podman not found. Install Podman Desktop."
    exit 1
}
$null = podman ps -q 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Podman daemon not responding. Run: podman machine start"
    exit 1
}

# --------------------------------------------------------------------------
# Workspace setup
# --------------------------------------------------------------------------
$wsDir = (Get-Location).Path -replace '\\', '/'
New-Item -ItemType Directory -Force -Path "station_out" | Out-Null

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Agent Factory SDLC Pipeline  (Local / Podman)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Workspace : $wsDir" -ForegroundColor Gray
Write-Host "  GH_TOKEN  : $($ghToken.Substring(0, [Math]::Min(7,$ghToken.Length)))... ($($ghToken.Length) chars)" -ForegroundColor Gray
Write-Host ""

# CI simulation variables injected into every container
$ciVars = @(
    "-e", "CI_MERGE_REQUEST_IID=1",
    "-e", "CI_MERGE_REQUEST_TITLE=Local pipeline run",
    "-e", "CI_MERGE_REQUEST_AUTHOR=local",
    "-e", "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME=feature/local-test",
    "-e", "CI_MERGE_REQUEST_TARGET_BRANCH_NAME=main",
    "-e", "CI_MERGE_REQUEST_DIFF_BASE_SHA=HEAD~1",
    "-e", "CI_PROJECT_PATH=local/test",
    "-e", "CI_API_V4_URL=https://gitlab.com/api/v4",
    "-e", "STATION_OUT=/workspace/station_out",
    "-e", "GH_TOKEN=$ghToken",
    "-e", "GITHUB_TOKEN=$ghToken",
    "-e", "COPILOT_GITHUB_TOKEN=$ghToken"
)

# --------------------------------------------------------------------------
# Invoke-Station: run a station bash script inside debian:bookworm-slim
# Station scripts live in station-workflows/scripts/ (volume-mounted at /workspace)
# --------------------------------------------------------------------------
function Invoke-Station {
    param([string]$Name)

    $scriptPath = "station-workflows/scripts/$Name.sh"
    if (-not (Test-Path $scriptPath)) {
        Write-Host "  x  Script not found: $scriptPath" -ForegroundColor Red
        return 1
    }

    Write-Host "|---------------------------------------------------------" -ForegroundColor Blue
    Write-Host "|  Station: $Name" -ForegroundColor Blue
    Write-Host "|---------------------------------------------------------" -ForegroundColor Blue
    Write-Host ""

    $podmanArgs = @(
        "run", "--rm",
        "-v", "${wsDir}:/workspace",
        "--workdir", "/workspace"
    ) + $ciVars + @(
        "debian:bookworm-slim",
        "bash", "/workspace/station-workflows/scripts/$Name.sh"
    )

    # Temporarily relax ErrorActionPreference so that harmless stderr
    # output from the container (e.g. debconf warnings from apt-get)
    # does not cause a NativeCommandError termination.
    # Pipe through Write-Host to keep podman stdout OFF the function
    # output pipeline (avoids polluting the integer return value).
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & podman @podmanArgs 2>&1 | ForEach-Object {
        if ($_ -is [System.Management.Automation.ErrorRecord]) {
            Write-Host $_.Exception.Message -ForegroundColor DarkYellow
        } else {
            Write-Host $_
        }
    }
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prevEAP
    Write-Host ""

    if ($code -eq 0) {
        Write-Host "  OK  $Name  PASSED" -ForegroundColor Green
    } else {
        Write-Host "  FAIL  $Name  (exit $code)" -ForegroundColor Red
    }
    Write-Host ""
    return $code
}

# --------------------------------------------------------------------------
# Station registry (A6 excluded - requires live GitLab API)
# --------------------------------------------------------------------------
$stationOrder = @(
    "A0-intake",
    "A1-policy-validation",
    "A2-security-static",
    "A3-prompt-injection",
    "A4-sandbox-simulation",
    "A5-policy-gate"
)

# --------------------------------------------------------------------------
# Determine what to run
# --------------------------------------------------------------------------
if ($Station) {
    if ($Station -notin $stationOrder) {
        Write-Error "Unknown station '$Station'. Valid: $($stationOrder -join ', ')"
        exit 1
    }
    $toRun = @($Station)
} else {
    $toRun = $stationOrder
}

# --------------------------------------------------------------------------
# Execute
# --------------------------------------------------------------------------
$failedStations = @()
foreach ($name in $toRun) {
    $code = Invoke-Station -Name $name
    if ($code -ne 0) {
        $failedStations += $name
        # A5 BLOCK exit is expected normal operation (gate logic), not a runner error.
        # For all other stations, log a warning but continue collecting results.
        if ($name -ne "A5-policy-gate") {
            Write-Host "  WARNING: $name failed; continuing pipeline to collect all results." -ForegroundColor Yellow
        }
    }
}

# A6 local-run notice
if (-not $Station -or $Station -eq "A6-github-update") {
    Write-Host "|---------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "|  Station: A6-github-update  (SKIPPED - local run)" -ForegroundColor DarkGray
    Write-Host "|---------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "  INFO: A6 posts results to GitLab MR. Run in CI for full execution." -ForegroundColor Yellow
    Write-Host ""
}

# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PIPELINE COMPLETE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($failedStations.Count -eq 0) {
    Write-Host "  All stations passed" -ForegroundColor Green
} else {
    Write-Host "  Failed stations: $($failedStations -join ', ')" -ForegroundColor Red
}

Write-Host ""
Write-Host "  Output artifacts in: station_out/" -ForegroundColor Gray
if (Test-Path "station_out") {
    Get-ChildItem "station_out" -Filter "*.json" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "    - $($_.Name)" -ForegroundColor Gray
    }
}
Write-Host ""