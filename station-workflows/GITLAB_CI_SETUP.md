# GitLab CI/CD Station-Gate Pipeline - Setup Guide

## Overview

This GitLab CI/CD pipeline implements the AI-SDLC Station-Gate workflow using **GitHub Copilot CLI as an autonomous agent** to execute validation stations. The pipeline runs automatically on merge requests that modify agent, skill, prompt, or instruction files.

## Architecture

The pipeline orchestrates 7 stations across 6 GitLab CI/CD stages:

```

  Merge Request Created/Updated                                
  (changes to *.agent.md, *.skill.md, *.prompt.md, etc.)      

                 
                 

  Stage: setup                                                 
   validate_prerequisites                                    
     - Check schemas exist                                     
     - Verify GH_TOKEN configured                              

                 
                 

  Stage: intake                                                
   station_a0_intake                                         
     - Extract MR metadata                                     
     - Get changed files (git diff)                            
     - Output: station_out/work_order.json                     

                 
                 
                                                     
  
  Stage: validation                      Stage: security              
   station_a1_policy                    station_a2_security       
     - Validate JSON schemas               - Scan for secrets         
     - Check manifests                     - Detect dangerous patterns
     - Output: policy_report.json          - Output: security_*.json  
     station_a3_prompt_injection
                                             - Detect injection patterns 
                                             - Output: promptsec_*.json  
                                        
                                                       
               
                                

  Stage: simulation                                            
   station_a4_sandbox                                        
     - Simulate malicious inputs                               
     - Static analysis of vulnerabilities                      
     - Output: sim_report.json                                 

                 
                 

  Stage: gate                                                  
   station_a5_policy_gate                                    
    - Aggregate all station reports                           
    - Apply decision logic                                    
    - Output: gate_decision.json                              
    - Exit 0 (APPROVE) | 1 (BLOCK) | 99 (REVIEW)              
                                                               
   manual_override_approve (manual)                          
     - Override for REVIEW decisions                           
     - Requires human approval                                 

                 
                 

  Stage: update                                                
   station_a6_gitlab_update (always runs)                    
     - Post results comment to MR                              
     - Apply label (approved/blocked/review)                   
     - Output: update_report.json                              

```

## Prerequisites

### 1. GitHub Copilot Subscription

You need an **active GitHub Copilot subscription** (Individual, Business, or Enterprise) to use GitHub Copilot CLI.

- Sign up at: https://github.com/features/copilot/plans
- Verify access: `gh auth status` after installation

### 2. Required Environment Variables

Configure these in **GitLab CI/CD Settings  Variables**:

| Variable | Description | Required | Masked | Protected |
|----------|-------------|----------|--------|-----------|
| `GH_TOKEN` | GitHub Personal Access Token with `copilot` scope |  Yes |  Yes |  Yes |
| `GITLAB_TOKEN` | GitLab Personal Access Token with `api` scope |  Yes |  Yes |  Yes |

#### Creating GH_TOKEN (GitHub):

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Select scopes:
   -  `copilot` - Required for Copilot CLI authentication
   -  `read:user` - Optional, for user info
4. Copy token immediately (shown once only)
5. Add to GitLab: **Your Project  Settings  CI/CD  Variables**

#### Creating GITLAB_TOKEN (GitLab):

1. Go to **Your Profile  Access Tokens**
2. Create token with scopes:
   -  `api` - Full API access
   -  `write_repository` - Update MR comments/labels
3. Copy token
4. Add to **Project  Settings  CI/CD  Variables**

### 3. Required Files in Repository

Ensure these files exist before running pipeline:

```
station-workflows/
 schemas/
    agent-manifest.schema.json    # Agent validation schema
    skill-manifest.schema.json    # Skill validation schema
 fixtures/
    malicious-inputs.json         # Test payloads for A4
    prompt-injection-payloads.json # Injection patterns for A3
 stations/
     A0-intake.prompt.md           # Station specifications
     A1-policy-validation.prompt.md
     A2-security-static.prompt.md
     A3-prompt-injection.prompt.md
     A4-sandbox-simulation.prompt.md
     A5-policy-gate.agent.md
     A6-github-update.prompt.md
```

### 4. GitLab Runner Configuration

This pipeline uses:
- **Docker executor** with `debian:bookworm-slim` image
- **Shared runners** OR dedicated project runners
- **Tags**: `docker` (optional, remove if using shared runners)

To use shared runners:
1. Go to **Project  Settings  CI/CD  Runners**
2. Enable **Shared Runners**

## Installation

1. **Copy `.gitlab-ci.yml` to your repository root**

