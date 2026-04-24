---
id: sk-patterns-clean-architecture
category: patterns
technology: Clean Architecture
version: "N/A"
tags: [architecture, layered, ddd, hexagonal]
last_reviewed: 2025-01-15
---

# Skill: Clean Architecture

## Structure conventions

```
src/
├── domain/                         # Layer 1 — Entities & Business Rules
│   ├── entities/                   # Business entities (pure POJO/classes)
│   │   ├── User.ts
│   │   └── Order.ts
│   ├── value-objects/              # Immutable Value Objects
│   │   ├── Email.ts
│   │   └── Money.ts
│   ├── enums/                      # Business enums
│   │   └── OrderStatus.ts
│   ├── errors/                     # Typed business errors
│   │   ├── DomainError.ts
│   │   └── InsufficientFundsError.ts
│   └── ports/                      # Interfaces (contracts) — driven ports
│       ├── UserRepository.ts       # Repository interface
│       └── PaymentGateway.ts       # External service interface
│
├── application/                    # Layer 2 — Use Cases
│   ├── use-cases/
│   │   ├── CreateOrder.ts          # One file = one use case
│   │   └── GetUserProfile.ts
│   ├── dto/                        # Use case input/output DTOs
│   │   ├── CreateOrderInput.ts
│   │   └── CreateOrderOutput.ts
│   └── ports/                      # Driving ports (interfaces for controllers)
│       └── CreateOrderPort.ts
│
├── infrastructure/                 # Layer 3 — Adapters & Frameworks
│   ├── persistence/                # Repository implementations
│   │   ├── TypeOrmUserRepository.ts
│   │   └── mappers/                # Entity ↔ ORM model mappers
│   │       └── UserMapper.ts
│   ├── external/                   # Clients for external services
│   │   └── StripePaymentGateway.ts
│   ├── config/                     # Framework configuration
│   │   └── database.config.ts
│   └── http/                       # Controllers / Resolvers
│       ├── controllers/
│       │   └── OrderController.ts
│       ├── middleware/
│       └── validators/             # Request validation (Zod, class-validator)
│
└── main/                           # Composition Root
    ├── app.module.ts               # DI wiring
    └── main.ts                     # Entry point
```

## Code conventions

### Dependency rule

The fundamental rule: **dependencies point inward**.

```
HTTP → Application → Domain
Infrastructure → Application → Domain
```

- `domain/` depends on NOTHING (no imports from application/, infrastructure/, or any framework)
- `application/` depends only on `domain/`
- `infrastructure/` depends on `domain/` and `application/`
- `main/` assembles everything (composition root)

### Entities

- **Pure**: no ORM decorator, no framework annotation
- **Built-in validation**: business invariants are validated in the constructor or methods
- **Immutable where possible**: use methods that return new instances

```typescript
// ✅ Pure entity
export class Order {
  private constructor(
    readonly id: string,
    readonly items: ReadonlyArray<OrderItem>,
    readonly status: OrderStatus,
    readonly createdAt: Date,
  ) {}

  static create(items: OrderItem[]): Order {
    if (items.length === 0) {
      throw new EmptyOrderError();
    }
    return new Order(generateId(), items, OrderStatus.DRAFT, new Date());
  }

  confirm(): Order {
    if (this.status !== OrderStatus.DRAFT) {
      throw new InvalidStatusTransitionError(this.status, OrderStatus.CONFIRMED);
    }
    return new Order(this.id, this.items, OrderStatus.CONFIRMED, this.createdAt);
  }

  get total(): Money {
    return this.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}
```

### Use Cases

- **One file = one use case**: class with a single public method `execute()`
- **Input/Output DTOs**: never pass an entity as a use case parameter
- **Orchestration**: the use case orchestrates calls to repositories and services
- **No business logic** in the use case — delegated to entities

```typescript
// ✅ Use case
export class CreateOrder {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly productRepo: ProductRepository,
  ) {}

  async execute(input: CreateOrderInput): Promise<CreateOrderOutput> {
    const items = await Promise.all(
      input.items.map(i => this.productRepo.findById(i.productId))
    );
    const order = Order.create(items.map(toOrderItem));
    await this.orderRepo.save(order);
    return CreateOrderOutput.from(order);
  }
}
```

### Repositories

- **Interface in `domain/ports/`** — implementation in `infrastructure/persistence/`
- **Business-named methods**: `findByEmail()`, not `findOneBy({ email })`
- **Returns domain entities** — never ORM models
- **Explicit mapper** between ORM model and domain entity

### Dependency injection

- All dependencies are injected via the constructor
- Wiring is done in `main/` (composition root)
- No `new` for dependencies inside business classes

## Test conventions

### Domain layer

- **Pure unit tests** (no mocks, no DB)
- Test invariants, state transitions, validations
- 100% coverage targeted

### Application layer (use cases)

- **Unit tests with mocks** of ports (repositories, services)
- One test per user story scenario
- Use in-memory repositories for speed

### Infrastructure layer

- **Integration tests** with a real database (TestContainers)
- Test mappers (entity ↔ ORM model)
- Test controllers (request → response)

## Mandatory rules

1. **NEVER import from `infrastructure/` in `domain/`** — violation of the dependency rule
2. **NEVER framework decorators in `domain/`** — entities are pure
3. **NEVER expose ORM models outside `infrastructure/persistence/`** — always map to a domain entity
4. **One use case = one class = one file** — no "catch-all service"
5. **Business errors are typed classes** in `domain/errors/` — no strings or HTTP codes
6. **DTOs are plain objects** (no entity, no ORM model)
7. **The composition root is the only place** where concrete implementations are referenced
8. **No conditional business logic in controllers** — everything goes through a use case
