# Project Booster CLI

Python CLI & API client for the **Project Booster** platform (v2.15).
Creates environments (InnerShift, Arcus), databases (PostgreSQL, MySQL, MongoDB,
Elasticsearch), CI/CD pipelines, web applications, and manages Artifactory repos
via the Project Booster REST API.

## Prerequisites

- Python 3.10+
- `requests` library (`pip install requests`)

## Setup

```bash
# From the repo root
cd scripts/project-booster

# Create a config file (interactive)
python -m project_booster init

# Or with arguments
python -m project_booster init \
  --url https://project-booster.dep.soprasteria.com \
  --token glpat-xxxxxxxxxxxxxxxxxxxx
```

This creates `.project-booster.json` in the current directory.
Alternatively, set environment variables:

```bash
export PROJECT_BOOSTER_TOKEN="glpat-..."
export PROJECT_BOOSTER_URL="https://project-booster.dep.soprasteria.com"  # optional
```

## Usage

```bash
# Shorthand
alias pb="python -m project_booster"

# Check auth
pb whoami

# Show platform config (scenario types, etc.)
pb config

# List all available scenario types
pb scenario-types
```

### Deploy (end-to-end shortcuts)

These commands handle the full flow: create scenario → trigger pipeline → wait
for completion → return credentials. Ideal for automation and CI/CD scripts.

#### Deploy a database on InnerShift

```bash
# PostgreSQL
pb deploy db postgresql my-namespace

# MySQL on Arcus
pb deploy db mysql my-namespace --orch-type arcus

# MongoDB with extra options
pb deploy db mongodb my-namespace \
  --extra-inputs '{"version": "6.0", "storageSize": "10Gi"}'

# Elasticsearch with longer timeout (15 min)
pb deploy db elasticsearch my-namespace --timeout 900
```

#### Deploy a web application

```bash
# Simple app
pb deploy app my-app my-namespace

# App with components definition
pb deploy app my-app my-namespace \
  --components '[{"name": "backend", "technology": "java", "template": "spring-boot"}, {"name": "frontend", "technology": "angular"}]'

# On Arcus instead of InnerShift
pb deploy app my-app my-namespace --orch-type arcus
```

#### Deploy any scenario type (generic)

```bash
# Generic deploy — works with all scenario types
pb deploy run --type new_tool \
  --inputs '{"toolType": "sonarqube", "namespace": "my-tools", "orchestratorType": "arcus"}'

# With custom timeout and poll interval
pb deploy run --type new_launchpad \
  --inputs '{"cloudProvider": "azure", "region": "westeurope"}' \
  --timeout 1200 --interval 15
```

### Scenarios (project templates)

```bash
# List your scenarios
pb scenarios list

# Create a new scenario
pb scenarios create --type new_web_app \
  --inputs '{"applicationName": "my-app", "namespace": "my-ns"}'

# Get details
pb scenarios get 42

# Duplicate an existing scenario
pb scenarios duplicate 42

# Archive / unarchive
pb scenarios archive 42
pb scenarios unarchive 42
```

### CI/CD Pipelines

```bash
# Trigger a pipeline for scenario 42
pb pipeline run 42

# Check status
pb pipeline status 42

# Wait for completion (blocks, polls every 10s, 10min timeout)
pb pipeline wait 42 --interval 10 --timeout 600

# Cancel a running pipeline
pb pipeline cancel 42

# Get generated credentials (GitLab tokens, DB passwords, etc.)
pb pipeline creds 42
```

### Environments (InnerShift / Arcus / OpenShift)

```bash
# Check orchestrator connectivity
pb env check innershift

# List namespaces
pb env namespaces innershift --page 0 --size 50

# List namespaces with deployed resources
pb env resources innershift

# Test namespace creation
pb env test-create innershift my-namespace

# Test namespace is writable
pb env test-write innershift my-namespace

# List services in a namespace
pb env services innershift my-namespace

# Get a specific deployed service by release name
pb env service innershift my-namespace my-release

# Get namespace details
pb env details innershift my-namespace

# Create a role binding
pb env role-binding innershift my-namespace \
  --body '{"group": "dev-team", "role": "edit"}'

# Set quotas
pb env quotas innershift my-namespace \
  --body '{"cpu": "4", "memory": "8Gi"}'
```

