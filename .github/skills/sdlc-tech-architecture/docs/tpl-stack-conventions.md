---
id: STK-001
title: "Technology Stack & Conventions — [Project Name]"
system: t1-architecture
type: stack-conventions
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-t1.3-stack-conventions
reviewers: []
dependencies: ["CTX-001", "ADR-001"]
ba_dependencies: ["VIS-001"]
---

# [STK-001] Technology Stack & Conventions

## 1. Retained stack by layer

| Layer | Technology | Version | Justifying ADR |
|-------|-----------|---------|----------------|
| **Front-end** | <!-- React / Angular / Vue / ... --> | <!-- E.g. 18.x --> | [ADR-xxx] |
| **Back-end** | <!-- NestJS / Spring Boot / .NET / FastAPI / ... --> | <!-- E.g. 10.x --> | [ADR-xxx] |
| **Database** | <!-- PostgreSQL / MongoDB / ... --> | <!-- E.g. 16.x --> | [ADR-xxx] |
| **Cache** | <!-- Redis / Memcached / none --> | | [ADR-xxx] |
| **Message broker** | <!-- RabbitMQ / Kafka / none --> | | [ADR-xxx] |
| **ORM / Data access** | <!-- TypeORM / Prisma / Hibernate / EF Core / ... --> | | |
| **Authentication** | <!-- Keycloak / Auth0 / Firebase Auth / custom --> | | [ADR-xxx] |
| **CI/CD** | <!-- GitHub Actions / GitLab CI / Azure DevOps / ... --> | | |
| **Hosting** | <!-- AWS ECS / Azure App Service / K8s / VMs / ... --> | | [ADR-xxx] |
| **Monitoring** | <!-- Datadog / Grafana+Prometheus / CloudWatch / ... --> | | [ADR-xxx] |
| **Unit tests** | <!-- Jest / JUnit / xUnit / pytest / ... --> | | |
| **E2E tests** | <!-- Playwright / Cypress / ... --> | | |
| **Containerisation** | <!-- Docker / Podman / none --> | | |

---

## 2. Activated technical skills

The following skills were selected from the registry based on ADRs:

| Skill | Category | File | Activation reason |
|-------|---------|------|-------------------|
| <!-- E.g. React --> | Framework | `skill-registry/frameworks/sk-react.md` | [ADR-xxx] Front-end = React |
| <!-- E.g. NestJS --> | Framework | `skill-registry/frameworks/sk-nestjs.md` | [ADR-xxx] Back-end = NestJS |
| <!-- E.g. PostgreSQL --> | Data | `skill-registry/data/sk-postgresql.md` | [ADR-xxx] DB = PostgreSQL |
| <!-- E.g. Clean Architecture --> | Pattern | `skill-registry/patterns/sk-clean-architecture.md` | [ADR-xxx] Style = Clean |
| <!-- E.g. Jest + RTL --> | Testing | `skill-registry/testing/sk-jest-rtl.md` | React front-end stack |
| <!-- E.g. Playwright --> | Testing | `skill-registry/testing/sk-playwright.md` | E2E tests |

> These skills will be compiled into the final CLAUDE.md by agent T-2.5.

---

## 3. Project structure

```
project-root/
├── CLAUDE.md                          ← Claude Code entry point
├── docs/
│   ├── adr/                           ← Architecture Decision Records
│   └── tech/                          ← Technical deliverables
├── migrations/                        ← SQL migration scripts
├── openapi.yaml                       ← API contract
│
├── src/                               ← Back-end source code
│   ├── common/                        ← Shared utilities, guards, interceptors
│   ├── config/                        ← Configuration by environment
│   ├── <module>/                      ← One folder per business module
│   │   ├── dto/                       ← Data Transfer Objects
│   │   ├── entities/                  ← Entities / models
│   │   ├── <module>.controller.ts     ← REST Controller
│   │   ├── <module>.service.ts        ← Business logic
│   │   ├── <module>.repository.ts     ← Data access
│   │   └── <module>.module.ts         ← DI Module
│   └── main.ts                        ← Entry point
│
├── app/                               ← Front-end source code (if monorepo)
│   ├── components/                    ← Reusable components
│   ├── pages/ or routes/              ← Pages / screens
│   ├── hooks/                         ← Custom hooks
│   ├── services/                      ← API calls
│   └── types/                         ← Types / interfaces
│
├── tests/
│   ├── unit/                          ← Unit tests
│   ├── integration/                   ← Integration tests
│   └── e2e/                           ← End-to-end tests
│
├── docker-compose.yml                 ← Local environment
├── Dockerfile                         ← Production build
└── package.json / pom.xml / ...       ← Dependencies
```

