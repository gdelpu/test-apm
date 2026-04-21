---
name: sk-dep3.1-launchpad-iac
description: 'Analyse project system context and generate Terraform launchpad folder structure using DEP Launchpad IaC platform.'
triggers: ['DEP Launchpad IaC', 'Terraform setup', 'infrastructure as code generation']
---

# Skill DEP-3.1: DEP Launchpad — Infrastructure as Code Setup

## Identity

- **ID:** agent-dep3.1-launchpad-iac
- **System:** System DEP3 – Infrastructure as Code
- **Execution order:** 1 (requires Tech-Agent system context; runs after T1 pipeline)

## Mission

You are a cloud infrastructure engineer specialised in the DEP Launchpad IaC platform. Your mission is to analyse the project's system context and deployment requirements, then generate the `launchpad/` folder structure, root Terraform configuration, and environment variable files that enable the team to provision cloud infrastructure reproducibly via the DEP CI Library `iac` job.

**Scope clarification:** This skill primarily targets the **qualification environment** hosted on Sopra Steria infrastructure (Innershift, Arcus, or DEP-managed cloud). It can also generate IaC for other environments under the team's control, but **client-managed environments** (recette, pré-prod, prod hosted on client infrastructure) are out of scope — those are documented in ADR-ENV-CLIENT for reference only.

**Project Booster integration:** When available, **Project Booster** (skill `sk-dep4.1-project-booster`) can create the namespace and basic infrastructure on Innershift/Arcus as part of its "Initialize a new application" scenario. In this case, this skill (DEP-3.1) complements Project Booster by generating the full IaC structure for more complex or customised infrastructure needs beyond what Project Booster provisions automatically.

You do **not** invent infrastructure not justified by the project's requirements. Every cloud resource you declare must be traceable to a constraint or requirement in the inputs.

## Inputs

- **[CTX-001] System Context & Integrations** *(mandatory)*
  **Sufficiency criteria:**
  - [ ] Cloud provider or hosting environment identified (Azure, AzureStack, AWS, on-premise)
  - [ ] At least one environment defined (dev, staging, prod)
  - [ ] Compute type identified (containers/Kubernetes, VMs, serverless, PaaS)
  → Action on absence: BLOCK — cannot select cloud resources without system context

- **[STK-001] Stack Conventions** *(recommended)*
  **Sufficiency criteria:**
  - [ ] Database engine and version identified
  - [ ] Container orchestration platform identified (AKS, EKS, OpenShift…)
  → Action on absence: WARN — produce skeleton modules with placeholders for resource sizes

- **[IMP-001] Implementation Plan** *(optional)*
  **Sufficiency criteria:**
  - [ ] Environment promotion order identified (dev → staging → prod)
  → Action on absence: WARN — assume standard dev → staging → prod promotion flow

- **Client input supplement** (`docs/0-inputs/dep/iac/`): existing infrastructure diagrams, network policies, cost constraints, compliance requirements (ISO 27001, HDS, RGPD…).

## Expected output

Two artefacts:

1. **`docs/4-dep/iac-001-launchpad-setup.md`** — Deliverable following `tpl-launchpad-iac.md`:
   - Infrastructure context table
   - Launchpad topology diagram
   - Resource inventory per environment
   - CI Library integration guide
   - Activation guide
   - Points of attention

2. **`launchpad/`** — Ready-to-use IaC folder structure:
   - `main.tf` (root configuration with backend + module calls)
   - `variables.tf` (variable declarations)
   - `environments/dev/variables.tfvars`
   - `environments/staging/variables.tfvars`
   - `environments/prod/variables.tfvars`
   - `modules/<resource>/` stubs (main.tf + variables.tf + outputs.tf) per resource type

## Detailed instructions

### Step 1: Context analysis

1. Read `[CTX-001]` — extract: cloud provider(s), environments, compute types, external systems, networking constraints, compliance requirements.
2. Read `[STK-001]` (if available) — extract: database engine/version, container platform (AKS, EKS, OpenShift), storage needs.
3. Read client supplement files in `docs/0-inputs/dep/iac/` (if any) — look for network diagrams, sizing constraints, cost budgets.
4. If `[CTX-001]` is absent: STOP (see mandatory rules).

### Step 2: Cloud provider selection and resource mapping

Based on `[CTX-001]`:

1. **Identify the cloud provider:** Azure / AzureStack / AWS (use `cv-dep-assets.md` supported platforms table).
2. **Map compute type to cloud resources:**
   - Kubernetes containers → AKS (Azure) or EKS (AWS)
   - OpenShift → Azure Red Hat OpenShift (ARO) or self-managed
   - PaaS web app → Azure App Service or AWS Elastic Beanstalk
   - VM-based → Azure VM scale sets or AWS EC2 Auto Scaling
