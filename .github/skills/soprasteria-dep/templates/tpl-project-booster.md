---
name: tpl-project-booster
description: 'Template for DEP Project Booster environment & pipeline provisioning deliverables.'
triggers: ['Project Booster template', 'DEP provisioning deliverable template']
id: PB-001
title: "DEP Project Booster — Environment & Pipeline Provisioning"
type: dep-pb
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-dep4.1
tech_dependencies: []
---

# PB-001 DEP Project Booster — Environment & Pipeline Provisioning

## 1. Project context

<!-- Summary of the project requirements that drove the provisioning choices -->

| Property | Value |
|----------|-------|
| Project name | — |
| Deployment target(s) | InnerShift / Arcus |
| Environments | dev, staging, prod |
| Application type | Web app / API / Multi-component |
| Languages & frameworks | — |
| Database(s) | — |
| Tools required | — |
| Team / group | — |

---

## 2. Environment provisioning plan

<!-- 
  PRE-FILL SOURCE: If ADR-ENV-QUALIF produced a `pb-provisioning-plan.json` file
  (in outputs/docs/2-tech/1-architecture/adr/), use it to pre-fill this table.
  The JSON contains the ordered list of operations, PB scenario types, and parameters
  determined during architecture decision-making (sk-t1.2, Step 2d).
  
  Each JSON "operations" entry maps to a row below.
  Entries with "pb_scenario": null are manual and should be marked ⏭️ skipped in this PB deliverable.
-->

<!-- Complete plan of operations, in execution order -->

| # | Operation | Scenario type | Target | Namespace | Status |
|---|-----------|---------------|--------|-----------|--------|
| 1 | Check orchestrator | — | innershift | — | ⬜ |
| 2 | Verify/create namespace (dev) | — | innershift | `<project>-dev` | ⬜ |
| 3 | Set quotas (dev) | — | innershift | `<project>-dev` | ⬜ |
| 4 | Create role bindings (dev) | — | innershift | `<project>-dev` | ⬜ |
| 5 | Deploy database (dev) | `new_database` | innershift | `<project>-dev` | ⬜ |
| 6 | Deploy application (dev) | `new_web_app` | innershift | `<project>-dev` | ⬜ |
| … | Repeat for staging, prod | … | … | … | ⬜ |

Status: ⬜ pending · 🔄 in progress · ✅ done · ❌ failed · ⏭️ skipped

---

## 3. Scenario inventory

<!-- List of all scenarios created on Project Booster -->

| Scenario ID | Type | Name / Description | Namespace | Pipeline status |
|-------------|------|--------------------|-----------|-----------------|
| — | `new_database` | PostgreSQL for backend | `<project>-dev` | — |
| — | `new_web_app` | Application scaffold | `<project>-dev` | — |

---

## 4. Namespace configuration

### 4.1 Resource quotas

| Namespace | CPU | Memory | Storage | Justification |
|-----------|-----|--------|---------|---------------|
| `<project>-dev` | 2 | 4Gi | 20Gi | Development workloads |
| `<project>-staging` | 4 | 8Gi | 50Gi | Integration testing |
| `<project>-prod` | 8 | 16Gi | 100Gi | Production workloads |

### 4.2 Role bindings

| Namespace | Group / User | Role | Purpose |
|-----------|-------------|------|---------|
| `<project>-dev` | `<team>` | edit | Development team access |
| `<project>-prod` | `<team>` | view | Read-only production access |

---

## 5. Database provisioning

<!-- Details for each provisioned database -->

### 5.1 Database: `<name>`

| Property | Value |
|----------|-------|
| Engine | PostgreSQL / MySQL / MongoDB / Elasticsearch |
| Version | — |
| Namespace | `<project>-dev` |
| Orchestrator | InnerShift |
| Scenario ID | — |
| Pipeline status | — |

**Connection details** (stored in CI/CD variables — never in code):
- Host: `<from pipeline credentials>`
- Port: `<from pipeline credentials>`
- Database: `<from pipeline credentials>`
- Username: `<from pipeline credentials>`
- Password: *stored in Project Booster secrets / CI/CD variables*

---

## 6. Application provisioning

<!-- Details for each provisioned application -->

### 6.1 Application: `<name>`

| Property | Value |
|----------|-------|
| Type | Web app / API |
| Components | backend (Java), frontend (Angular) |
| Namespace | `<project>-dev` |
| Orchestrator | InnerShift |
| Scenario ID | — |
| Pipeline status | — |

**Created resources:**
- GitLab group: `<innersource-url>/<group>`
- GitLab project(s): `<innersource-url>/<group>/<project>`
- CI/CD pipeline: configured with DEP CI Library
- Deployed at: `<namespace>.apps.innershift.soprasteria.com`

---

## 7. Tool provisioning

<!-- Details for each provisioned tool (if applicable) -->

| Tool | Namespace | Orchestrator | Scenario ID | Status |
|------|-----------|-------------|-------------|--------|
| SonarQube | `<tools-ns>` | Arcus | — | — |

---

## 8. Execution log

<!-- Pipeline execution details — paste summary, not full JSON -->

```
Scenario #XX — new_database (postgresql)
  Pipeline triggered: YYYY-MM-DD HH:MM
  Actions: 5/5 completed
  Status: COMPLETED
  Duration: 4m 32s

Scenario #YY — new_web_app
  Pipeline triggered: YYYY-MM-DD HH:MM
  Actions: 8/8 completed
  Status: COMPLETED
  Duration: 7m 15s
```

---

## 9. Credentials & access summary

> ⚠️ Actual passwords and tokens are NOT stored in this document.
> They are available via `python -m project_booster pipeline creds <scenario-id>`
> and should be stored in GitLab CI/CD variables or a secrets manager.

| Resource | Access method | Credential location |
|----------|--------------|---------------------|
| PostgreSQL (dev) | Host + port from pipeline | CI/CD variable `DB_DEV_*` |
| GitLab project | Personal access token | Project Booster secrets |
| InnerShift namespace | RBAC role binding | Orchestrator RBAC |

---

## 10. Points of attention

<!-- Assumptions, risks, open items, sizing decisions -->

| # | Type | Description | Action needed |
|---|------|-------------|---------------|
| 1 | Assumption | Resource quota sizing based on standard DEP guidelines | Validate with team |
| 2 | Open item | Production provisioning pending client approval | Confirm before proceeding |