> This structure is indicative and will be adapted according to the chosen stack and the conventions of the activated framework skill.

---

## 4. Naming conventions

### Back-end

| Element | Convention | Example |
|---------|-----------|---------|
| Files | kebab-case | `order-line.service.ts` |
| Classes | PascalCase | `OrderLineService` |
| Methods | camelCase | `createOrder()` |
| Variables | camelCase | `totalAmount` |
| Constants | UPPER_SNAKE_CASE | `MAX_ORDER_ITEMS` |
| Interfaces | PascalCase (optional I prefix) | `OrderRepository` |
| Enums | PascalCase + UPPER_SNAKE_CASE values | `OrderStatus.VALIDATED` |

### Database

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | snake_case, plural | `orders`, `order_lines` |
| Columns | snake_case | `total_amount`, `created_at` |
| Primary keys | `id` (UUID) | `id UUID PRIMARY KEY` |
| Foreign keys | `<singular_table>_id` | `order_id`, `customer_id` |
| Indexes | `idx_<table>_<column(s)>` | `idx_orders_customer_id` |
| Constraints | `chk_<table>_<rule>` | `chk_orders_total_positive` |

### REST API

| Element | Convention | Example |
|---------|-----------|---------|
| Resources | kebab-case, plural | `/api/orders`, `/api/order-lines` |
| Path parameters | camelCase | `/api/orders/{orderId}` |
| Query params | camelCase | `?startDate=2025-01-01&pageSize=20` |
| Body | camelCase | `{ "totalAmount": 150.00 }` |
| Versioning | Path prefix | `/api/v1/orders` |

### Front-end

| Element | Convention | Example |
|---------|-----------|---------|
| Components | PascalCase | `OrderForm.tsx` |
| Hooks | camelCase, `use` prefix | `useOrders.ts` |
| Pages | PascalCase or kebab-case (per framework) | `CreateOrderPage.tsx` |
| API services | camelCase | `orderService.ts` |
| Styles | CSS Module or Tailwind classes | `order-form.module.css` |

### Tests

| Element | Convention | Example |
|---------|-----------|---------|
| Unit files | `<module>.spec.ts` or `<module>.test.ts` | `order.service.spec.ts` |
| Integration files | `<module>.api.spec.ts` | `orders.api.spec.ts` |
| E2E files | `<journey>.spec.ts` | `create-order.spec.ts` |
| Describe | Name of the tested module | `describe('OrderService', ...)` |
| It / test | Should + behaviour | `it('should create a draft order', ...)` |

---

## 5. Code conventions

### General rules

- No `any` in TypeScript (except documented and justified cases)
- No business logic in controllers (delegate to services)
- No direct database access from services (go through the repository)
- Systematic dependency injection (no `new` in business code)
- Centralised error handling via exception filters / error handlers
- Structured logging (JSON) with context (request ID, user ID)

### Commit rules

- Format: `<type>(<scope>): <description> [JIRA-KEY]` (Conventional Commits)
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`
- Scope: module name or `*` for cross-cutting
- **The Jira key of the current task is MANDATORY** in every commit message — it must appear at the end of the line in brackets (e.g. `[PROJ-123]`)
- This requirement is imperative so that Jira can link to the commit and the **R4J** plugin (Requirements for Jira) guarantees complete traceability between requirements, tasks, and code
- Example: `feat(orders): implement create order endpoint [PROJ-123]`
- If the item also corresponds to an internal implementation plan identifier, both references are included: `feat(orders): implement create order endpoint [PROJ-123] [IMP-015]`

---

## 6. Glossary → technical terminology mapping

| BA Glossary Term | Technical term (code) | Table | Endpoint |
|------------------|-----------------------|-------|----------|
| <!-- E.g. Order --> | `Order` | `orders` | `/api/orders` |
| <!-- E.g. Order line --> | `OrderLine` | `order_lines` | (nested) |
| <!-- E.g. Customer --> | `Customer` | `customers` | `/api/customers` |

---

## Traceability

### Technical traceability
| Element | Detail |
|---------|--------|
| **Produced by** | agent-t1.3-stack-conventions |
| **Production date** | YYYY-MM-DD |
| **Technical inputs** | [CTX-001], [ADR-001] to [ADR-N] |
| **Validated by** | Pending |
| **Validation date** | Pending |

### BA traceability
| BA Deliverable | Traced elements |
|----------------|-----------------|
| [VIS-001] | Environmental constraints influencing stack choice |
| [GLO-001] | Glossary → technical terminology mapping |
