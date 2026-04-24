---
id: sk-testing-playwright
category: testing
technology: Playwright
version: ">=1.40"
tags: [e2e, browser, automation, accessibility]
last_reviewed: 2026-03-03
---

# Skill: Playwright (E2E Tests)

## Structure conventions

```
tests/
├── e2e/
│   ├── pages/                        # Page Object Models
│   │   ├── LoginPage.ts
│   │   ├── DashboardPage.ts
│   │   └── index.ts                  # Centralised re-export
│   ├── fixtures/
│   │   ├── auth.fixture.ts           # Authentication fixtures
│   │   └── base.fixture.ts           # Base fixture (extend test)
│   ├── helpers/
│   │   └── seed-loader.ts            # Seed loading [DAT-TEST-001]
│   └── specs/                        # E2E spec files
│       ├── auth.e2e.spec.ts
│       ├── orders.e2e.spec.ts
│       └── ...
├── playwright.config.ts              # Global configuration
└── .auth/                            # Saved authentication states
    └── .gitkeep                      # (JSON files generated dynamically)
```

## Code conventions

### Global configuration (`playwright.config.ts`)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e/specs',
  testMatch: '**/*.e2e.spec.ts',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    // Setup: shared authentication
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### Page Object Model (POM)

```typescript
// tests/e2e/pages/OrderFormPage.ts
import { type Page, type Locator } from '@playwright/test';

export class OrderFormPage {
  // Locators declared as class properties
  readonly titleInput: Locator;
  readonly quantityInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private readonly page: Page) {
    // Selector preference order:
    // 1. getByRole  2. getByLabel  3. getByTestId  (never arbitrary CSS)
    this.titleInput = page.getByLabel('Order title');
    this.quantityInput = page.getByRole('spinbutton', { name: 'Quantity' });
    this.submitButton = page.getByRole('button', { name: /confirm/i });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/orders/new');
  }

  async fillForm(data: { title: string; quantity: number }) {
    await this.titleInput.fill(data.title);
    await this.quantityInput.fill(String(data.quantity));
  }

  async submit() {
    await this.submitButton.click();
  }
}
```

### Authentication fixtures

```typescript
// tests/e2e/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.login(process.env.TEST_USER_EMAIL!, process.env.TEST_USER_PASSWORD!);
    await use(page);
  },
});

export { expect } from '@playwright/test';
```

### Spec file structure

```typescript
// tests/e2e/specs/orders.e2e.spec.ts
import { test, expect } from '../fixtures/base.fixture';
import { OrderFormPage } from '../pages/OrderFormPage';
import { OrderListPage } from '../pages/OrderListPage';

// Implements: [E2E-TST-001], [US-012] AC-3, [US-005] AC-1
test.describe('Order creation and validation', () => {
  test.beforeEach(async ({ page }) => {
    // Load specific dataset if needed
    // Base seeds are loaded by the global setup
  });

  test('should create an order and see it in the list', async ({ page }) => {
    // Arrange
    const formPage = new OrderFormPage(page);
    const listPage = new OrderListPage(page);
    await formPage.goto();

    // Act
    await formPage.fillForm({ title: 'Test order', quantity: 5 });
    await formPage.submit();

    // Assert
    await expect(page).toHaveURL(/\/orders\/\d+/);
    await listPage.goto();
    await expect(listPage.getOrderByTitle('Test order')).toBeVisible();
  });

  test('should display an error if the quantity is invalid', async ({ page }) => {
    // Arrange
    const formPage = new OrderFormPage(page);
    await formPage.goto();

    // Act
    await formPage.fillForm({ title: 'Test order', quantity: -1 });
    await formPage.submit();

    // Assert
    await expect(formPage.errorMessage).toContainText(/invalid quantity/i);
    await expect(page).toHaveURL('/orders/new');
  });
});
```

### Naming conventions

