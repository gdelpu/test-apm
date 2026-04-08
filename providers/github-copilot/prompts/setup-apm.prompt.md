---
name: setup-apm
mode: agent
description: 'Install the AI SDLC Foundation into the current repo via APM bootstrap.'
---

# /setup-apm

Set up the AI SDLC Foundation in the current consumer repository.

## What this does

Downloads and installs the `ssg-ai-backbone` APM bundle from the GitLab
Generic Package Registry into the current workspace, giving you access to
all agents, prompts, workflows, and knowledge assets.

## Steps

1. Ask the user for required inputs (if not already known):
   - **Version** — semver to install (e.g. `0.0.1`) or `latest`
   - **Token** — personal access token (or `$env:GITLAB_TOKEN`)
   - **Mode** — `standard` (default, runtime-only) or `expandable` (full source + customization)
   - **Target** — `copilot` (default), `claude`, or `all`

   The project ID (`545119`) and GitLab URL (`https://innersource.soprasteria.com`) are hardcoded in the bootstrap script.

2. Run the bootstrap script in a terminal:

   **PowerShell (Windows):**
   ```powershell
   .\scripts\bootstrap-apm.ps1 `
     -Version <version> `
     -Token <token> `
     -Mode <mode> `
     -Target <target>
   ```

   **Bash (Linux / macOS):**
   ```bash
   bash scripts/bootstrap-apm.sh \
     --version <version> \
     --token <token> \
     --mode <mode> \
     --target <target>
   ```

   If the bootstrap script is not present locally, download it first:
   ```powershell
   Invoke-WebRequest -Uri "https://innersource.soprasteria.com/api/v4/projects/545119/repository/files/scripts%2Fbootstrap-apm.ps1/raw?ref=main" `
     -Headers @{ 'PRIVATE-TOKEN' = '<token>' } -OutFile bootstrap-apm.ps1
   ```

3. After installation, instruct the user to commit:
   - **Standard mode:** `git add .github/ .apm.lock.yaml`
   - **Expandable mode:** `git add .apm/ providers/ knowledge/ providers-local/ .apm.lock.yaml apm.yml`

4. Confirm the user can now invoke `@hub-orchestrator` or `/workflow-feature`.
