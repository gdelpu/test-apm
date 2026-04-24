---
id: sk-infrastructure-aws
category: infrastructure
technology: AWS
version: ">=2024"
tags: [cloud, iac, serverless, ecs, rds]
last_reviewed: 2025-01-15
---

# Skill: AWS (Amazon Web Services)

## Structure conventions

```
infrastructure/
├── cdk/                        # AWS CDK (if IaC via CDK)
│   ├── bin/
│   │   └── app.ts              # Entry point
│   ├── lib/
│   │   ├── stacks/
│   │   │   ├── network-stack.ts
│   │   │   ├── database-stack.ts
│   │   │   ├── compute-stack.ts
│   │   │   └── monitoring-stack.ts
│   │   └── constructs/         # Reusable constructs
│   └── cdk.json
├── terraform/                  # Alternative: Terraform
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   ├── modules/
│   └── main.tf
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
└── scripts/
    ├── deploy.sh
    └── seed-db.sh
```

## Code conventions

### Infrastructure principles

- **Infrastructure as Code**: everything is versioned — zero manual configuration via the console
- **Immutable infrastructure**: no in-place modification, replace resources
- **Least privilege**: each service has an IAM role with the minimum required permissions
- **Encryption everywhere**: data encrypted at rest (KMS) and in transit (TLS)

### Resource naming

```
{project}-{env}-{service}-{resource}
```

| Component | Convention | Example |
|-----------|-----------|---------|
| Project | kebab-case, short | `myapp` |
| Environment | `dev`, `staging`, `prod` | `dev` |
| Service | kebab-case | `api`, `worker`, `web` |
| Resource | short AWS type | `sg`, `rds`, `ecs`, `s3` |

Examples:
- `myapp-prod-api-ecs` — ECS cluster for the API in production
- `myapp-dev-db-rds` — RDS instance in development
- `myapp-staging-assets-s3` — S3 bucket for assets in staging

### Mandatory tags

All AWS resources MUST have the following tags:

| Tag | Description | Example |
|-----|------------|---------|
| `Project` | Project name | `myapp` |
| `Environment` | Environment | `dev`, `staging`, `prod` |
| `Service` | Owning service | `api`, `web` |
| `ManagedBy` | Management tool | `cdk`, `terraform` |
| `CostCenter` | Cost centre | `engineering` |

### Recommended services by use case

| Need | AWS Service | Alternative |
|------|------------|-------------|
| Compute (containers) | ECS Fargate | EKS (if K8s required) |
| Compute (serverless) | Lambda | — |
| Relational database | RDS (Aurora) | RDS PostgreSQL |
| Cache | ElastiCache (Redis) | — |
| Queue / Messages | SQS | SNS + SQS (fan-out) |
| Event bus | EventBridge | — |
| File storage | S3 | — |
| CDN | CloudFront | — |
| DNS | Route 53 | — |
| Secrets | Secrets Manager | SSM Parameter Store |
| Monitoring | CloudWatch | Datadog (if budget) |
| Logs | CloudWatch Logs | — |
| CI/CD | GitHub Actions + ECR | CodePipeline |

### Environment management

- **dev**: minimal resources, scaling at 1, small instances
- **staging**: identical configuration to prod, anonymised data
- **prod**: Multi-AZ, auto-scaling, backups enabled

## Test conventions

### Infrastructure

- **CDK**: `cdk synth` + snapshot tests to verify the CloudFormation template
- **Terraform**: `terraform plan` in CI to detect drifts
- **Localstack**: for local AWS integration tests (S3, SQS, DynamoDB)
- **Checkov / tfsec**: IaC security scan in CI

### Pre-deployment validation

1. Lint IaC (`cdk synth` or `terraform validate`)
2. Security scan (Checkov)
3. Cost estimation (`infracost` if Terraform)
4. Plan review (diff visible in PR)

## Mandatory rules

1. **NEVER hardcode credentials** — use Secrets Manager or SSM Parameter Store
2. **NEVER resources without tags** — the 5 mandatory tags are non-negotiable
3. **NEVER `0.0.0.0/0` in ingress** on security groups (except public ALB)
4. **ALWAYS enable encryption** at rest (RDS, S3, EBS, SQS)
5. **ALWAYS enable access logs** (ALB, S3, CloudTrail)
6. **ALWAYS configure automatic backups** for RDS (retention ≥ 7 days)
7. **ALWAYS use private subnets** for internal services (RDS, ECS tasks)
8. **Multi-AZ mandatory in production** for RDS and ECS
9. **No wildcard `*` in IAM policies** — specify exact resources and actions
10. **Dockerfiles MUST use official tagged base images** — no `latest`