### Secrets

```bash
pb secrets list
pb secrets create --key https://gitlab.example.com --value glpat-xxx \
  --type openshift --label "My GitLab token"
pb secrets delete 7
```

### Trusted Certificates

```bash
pb certs list
pb certs add --pem-file ./my-ca.pem
pb certs delete 3
```

### Artifactory

```bash
pb artifactory repos --page 0 --size 20
pb artifactory create-repos --body '{"key": "my-repo", "rclass": "local"}'
```

### Admin Commands

```bash
pb admin config reload --branch main
pb admin config reset
pb admin banners list
pb admin banners create --body '{"message": "Maintenance tonight", "type": "warning"}'
pb admin metrics connections
pb admin metrics usage
pb admin metrics ratings
```

## Scenario Types

| Type | Description |
|------|-------------|
| `new_web_app` | Create a new web application (mono or multi-component) |
| `new_web_doc` | Create a static documentation site (GitLab Pages) |
| `new_tool` | Deploy a tool/service (Nexus, Vault, SonarQube, …) |
| `update_service` | Update an existing deployed service |
| `new_database` | Deploy a standalone database (PostgreSQL, MySQL, MongoDB, Elasticsearch) |
| `update_database` | Update an existing database |
| `new_launchpad` | Deploy infrastructure on cloud (Azure, AWS, AzureStack) |
| `new_repository` | Create a new Artifactory repository |
| `configure_kube_green_for_service` | Configure Kube-Green on Arcus |
| `configure_kube_green_for_app` | Configure Kube-Green on InnerShift |
| `configure_kasten_for_service` | Configure Kasten backup on Arcus |
| `configure_kasten_for_app` | Configure Kasten backup on InnerShift |
| `remove_resources_for_service` | Remove resources from Innersource + Arcus |
| `remove_resources_for_application` | Remove resources from Innersource + InnerShift |

Use `pb scenario-types` to list types available on your instance (fetched from `/api/config`).

## API Coverage

All 51 endpoints of the Project Booster API v2.15 are implemented, plus high-level helpers:

| Category | Endpoints |
|----------|-----------|
| Index | GET /api |
| Users | GET/DELETE current, GET/PUT profile |
| Secrets | POST, GET list, GET by id, DELETE |
| Trusted certificates | GET list, POST, DELETE |
| Ratings | GET, POST |
| Scenarios | POST, GET list, GET all, GET by id, PUT, PATCH, DELETE, children, scopes, duplicate |
| Pipelines | POST trigger, GET status, DELETE cancel, GET credentials, wait (polling) |
| Orchestrators | check, namespaces (list/test-create/test-write/resources), namespace details, services (list/get), role-binding, quotas |
| Artifactory | GET repos, POST repos |
| Certificates | GET by URL |
| Config | GET, PUT reload, DELETE reset, GET auth, banners |
| Metrics | connections, usage, ratings |
| **High-level helpers** | `deploy()`, `deploy_database()`, `deploy_app()`, `create_database()`, `create_app()`, `create_tool()`, `get_scenario_types()` |

## Programmatic Usage

```python
from project_booster.config import load_config
from project_booster.booster_client import BoosterClient

client = BoosterClient(load_config())

# Deploy a PostgreSQL database on InnerShift (full end-to-end)
result = client.deploy_database("postgresql", "my-namespace")
print(result["credentials"])  # DB host, port, user, password

# Deploy a web app with components
result = client.deploy_app(
    "my-app", "my-namespace",
    components=[
        {"name": "api", "technology": "java", "template": "spring-boot"},
        {"name": "web", "technology": "angular"},
    ],
)

# Generic deploy for any scenario type
result = client.deploy(
    "new_tool",
    {"toolType": "sonarqube", "namespace": "tools", "orchestratorType": "arcus"},
    timeout=900,
)

# Lower-level: create scenario + manage pipeline manually
scenario = client.create_scenario("new_database", inputs={...})
client.create_pipeline(scenario["id"])
pipeline = client.wait_for_pipeline(scenario["id"], timeout=600)
creds = client.get_pipeline_credentials(scenario["id"])
```
