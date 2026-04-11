# /setup-apm

Install the AI SDLC Foundation into the current consumer repository.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `version` | No | `0.0.1` | Semver to install, or `latest` |
| `project-id` | No | `545119` | Numeric GitLab project ID of `ai-sdlc-foundation` |
| `gitlab-url` | No | `https://innersource.soprasteria.com` | GitLab instance URL |
| `token` | Yes | `$GITLAB_TOKEN` | Personal access token |
| `mode` | No | `standard` | `standard` (runtime-only) or `expandable` (full source) |
| `target` | No | `copilot` | `copilot`, `claude`, or `all` |

## Steps

1. Collect inputs from the user (prompt for any missing required values).

2. Download the bootstrap script from the source repo if not present locally:

   ```bash
   curl --fail --silent \
     --header "PRIVATE-TOKEN: ${TOKEN}" \
     -o bootstrap-apm.sh \
     "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/repository/files/scripts%2Fbootstrap-apm.sh/raw?ref=main"
   chmod +x bootstrap-apm.sh
   ```

3. Run the bootstrap:

   ```bash
   ./bootstrap-apm.sh \
     --version "${VERSION}" \
     --project-id "${PROJECT_ID}" \
     --gitlab-url "${GITLAB_URL}" \
     --token "${TOKEN}" \
     --mode "${MODE}" \
     --target "${TARGET}"
   ```

4. Instruct the user to commit:
   - **Standard:** `git add .github/ .apm.lock.yaml`
   - **Expandable:** `git add .apm/ providers/ providers-local/ .apm.lock.yaml apm.yml`

5. Confirm agents are available (`@hub-orchestrator`, `/workflow-feature`).

## Outputs

- `.github/` directory (Copilot runtime projection) or full source tree
- `.apm.lock.yaml` tracking the installed version
