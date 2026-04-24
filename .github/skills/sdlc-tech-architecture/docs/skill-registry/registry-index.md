# Skill Registry — Index

## Overview

The skill registry is a curated catalogue of technical conventions and best practices, organised by category. Each skill is a standalone Markdown file documenting the conventions specific to a technology.

## Principles

1. **Curated by the architecture team**: each skill is validated before integration
2. **Sources**: community CLAUDE.md files, `.cursorrules`, official documentation, experience feedback
3. **Activated by agent T-1.3**: only the skills relevant to the project's stack are selected
4. **Inlined in CLAUDE.md**: agent T-2.5 compiles activated skills directly into the final deliverable

## Structure of a skill

Each skill in the registry follows this format:

```yaml
---
id: sk-{category}-{technology}
category: frameworks | infrastructure | patterns | data | testing
technology: technology-name
version: ">=X.Y"
tags: [tag1, tag2]
last_reviewed: YYYY-MM-DD
---
```

Followed by content:
- **Structure conventions**: file and folder organisation
- **Code conventions**: patterns, anti-patterns, idioms
- **Test conventions**: specific testing tools and patterns
- **Mandatory rules**: critical MUST and MUST NOT rules

## Categories

### 🏗️ Frameworks (`frameworks/`)

Skills specific to application frameworks.

| Skill | Technology | Tags |
|-------|------------|------|
| [sk-react.md](frameworks/sk-react.md) | React 18+ | `frontend`, `spa`, `hooks` |
| [sk-nextjs.md](frameworks/sk-nextjs.md) | Next.js 14+ | `frontend`, `ssr`, `app-router` |
| [sk-nestjs.md](frameworks/sk-nestjs.md) | NestJS 10+ | `backend`, `nodejs`, `typescript` |
| [sk-spring-boot.md](frameworks/sk-spring-boot.md) | Spring Boot 3+ | `backend`, `java`, `kotlin` |
| [sk-fastapi.md](frameworks/sk-fastapi.md) | FastAPI 0.100+ | `backend`, `python`, `async` |

### 🏗️ Infrastructure (`infrastructure/`)

Skills specific to infrastructure and deployment services.

| Skill | Technology | Tags |
|-------|------------|------|
| [sk-aws.md](infrastructure/sk-aws.md) | AWS | `cloud`, `iac`, `serverless` |
| [sk-docker.md](infrastructure/sk-docker.md) | Docker & Compose | `container`, `devops` |
| [sk-github-actions.md](infrastructure/sk-github-actions.md) | GitHub Actions | `ci-cd`, `automation` |

### 🧩 Patterns (`patterns/`)

Skills specific to architecture and design patterns.

| Skill | Pattern | Tags |
|-------|---------|------|
| [sk-clean-architecture.md](patterns/sk-clean-architecture.md) | Clean Architecture | `architecture`, `layered`, `ddd` |
| [sk-cqrs-event-sourcing.md](patterns/sk-cqrs-event-sourcing.md) | CQRS + Event Sourcing | `architecture`, `event-driven` |

### 💾 Data (`data/`)

Skills specific to databases and ORMs.

| Skill | Technology | Tags |
|-------|------------|------|
| [sk-postgresql.md](data/sk-postgresql.md) | PostgreSQL 15+ | `rdbms`, `sql`, `jsonb` |
| [sk-prisma.md](data/sk-prisma.md) | Prisma ORM | `orm`, `typescript`, `migrations` |
| [sk-typeorm.md](data/sk-typeorm.md) | TypeORM | `orm`, `typescript`, `migrations` |

### 🧪 Testing (`testing/`)

Skills specific to testing tools and strategies.

| Skill | Technology | Tags |
|-------|------------|------|
| [sk-jest-rtl.md](testing/sk-jest-rtl.md) | Jest + React Testing Library | `unit`, `component`, `frontend` |
| [sk-playwright.md](testing/sk-playwright.md) | Playwright | `e2e`, `browser`, `automation` |
| [sk-vitest.md](testing/sk-vitest.md) | Vitest | `unit`, `fast`, `esm` |

## Contributing a skill

To add a new skill to the registry:

1. Create the file in the appropriate category: `{category}/sk-{technology}.md`
2. Follow the YAML front matter format above
3. Structure the content according to the sections: Structure conventions, Code conventions, Test conventions, Mandatory rules
4. Have it validated by the architecture team
5. Update this index

## Search by tags

| Tag | Skills |
|-----|--------|
| `backend` | sk-nestjs, sk-spring-boot, sk-fastapi |
| `frontend` | sk-react, sk-nextjs |
| `typescript` | sk-nestjs, sk-prisma, sk-typeorm, sk-jest-rtl, sk-vitest |
| `python` | sk-fastapi |
| `java` | sk-spring-boot |
| `orm` | sk-prisma, sk-typeorm |
| `e2e` | sk-playwright |
| `cloud` | sk-aws |
| `ci-cd` | sk-github-actions |
