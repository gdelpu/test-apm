---
name: azure-resource-query
description: 'Query and manage Azure resources via Azure MCP server — validate IaC against live state, check service health, pull infrastructure topology.'
triggers:
  - azure resource query
  - azure infrastructure
  - azure service health
  - validate azure deployment
  - azure live state
---

# Skill: azure-resource-query

## Goal

Query Azure resources via the Azure MCP server to validate infrastructure-as-code against live state, check service health, and pull current topology for architecture documentation.

## MCP Server

- **Registry ID**: `azure-mcp`
- **Repository**: https://github.com/microsoft/mcp
- **Auth**: Azure Identity (managed identity, CLI login, or service principal)
- **Env**: `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`

## When to use

- Validating Bicep/ARM/Terraform against deployed Azure resources
- Checking Azure service health before deployment
- Pulling current infrastructure topology for C4 diagrams
- Verifying Azure Monitor / App Insights configuration

## When NOT to use

- For AWS resources (use `aws-resource-query` skill)
- For Azure DevOps work items (use `azdo-ops` skill)
- When no Azure subscription is configured

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `azure-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Query resources

Based on the user's request:
- **Resource inventory**: List resources in subscription/resource group
- **IaC validation**: Compare local IaC templates against deployed state, report drift
- **Service health**: Check Azure Service Health for active incidents affecting the subscription
- **Topology pull**: Extract resource relationships for architecture diagrams

### Step 3 — Format results

Write results to the appropriate output file with standard metadata frontmatter.

### Fallback (without MCP)

If `azure-mcp` is unavailable:
1. Parse local IaC files (Bicep, ARM, Terraform) for declared resources
2. Warn that live-state validation is unavailable
3. Produce output based on local templates only
4. Instruct user to run `az` CLI commands manually for live-state queries

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/azure-resources.md`

## Security

- Never expose subscription IDs, tenant IDs, or resource IDs in output files — use `[REDACTED:azure-id]` placeholders
- Restrict queries to the authenticated subscription only
- Do not modify or delete Azure resources — read-only operations only
