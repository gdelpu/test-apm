---
name: sk-dep4.1-project-booster
description: 'Provision environments, databases, applications, tools, and CI/CD pipelines on InnerShift/Arcus via the Project Booster API.'
triggers: ['DEP Project Booster', 'InnerShift', 'Arcus', 'database provisioning', 'project booster', 'environment creation', 'namespace creation', 'deploy database', 'deploy application']
---

# Skill DEP-4.1: DEP Project Booster — Provisioning Capabilities

## Identity

- **ID:** sk-dep4.1-project-booster
- **System:** System DEP4 – Environment & Pipeline Provisioning
- **Tool:** `scripts/project-booster/` (Python CLI + API client)

## Purpose

This skill provides agents with the capability to provision resources on the DEP Project Booster platform. Any agent needing to create environments, databases, applications, or tools can use this skill. The agent decides **what** to provision based on its own context; this skill describes **how**.

## Prerequisites

The Project Booster CLI must be configured before use:

```bash
# Option A: interactive init
python -m project_booster init

# Option B: environment variables
export PROJECT_BOOSTER_TOKEN="glpat-..."
export PROJECT_BOOSTER_URL="https://project-booster.dep.soprasteria.com"
```

If not configured, every command will fail with a clear error message.

---

## Available capabilities

### Capability 1 — Discover available scenario types

Before provisioning, an agent can query the platform to discover what's available:

```bash
python -m project_booster scenario-types
python -m project_booster config
```

Known scenario types:

| Type | Creates | Includes CI/CD? |
|------|---------|-----------------|
| `new_web_app` | GitLab project(s) + CI/CD pipeline + deployment on InnerShift/Arcus | **Yes** — full GitLab CI pipeline |
| `new_web_doc` | Static documentation site (GitLab Pages) | Yes |
| `new_database` | Standalone database instance (PostgreSQL, MySQL, MongoDB, Elasticsearch) | No |
| `update_database` | Updates an existing database | No |
| `new_tool` | Tool/service (SonarQube, Nexus, Vault, DefectDojo, …) on Arcus | Depends on tool |
| `update_service` | Updates an existing deployed service | No |
| `new_launchpad` | Infrastructure on cloud (Azure, AWS, AzureStack) | No |
| `new_repository` | Artifactory repository | No |
| `configure_kube_green_for_app` | Kube-Green sleep schedule on InnerShift | No |
| `configure_kube_green_for_service` | Kube-Green sleep schedule on Arcus | No |
| `configure_kasten_for_app` | Kasten backup on InnerShift | No |
| `configure_kasten_for_service` | Kasten backup on Arcus | No |
| `remove_resources_for_application` | Removes resources from InnerShift | No |
| `remove_resources_for_service` | Removes resources from Arcus | No |

> **Note:** `new_web_app` is the only scenario that creates CI/CD pipelines. There is no standalone "create CI" scenario — CI is bundled with application creation.

---

### Capability 2 — Environment management (namespaces)

Manage InnerShift and Arcus namespaces. The `type` parameter is the orchestrator: `innershift`, `arcus`, or any platform-specific value.

**Check connectivity:**
```bash
python -m project_booster env check <type>
```

**List namespaces:**
```bash
python -m project_booster env namespaces <type> --page 0 --size 50
```

**Test if a namespace can be created:**
```bash
python -m project_booster env test-create <type> <namespace-name>
```

**Test if an existing namespace is writable:**
```bash
python -m project_booster env test-write <type> <namespace-name>
```

**Get namespace details:**
```bash
python -m project_booster env details <type> <namespace-name>
```

**List services deployed in a namespace:**
```bash
python -m project_booster env services <type> <namespace-name>
```

**Get a specific service by release name:**
```bash
python -m project_booster env service <type> <namespace-name> <release-name>
```

**Create role bindings (RBAC):**
```bash
python -m project_booster env role-binding <type> <namespace> \
  --body '{"group": "<team>", "role": "edit"}'
```

**Set resource quotas:**
```bash
python -m project_booster env quotas <type> <namespace> \
  --body '{"cpu": "4", "memory": "8Gi"}'
```

---

### Capability 3 — Deploy a database

Supported engines: `postgresql`, `mysql`, `mongodb`, `elasticsearch`.

**End-to-end (create scenario + pipeline + wait + return credentials):**
```bash
python -m project_booster deploy db <engine> <namespace> \
  --orch-type innershift \
  --timeout 900
```

**With extra inputs:**
```bash
python -m project_booster deploy db postgresql my-ns \
  --extra-inputs '{"version": "15", "storageSize": "10Gi"}'
```

The command blocks until the pipeline completes and returns a JSON with:
- `scenario` — the created scenario object
- `pipeline` — final pipeline status and actions
- `credentials` — database connection details (host, port, user, password)

