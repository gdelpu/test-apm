---
id: TST-001
title: "Test Strategy — [Project Name]"
system: t2-design
type: test-strategy
status: draft
version: "1.0"
last_updated: YYYY-MM-DD
author: agent-t2.4-test-strategy
reviewers: []
dependencies: ["CTX-001", "ADR-001", "STK-001", "DAT-001", "API-001"]
ba_dependencies: ["DOM-001", "BRL-001", "TST-001"]
---

# [TST-001] Test Strategy

## 1. Test pyramid

```
          ╱╲
         ╱ E2E ╲          ← Few tests, costly, critical scenarios
        ╱────────╲
       ╱ Integration ╲    ← Moderate tests, API + DB, contracts
      ╱────────────────╲
     ╱    Unit           ╲ ← Many tests, fast, business logic
    ╱──────────────────────╲
```

| Level | Target | Quantity | Speed | When |
|-------|--------|----------|-------|------|
| **Unit** | Services, validators, UI components | Many | < 1s/test | At every commit |
| **Integration** | API endpoints + DB, coupled modules | Moderate | < 5s/test | At every PR |
| **E2E** | Complete user journeys | Few | < 30s/test | Before deployment |

---

## 2. Tooling by type

| Test type | Framework | Runner | Assertion | Mocks |
|-----------|-----------|--------|-----------|-------|
| **Unit back-end** | <!-- Jest / JUnit / xUnit / pytest --> | <!-- same --> | <!-- expect / assertThat --> | <!-- jest.mock / Mockito / Moq --> |
| **Unit front-end** | <!-- Jest + RTL / Vitest --> | <!-- same --> | <!-- expect --> | <!-- jest.mock / MSW --> |
| **API integration** | <!-- Supertest / RestAssured / WebApplicationFactory --> | <!-- Jest / JUnit --> | | <!-- Testcontainers for DB --> |
| **E2E** | <!-- Playwright / Cypress --> | <!-- same --> | <!-- expect(page) --> | Full stack with stubs `[ENB-STUB-XXX]` (see § Test environment) |
| **Performance** | <!-- k6 / Artillery / JMeter --> | CLI / CI | p95/p99 thresholds | |
| **Security** | <!-- OWASP ZAP / Snyk / npm audit --> | CI | 0 critical vulnerabilities | |

---

## 3. Test conventions

### File naming

| Type | Convention | Example |
|------|-----------|---------|
| Unit back | `<module>.service.spec.ts` | `order.service.spec.ts` |
| Unit front | `<Component>.test.tsx` | `OrderForm.test.tsx` |
| Integration | `<module>.api.spec.ts` | `orders.api.spec.ts` |
| E2E | `<journey>.spec.ts` | `create-order.spec.ts` |

### Test structure

```typescript
describe('[Module] - [Context]', () => {
  describe('method or action', () => {
    it('should [expected behaviour] when [condition]', () => {
      // Arrange (Given)
      // Act (When)
      // Assert (Then)
    });
  });
});
```

### Test naming convention

- **Describe**: Name of the module or component being tested
- **It/test**: `should <expected result> when <condition>`
- Always follow the **Arrange / Act / Assert** pattern (= Given / When / Then)
- Use concrete values (not "valid data", but `{ amount: 150.00, status: "draft" }`)

### Traceability comments in tests

```typescript
describe('OrderService', () => {
  // Tests: [BR-VAL-001] Minimum order amount
  it('should reject order when total is below 10.00', () => {
    // Implements: [US-012] AC-003, [BR-VAL-001]
    ...
  });
});
```

---

## 4. Coverage thresholds

| Metric | Minimum threshold | Target | Applied to |
|--------|------------------|-------|------------|
| **Line coverage** | **90%** | 95% | Business code (services, validators) |
| **Branch coverage** | **90%** | 95% | Business code |
| **Function coverage** | **90%** | 95% | All code |

> ⚠️ These thresholds are **blocking in CI**. A build whose unit coverage is below 90% cannot be merged. Any exception must be documented and approved by the lead developer.

**Coverage exclusions:**
- Configuration files
- DTOs (pure data classes)
- DI modules (wiring)
- Infrastructure code (migrations, seed)

## 4bis. API endpoint coverage

Each endpoint defined in `[API-xxx]` must be covered by **at least one automated integration test**.

| Priority | Cases to cover |
|----------|---------------|
| **Mandatory** | Nominal case (happy path) |
| **Mandatory** | Authentication / authorisation (401, 403) |
| **Mandatory on critical endpoints** | Business error cases (4xx with expected message) |
| **Recommended** | Edge cases (min/max values, absent optional fields) |

The API coverage matrix must be produced by agent T-2.4:

| Endpoint | Method | Nominal | Auth | Business errors | Edge cases |
|----------|--------|---------|------|-----------------|------------|
| `/api/orders` | POST | ✅ | ✅ | ✅ | ⬜ |
| `/api/orders/{id}` | GET | ✅ | ✅ | ⬜ | ⬜ |

---

## 5. Business rule coverage

| BA Rule | Type | Corresponding test(s) | Level |
|---------|------|----------------------|-------|
| [BR-VAL-xxx] | Validation | `order.service.spec.ts` → "should reject when..." | Unit |
| [BR-CAL-xxx] | Calculation | `order.service.spec.ts` → "should calculate tax..." | Unit |
| [BR-TRG-xxx] | Trigger | `orders.api.spec.ts` → "should emit event when..." | Integration |
| [BR-COH-xxx] | Consistency | `orders.api.spec.ts` → "should prevent when..." | Integration |

---

## 6. BA scenario coverage

The BA test scenarios `[TS-xxx]` from the `[TST-001]` BA dossier are implemented as follows:

