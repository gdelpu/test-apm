#!/usr/bin/env pwsh
<#
.SYNOPSIS
Compare feature specification against prototype implementation

.DESCRIPTION
Scans the prototype directory to identify relevant files and patterns
for a given feature. Outputs structured data for AI agent analysis.

.PARAMETER FeatureName
The name of the feature (used for semantic search)

.PARAMETER FeatureDir
The feature spec directory (to read spec.md)

.PARAMETER Json
Output in JSON format

.EXAMPLE
./compare-with-prototype.ps1 -FeatureName "user-authentication" -Json

.EXAMPLE
./compare-with-prototype.ps1 -FeatureDir "c:\path\to\specs\042-feature" -Json
#>
param(
    [Parameter(Mandatory=$false)]
    [string]$FeatureName,
    
    [Parameter(Mandatory=$false)]
    [string]$FeatureDir,
    
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

function Write-Info {
    param([string]$Message)
    if (-not $Json) {
        Write-Host "[INFO] $Message" -ForegroundColor Cyan
    }
}

function Write-Err {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Import common functions if available
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CommonPath = Join-Path $ScriptDir 'common.ps1'
if (Test-Path $CommonPath) {
    . $CommonPath
    $envData = Get-FeaturePathsEnv
    $REPO_ROOT = $envData.REPO_ROOT
} else {
    # Fallback: find repo root manually
    $current = $PSScriptRoot
    while ($current) {
        if ((Test-Path (Join-Path $current '.git')) -or (Test-Path (Join-Path $current '.specify'))) {
            $REPO_ROOT = $current
            break
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) { break }
        $current = $parent
    }
    if (-not $REPO_ROOT) {
        Write-Err "Could not determine repository root"
        exit 1
    }
}

$PROTOTYPE_DIR = Join-Path $REPO_ROOT 'prototype'
$PROTOTYPE_SRC = Join-Path $PROTOTYPE_DIR 'src'

function Test-PrototypeExists {
    return (Test-Path $PROTOTYPE_DIR) -and (Test-Path $PROTOTYPE_SRC)
}

function Get-PrototypeStructure {
    if (-not (Test-PrototypeExists)) {
        return @{
            exists = $false
            message = "Prototype directory not found at $PROTOTYPE_DIR"
        }
    }
    
    $structure = @{
        exists = $true
        rootPath = $PROTOTYPE_SRC
        components = @()
        pages = @()
        features = @()
        styles = @()
        utilities = @()
        totalFiles = 0
    }
    
    # Scan for common patterns
    $componentsDir = Join-Path $PROTOTYPE_SRC 'components'
    $pagesDir = Join-Path $PROTOTYPE_SRC 'pages'
    $featuresDir = Join-Path $PROTOTYPE_SRC 'features'
    
    if (Test-Path $componentsDir) {
        $structure.components = @(Get-ChildItem -Path $componentsDir -Recurse -Include *.tsx,*.ts,*.jsx,*.js -File |
            ForEach-Object { $_.FullName })
    }
    
    if (Test-Path $pagesDir) {
        $structure.pages = @(Get-ChildItem -Path $pagesDir -Recurse -Include *.tsx,*.ts,*.jsx,*.js -File |
            ForEach-Object { $_.FullName })
    }
    
    if (Test-Path $featuresDir) {
        $structure.features = @(Get-ChildItem -Path $featuresDir -Recurse -Include *.tsx,*.ts,*.jsx,*.js -File |
            ForEach-Object { $_.FullName })
    }
    
    # Get all TypeScript/JavaScript files
    $allFiles = Get-ChildItem -Path $PROTOTYPE_SRC -Recurse -Include *.tsx,*.ts,*.jsx,*.js -File
    $structure.totalFiles = $allFiles.Count
    
    return $structure
}

function Get-PrototypePatterns {
    $patterns = @{
        componentLibrary = "Unknown"
        styling = @()
        stateManagement = "Unknown"
        routing = "Unknown"
        apiClient = "Unknown"
        buildTool = "Unknown"
        testing = @()
    }
    
    # Check package.json for dependencies
    $packageJson = Join-Path $PROTOTYPE_DIR 'package.json'
    if (Test-Path $packageJson) {
        try {
            $pkg = Get-Content $packageJson -Raw | ConvertFrom-Json
            
            # Check all dependencies
            $allDeps = @{}
            if ($pkg.dependencies) {
                $pkg.dependencies.PSObject.Properties | ForEach-Object {
                    $allDeps[$_.Name] = $_.Value
                }
            }
            if ($pkg.devDependencies) {
                $pkg.devDependencies.PSObject.Properties | ForEach-Object {
                    $allDeps[$_.Name] = $_.Value
                }
            }
            
            # Routing
            if ($allDeps.ContainsKey('react-router-dom')) {
                $patterns.routing = "React Router"
            } elseif ($allDeps.ContainsKey('@tanstack/react-router')) {
                $patterns.routing = "TanStack Router"
            }
            
            # Styling
            if ($allDeps.ContainsKey('tailwindcss')) {
                $patterns.styling += "Tailwind CSS"
            }
            if ($allDeps.ContainsKey('styled-components')) {
                $patterns.styling += "Styled Components"
            }
            
            # API Client
            if ($allDeps.ContainsKey('axios')) {
                $patterns.apiClient = "Axios"
            } elseif ($allDeps.ContainsKey('fetch')) {
                $patterns.apiClient = "Fetch API"
            }
            
            # State Management
            if ($allDeps.ContainsKey('react-query') -or $allDeps.ContainsKey('@tanstack/react-query')) {
                $patterns.stateManagement = "React Query / TanStack Query"
            } elseif ($allDeps.ContainsKey('zustand')) {
                $patterns.stateManagement = "Zustand"
            } elseif ($allDeps.ContainsKey('redux')) {
                $patterns.stateManagement = "Redux"
            }
            
            # Build Tool
            if ($allDeps.ContainsKey('vite')) {
                $patterns.buildTool = "Vite"
            } elseif ($allDeps.ContainsKey('webpack')) {
                $patterns.buildTool = "Webpack"
            }
            
            # Testing
            if ($allDeps.ContainsKey('vitest')) {
                $patterns.testing += "Vitest"
            }
            if ($allDeps.ContainsKey('playwright')) {
                $patterns.testing += "Playwright"
            }
            if ($allDeps.ContainsKey('@testing-library/react')) {
                $patterns.testing += "React Testing Library"
            }
        }
        catch {
            Write-Err "Could not parse package.json: $_"
        }
    }
    
    return $patterns
}

# Main execution
if (-not (Test-PrototypeExists)) {
    if ($Json) {
        @{
            exists = $false
            message = "Prototype directory not found at $PROTOTYPE_DIR"
            skip = $true
        } | ConvertTo-Json -Depth 5
    } else {
        Write-Host "Prototype directory not found" -ForegroundColor Yellow
        Write-Host "Expected location: $PROTOTYPE_DIR" -ForegroundColor Yellow
        Write-Host "Skipping prototype comparison" -ForegroundColor Yellow
    }
    exit 0
}

if ($Json) {
    $structure = Get-PrototypeStructure
    
    if ($structure.exists) {
        $structure.patterns = Get-PrototypePatterns
        $structure.instructions = @(
            "Use semantic_search to find prototype files relevant to the feature",
            "Read relevant prototype files to understand implementation patterns",
            "Compare spec functional requirements against prototype implementation",
            "Identify UI patterns, component structure, and styling to follow",
            "Note differences between spec and prototype (intentional or accidental)",
            "Generate recommendations for implementation alignment",
            "Add prototype file references to clarification context"
        )
        $structure.featureName = if ($FeatureName) { $FeatureName } else { "Unknown" }
        $structure.featureDir = if ($FeatureDir) { $FeatureDir } else { "Unknown" }
    }
    
    $structure | ConvertTo-Json -Depth 5
} else {
    Write-Info "Prototype found: $PROTOTYPE_SRC"
    
    $structure = Get-PrototypeStructure
    $patterns = Get-PrototypePatterns
    
    Write-Host ""
    Write-Host "Prototype Structure:" -ForegroundColor Cyan
    Write-Host "  Components: $($structure.components.Count) files" -ForegroundColor White
    Write-Host "  Pages: $($structure.pages.Count) files" -ForegroundColor White
    Write-Host "  Features: $($structure.features.Count) files" -ForegroundColor White
    Write-Host "  Total Files: $($structure.totalFiles)" -ForegroundColor White
    Write-Host ""
    Write-Host "Detected Patterns:" -ForegroundColor Yellow
    Write-Host "  Build Tool: $($patterns.buildTool)" -ForegroundColor White
    Write-Host "  Routing: $($patterns.routing)" -ForegroundColor White
    Write-Host "  Styling: $($patterns.styling -join ', ')" -ForegroundColor White
    Write-Host "  State: $($patterns.stateManagement)" -ForegroundColor White
    Write-Host "  API: $($patterns.apiClient)" -ForegroundColor White
    if ($patterns.testing.Count -gt 0) {
        Write-Host "  Testing: $($patterns.testing -join ', ')" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "Next Steps for Agent:" -ForegroundColor Green
    Write-Host "  1. Use semantic_search to find relevant prototype files for the feature" -ForegroundColor White
    Write-Host "  2. Read and analyze those files for patterns and implementation details" -ForegroundColor White
    Write-Host "  3. Compare spec requirements against prototype implementation" -ForegroundColor White
    Write-Host "  4. Generate comparison report with recommendations" -ForegroundColor White
}

exit 0
