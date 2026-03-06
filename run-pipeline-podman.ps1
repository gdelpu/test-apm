# Direct Podman runner for Agent Factory pipeline (Windows-native)
# Bypasses gitlab-ci-local for Windows compatibility

param(
    [Parameter(Position=0)]
    [string]$Station,
    
    [switch]$Help
)

function Write-Success { param([string]$msg) Write-Host " $msg" -ForegroundColor Green }
function Write-Info    { param([string]$msg) Write-Host " $msg" -ForegroundColor Cyan }
function Write-Warn    { param([string]$msg) Write-Host " $msg" -ForegroundColor Yellow }
function Write-Err     { param([string]$msg) Write-Host " $msg" -ForegroundColor Red }

if ($Help) {
    Write-Host @"
Agent Factory Pipeline - Direct Podman Runner
==============================================

USAGE:
  .\run-pipeline-podman.ps1 [Station]

STATIONS:
  A0-intake              Parse MR diff and create work order
  A1-policy-validation   Validate against policy rules
  A2-security-static     Security static analysis
  A3-prompt-injection    Prompt injection checks
  A4-sandbox-simulation  Sandbox testing
  A5-policy-gate         Final gate decision
  A6-github-update       Update GitHub (skipped locally)
  (empty)                Run all stations in sequence

EXAMPLES:
  .\run-pipeline-podman.ps1              # Run full pipeline
  .\run-pipeline-podman.ps1 A0-intake    # Run single station
  .\run-pipeline-podman.ps1 A5-policy-gate

OUTPUT:
  All results written to station_out/ directory

"@
    exit 0
}

# Pre-flight checks
Write-Info "Pre-flight checks..."

if (-not (Get-Command podman -ErrorAction SilentlyContinue)) {
    Write-Err "Podman not found. Install Podman Desktop."
    exit 1
}

try {
    podman ps 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Podman is not running. Start Podman Desktop or run: podman machine start"
        exit 1
    }
} catch {
    Write-Err "Podman error. Try: podman machine start"
    exit 1
}

Write-Success "Podman ready"

# Create output directory
New-Item -ItemType Directory -Force -Path "station_out" | Out-Null
Write-Info "Output directory: station_out/"

# Get absolute path for volume mounting
$workspaceDir = (Get-Location).Path.Replace('\', '/')

# Station runner function
function Run-Station {
    param(
        [string]$Name,
        [string]$Script,
        [string]$Image = "python:3.12-slim"
    )
    
    Write-Info "Running $Name..."
    
    $cmd = @"
cd /workspace && \
apt-get update -qq && apt-get install -y -qq git > /dev/null && \
git config --global --add safe.directory /workspace && \
pip install --quiet --no-cache-dir PyYAML requests jsonschema && \
python $Script
"@
    
    podman run --rm `
        -v "${workspaceDir}:/workspace" `
        -w /workspace `
        -e CI_MERGE_REQUEST_IID=1 `
        -e CI_MERGE_REQUEST_SOURCE_BRANCH_NAME=feature/test `
        -e CI_MERGE_REQUEST_TARGET_BRANCH_NAME=main `
        -e CI_MERGE_REQUEST_DIFF_BASE_SHA=HEAD~1 `
        -e CI_PROJECT_PATH=local/test `
        -e PIP_NO_COLOR=1 `
        $Image `
        bash -c $cmd
    
    return $LASTEXITCODE
}

# Define stations
$stations = @{
    "A0-intake" = "station-workflows/implementations/A0-intake.py"
    "A1-policy-validation" = "station-workflows/implementations/A1-policy-validation.py"
    "A2-security-static" = "station-workflows/implementations/A2-security-static.py"
    "A3-prompt-injection" = "station-workflows/implementations/A3-prompt-injection.py"
    "A4-sandbox-simulation" = "station-workflows/implementations/A4-sandbox-simulation.py"
    "A5-policy-gate" = "station-workflows/implementations/A5-policy-gate.py"
}

# Run requested station(s)
if ($Station) {
    if (-not $stations.ContainsKey($Station)) {
        Write-Err "Unknown station: $Station"
        Write-Info "Valid stations: $($stations.Keys -join ', ')"
        exit 1
    }
    
    $exitCode = Run-Station -Name $Station -Script $stations[$Station]
    
    if ($exitCode -eq 0) {
        Write-Success "$Station completed"
    } else {
        Write-Err "$Station failed with exit code $exitCode"
        exit $exitCode
    }
} else {
    # Run all stations in sequence
    Write-Info "Running full pipeline (6 stations, A6 skipped for local)"
    Write-Host ""
    
    $failed = $false
    foreach ($stationName in @("A0-intake", "A1-policy-validation", "A2-security-static", 
                               "A3-prompt-injection", "A4-sandbox-simulation", "A5-policy-gate")) {
        $exitCode = Run-Station -Name $stationName -Script $stations[$stationName]
        
        if ($exitCode -eq 0) {
            Write-Success "$stationName completed"
        } else {
            Write-Err "$stationName failed"
            $failed = $true
            break
        }
        Write-Host ""
    }
    
    if (-not $failed) {
        Write-Host ""
        Write-Success "Pipeline completed successfully!"
        Write-Info "Results in station_out/"
    } else {
        Write-Host ""
        Write-Err "Pipeline failed"
        exit 1
    }
}