- **Spec files:** `{domain}.e2e.spec.ts`
- **Page Objects:** `{PageName}Page.ts` (PascalCase)
- **Fixtures:** `{context}.fixture.ts`
- **`test.describe`**: description of the feature or flow under test
- **`test`**: starts with `should` + expected behaviour

### Authentication management

```typescript
// tests/e2e/setup/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('reference user authentication', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL('/dashboard');
  // Save authentication state for reuse
  await page.context().storageState({ path: '.auth/user.json' });
});
```

---

## Accessibility (axe-core + Playwright)

### Principle

Each E2E spec includes an accessibility assertion **on every page navigated**. The objective is to detect WCAG 2.1 AA violations at the system flow level, complementing `jest-axe` assertions at the component level.

### axe setup in Playwright

```typescript
// tests/e2e/helpers/accessibility.ts
import { type Page, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export async function checkAccessibility(
  page: Page,
  options?: {
    tags?: string[];         // e.g. ['wcag2a', 'wcag2aa', 'wcag21aa']
    exclude?: string[];      // CSS selectors to exclude (e.g. ['#chatbot-widget'])
  }
) {
  const results = await new AxeBuilder({ page })
    .withTags(options?.tags ?? ['wcag2a', 'wcag2aa'])
    .exclude(options?.exclude ?? [])
    .analyze();

  expect(results.violations).toEqual([]);
}
```

### Usage in specs

```typescript
import { checkAccessibility } from '../helpers/accessibility';

test.describe('Order form', () => {
  test('should be accessible on the creation page', async ({ page }) => {
    // Arrange
    const formPage = new OrderFormPage(page);
    await formPage.goto();

    // Accessibility assertion — include on every page navigated
    await checkAccessibility(page);
  });

  test('should create an order and see it in the list', async ({ page }) => {
    const formPage = new OrderFormPage(page);
    const listPage = new OrderListPage(page);

    await formPage.goto();
    await checkAccessibility(page);                        // ← form page

    await formPage.fillForm({ title: 'Test order', quantity: 5 });
    await formPage.submit();

    await listPage.goto();
    await checkAccessibility(page);                        // ← list page
  });
});
```

### Handling known false positives

```typescript
// Log known and accepted violations in a dedicated file
// tests/e2e/helpers/accessibility-known-issues.ts
export const KNOWN_A11Y_VIOLATIONS = [
  {
    id: 'color-contrast',
    description: 'Third-party widget #widget-xyz — outside our control',
    selector: '#widget-xyz',
  },
];

// In checkAccessibility, filter known violations before assertion
```

### Rule: when to assert accessibility

| Situation | Assertion required |
|---|---|
| Each new page navigated in an E2E flow | ✅ Mandatory |
| State after an action (modal opened, error message displayed) | ✅ Mandatory |
| Navigation within a component without page change (SPA) | ✅ Mandatory |
| Intermediate step in a multi-page form | ✅ Mandatory |

---

## Mandatory rules

1. **NEVER arbitrary CSS selectors** — only `getByRole`, `getByLabel`, `getByTestId` (with explicit `data-testid`), `getByText` for content
2. **NEVER `page.waitForTimeout()`** — use `waitForURL`, `waitForSelector`, `waitFor` with condition, or `expect(locator).toBeVisible()`
3. **ALWAYS use Page Object Model** — no inline selectors in spec files
4. **Selectors come from Playwright MCP sessions** — not invented by hand (avoids fragile selectors)
5. **ALWAYS `checkAccessibility()` on every page navigated** — no E2E flow without an axe assertion
6. **WCAG 2.1 AA by default** — minimum level unless the project defines a different level in `[NFR-TEST-xxx]`
7. **E2E tests are independent** — a test does not depend on state left by another test
8. **Shared authentication via `storageState`** — do not re-login in each test
9. **Environment variables for credentials** — never hardcoded values (email/password)
10. **Screenshots and traces enabled in CI** — `screenshot: 'only-on-failure'`, `trace: 'on-first-retry'`
