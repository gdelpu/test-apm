# PowerShell script to run GitLab CI pipeline locally using gitlab-ci-local
# Usage: .\run-pipeline-local.ps1 [JobName] [-Install] [-Help]

param(
    [Parameter(Position=0)]
    [string]$JobName,
    
    [switch]$Install,
    [switch]$Help
)

function Write-Success { param([string]$msg) Write-Host " $msg" -ForegroundColor Green }
function Write-Info    { param([string]$msg) Write-Host " $msg" -ForegroundColor Cyan }
function Write-Warn    { param([string]$msg) Write-Host " $msg" -ForegroundColor Yellow }
function Write-Err     { param([string]$msg) Write-Host " $msg" -ForegroundColor Red }

if ($Help) {
    Write-Host @"
GitLab CI Local Pipeline Runner
================================

PREREQUISITES:
   Node.js v16+ installed
  • Podman Desktop running
   gitlab-ci-local installed (use -Install flag)

USAGE:
  .\run-pipeline-local.ps1 [JobName] [-Install] [-Help]

EXAMPLES:
  .\run-pipeline-local.ps1 -Install           # Install gitlab-ci-local
  .\run-pipeline-local.ps1                    # Run full pipeline
  .\run-pipeline-local.ps1 A0-intake          # Run single station
  .\run-pipeline-local.ps1 A5-policy-gate     # Run gate decision

STATION OUTPUTS:
  station_out/work_order.json        (A0)
  station_out/policy_report.json     (A1)
  station_out/security_report.json   (A2)
  station_out/promptsec_report.json  (A3)
  station_out/sim_report.json        (A4)
  station_out/gate_decision.json     (A5)

For detailed documentation, see LOCAL_TESTING.md
"@
    exit 0
}

if ($Install) {
    Write-Info "Installing gitlab-ci-local..."
    
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Err "npm not found. Install Node.js v16+ first."
        Write-Info "Download from: https://nodejs.org/"
        exit 1
    }
    
    npm install -g gitlab-ci-local
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "gitlab-ci-local installed successfully"
        Write-Info "You can now run: .\run-pipeline-local.ps1"
    } else {
        Write-Err "Installation failed. Check npm output above."
        exit 1
    }
    exit 0
}

Write-Info "Running pre-flight checks..."

if (-not (Get-Command gitlab-ci-local -ErrorAction SilentlyContinue)) {
    Write-Err "gitlab-ci-local not found"
    Write-Info "Install with: .\run-pipeline-local.ps1 -Install"
    exit 1
}

if (-not (Test-Path ".gitlab-ci.yml")) {
    Write-Err ".gitlab-ci.yml not found in current directory"
    Write-Info "Make sure you're running from repository root"
    exit 1
}

# Check for Podman (preferred) or Docker
$containerRuntime = $null
if (Get-Command podman -ErrorAction SilentlyContinue) {
    $containerRuntime = "podman"
    try {
        podman ps 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Err "Podman is not running"
            Write-Info "Start Podman Desktop or run: podman machine start"
            exit 1
        }
    } catch {
        Write-Err "Podman is installed but not responding"
        Write-Info "Try: podman machine start"
        exit 1
    }
} elseif (Get-Command docker -ErrorAction SilentlyContinue) {
    $containerRuntime = "docker"
    try {
        docker ps 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Err "Docker is not running"
            Write-Info "Start Docker Desktop and try again"
            exit 1
        }
    } catch {
        Write-Err "Docker is installed but not responding"
        exit 1
    }
} else {
    Write-Err "No container runtime found"
    Write-Info "Install Podman Desktop from: https://podman-desktop.io/"
    Write-Info "Or Docker Desktop from: https://docker.com/"
    exit 1
}

Write-Success "Container runtime detected: $containerRuntime"

Write-Success "Pre-flight checks passed"
Write-Host ""

if ($JobName) {
    Write-Info "Running job: $JobName"
    gitlab-ci-local $JobName
} else {
    Write-Info "Running full pipeline (all stations)"
    gitlab-ci-local
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Success "Pipeline completed successfully"
    Write-Info "Check station_out/ for generated artifacts"
} else {
    Write-Host ""
    Write-Err "Pipeline failed with exit code $LASTEXITCODE"
    Write-Info "Review output above for errors"
    exit $LASTEXITCODE
}
