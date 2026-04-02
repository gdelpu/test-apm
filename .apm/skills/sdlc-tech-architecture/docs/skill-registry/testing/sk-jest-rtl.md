---
id: sk-testing-jest-rtl
category: testing
technology: Jest + React Testing Library
version: ">=29.0"
tags: [unit, component, frontend, react, typescript]
last_reviewed: 2025-01-15
---

# Skill: Jest + React Testing Library (RTL)

## Structure conventions

```
src/
├── components/
│   └── UserCard/
│       ├── UserCard.tsx
│       ├── UserCard.spec.tsx        # Collocated test
│       └── index.ts
├── features/
│   └── orders/
│       ├── components/
│       │   └── OrderList.spec.tsx
│       ├── hooks/
│       │   └── useFetchOrders.spec.ts
│       └── services/
│           └── order.service.spec.ts
└── test/                            # Global config and helpers
    ├── setup.ts                     # Jest setup file
    ├── mocks/
    │   ├── handlers.ts              # MSW handlers
    │   └── server.ts                # MSW server setup
    ├── factories/
    │   ├── user.factory.ts          # Factory for creating mock User objects
    │   └── order.factory.ts
    └── utils/
        ├── render.tsx               # Custom render with providers
        └── expectations.ts          # Custom matchers
```

## Code conventions

### Test file naming

- **Unit tests**: `{Name}.spec.ts` or `{Name}.spec.tsx`
- **Integration tests**: `{Name}.integration.spec.ts`
- **Collocation**: the test is in the same folder as the tested file

### Test structure

```tsx
describe('OrderList', () => {
  // Common arrange (if applicable)
  const defaultProps: OrderListProps = {
    filters: { status: 'active' },
  };

  // Happy path
  it('should display the list of orders', async () => {
    // Arrange
    render(<OrderList {...defaultProps} />);

    // Act (implicit — render is the action)

    // Assert
    expect(await screen.findByText('Order #001')).toBeInTheDocument();
    expect(screen.getAllByRole('row')).toHaveLength(3);
  });

  // Error case
  it('should display an error message when the API fails', async () => {
    // Arrange
    server.use(
      http.get('/api/orders', () => HttpResponse.json(null, { status: 500 }))
    );

    // Act
    render(<OrderList {...defaultProps} />);

    // Assert
    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });

  // User interaction
  it('should call onSelect when an order is clicked', async () => {
    // Arrange
    const onSelect = vi.fn();
    render(<OrderList {...defaultProps} onSelect={onSelect} />);

    // Act
    await userEvent.click(await screen.findByText('Order #001'));

    // Assert
    expect(onSelect).toHaveBeenCalledWith('order-001');
  });
});
```

### `describe` / `it` conventions

- **`describe`**: the name of the component, hook or service under test
- **`it`**: starts with `should` + expected behaviour
- **Nested `describe`** to group by context:

```tsx
describe('OrderForm', () => {
  describe('when the form is empty', () => {
    it('should disable the submit button', () => { ... });
  });

  describe('when the form is filled', () => {
    it('should enable the submit button', () => { ... });
    it('should call onSubmit with the form data', () => { ... });
  });

  describe('when the API returns an error', () => {
    it('should display the error message', () => { ... });
  });
});
```

### RTL selectors (in order of preference)

1. **`getByRole`** — accessible, recommended by default
2. **`getByLabelText`** — for form fields
3. **`getByPlaceholderText`** — if no label
4. **`getByText`** — for text content
5. **`getByDisplayValue`** — for inputs with a value
6. **`getByTestId`** — **last resort** only

```tsx
// ✅ Preferred
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText('Email');

// ❌ Avoid
screen.getByTestId('submit-button');
document.querySelector('.btn-submit');
```

### Async

- **`findBy*`** for elements that appear after an async render (API call, etc.)
- **`waitFor`** for complex async assertions
- **`userEvent`** instead of `fireEvent` — simulates real user behaviour

```tsx
// ✅ Correct
const element = await screen.findByText('Loaded');
await userEvent.type(screen.getByLabelText('Name'), 'John');

// ❌ Incorrect
fireEvent.change(input, { target: { value: 'John' } });
```

### Mocking

#### MSW (Mock Service Worker) for APIs

```tsx
// test/mocks/handlers.ts
export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([userFactory.build(), userFactory.build()]);
  }),
  http.post('/api/orders', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: 'order-001', ...body }, { status: 201 });
  }),
];
```

- **MSW preferred** over `jest.mock()` for API calls
- Default handlers are in `test/mocks/handlers.ts`
- Override per test with `server.use(...)` for error cases

#### Module mocking

```tsx
// ✅ Targeted mock
vi.mock('../services/analytics', () => ({
  trackEvent: vi.fn(),
}));

// ❌ Avoid overly broad mock
vi.mock('react-router-dom');  // Mocks the entire module
```

### Factories

```tsx
// test/factories/user.factory.ts
import { faker } from '@faker-js/faker';

export const userFactory = {
  build: (overrides: Partial<User> = {}): User => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    role: 'user',
    createdAt: faker.date.past().toISOString(),
    ...overrides,
  }),
  buildList: (count: number, overrides?: Partial<User>): User[] =>
    Array.from({ length: count }, () => userFactory.build(overrides)),
};
```

### Custom Render

```tsx
// test/utils/render.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';

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

### Installation and setup

```typescript
// test/setup.ts
import { configureAxe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);
```

### Usage in tests

```tsx
import { axe } from 'jest-axe';

describe('UserCard', () => {
  // Functional case
  it('should display user name and email', () => {
    const user = userFactory.build();
    render(<UserCard user={user} />);
    expect(screen.getByText(user.name)).toBeInTheDocument();
  });

  // Accessibility assertion — mandatory on every new rendered component
  it('should be accessible', async () => {
    const { container } = render(<UserCard user={userFactory.build()} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
```

### Application rule

| Situation | Assertion required |
|---|---|
| New rendered React component | ✅ Mandatory — `expect(await axe(container)).toHaveNoViolations()` |
| Existing component modified (HTML structure) | ✅ Mandatory |
| Pure logic test (service, hook without render) | ❌ Not applicable |
| Component with loading or error state | ✅ Test each state |

### Handling known false positives

```tsx
// If a violation is outside the project's control (third-party component):
const results = await axe(container, {
  rules: { 'color-contrast': { enabled: false } }, // document the reason
});
expect(results).toHaveNoViolations();
// Comment why this rule is disabled
```

Rule disabling MUST be rare and documented. Real violations in our code are not false positives — they must be fixed.

---

## Mandatory rules

1. **NEVER test implementation details** — no tests on internal state, CSS class names, or exact DOM structure
2. **ALWAYS `userEvent` instead of `fireEvent`** — except for events not supported by userEvent
3. **ALWAYS `findBy*` for async** — never `getBy*` + `waitFor` when `findBy*` suffices
4. **Tests MUST be independent** — no order dependency between `it` blocks
5. **NEVER `sleep` or `setTimeout` in tests** — use `waitFor` or `findBy*`
6. **MSW for API mocks** — no `jest.mock()` on fetch/axios
7. **One test = one behaviour** — no test that verifies 10 different things
8. **Factories produce realistic data** — use `@faker-js/faker`
9. **`getByTestId` is a last resort** — prefer accessible selectors
10. **Automatic cleanup** — RTL does it by default, do not call `cleanup()` manually
11. **ALWAYS `jest-axe` on every new rendered component** — `expect(await axe(container)).toHaveNoViolations()` is mandatory, not optional