| BA Scenario | BA Type | Technical test | Level |
|-------------|---------|----------------|-------|
| [TS-001] | Nominal | `create-order.spec.ts` → "should create order successfully" | E2E |
| [TS-010] | Edge case | `order.service.spec.ts` → "should accept minimum amount" | Unit |
| [TS-020] | Error | `order.service.spec.ts` → "should reject negative amount" | Unit |

---

## 7. NFR tests

### Performance

| Scenario | Endpoint | p95 threshold | p99 threshold | Load | Tool |
|----------|----------|--------------|--------------|------|------|
| <!-- E.g. Order creation --> | POST /api/orders | <!-- < 200ms --> | <!-- < 500ms --> | <!-- 100 req/s --> | <!-- k6 --> |
| <!-- E.g. Order list --> | GET /api/orders | <!-- < 100ms --> | <!-- < 300ms --> | <!-- 200 req/s --> | <!-- k6 --> |

### Security

| Check | Frequency | Tool | Threshold |
|-------|-----------|------|-----------|
| Dependency vulnerabilities | Every build | <!-- npm audit / Snyk --> | 0 critical, 0 high |
| OWASP Top 10 | Weekly | <!-- ZAP --> | 0 high alerts |
| Secrets in code | Every commit | <!-- TruffleHog / GitLeaks --> | 0 secret |

---

## 8. Test data

### Authoritative source: `[DAT-TEST-001]`

> *The seeds catalogue `[DAT-TEST-001]`, produced by BA agent 3.6, is the authoritative source of test datasets. It defines the FK insertion graph, the shared dataset, and per-scenario datasets, with a business justification for each significant value. Claude Code generates factories, SQL seeds, and fixtures from this catalogue.*

| Deliverable | Status | Note |
|-------------|--------|------|
| `[DAT-TEST-001]` BA Seeds Catalogue | <!-- Available / Pending --> | <!-- Link to file --> |

### Strategy by level

| Level | Data source | Reset | Authoritative source |
|-------|-------------|-------|---------------------|
| Unit | Inline data in the test (factories/builders) — cover each conditional branch | N/A | Business logic + [BRL-001] |
| Integration | Shared dataset + per-scenario datasets from `[DAT-TEST-001]` | Before each suite | `[DAT-TEST-001]` section 2 + 3 |
| E2E | Seeds from `[DAT-TEST-001]` + API setup calls | Before each scenario | `[DAT-TEST-001]` section 6 |

### Rule: branch coverage for unit tests

For each tested method, identify all conditional branches (`if/else`, `switch`, ternary operator, guard clause, `try/catch`) and generate one test case per branch. Do not settle for tests that merely "pass": the 90% branch coverage threshold is blocking.

### Factories / Builders

```typescript
// tests/factories/order.factory.ts
export const createTestOrder = (overrides?: Partial<Order>): Order => ({
  id: 'test-uuid-001',
  customerId: 'customer-uuid-001',
  status: 'draft',
  total: 150.00,
  createdAt: new Date('2025-01-15T10:00:00Z'),
  ...overrides,
});
```

---

## 9. Test environment

### Application startup

The startup procedure is defined in **`[STK-001] § Local startup`** (from ADR-ENV). It must be executed before any Playwright MCP navigation.

| Property | Value |
|----------|-------|
| **Start command** | <!-- E.g. `docker compose up` / `npm run dev:all` — see STK-001 --> |
| **Local URL** | <!-- E.g. http://localhost:3000 --> |
| **Health endpoint** | <!-- E.g. GET /health → 200 OK --> |
| **Required environment variables** | <!-- E.g. DATABASE_URL, AUTH_SECRET — see STK-001 --> |

### External system stubbing

For each external system identified in `[CTX-001]`, a stub enabler (`[ENB-STUB-XXX]`) must be implemented before the application can start in the test environment.

| External system | Stub type | Enabler | Status |
|----------------|-----------|---------|--------|
| <!-- E.g. Stripe payment service --> | <!-- MSW / WireMock / sandbox --> | <!-- [ENB-STUB-001] --> | <!-- Done / Pending --> |
| <!-- E.g. SendGrid email service --> | <!-- MSW / WireMock / fake env var --> | <!-- [ENB-STUB-002] --> | <!-- Done / Pending --> |

> ⚠️ **Mandatory rule:** no Playwright MCP navigation can start if a stub enabler is in `Pending` state. Navigating an application partially connected to real systems is forbidden in a test environment.

### Readiness check

Before any Playwright MCP navigation, Claude Code performs a readiness check:

```
curl -f http://localhost:{PORT}/health || echo "Application not ready — navigation blocked"
```

If the check fails, Claude Code must flag the blocker and not continue.

---

## 10. CI configuration

```yaml
# CI pipeline excerpt
test:
  stages:
    - unit-tests:
        command: npm test -- --coverage
        threshold: 80% lines
    - integration-tests:
        command: npm run test:integration
        services: [postgres, redis]
    - e2e-tests:
        command: npm run test:e2e
        services: [full-stack, stub-servers]  # stub-servers = external system stubs [ENB-STUB-XXX]
    - security-scan:
        command: npm audit --audit-level=high
```

---

## Traceability

### Technical traceability
| Element | Detail |
|---------|--------|
| **Produced by** | agent-t2.4-test-strategy |
| **Production date** | YYYY-MM-DD |
| **Technical inputs** | [CTX-001], [ADR-xxx], [STK-001], [DAT-001], [API-001], [ENB-xxx] |
| **Validated by** | Pending |
| **Validation date** | Pending |

### BA traceability
| BA Deliverable | Traced elements |
|----------------|-----------------|
| [BRL-001] | Business rules → Unit and integration tests |
| [TST-001] BA | BA scenarios → E2E and integration tests |
| [US-xxx] | Acceptance criteria → Tests per story |
