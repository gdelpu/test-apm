---
id: sk-frameworks-react
category: frameworks
technology: React
version: ">=18.0"
tags: [frontend, spa, hooks, typescript]
last_reviewed: 2025-01-15
---

# Skill: React 18+

## Structure conventions

```
src/
├── app/                    # Entry point, providers, routing
│   ├── App.tsx
│   ├── providers.tsx       # Composition of context providers
│   └── routes.tsx          # Route configuration
├── components/             # Reusable components (internal UI library)
│   ├── ui/                 # Atomic components (Button, Input, Modal)
│   │   ├── Button.tsx
│   │   ├── Button.spec.tsx
│   │   └── index.ts
│   └── layout/             # Layout components (Header, Sidebar)
├── features/               # Feature modules (domain-based slicing)
│   └── {feature-name}/
│       ├── components/     # Components specific to the feature
│       ├── hooks/          # Hooks specific to the feature
│       ├── services/       # API calls for the feature
│       ├── types.ts        # TypeScript types for the feature
│       └── index.ts        # Entry point (barrel export)
├── hooks/                  # Generic reusable hooks
├── services/               # Generic API services
│   ├── api-client.ts       # Configured axios/fetch instance
│   └── {resource}.service.ts
├── stores/                 # State management (if Zustand/Redux)
├── types/                  # Global types and DTOs
├── utils/                  # Pure utility functions
└── test/                   # Test configuration and helpers
    ├── setup.ts
    ├── mocks/
    └── factories/
```

## Code conventions

### Components

- **Naming**: PascalCase for components, `{Name}.tsx`
- **Type**: Function components only — no class components
- **Export**: Named export preferred, no default export (except pages if required by the framework)
- **Props**: Defined via `interface {Name}Props` in the same file
- **Destructuring**: Always destructure props in the signature

```tsx
// ✅ Correct
interface UserCardProps {
  user: User;
  onSelect: (userId: string) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
  return (/* ... */);
}

// ❌ Incorrect
export default function UserCard(props: any) { /* ... */ }
```

### Hooks

- **Naming**: `use{Action}{Resource}` — e.g. `useFetchUsers`, `useCreateOrder`
- **Custom hooks**: extract reusable logic into dedicated hooks
- **No business logic in components** — always in a hook or a service
- **Effect dependencies**: exhaustive-deps ESLint rule is mandatory

```tsx
// ✅ Data fetching hook
export function useFetchUsers(filters: UserFilters) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => userService.getAll(filters),
  });
}
```

### State management

- **Local state**: `useState` for simple UI state
- **Server state**: React Query (TanStack Query) — no Redux state for server data
- **Global client state**: Zustand or Context API for shared client state
- **No prop drilling** beyond 2 levels — use Context or Zustand

### Error handling

- **Error Boundaries**: at least one per feature route
- **Toast/notifications**: centralised via a `useNotification` hook
- **API errors**: intercepted at the service level, propagated as business types

## Test conventions

- **Framework**: Jest + React Testing Library (RTL)
- **Naming**: `{Component}.spec.tsx` (collocated with the component)
- **Philosophy**: test user behaviour, not implementation
- **No tests on implementation details** (no internal state testing)

```tsx
// ✅ Correct RTL test
describe('UserCard', () => {
  it('should display the user name', () => {
    render(<UserCard user={mockUser} onSelect={vi.fn()} />);
    expect(screen.getByText(mockUser.name)).toBeInTheDocument();
  });

  it('should call onSelect when clicked', async () => {
    const onSelect = vi.fn();
    render(<UserCard user={mockUser} onSelect={onSelect} />);
    await userEvent.click(screen.getByRole('button'));
    expect(onSelect).toHaveBeenCalledWith(mockUser.id);
  });
});
```

- **Mocks**: mock API services, not internal hooks
- **Factories**: use factories for test data
- **Accessibility**: `getByRole` preferred over `getByTestId`

## Mandatory rules

1. **NEVER `any`** — use precise types or `unknown` if necessary
2. **NEVER `useEffect` for server data synchronisation** — use React Query
3. **NEVER direct DOM manipulation** — only via React refs if necessary
4. **ALWAYS memoize callbacks passed to children** if children are memoized (`useCallback`)
5. **ALWAYS separate business logic from UI** — hooks for logic, components for rendering
6. **ALWAYS use barrel exports** (`index.ts`) for features and components
7. **ALWAYS type custom hook return values** — no implicit inference on public signatures
8. **List keys (`key`) MUST be stable identifiers** — never the array index