2. **Configure environment variables** (see Prerequisites #2 above)

3. **Commit and push**:
   ```bash
   git add .gitlab-ci.yml
   git commit -m "Add station-gate CI/CD pipeline"
   git push origin main
   ```

4. **Test with a merge request**:
   ```bash
   git checkout -b test/pipeline-validation
   # Make a change to an agent or skill file
   git add .
   git commit -m "Test pipeline"
   git push origin test/pipeline-validation
   # Create MR in GitLab UI
   ```

## Usage

### Automatic Trigger

Pipeline automatically runs when:
- **Event**: Merge request created or updated
- **Changes**: Files matching these patterns:
  - `**/*.agent.md`
  - `**/*.skill.md`
  - `**/*.prompt.md`
  - `**/*.instructions.md`

### Gate Decisions

Station A5 makes one of three decisions:

####  APPROVE
- **Criteria**: No CRITICAL or HIGH severity findings
- **Action**: Pipeline succeeds, MR can be merged
- **Label Applied**: `station-gate::approved`

####  BLOCK
- **Criteria**: 
  - Any CRITICAL severity finding
  - More than 2 HIGH severity findings
  - Confirmed secret exposure
  - Direct injection vulnerability
- **Action**: Pipeline fails, MR cannot be merged
- **Label Applied**: `station-gate::blocked`

####  REVIEW
- **Criteria**:
  - 1-2 HIGH severity findings
  - More than 5 MEDIUM severity findings
  - Requires human judgment
- **Action**: Pipeline pauses, manual approval required
- **Label Applied**: `station-gate::review`

### Manual Override

For **REVIEW** decisions requiring human approval:

1. View gate decision in MR comment
2. Review findings in pipeline artifacts
3. If approved, click **Manual job  manual_override_approve**
4. Override recorded in `station_out/manual_override.json`

## Station Outputs

All station outputs are saved as **GitLab CI artifacts** for 1 week:

| Artifact | Station | Description |
|----------|---------|-------------|
| `station_out/work_order.json` | A0 | MR metadata and changed files |
| `station_out/policy_report.json` | A1 | Schema validation results |
| `station_out/security_report.json` | A2 | Secret/pattern scan results |
| `station_out/promptsec_report.json` | A3 | Injection vulnerability findings |
| `station_out/sim_report.json` | A4 | Sandbox simulation results |
| `station_out/gate_decision.json` | A5 | Final gate decision |
| `station_out/update_report.json` | A6 | GitLab API update status |
| `station_out/manual_override.json` | Manual | Override approval record |

Access artifacts:
1. Go to **Pipelines  Select pipeline  Jobs**
2. Click job name  **Download  station_out/**

## Debugging

### View Copilot CLI Execution

Each station logs full Copilot CLI output. To debug:

1. Navigate to **Pipelines  Failed pipeline**
2. Click failing station job (e.g., `station_a2_security`)
3. Scroll through job log to see:
   - Copilot CLI prompt sent
   - Tool invocations and permissions
   - Output file creation
   - Error messages

### Common Issues

####  Error: `GH_TOKEN not set`

**Solution**: Configure GH_TOKEN environment variable
```bash
# In GitLab: Settings  CI/CD  Variables
# Add: GH_TOKEN = <your-github-pat>
```

####  Error: `work_order.json not created`

**Cause**: Station A0 failed to generate output

**Solution**: 
1. Check git configuration in job log
2. Verify changed files were detected
3. Review Copilot CLI prompt formatting

####  Error: `Missing agent-manifest.schema.json`

**Solution**: Ensure schema files exist in `station-workflows/schemas/`

####  Copilot CLI not installed

**Solution**: Update `.copilot_job` template in `.gitlab-ci.yml`:
```yaml
before_script:
  - apt-get update && apt-get install -y curl git jq
  - curl -fsSL https://gh.io/copilot-install | bash
  - export PATH="$HOME/.local/bin:$PATH"
```

### Testing Locally

You can test stations locally before pushing:

```bash
# Install GitHub Copilot CLI locally
gh extension install github/gh-copilot

# Authenticate
gh auth login

# Test Station A0 manually
copilot -p "You are Station A0... [paste prompt from .gitlab-ci.yml]" \
  --allow-tool "shell(git)" --allow-tool "shell(date)"

# Check output
cat station_out/work_order.json | jq .
```

## Security Considerations

### Tool Permissions

Each station runs with **least-privilege tool access**:

| Station | Allowed Tools | Denied Tools |
|---------|---------------|--------------|
| A0 | `shell(git)`, `shell(date)` | `*` (wildcard denied) |
| A1 | File read only | `shell(*)` |
| A2 | `shell(grep)`, `shell(find)`, `shell(cat)` | `shell(curl)` |
| A3 | File read only | `shell(*)` |
| A4 | File read only | `shell(*)` |
| A5 | File read only | `shell(*)` |
| A6 | `curl` for API | `shell(*)` |

### Secure Secrets

-  Store tokens in GitLab CI/CD Variables (masked + protected)
-  Never hardcode credentials in `.gitlab-ci.yml`
-  Rotate `GH_TOKEN` and `GITLAB_TOKEN` quarterly
-  Use separate tokens for different projects

### Container Isolation

- Each job runs in isolated Docker container
- Containers destroyed after job completion
- No persistent state between jobs

## Customization

### Adjust Gate Logic

To modify decision criteria, edit Station A5 prompt in `.gitlab-ci.yml`:

```yaml
station_a5_policy_gate:
  script:
    - |
      copilot -p "
      ...
      ## Decision Logic
      1. **BLOCK** if ANY of:
         - CRITICAL severity > 0  #  Customize threshold
         - HIGH severity > 5      #  Adjust count
      ...
      "
```

### Add Custom Station

To add a new validation station (e.g., A7 - License Compliance):

```yaml
station_a7_licensing:
  stage: validation
  extends: .copilot_job
  needs:
    - job: station_a0_intake
      artifacts: true
  script:
    - |
      copilot -p "
      You are Station A7: License Compliance.
      
      Scan changed files for:
      1. SPDX license identifiers
      2. Copyright headers
      3. OSS license compatibility
      
      Output: station_out/license_report.json
      " --deny-tool "shell(*)"
    - test -f station_out/license_report.json
  artifacts:
    paths:
      - station_out/license_report.json
```

Then update A5 to read `license_report.json`.

### Change Trigger Patterns

To trigger on different file types, modify workflow rules:

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.agent.md"
        - "**/*.skill.md"
        - "docs/**/*"          #  Add documentation files
        - "config/**/*.yaml"   #  Add config files
```

## Performance

### Pipeline Duration

Typical execution times:

| Stage | Jobs | Duration |
|-------|------|----------|
| Setup | 1 | ~30s |
| Intake | 1 | ~45s |
| Validation | 1 | ~60s |
| Security | 2 (parallel) | ~90s |
| Simulation | 1 | ~120s |
| Gate | 1 (+manual) | ~30s |
| Update | 1 | ~15s |
| **Total** | **~6 minutes** | **+ manual wait** |

### Optimization Tips

1. **Run stations in parallel** where possible (A2 + A3 already do)
2. **Cache Docker images** in GitLab container registry
3. **Use dedicated runners** for faster execution
4. **Reduce Copilot CLI prompt size** by referencing files instead of embedding content

## Cost Analysis

### GitHub Copilot Usage

Each station invocation consumes **1 Copilot request** (claude-sonnet-4 at 1x multiplier).

- **Per MR**: 6-7 Copilot requests
- **Monthly quota** (Individual): 400 requests
- **Max MRs/month**: ~57 MRs

For high-volume projects, consider **Copilot Business** or **Enterprise** plans.

### GitLab Runner Costs

- **Shared runners**: 400 CI/CD minutes/month (Free tier)
- This pipeline: ~6 minutes per run
- **Max runs/month**: ~66 MRs

For more capacity, upgrade to **GitLab Premium** or use **dedicated runners**.

## Troubleshooting

### Pipeline Not Triggering

**Check**:
1. Are you creating a merge request?
2. Do changed files match trigger patterns?
3. Are GitLab Shared Runners enabled?

**Solution**:
```bash
# Verify pipeline rules
# In .gitlab-ci.yml, check workflow.rules section
```

### Station A0 Can't Access Git History

**Error**: `fatal: not a git repository`

**Solution**: Add to `.copilot_job.before_script`:
```yaml
- git config --global --add safe.directory ${CI_PROJECT_DIR}
```

### Copilot CLI Rate Limited

**Error**: `429 Too Many Requests`

**Solution**:
1. Reduce concurrent MRs
2. Upgrade to Copilot Business/Enterprise
3. Add retry logic with exponential backoff

## Support

- **GitLab CI/CD Docs**: https://docs.gitlab.com/ee/ci/
- **GitHub Copilot CLI Docs**: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line
- **Station Specifications**: See `station-workflows/stations/*.md`

## License

This pipeline configuration is part of the ai-sdlc-foundation project.