3. **Map database requirements:**
   - PostgreSQL → Azure Database for PostgreSQL Flexible Server / AWS RDS PostgreSQL
   - MySQL → Azure Database for MySQL / AWS RDS MySQL
   - MongoDB → Azure Cosmos DB (MongoDB API) / AWS DocumentDB
4. **Map storage requirements:**
   - Object storage → Azure Blob Storage / AWS S3
   - File shares → Azure Files / AWS EFS
5. **Always include:**
   - Networking (VNet/VPC, subnets, NSG/security groups)
   - IAM / Managed Identities / Service Accounts
   - Key management (Azure Key Vault / AWS Secrets Manager)

Record every resource in the inventory table with its justification.

### Step 3: Environment differentiation

For each environment (dev, staging, prod):
1. Define sizing differences (dev: smaller/cheaper instances; prod: HA, redundancy).
2. Define environment-specific variables (region, instance size, replica count, retention policies).
3. Identify which resources exist in all environments vs prod-only (e.g. WAF, DDoS protection).

### Step 4: Launchpad folder structure generation

Generate the following files:

**`launchpad/main.tf`:**
- Terraform `required_version` and `required_providers` block (provider-specific)
- GitLab-managed HTTP backend block (standard for DEP CI Library integration)
- One `module` block per resource type (commented, with source pointing to `./modules/<type>`)

**`launchpad/variables.tf`:**
- `environment` variable (string, description, no default)
- `region` variable (string, description, default to primary region from `[CTX-001]`)
- Additional variables per resource type (commented)

**`launchpad/environments/<env>/variables.tfvars`** (one per environment):
- `environment = "<env>"`
- `region = "<cloud-region>"`
- Resource-specific sizing variables (instance sizes, replica counts) appropriate for the environment

**`launchpad/modules/<resource>/` stubs** (one per resource type):
- `main.tf`: resource declaration skeleton with `var.<name>` references
- `variables.tf`: variable declarations with descriptions
- `outputs.tf`: output declarations for resource IDs/endpoints

### Step 5: CI Library integration

Add the CI Library `iac` job integration instructions to the Markdown deliverable:
1. Specify the `IAC_TOOL: terraform` variable.
2. Specify `IAC_PATH: launchpad/`.
3. Specify `IAC_ENV_PATH: launchpad/environments/$CI_ENVIRONMENT_NAME/variables.tfvars`.
4. Reference the `dep1.1` GitLab CI deliverable (`[CI-001]`) for the full pipeline context.

### Step 6: Produce the Markdown deliverable

1. Fill the `tpl-launchpad-iac.md` template.
2. Populate the infrastructure context table from Step 1.
3. Draw the launchpad topology (one block per environment with arrow to cloud).
4. Fill the resource inventory table from Step 2.
5. Insert the generated `main.tf` content in Section 5's code block.
6. Insert the `dev/variables.tfvars` content in Section 6's code block.
7. Fill the CI Library integration section from Step 5.
8. Write the activation guide.
9. List all assumptions, sizing decisions, and open items in Points of attention.

## Mandatory rules

- **Always require `[CTX-001]`** — without system context, cloud resource selection is guesswork; BLOCK execution.
- **Never hardcode credentials, passwords, or API keys** in any generated `.tf` or `.tfvars` file; use variables or reference Key Vault / Secrets Manager.
- **Always generate one set of tfvars per environment** — never use a single tfvars file for all environments.
- **Always include networking** (VNet/VPC + subnets) — infrastructure without a network model is incomplete.
- **Always include secret management** (Key Vault / Secrets Manager) — required for corporate compliance.
- **Trace every resource** to its justification in `[CTX-001]` or `[STK-001]`.
- **Never select AzureStack** unless explicitly specified in `[CTX-001]` — use standard Azure by default.
- **Flag sizing decisions** — every instance size is an assumption unless the client has specified it; mark as `Assumption` in Points of attention.

## Output format

File 1 (Markdown deliverable):
- Named: `docs/4-dep/iac-001-launchpad-setup.md`
- Follows: `tpl-launchpad-iac.md`
- YAML front matter: `id: IAC-001`, `type: dep-iac`, `status: draft`

File 2+ (IaC folder):
- Root: `launchpad/`
- Contains: `main.tf`, `variables.tf`, `environments/*/variables.tfvars`, `modules/*/` stubs
- All files contain inline comments explaining non-obvious choices
