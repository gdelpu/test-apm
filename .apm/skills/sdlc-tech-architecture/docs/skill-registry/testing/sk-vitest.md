---
id: sk-testing-vitest
category: testing
technology: Vitest
version: ">=1.0"
tags: [unit, fast, esm, typescript, vite]
last_reviewed: 2026-03-03
---

# Skill: Vitest

## Structure conventions

```
src/
├── components/
│   └── UserCard/
│       ├── UserCard.tsx
│       ├── UserCard.spec.tsx        # Collocated test
│       └── index.ts
├── utils/
│   ├── formatDate.ts
│   └── formatDate.spec.ts
└── test/                            # Global config and helpers
    ├── setup.ts                     # Vitest setup file
    ├── mocks/
    │   ├── handlers.ts              # MSW handlers
    │   └── server.ts                # MSW server setup
    ├── factories/
    │   └── user.factory.ts
    └── utils/
        └── render.tsx               # Custom render with providers
```

## Code conventions

### Configuration (`vitest.config.ts`)

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      thresholds: {
        lines: 90,
        branches: 90,
        functions: 90,
        statements: 90,
      },
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/index.ts',
      ],
    },
  },
});
```

### Setup file (`src/test/setup.ts`)

```typescript
import '@testing-library/jest-dom';
import { configureAxe, toHaveNoViolations } from 'jest-axe';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from './mocks/server';

// Accessibility assertions
expect.extend(toHaveNoViolations);

// MSW
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Test structure

```typescript
// UserCard.spec.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import { UserCard } from './UserCard';
import { userFactory } from '../../test/factories/user.factory';

describe('UserCard', () => {
  it('should display user name and email', () => {
    // Arrange
    const user = userFactory.build({ name: 'Alice Martin', email: 'alice@test.fr' });

    // Act
    const { container } = render(<UserCard user={user} />);

    // Assert
    expect(screen.getByText('Alice Martin')).toBeInTheDocument();
    expect(screen.getByText('alice@test.fr')).toBeInTheDocument();
  });

  it('should be accessible', async () => {
    // Arrange
    const user = userFactory.build();
    const { container } = render(<UserCard user={user} />);

    // Accessibility assertion — mandatory on every new component
    expect(await axe(container)).toHaveNoViolations();
  });

  it('should call onSelect when clicked', async () => {
    // Arrange
    const user = userFactory.build();
    const onSelect = vi.fn();
    render(<UserCard user={user} onSelect={onSelect} />);

    // Act
    await userEvent.click(screen.getByRole('article'));

    // Assert
    expect(onSelect).toHaveBeenCalledWith(user.id);
  });
});
```

### `describe` / `it` conventions

- Identical to `sk-jest-rtl.md`: `describe` = component/module name, `it` starts with `should`
- Nested `describe` to group by context (`when the form is empty`, etc.)

### Mocking with `vi`

```typescript
// Module mock
vi.mock('../services/analytics', () => ({
  trackEvent: vi.fn(),
}));

// Spy on a method
const spy = vi.spyOn(service, 'calculate');
expect(spy).toHaveBeenCalledWith(42);

// Date mock
vi.setSystemTime(new Date('2026-01-15'));
vi.useRealTimers(); // restore after the test
```

### Factories

Identical to `sk-jest-rtl.md` — use `@faker-js/faker` with the `build()` / `buildList()` pattern.

### Custom render (identical to `sk-jest-rtl.md`)

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { render } from '@testing-library/react';

export function renderWithProviders(
  ui: React.ReactElement,
  options?: { route?: string }
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[options?.route ?? '/']}>
        {ui}
      </MemoryRouter>
    </QueryClientProvider>
  );
}
```

## Accessibility (jest-axe)

Identical to `sk-jest-rtl.md` — `jest-axe` works with Vitest via `expect.extend(toHaveNoViolations)`.

```typescript
it('should be accessible', async () => {
  const { container } = render(<MyComponent />);
  expect(await axe(container)).toHaveNoViolations();
});
```

Rule: every new rendered component MUST have a `should be accessible` test.

## Differences with Jest

| Topic | Jest | Vitest |
|---|---|---|
| Import | `import { jest }` | `import { vi }` |
| Mocking | `jest.fn()`, `jest.mock()` | `vi.fn()`, `vi.mock()` |
| Timers | `jest.useFakeTimers()` | `vi.useFakeTimers()` |
| Spy | `jest.spyOn()` | `vi.spyOn()` |
| Config | `jest.config.ts` | `vitest.config.ts` |
| Globals | via `@types/jest` | via `globals: true` in config |
| ESM | Requires special config | Native |
| Speed | Standard | Faster (HMR, threads) |

## Mandatory rules

1. **ALWAYS `vi.*` instead of `jest.*`** — do not mix both in a Vitest project
2. **Coverage thresholds ≥ 90%** line and branch — configured in `vitest.config.ts`, non-negotiable
3. **ALWAYS `jest-axe` on every new component** — `expect(await axe(container)).toHaveNoViolations()`
4. **MSW for API mocks** — same convention as `sk-jest-rtl.md`
5. **`globals: true` in config** — avoids importing `describe`, `it`, `expect` in every file
6. **Coverage provider `v8`** — faster and native on Vite/Vitest projects
7. **NEVER `vi.mock()` on what is actually being tested** — only mock external dependencies
8. **Independent tests** — use `vi.restoreAllMocks()` in `afterEach` if spies are used
9. **`environment: 'jsdom'`** for React component tests — `node` for pure services/utils
10. **Automatic cleanup** — `@testing-library/react` does it by default with Vitest
