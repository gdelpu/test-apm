---
name: aws-resource-query
description: 'Query and inspect AWS resources via AWS MCP server — validate CloudFormation/CDK against live state, check service quotas and health.'
triggers:
  - aws resource query
  - aws infrastructure
  - aws service health
  - validate aws deployment
  - cloudformation validation
---

# Skill: aws-resource-query

## Goal

Query AWS resources via the AWS MCP server to validate CloudFormation/CDK against live state, check service quotas, and pull current infrastructure topology.

## MCP Server

- **Registry ID**: `aws-mcp`
- **Repository**: https://docs.aws.amazon.com/aws-mcp/latest/userguide/what-is-mcp-server.html
- **Auth**: AWS credentials (profile, access key, or IAM role)
- **Env**: `AWS_PROFILE`, `AWS_REGION`

## When to use

- Validating CloudFormation / CDK stacks against deployed resources
- Checking AWS service quotas and limits
- Pulling current infrastructure topology for architecture documentation
- Verifying CloudWatch / X-Ray configuration

## When NOT to use

- For Azure resources (use `azure-resource-query` skill)
- When no AWS credentials are configured

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `aws-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Query resources

Based on the user's request:
- **Stack validation**: Compare local CloudFormation/CDK against deployed stacks, report drift
- **Service quotas**: Check current usage against AWS service quotas
- **Resource inventory**: List resources by region, service, or tag
- **Monitoring check**: Verify CloudWatch alarms and X-Ray tracing configuration

### Step 3 — Format results

Write results to the appropriate output file with standard metadata frontmatter.

### Fallback (without MCP)

If `aws-mcp` is unavailable:
1. Parse local CloudFormation/CDK templates for declared resources
2. Warn that live-state validation is unavailable
3. Produce output based on local templates only
4. Instruct user to run `aws` CLI commands manually for live-state queries

## Output

Use `edit/editFiles` to write: `outputs/specs/features/<feature>/aws-resources.md`

## Security

- Never expose AWS account IDs, access keys, or ARNs in output files — use `[REDACTED:aws-id]` placeholders
- Restrict queries to the authenticated account/region only
- Do not modify or delete AWS resources — read-only operations only
