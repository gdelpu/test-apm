# APM Bundle Distribution

> How to build, publish, and consume APM bundles from the `ai-sdlc-foundation` repository.

---

## Overview

The AI SDLC Foundation produces **APM bundles** — self-contained archives of
agents, skills, workflows, prompts, and knowledge — packaged per target runtime.

Two distribution channels are available:

| Channel | Trigger | Lifetime | Use Case |
|---------|---------|----------|----------|
| **GitLab Job Artifacts** | Every branch/tag push | 14 days | CI consumption, testing, previews |
| **GitLab Generic Package Registry** | Tag push only | Permanent | Versioned cross-project distribution |

---

## Pipeline Flow

```text
Branch push                        Tag push (e.g. v1.2.0)
    │                                  │
    ├─ validate (MR only)              ├─ validate (MR only)
    ├─ stations (MR only)              ├─ stations (MR only)
    │                                  │
    ├─ build:apm-bundles ─────────┐    ├─ build:apm-bundles ─────────┐
    │   apm install               │    │   apm install               │
    │   apm pack --target copilot │    │   apm pack --target copilot │
    │   apm pack --target claude  │    │   apm pack --target claude  │
    │   apm pack --target all     │    │   apm pack --target all     │
    │   SHA-256 checksums         │    │   SHA-256 checksums         │
    │                             │    │                             │
    ├─ test:apm-smoke ────────────┘    ├─ test:apm-smoke ────────────┘
    │   verify archive integrity       │   verify archive integrity
    │                                  │
    └─ dist/ as job artifacts ─────    ├─ publish:apm-registry
              (14 days)                │   curl → Generic Package Registry
                                       │   version = CI_COMMIT_TAG
                                       └─ permanent versioned packages
```

---

## Semantic Versioning

