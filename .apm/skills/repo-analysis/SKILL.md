---
name: repo-analysis
description: 'Explore and analyze a code repository to understand its structure, services, components, dependencies, and architectural patterns. Produces high-level documentation for downstream workflows.'
triggers: ['repo analysis', 'repository analysis', 'codebase exploration', 'architecture discovery', 'service inventory', 'dependency mapping', 'code structure']
version: '1.0.0'
---

# Skill: Repository Analysis

## Purpose

Explore and analyze a code repository to produce a high-level architectural and functional overview. Used as a foundation skill by multiple agents (Repository Analyzer, Analysis Agent, Modernization Agent) and workflows (bug-fixing, incident-resolution, modernization, maturity-assessment, idea-to-spec).

## When to Use

- Brownfield contexts requiring a baseline understanding of existing code
- Bug triage and incident analysis to identify affected components
- Modernization assessments to catalog what exists before planning changes
- Maturity assessments to evaluate repository health
- Specification writing that needs domain context from an existing codebase

## Procedure

### 1. Structure Discovery

Scan the repository tree and identify:

- Root project type (monorepo, multi-module, single project)
- Build system (Maven, Gradle, npm, dotnet, Cargo, etc.)
- Primary languages and frameworks
- Configuration files and their purpose
- CI/CD pipeline definitions

### 2. Service / Component Inventory

For each identifiable service or component:

- Name and location (path)
- Primary responsibility (1–2 sentences)
- Entry points (API controllers, CLI commands, event handlers, scheduled jobs)
- Key internal modules / layers (domain, infrastructure, presentation)

### 3. Dependency Mapping

- **Internal dependencies**: which services/components call or depend on each other
- **External dependencies**: third-party libraries, APIs, databases, message brokers
- Produce a dependency matrix or adjacency list

### 4. Documentation Assessment

- Existing README files and their completeness
- API documentation (OpenAPI specs, GraphQL schemas)
- Architecture decision records (ADRs)
- Missing or stale documentation

### 5. Pattern Recognition

Identify recurring patterns:

- Architectural style (layered, hexagonal, microservices, modular monolith)
- Common libraries or abstractions used across services
- Testing patterns (unit, integration, e2e)
- Deployment patterns (containers, serverless, VMs)

## Constraints

- Read-only — do not execute commands, modify files, or access credentials
- Skip sensitive file patterns: `.env`, `*.pem`, `*.key`, `.aws/*`, `.ssh/*`
- Max 50 files per service scan; 5-level directory recursion limit
- Focus on business capabilities — skip non-functional deep dives unless specifically requested

## Output

The skill produces structured documentation, typically:

- `overview.md` — Purpose, problem solved, main services
- `services.md` — Service list with responsibilities and key components
- `dependencies.md` — Dependency matrix (internal + external)

Output format adapts to the consuming workflow. When used inline (not generating standalone docs), provide findings as structured data that the parent agent can incorporate.

```json
{
  "project_type": "monorepo",
  "languages": ["TypeScript", "Python"],
  "services": [
    {
      "name": "api-gateway",
      "path": "packages/api-gateway",
      "responsibility": "HTTP routing and authentication",
      "entry_points": ["src/main.ts"],
      "dependencies": ["user-service", "order-service"]
    }
  ],
  "external_dependencies": [
    { "name": "PostgreSQL", "type": "database", "used_by": ["user-service"] }
  ],
  "patterns": {
    "architecture": "microservices",
    "testing": "jest + supertest",
    "deployment": "Docker + Kubernetes"
  }
}
```