**Manual step-by-step alternative:**
```bash
# 1. Create scenario
python -m project_booster scenarios create --type new_database \
  --inputs '{"databaseType": "postgresql", "namespace": "my-ns", "orchestratorType": "innershift"}'

# 2. Trigger pipeline (use the scenario ID from step 1)
python -m project_booster pipeline run <scenario-id>

# 3. Wait for completion
python -m project_booster pipeline wait <scenario-id> --timeout 900

# 4. Get credentials
python -m project_booster pipeline creds <scenario-id>
```

---

### Capability 4 — Deploy a web application (includes CI/CD)

Creates GitLab project(s) with CI/CD pipelines and deploys to InnerShift/Arcus.

**End-to-end:**
```bash
python -m project_booster deploy app <app-name> <namespace> \
  --orch-type innershift \
  --timeout 900
```

**With component definitions:**
```bash
python -m project_booster deploy app my-app my-ns \
  --components '[
    {"name": "backend", "technology": "java", "template": "spring-boot"},
    {"name": "frontend", "technology": "angular"}
  ]'
```

**What the pipeline creates:**
1. GitLab group and subgroup on Innersource
2. GitLab project per component (backend, frontend, …)
3. Pre-configured CI/CD pipeline in each project (DEP CI Library)
4. InnerShift/Arcus namespace (if not existing)
5. Initial deployment of all components

The returned `credentials` include GitLab project URLs and access tokens.

---

### Capability 5 — Deploy a tool or service

Deploy shared tools on Arcus (or InnerShift):

```bash
python -m project_booster deploy run --type new_tool \
  --inputs '{"toolType": "sonarqube", "namespace": "tools-ns", "orchestratorType": "arcus"}' \
  --timeout 900
```

Available tools: `sonarqube`, `nexus`, `vault`, `defectdojo`, `dependency-track`, `packmind`, `suricate`.

---

### Capability 6 — Generic scenario deployment

For any scenario type not covered by the shortcuts:

```bash
python -m project_booster deploy run --type <scenario-type> \
  --inputs '<json-inputs>' \
  --timeout <seconds>
```

The `inputs` JSON structure varies per scenario type. Use `python -m project_booster config` to discover available input schemas from the platform.

---

### Capability 7 — Manage secrets

Store credentials used by the platform:

```bash
# List secrets
python -m project_booster secrets list

# Create a secret
python -m project_booster secrets create \
  --key https://gitlab.example.com --value glpat-xxx \
  --type openshift --label "My GitLab token"

# Delete a secret
python -m project_booster secrets delete <id>
```

---

### Capability 8 — Manage Artifactory repositories

```bash
python -m project_booster artifactory repos
python -m project_booster artifactory create-repos \
  --body '{"key": "my-repo", "rclass": "local"}'
```

---

### Capability 9 — Query scenario and pipeline status

```bash
# List all scenarios
python -m project_booster scenarios list

# Get scenario details
python -m project_booster scenarios get <id>

# Get pipeline status
python -m project_booster pipeline status <id>

# Get pipeline credentials
python -m project_booster pipeline creds <id>

# Cancel a running pipeline
python -m project_booster pipeline cancel <id>
```

---

## Programmatic usage (Python)

When an agent has access to Python execution, it can use the client directly:

```python
from scripts.project_booster.config import load_config
from scripts.project_booster.booster_client import BoosterClient

client = BoosterClient(load_config())

# Deploy a database (blocks until done)
result = client.deploy_database("postgresql", "my-namespace")
print(result["credentials"])

# Deploy an app
result = client.deploy_app("my-app", "my-namespace",
    components=[{"name": "api", "technology": "java"}])

# Low-level: just create a scenario
scenario = client.create_scenario("new_database",
    inputs={"databaseType": "mysql", "namespace": "ns"})
```

---

## Output artefacts

When an agent uses this skill as part of a delivery workflow, it should produce:

- **Deliverable:** `docs/4-dep/pb-001-project-booster-setup.md` using template `tpl-project-booster.md`
  - What was provisioned, scenario IDs, pipeline results, credentials references
- **Execution results:** Pipeline JSONs in `outputs/project-booster/`

When used for a quick standalone operation (e.g. "just create a database"), the deliverable is optional — the CLI output is sufficient.

## Key constraints

- **Credentials:** Never hardcode passwords or tokens in output files. Reference CI/CD variables or the Project Booster secrets store.
- **Production:** Agents should confirm with the user before provisioning production environments.
- **Quotas:** Always set resource quotas when creating namespaces — unbounded namespaces can exhaust cluster resources.
- **Connectivity:** Always verify orchestrator connectivity (`env check`) before the first provisioning operation in a session.
