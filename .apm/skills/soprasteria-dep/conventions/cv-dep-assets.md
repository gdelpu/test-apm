---
name: cv-dep-assets
description: 'Convention providing the DEP-Agents with structured knowledge about CI Library, Modern Workstation, and DEP Launchpad assets.'
triggers: ['DEP asset reference', 'CI Library lookup', 'Modern Workstation module', 'Launchpad IaC resource']
---

# Convention: DEP Assets Knowledge Base

## Purpose

This convention provides the DEP-Agents with structured knowledge about the three DEP assets they promote: **CI Library**, **Modern Workstation**, and **DEP Launchpad**. It is the authoritative reference for every configuration choice made by DEP agents.

---

## 1. DEP CI Library

### What it is
A GitLab CI/CD job library providing 56+ reusable jobs across 13+ pipeline stages. Include it in any project `.gitlab-ci.yml` with a single `include` directive.

### Standard include
```yaml
include:
  - project: "dep/library/ci-library"
    ref: production
    file: "main.yml"
```

### Pipeline stages (ordered)
`init` → `lint` → `build-application` → `test-application` → `build-image` → `analysis` → `analysis2` → `security-check` → `deploy` → `pre-acceptance` → `acceptance` → `performance` → `release` → `post-release` → `destroy`

### Key job families

| Family | Stage | Jobs | When to use |
|--------|-------|------|-------------|
| Branch/commit validation | init | `branch-lint`, `commit-lint` | Always |
| Secret detection | lint | `gitleaks` | Always |
| Dockerfile linting | lint | `hadolint` | When project has a Dockerfile |
| IaC security | lint | `kics` | When project has Terraform/IaC |
| Shell linting | lint | `shellcheck` | When project has shell scripts |
| Build | build-application | `build-application` | Always |
| Tests | test-application | `test-application` | Always |
| Container build | build-image | `build-image` | When project delivers a container image |
| Code quality | analysis | `sonarqube` | Always (mandatory quality gate) |
| SAST | analysis | `checkmarx` | Projects with security requirements |
| Dependency vuln. | analysis | `snyk`, `dependency-check` | Always for production apps |
| Container scan | analysis | `trivy` | When project has a container image |
| SBOM | analysis | `sbom-image`, `sbom-binary` | Production applications |
| Security gate | security-check | `defectdojo`, `dependency-track` | Always for production apps |
| Deployment | deploy | `helm-kubernetes`, `helm-openshift`, `azure-swa`, `iac` | Per target platform |
| AI MR review | analysis | `mr-agent` | All projects (reduces review effort) |
| Acceptance | acceptance | `functional-test`, `owasp-zap` | Production apps |
| Release | release | `tag-version`, `bump-version` | Versioned projects |
| Maintenance | post-release | `renovatebot` | All projects (dependency hygiene) |

### Branch strategy variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MAIN_BRANCH_REGEX` | `^(main\|master\|dev.*)$` | Main branches |
| `TEST_BRANCH_REGEX` | `^(staging\|pre-prod\|qualif\|qa\|test.*)$` | Test branches |
| `PRODUCTION_BRANCH_REGEX` | `^(prod\|rel.*)$` | Production branches |

### Version management: supported project files
`pom.xml`, `package.json`, `.csproj`, `setup.py`, `pyproject.toml`, `build.gradle`, `composer.json`, `VERSION` file

---

## 2. Modern Workstation

### What it is
A cross-platform workstation automation tool (Windows 10+, Linux Debian/Ubuntu) with 30+ modules configurable via a single `mw-config.yml` YAML file.

### CLI usage
```bash
mwctl module configure <module-name>   # Install & configure
mwctl module start <module-name>       # Start service
mwctl module stop <module-name>        # Stop service
mwctl module unconfigure <module-name> # Remove
```

### Available modules by category

| Category | Modules | Notes |
|----------|---------|-------|
| Databases | `postgresql` (v10–15), `mysql`, `mariadb`, `mongodb` | Version-specific |
| Runtime | `java`, `nodejs`, `nvm`, `maven` | Multiple versions supported |
| Containers | `podman` (v4) | Includes podman machine |
| Source control | `git` | Repos + certificates |
| IDEs | `vscode`, `intellij`, `eclipse`, `soapui` | With plugin/extension support |
| SSH/Remote | `ssh`, `putty`, `winscp`, `mobaxterm`, `mremoteng` | Corporate VPN-compatible |
| System | `wsl2`, `notepad++`, `hosts`, `keepass`, `keepassxc` | WSL2 with VPN support |
| Database UI | `dbeaver` | — |
| File transfer | `filezilla` | — |

### mw-config.yml structure
```yaml
modules:
  - name: <module-name>
    version: <version>           # optional, uses latest if omitted
    configuration:
      <key>: <value>             # module-specific config
  - name: <module-name>
    path: <external-module-path> # for custom/external modules
```

