# MCP Setup Guide — Consumer Reference

> Hands-on guide to configure MCP (Model Context Protocol) servers for your AI SDLC Foundation installation.

> **Quick start**: Use the Hub Orchestrator (`@hub-orchestrator configure MCP`) for auto-detection and guided setup. This guide covers manual configuration and advanced topics.

---

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Quick Start](#quick-start)
- [Profiles](#profiles)
- [Per-Server Setup](#per-server-setup)
  - [Azure](#azure)
  - [AWS](#aws)
  - [GitHub](#github)
  - [GitLab](#gitlab)
  - [Azure DevOps (Local)](#azure-devops-local)
  - [Azure DevOps (Remote)](#azure-devops-remote)
  - [Atlassian](#atlassian)
  - [Work-iq (Microsoft 365)](#work-iq-microsoft-365)
  - [MsLearn](#mslearn)
  - [Context7](#context7)
  - [Playwright](#playwright)
  - [SemGrep](#semgrep)
  - [SonarQube](#sonarqube)
  - [Figma](#figma)
- [Fallback Behavior](#fallback-behavior)
- [Version Management](#version-management)
- [Client-Specific Overrides](#client-specific-overrides)
- [Verify Connectivity](#verify-connectivity)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that allows AI agents to interact with external tools and services through a unified interface. Instead of relying solely on built-in capabilities, agents can call MCP servers to query live data, run analysis tools, or interact with external platforms.

The AI SDLC Foundation supports 14 curated MCP servers. **All are optional** — every workflow runs without any MCP server configured. MCP servers provide enrichments: live infrastructure data, current documentation, browser automation, and platform integrations.

> Learn more: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

---

## Quick Start

### Option 1: Hub Orchestrator (recommended)

```
@hub-orchestrator configure MCP
```

The Hub Orchestrator will auto-detect your platform, recommend a profile, ask a few questions, and generate the configuration.

### Option 2: First 5 minutes — starter pair

Install **Context7** (up-to-date library docs) and **Playwright** (browser automation) for immediate value:

**VS Code** — add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Claude Code** — add to `.claude/mcp.json` (same format).

### Option 3: Profile-based

Pick a profile and generate the full configuration:

```
@hub-orchestrator configure MCP with github-stack profile
```

---

## Profiles

Curated server sets for common development stacks:

| Profile | Servers included | Best for |
|---------|-----------------|----------|
| `github-stack` | GitHub, Context7, Playwright, SemGrep, SonarQube | GitHub-native projects |
| `gitlab-stack` | GitLab, Context7, Playwright, SemGrep, Atlassian, SonarQube | GitLab CI/CD with Atlassian PM |
| `azure-devops-stack` | Azure, ADO (Local+Remote), MsLearn, Context7, Work-iq, Playwright, SonarQube | Microsoft-centric stacks |
| `full` | All 14 servers | Maximum capability (configure auth per-server) |

---

## Per-Server Setup

### Azure

**What it does**: Query Azure resources, validate IaC against live state, check service health.

**Prerequisites**: Azure CLI logged in or service principal configured.

**Skills enhanced**: `soprasteria-dep`, `sdlc-tech-architecture`, `observability-readiness`

**Configuration**:
```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["@azure/mcp@latest"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "${input:AZURE_SUBSCRIPTION_ID}",
        "AZURE_TENANT_ID": "${input:AZURE_TENANT_ID}"
      }
    }
  }
}
```

**Troubleshooting**: Ensure `az login` has been run. Check `az account show` for correct subscription.

---

### AWS

**What it does**: Query AWS resources, validate CloudFormation/CDK, check service quotas.

**Prerequisites**: AWS CLI configured with credentials.

**Skills enhanced**: `soprasteria-dep`

**Configuration**:
```json
{
  "servers": {
    "aws": {
      "command": "npx",
      "args": ["@aws/mcp@latest"],
      "env": {
        "AWS_PROFILE": "${input:AWS_PROFILE}",
        "AWS_REGION": "${input:AWS_REGION}"
      }
    }
  }
}
```

**Troubleshooting**: Run `aws sts get-caller-identity` to verify credentials.

---

### GitHub

**What it does**: Issue/PR management, code search, Actions status, releases.

**Prerequisites**: GitHub Personal Access Token with appropriate scopes.

**Skills enhanced**: `pr-checks`, `code-implementation`

**Configuration**:
```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["@github/mcp-server@latest"],
      "env": {
        "GITHUB_TOKEN": "${input:GITHUB_TOKEN}"
      }
    }
  }
}
```

**Troubleshooting**: Ensure token has `repo`, `read:org` scopes.

---

### GitLab

**What it does**: MR management, pipeline status, container registry, wiki.

**Prerequisites**: GitLab Personal Access Token.

**Skills enhanced**: `soprasteria-dep`, `pr-checks`

**Configuration**:
```json
{
  "servers": {
    "gitlab": {
      "command": "npx",
      "args": ["@gitlab/mcp-server@latest"],
      "env": {
        "GITLAB_TOKEN": "${input:GITLAB_TOKEN}",
        "GITLAB_URL": "${input:GITLAB_URL}"
      }
    }
  }
}
```

**Troubleshooting**: Token needs `api` or `read_api` scope. Check URL is correct (self-hosted vs gitlab.com).

---

### Azure DevOps (Local)

**What it does**: Work items, boards, pipelines, artifact feeds (self-hosted).

**Prerequisites**: Azure DevOps PAT with appropriate scopes.

**Skills enhanced**: `sdlc-steer-planning`, `sdlc-steer-sprint`, `pr-checks`

**Configuration**:
```json
{
  "servers": {
    "azdo-local": {
      "command": "npx",
      "args": ["@microsoft/azure-devops-mcp@latest"],
      "env": {
        "AZURE_DEVOPS_ORG": "${input:AZURE_DEVOPS_ORG}",
        "AZURE_DEVOPS_PAT": "${input:AZURE_DEVOPS_PAT}"
      }
    }
  }
}
```

---

### Azure DevOps (Remote)

**What it does**: Same as local, via Azure-hosted remote MCP endpoint.

**Prerequisites**: Azure DevOps remote MCP URL configured.

**Configuration**:
```json
{
  "servers": {
    "azdo-remote": {
      "url": "${input:AZURE_DEVOPS_MCP_URL}"
    }
  }
}
```

---

### Atlassian

**What it does**: Jira issue CRUD, Confluence page management, Bitbucket integration.

**Prerequisites**: Atlassian API token + site URL.

**Skills enhanced**: `sdlc-confluence-sync`, all SDLC agents with Jira integration

**Configuration**:
```json
{
  "servers": {
    "atlassian": {
      "command": "npx",
      "args": ["@atlassian/mcp-server@latest"],
      "env": {
        "ATLASSIAN_SITE": "${input:ATLASSIAN_SITE}",
        "ATLASSIAN_API_TOKEN": "${input:ATLASSIAN_API_TOKEN}",
        "ATLASSIAN_EMAIL": "${input:ATLASSIAN_EMAIL}"
      }
    }
  }
}
```

**Troubleshooting**: Site should be `your-org.atlassian.net`. Token created at [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens).

---

### Work-iq (Microsoft 365)

**What it does**: Query M365 data — emails, meetings, Teams messages, OneDrive, people.

**Prerequisites**: Node.js 18+, **Entra tenant admin consent** (see [admin guide](https://github.com/microsoft/work-iq/blob/main/ADMIN-INSTRUCTIONS.md)).

**Skills enhanced**: `sdlc-steer-governance`, `sdlc-steer-sprint`

> **Important**: All M365 data is automatically scanned for PII and redacted before inclusion in outputs.

**Configuration**:
```json
{
  "servers": {
    "workiq": {
      "command": "npx",
      "args": ["-y", "@microsoft/workiq", "mcp"]
    }
  }
}
```

**Troubleshooting**: Run `npx -y @microsoft/workiq accept-eula` first. Contact your tenant admin for consent.

---

### MsLearn

**What it does**: Query Microsoft Learn for .NET, Azure, M365, PowerShell documentation.

**Prerequisites**: None.

**Skills enhanced**: `docs-architect`, `api-documentation`, `dotnet-backend`

**Configuration**:
```json
{
  "servers": {
    "mslearn": {
      "command": "npx",
      "args": ["@microsoftdocs/mcp@latest"]
    }
  }
}
```

---

### Context7

**What it does**: Fetch up-to-date, version-specific documentation for any library or framework.

**Prerequisites**: None (API key optional for higher rate limits).

**Skills enhanced**: `code-implementation`, `code-refactoring`, all framework-specific skills

> **Recommended for all consumers** — prevents code generation based on outdated training data.

**Configuration**:
```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

For higher rate limits, add API key from [context7.com/dashboard](https://context7.com/dashboard):
```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "CONTEXT7_API_KEY": "${input:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

---

### Playwright

**What it does**: Browser automation via accessibility snapshots — navigate, interact, inspect, record tests.

**Prerequisites**: Node.js 18+.

**Skills enhanced**: `sdlc-test-campaign`, `sdlc-tech-quality`

**Configuration**:
```json
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

For headless mode (CI): add `"--headless"` to args.

---

### SemGrep

**What it does**: Run SAST rules, query rule registry, get fix suggestions.

**Prerequisites**: `pip install semgrep`.

**Skills enhanced**: `security-scan`, `static-analysis`

**Configuration**:
```json
{
  "servers": {
    "semgrep": {
      "command": "semgrep",
      "args": ["mcp"]
    }
  }
}
```

For Semgrep Cloud rules (optional):
```json
{
  "env": {
    "SEMGREP_APP_TOKEN": "${input:SEMGREP_APP_TOKEN}"
  }
}
```

---

### SonarQube

**What it does**: Code quality and security analysis — retrieve issues, quality gate status, coverage, duplications, security hotspots, and metrics from SonarQube Server or SonarQube Cloud.

**Prerequisites**: Docker (or any OCI-compatible runtime). SonarQube Server 2025.1+, SonarQube Cloud, or SonarQube Community Build. A SonarQube user token.

**Skills enhanced**: `static-analysis`, `security-scan`, `quality-report`

**Configuration** (SonarQube Cloud):
```json
{
  "servers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init", "--pull=always",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_ORG",
        "mcp/sonarqube"
      ],
      "env": {
        "SONARQUBE_TOKEN": "${input:SONARQUBE_TOKEN}",
        "SONARQUBE_ORG": "${input:SONARQUBE_ORG}"
      }
    }
  }
}
```

**Configuration** (SonarQube Server / Community Build):
```json
{
  "servers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init", "--pull=always",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "mcp/sonarqube"
      ],
      "env": {
        "SONARQUBE_TOKEN": "${input:SONARQUBE_TOKEN}",
        "SONARQUBE_URL": "${input:SONARQUBE_URL}"
      }
    }
  }
}
```

To disable telemetry, add `"-e", "TELEMETRY_DISABLED"` to `args` and `"TELEMETRY_DISABLED": "true"` to `env`.

**Troubleshooting**: Ensure Docker is running. Verify token with the SonarQube API (`/api/authentication/validate`). For SonarQube Cloud US region, set `SONARQUBE_URL` to `https://sonarqube.us`.

> See [SonarQube MCP Server docs](https://docs.sonarsource.com/sonarqube-mcp-server) for advanced configuration (HTTPS transport, team deployments, SonarQube for IDE integration).

---

### Figma

**What it does**: Read Figma designs, extract component specs, validate against design tokens.

**Prerequisites**: Figma Personal Access Token.

**Skills enhanced**: `sdlc-ba-functional-design`, `brand-audit`

**Configuration**:
```json
{
  "servers": {
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server@latest"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${input:FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

---

## Fallback Behavior

Every workflow runs without any MCP server. When a server is unavailable, skills degrade gracefully:

| Category | With MCP | Without MCP |
|----------|----------|-------------|
| Cloud (Azure, AWS) | Live resource queries, IaC drift detection | Local IaC templates, manual portal checks |
| DevOps (GitHub, GitLab, ADO) | Live PR/pipeline/issue data | Local git/diff, manual platform UI |
| Documentation (MsLearn, Context7) | Current, verified API docs | Agent training knowledge + `[DOCS-NOT-VERIFIED]` markers |
| Testing (Playwright, SemGrep) | Live browser/SAST execution | CLI tools or regex-based pattern scans |
| Quality (SonarQube) | Live issues, quality gates, coverage metrics | SonarQube CLI scanner, local linters (ESLint, Pylint) |
| Collaboration (Atlassian, Work-iq) | Live Jira/M365 data | Manual input, local Markdown files |
| Design (Figma) | Bidirectional design sync | Local HTML prototypes |

---

## Version Management

By default, servers use `@latest`. To pin a specific version:

```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@1.2.0"]
    }
  }
}
```

The canonical versions are in `.apm/contexts/mcp-registry.yaml`. Consumer overrides in `.vscode/mcp.json` take precedence.

---

## Client-Specific Overrides

For client-specific MCP configurations, create `clients/<name>/mcp-overrides.yaml`:

```yaml
# clients/acme/mcp-overrides.yaml
overrides:
  atlassian-mcp:
    install:
      env:
        ATLASSIAN_SITE: acme.atlassian.net
  context7:
    default_version: '@1.0.0'
additions: []
removals: []
```

These overrides are merged on top of profile defaults during configuration generation.

---

## Verify Connectivity

After configuring MCP servers, verify connectivity:

```
@hub-orchestrator verify MCP
```

Or use the `mcp-configuration` skill directly:

```
/workflow-configure-mcp verify
```

This checks each configured server for:
- Environment variables set
- Server reachable
- Authentication valid

---

## Security

- **Credentials**: Never stored in configuration files — always use `${input:VAR}` placeholders that prompt at runtime.
- **Data handling**: All MCP-returned data is treated as untrusted input and sanitised.
- **M365 data**: Mandatory PII redaction on all Work-iq data before inclusion in outputs.
- **Audit trail**: External MCP usage is logged in the audit trace with a ×1.5 risk multiplier.
- **Scope**: Playwright restricted to project domain/localhost. SemGrep restricted to workspace files.

---

## Troubleshooting

### "MCP server not found"

Ensure Node.js 18+ is installed: `node --version`. Most servers are distributed via npm/npx.

### "Authentication failed"

Check that the required environment variable is set in your terminal session. VS Code `${input:VAR}` prompts at startup — check the notification area.

### "Server timeout"

Some MCP servers need initial setup time. Try increasing timeout or running the server manually first to complete any one-time setup (e.g., `workiq accept-eula`).

### "Rate limited" (Context7)

Get a free API key at [context7.com/dashboard](https://context7.com/dashboard) and set `CONTEXT7_API_KEY`.