Tags **must** follow [Semantic Versioning](https://semver.org/):

```
v<MAJOR>.<MINOR>.<PATCH>[-prerelease][+build]
```

| Tag Example | Meaning |
|-------------|---------|
| `v1.0.0` | Initial stable release |
| `v1.1.0` | New agents/skills/workflows added (backward-compatible) |
| `v2.0.0` | Breaking changes to canonical structure |
| `v1.2.0-rc.1` | Release candidate |

The publish script strips the leading `v` when registering the package version.

### Creating a release

```bash
git tag -a v1.2.0 -m "Release 1.2.0 — add SDLC harness workflows"
git push origin v1.2.0
```

This triggers: `build:apm-bundles` → `publish:apm-registry`.

---

## Built Archives

The build job produces the following archives in `dist/`:

| Archive | Contents |
|---------|----------|
| `ssg-ai-backbone-copilot.tar.gz` | GitHub Copilot runtime bundle |
| `ssg-ai-backbone-claude.tar.gz` | Claude Code runtime bundle |
| `ssg-ai-backbone-all.tar.gz` | Complete bundle (all targets) |
| `SHA256SUMS` | Integrity checksums for all archives |

### Bundle Contents

Each bundle includes the canonical APM assets as declared in `apm.yml`:

| Layer | Path | Included |
|-------|------|----------|
| Agents | `.apm/agents/` | ✅ All bundles |
| Skills | `.apm/skills/` | ✅ All bundles |
| Prompts | `.apm/prompts/` | ✅ All bundles |
| Instructions | `.apm/instructions/` | ✅ All bundles |
| Contexts | `.apm/contexts/` | ✅ All bundles |
| Workflows | `.apm/workflows/` | ✅ All bundles |
| Knowledge | `knowledge/` | ✅ All bundles |

The **knowledge/** folder is distributed intentionally — it contains the
constitution, governance schemas, playbooks, and brand assets that agents and
skills reference at runtime. Excluding it would produce incomplete bundles.

| Knowledge Area | Contents |
|----------------|----------|
| `knowledge/constitution/` | Engineering principles, enterprise defaults, greenfield/brownfield guides |
| `knowledge/governance/` | Architecture principles, security/testing policies, JSON schemas |
| `knowledge/playbooks/` | Brownfield, greenfield, modernization, workflow playbooks |
| `knowledge/brand/` | Sopra Steria brand guidelines, icons, logos, templates |

---

## Install Modes

The installer supports two modes via the `-Mode` / `--mode` flag:

| Aspect | Standard (default) | Expandable |
|--------|-------------------|------------|
| **What's delivered** | Runtime directory only (e.g. `.github/`) | Full source tree + runtime projection |
| **What's committed** | `.github/` + `.apm.lock.yaml` | Everything except generated runtime dirs |
| **Canonical content** | Projected inline into runtime dir | Stays in `.apm/` as-is |
| **`providers-local/`** | Not available | Scaffolded for local overrides |
| **Path references** | Rewritten to runtime paths | Original `.apm/` paths preserved |
| **Update behavior** | Replaces runtime dir entirely | Replaces upstream, preserves `providers-local/` |
| **Best for** | Quick consumption, CI integration | Customization, contributing back |

### Standard Mode Directory Layout

```
my-project/
  .github/
    agents/
    prompts/
    instructions/
    skills/
    workflows/
    contexts/
    templates/
    knowledge/
    copilot-instructions.md
  .apm.lock.yaml
```

### Expandable Mode Directory Layout

```
my-project/.apm-dist/
  .apm/
    agents/
    skills/
    workflows/
    ...
  providers/
    github-copilot/
      agents/
      prompts/
      instructions/
  providers-local/
    github-copilot/
      agents/
      prompts/
      instructions/
      README.md
  knowledge/
  .github/           ← generated by projection
  .apm.lock.yaml
  .gitignore
```

### Provider Selection

Both modes accept a `--provider` flag (default: `github-copilot`). The
projection script reads `apm.yml` to resolve provider adapter and runtime paths,
making the system provider-agnostic.

Available providers are defined in `apm.yml` under the `providers:` key.

### Lock File (.apm.lock.yaml)

Both modes produce a `.apm.lock.yaml` at the install root. This file records:

- **version** — installed APM version
- **mode** — standard or expandable
- **provider** — which provider adapter was projected
- **timestamps** — install and last update times
- **source** — package name, archive filename, SHA-256 checksum

The installer detects an existing lock file and handles updates appropriately:
standard mode replaces the runtime directory; expandable mode preserves
`providers-local/` and re-projects.

---

## Consumer Guide

### Option 1: GitLab Generic Package Registry

Use this for **versioned, stable consumption** in other projects.

#### curl (any CI/CD or local)

```bash
# Set your variables
GITLAB_URL="https://gitlab.com"      # or your self-hosted instance
PROJECT_ID="12345"                    # source project ID
VERSION="1.2.0"
TARGET="copilot"                      # copilot (default) | claude | all
TOKEN="${GITLAB_TOKEN}"               # Private-Token or Job-Token

# Download
curl --header "PRIVATE-TOKEN: ${TOKEN}" \
  -o "ssg-ai-backbone-${TARGET}.tar.gz" \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/packages/generic/ssg-ai-backbone/${VERSION}/ssg-ai-backbone-${TARGET}.tar.gz"

# Verify checksum
curl --header "PRIVATE-TOKEN: ${TOKEN}" \
  -o SHA256SUMS \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/packages/generic/ssg-ai-backbone/${VERSION}/SHA256SUMS"

sha256sum --check --ignore-missing SHA256SUMS

# Extract
tar -xzf "ssg-ai-backbone-${TARGET}.tar.gz"
```

#### Consumer `.gitlab-ci.yml` example (Package Registry)

```yaml
variables:
  APM_SOURCE_PROJECT_ID: "12345"
  APM_VERSION: "1.2.0"
  APM_TARGET: "copilot"               # default target

stages:
  - setup
  - build

install-apm:
  stage: setup
  image: node:20-bookworm-slim
  script:
    - |
      curl --fail --silent --show-error \
        --header "JOB-TOKEN: ${CI_JOB_TOKEN}" \
        -o "ssg-ai-backbone-${APM_TARGET}.tar.gz" \
        "${CI_API_V4_URL}/projects/${APM_SOURCE_PROJECT_ID}/packages/generic/ssg-ai-backbone/${APM_VERSION}/ssg-ai-backbone-${APM_TARGET}.tar.gz"
    - tar -xzf "ssg-ai-backbone-${APM_TARGET}.tar.gz" -C .apm-dist/
  artifacts:
    paths:
      - .apm-dist/
    expire_in: 1 day

build:
  stage: build
  needs: [install-apm]
  script:
    - echo "APM bundle available in .apm-dist/"
    - ls -la .apm-dist/
```

> **Note**: Cross-project `CI_JOB_TOKEN` access requires the source project to
> allow the consuming project in **Settings → CI/CD → Token Access**.

### Option 2: Upstream Artifacts (Pipeline Trigger)

Use this for **CI-to-CI consumption** when you want the latest build from a
specific branch or pipeline.

#### Consumer `.gitlab-ci.yml` example (Upstream Artifacts)

```yaml
variables:
  APM_SOURCE_PROJECT: "group/ai-sdlc-foundation"
  APM_SOURCE_REF: "main"

stages:
  - setup
  - build

fetch-apm:
  stage: setup
  trigger:
    project: ${APM_SOURCE_PROJECT}
    branch: ${APM_SOURCE_REF}
    strategy: depend
  # This triggers the upstream pipeline; use needs:project for artifacts

use-apm:
  stage: build
  needs:
    - project: ${APM_SOURCE_PROJECT}
      job: build:apm-bundles
      ref: ${APM_SOURCE_REF}
      artifacts: true
  script:
    - echo "APM archives available in dist/"
    - ls -la dist/
```

> **Note**: Upstream artifact access requires the consuming project to be in
> the same group hierarchy or have explicit CI/CD job token permissions.

### Option 3: Install Scripts

Pre-built install scripts simplify consumption for developers and CI pipelines.

#### Linux / macOS

```bash
# Download the installer (or copy from the source repo)
curl -o install-apm-bundle.sh \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/repository/files/scripts%2Finstall-apm-bundle.sh/raw?ref=main" \
  --header "PRIVATE-TOKEN: ${TOKEN}"

chmod +x install-apm-bundle.sh

# Standard mode (default) — runtime projection only
./install-apm-bundle.sh \
  --version 1.2.0 \
  --target copilot \
  --project-id 12345 \
  --token "${GITLAB_TOKEN}"

# Expandable mode — full source with local override support
./install-apm-bundle.sh \
  --version 1.2.0 \
  --target copilot \
  --mode expandable \
  --project-id 12345 \
  --token "${GITLAB_TOKEN}"
```

#### Windows (PowerShell)

```powershell
# Download the installer (or copy from the source repo)
Invoke-WebRequest -Uri "$GitLabUrl/api/v4/projects/$ProjectId/repository/files/scripts%2Finstall-apm-bundle.ps1/raw?ref=main" `
  -Headers @{ 'PRIVATE-TOKEN' = $Token } `
  -OutFile install-apm-bundle.ps1

# Standard mode (default)
.\install-apm-bundle.ps1 `
  -Version 1.2.0 `
  -Target copilot `
  -ProjectId 12345 `
  -Token $env:GITLAB_TOKEN

# Expandable mode
.\install-apm-bundle.ps1 `
  -Version 1.2.0 `
  -Target copilot `
  -Mode expandable `
  -ProjectId 12345 `
  -Token $env:GITLAB_TOKEN
```

---

## Local Build

You can build bundles locally without CI/CD:

```bash
cd ai-sdlc-foundation

# Build all targets
bash scripts/apm-build.sh

# Build specific targets
bash scripts/apm-build.sh --targets copilot,claude

# Dry-run publish (prints upload commands)
bash scripts/apm-publish.sh --version 1.2.0 --dry-run
```

---

## Troubleshooting

### Protected Tags (Recommended)

Configure **protected tags** in GitLab to prevent unauthorized publishes:

1. Go to **Settings → Repository → Protected Tags**
2. Add pattern: `v*`
3. Set "Allowed to create" to **Maintainers** (or a deploy key)

This ensures only authorized users can push semver tags that trigger registry
publishing.

### Build job fails with "apm: command not found"

The `build:apm-bundles` job installs `@anthropic/apm` globally via npm. Verify
your runner has internet access and npm registry connectivity.

### Publish returns HTTP 403

- Ensure `CI_JOB_TOKEN` has write access to the package registry
- Check **Settings → CI/CD → Token Permissions** on the source project

### Consumer gets HTTP 404 for a package

- Verify the version tag exists: `git tag -l 'v*'`
- Confirm the publish job succeeded for that tag
- Check the exact package name and version in **Packages & Registries**

### Cross-project CI_JOB_TOKEN fails

The source project must explicitly allow the consuming project:
1. Go to source project → **Settings → CI/CD → Token Access**
2. Add the consuming project to the allow list

### Checksum verification fails

Re-download the archive and checksums file. If the issue persists, the package
may have been corrupted during upload — re-run the tag pipeline.