### Selection rules
- **Always include:** `git`
- **Include per stack:** match project tech stack to modules (Java → `java` + `maven`; Node.js → `nodejs` or `nvm`; databases → matching DB module)
- **Include per role:** developer = IDE; ops/devops = `ssh` + remote tools
- **Corporate environments:** always include `wsl2` for Windows users who need Linux tooling

---

## 3. DEP Launchpad (IaC)

### What it is
An Infrastructure-as-Code platform wrapper supporting Azure, AzureStack, and AWS. One launchpad instance per project environment (dev, staging, prod). Manages cloud resource creation and lifecycle.

### Supported platforms

| Cloud | Resources | Notes |
|-------|-----------|-------|
| Azure | VMs, AKS, App Services, Storage, Networking, KeyVault | Full support |
| AzureStack | Subset of Azure resources | For on-premise cloud |
| AWS | EC2, EKS, S3, RDS, VPC | Full support |

### Configuration files structure
```
launchpad/
├── environments/
│   ├── dev/
│   │   └── variables.tf (or vars.yml)
│   ├── staging/
│   │   └── variables.tf (or vars.yml)
│   └── prod/
│       └── variables.tf (or vars.yml)
├── modules/
│   └── <resource-type>/        # reusable IaC modules
├── main.tf (or main.yml)       # root configuration
└── README.md
```

### Launchpad selection rules
- One launchpad per **environment** (dev ≠ staging ≠ prod)
- Match cloud provider to project requirements from `[CTX-001]`
- Always define: networking, IAM/permissions, core compute/containers, storage
- Always separate: environment-specific variables from shared modules

### Integration with CI Library
The `iac` deploy job in ci-library triggers the launchpad:
```yaml
variables:
  IAC_TOOL: terraform          # or ansible, helm
  IAC_PATH: launchpad/
  DEPLOY_ENV: $CI_ENVIRONMENT_NAME
```

---

## 4. DEP Project Booster

### What it is
A platform API for automated provisioning of environments, databases, CI/CD pipelines, and application scaffolding on InnerShift (public cloud OpenShift) and Arcus (on-premise OpenShift). Accessible via REST API and CLI tool.

### CLI tool
Located at `scripts/project-booster/`. Run with:
```bash
python -m project_booster <command> [options]
```

### Supported scenario types

| Type | Description | Target |
|------|-------------|--------|
| `new_web_app` | Create web application (mono or multi-component) | InnerShift / Arcus |
| `new_web_doc` | Create static documentation site (GitLab Pages) | Innersource |
| `new_tool` | Deploy tool/service (Nexus, Vault, SonarQube, …) | Arcus |
| `update_service` | Update an existing deployed service | InnerShift / Arcus |
| `new_database` | Deploy standalone database | InnerShift |
| `update_database` | Update an existing database | InnerShift |
| `new_launchpad` | Deploy infrastructure on cloud (Azure, AWS) | Cloud |
| `new_repository` | Create Artifactory repository | Artifactory |
| `configure_kube_green_for_service` | Configure Kube-Green (Arcus) | Arcus |
| `configure_kube_green_for_app` | Configure Kube-Green (InnerShift) | InnerShift |
| `configure_kasten_for_service` | Configure Kasten backup (Arcus) | Arcus |
| `configure_kasten_for_app` | Configure Kasten backup (InnerShift) | InnerShift |
| `remove_resources_for_service` | Remove resources (Arcus) | Arcus |
| `remove_resources_for_application` | Remove resources (InnerShift) | InnerShift |

### Supported databases

| Engine | Versions | Notes |
|--------|----------|-------|
| PostgreSQL | Platform-managed | Deployed on InnerShift |
| MySQL | Platform-managed | Deployed on InnerShift |
| MongoDB | Platform-managed | Deployed on InnerShift |
| Elasticsearch | Platform-managed | Deployed on InnerShift |

### Deployable tools

| Tool | Purpose |
|------|---------|
| SonarQube | Code quality analysis |
| Nexus | Artifact repository |
| Vault | Secrets management |
| DefectDojo | Security vulnerability management |
| Dependency-Track | Dependency vulnerability tracking |
| Packmind | Code pattern detection |
| Suricate | Security monitoring |

### Provisioning flow
1. **Check orchestrator** — verify connectivity to InnerShift/Arcus
2. **Verify/create namespace** — test namespace creation or writability
3. **Set quotas & role bindings** — configure resource limits and RBAC
4. **Create scenario** — define what to provision (app, db, tool)
5. **Trigger pipeline** — start automated provisioning
6. **Wait for completion** — poll until COMPLETED / FAILED
7. **Retrieve credentials** — database connections, GitLab tokens

### Selection rules
- **Databases** → `new_database` on InnerShift (close to application workloads)
- **Applications** → `new_web_app` on InnerShift (includes GitLab project + CI/CD)
- **Shared tools** → `new_tool` on Arcus (shared infrastructure)
- **Always** check orchestrator connectivity before provisioning
- **Always** set resource quotas on namespaces
- **Always** provision dev first, then staging, then prod
- **Never** provision production without explicit confirmation
