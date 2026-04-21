# Pre-Hook: Verify Source Manifest

## Purpose

Cryptographic integrity check for `steer-review-report.md` before the Go/No-Go station consumes it. This is an **external, non-LLM** verification step — it runs as a script, not as an agent instruction.

## When to Run

- **Before** the `steer-go-nogo` station in `sdlc-steer.yml` and `sdlc-full.yml`
- Triggered automatically by the workflow engine as a `pre` hook on the Go/No-Go station

## What It Does

1. Parse the `source_manifest` section from `outputs/docs/3-steer/reviews/steer-review-report.md`
2. For each entry in the manifest:
   - Read the listed source file from its canonical path
   - Compute SHA-256 of the file content
   - Compare against expected integrity (file must exist and be non-empty)
3. Record result in `workflow-state.md`:
   - `hash-check: passed` — all source files exist and are non-empty
   - `hash-check: failed` — one or more source files missing, empty, or path mismatch
4. If `hash-check: failed`, the workflow engine must **block** the Go/No-Go station from running

## Implementation

The workflow engine should execute this as a shell/PowerShell script. A reference implementation:

```powershell
# verify-source-manifest.ps1
param(
    [string]$ReviewReport = "outputs/docs/3-steer/reviews/steer-review-report.md",
    [string]$StateFile = "workflow-state.md"
)

$content = Get-Content $ReviewReport -Raw -ErrorAction Stop
$manifestSection = $false
$files = @()

foreach ($line in ($content -split "`n")) {
    if ($line -match '^\s*##?\s*source_manifest') { $manifestSection = $true; continue }
    if ($manifestSection -and $line -match '^\s*##?\s') { break }
    if ($manifestSection -and $line -match '^\s*-\s*File path:\s*(.+)$') {
        $files += $Matches[1].Trim()
    }
}

$allOk = $true
foreach ($f in $files) {
    if (-not (Test-Path $f) -or (Get-Item $f).Length -eq 0) {
        Write-Warning "FAIL: $f missing or empty"
        $allOk = $false
    } else {
        $hash = (Get-FileHash $f -Algorithm SHA256).Hash
        Write-Host "OK: $f ($hash)"
    }
}

$flag = if ($allOk) { "hash-check: passed" } else { "hash-check: failed" }
Add-Content $StateFile "`n$flag`n"
Write-Host $flag
exit $(if ($allOk) { 0 } else { 1 })
```

## Security Notes

- This hook runs outside the LLM context — it performs real cryptographic operations
- The steer-manager agent should only check for the `hash-check: passed` flag in the workflow state file
- If the flag is absent, the steer-manager must treat it as `failed` and halt
