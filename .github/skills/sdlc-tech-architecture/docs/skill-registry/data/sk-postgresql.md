---
id: sk-data-postgresql
category: data
technology: PostgreSQL
version: ">=15"
tags: [rdbms, sql, jsonb, extensions]
last_reviewed: 2025-01-15
---

# Skill: PostgreSQL 15+

## Structure conventions

### Migration organisation

```
migrations/
├── 001_initial_schema.sql          # Core tables
├── 002_add_indexes.sql             # Performance indexes
├── 003_seed_reference_data.sql     # Reference data
└── ...
```

- **Sequential numbering**: `{NNN}_{description}.sql`
- **Each migration is reversible**: include a `-- Down` block or a companion file
- **One concern per migration**: do not mix schema, data and indexes

### SQL script organisation

```
sql/
├── functions/          # Functions and stored procedures
├── triggers/           # Triggers
├── views/              # Views
├── indexes/            # Index scripts for tuning
└── seeds/              # Seed data per environment
    ├── dev/
    └── staging/
```

## Code conventions

### Naming

| Object | Convention | Example |
|--------|-----------|---------|
| Table | snake_case, **plural** | `users`, `order_items` |
| Column | snake_case, singular | `first_name`, `created_at` |
| Primary key | `id` (within the table) | `users.id` |
| Foreign key | `{singular_table}_id` | `user_id`, `order_id` |
| Index | `idx_{table}_{columns}` | `idx_users_email` |
| Unique index | `udx_{table}_{columns}` | `udx_users_email` |
| CHECK constraint | `chk_{table}_{description}` | `chk_orders_amount_positive` |
| UNIQUE constraint | `uq_{table}_{columns}` | `uq_users_email` |
| FK constraint | `fk_{table}_{ref_table}` | `fk_orders_users` |
| Enum type | snake_case, singular | `order_status` |
| Function | snake_case, verb | `calculate_total()` |
| Trigger | `trg_{table}_{event}` | `trg_users_updated_at` |
| View | `vw_{description}` | `vw_active_orders` |

### Recommended data types

| Use | PostgreSQL type | Note |
|-----|----------------|------|
| Identifier | `UUID` | With `gen_random_uuid()` |
| Short text (< 255) | `VARCHAR(n)` | Always with max length |
| Long text | `TEXT` | For descriptions, content |
| Boolean | `BOOLEAN` | No `SMALLINT` 0/1 |
| Integer | `INTEGER` / `BIGINT` | `BIGINT` for FKs if in doubt |
| Decimal (money) | `NUMERIC(precision, scale)` | Never `FLOAT` for money |
| Date | `DATE` | Without time |
| Timestamp | `TIMESTAMPTZ` | **Always** with timezone |
| Structured JSON | `JSONB` | Never `JSON` (not indexable) |
| Email | `CITEXT` | Case-insensitive (extension) |
| Enum | Custom `ENUM` type | See enums section |

### Mandatory audit columns

Each business table MUST have:

```sql
created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

With a trigger for `updated_at`:

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_{table}_updated_at
  BEFORE UPDATE ON {table}
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Soft delete (if applicable)

```sql
deleted_at  TIMESTAMPTZ NULL
```

- Default queries exclude deleted entries: `WHERE deleted_at IS NULL`
- Create a `vw_{table}_active` view if frequently used

### Indexes

- **Index on every FK**: PostgreSQL does not create them automatically
- **Index on frequently searched columns**: email, username, status
- **Composite index**: columns in decreasing selectivity order
- **Partial index** for frequent filters: `WHERE deleted_at IS NULL`
- **GIN index** for JSONB and full-text search

```sql
-- FK index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Partial index (soft delete)
CREATE INDEX idx_orders_active ON orders(status) WHERE deleted_at IS NULL;

-- GIN index for JSONB
CREATE INDEX idx_products_metadata ON products USING GIN(metadata);
```

### Enums

Use PostgreSQL ENUM types for finite, stable values:

```sql
CREATE TYPE order_status AS ENUM ('draft', 'confirmed', 'shipped', 'delivered', 'cancelled');
```

- **Value naming**: snake_case, lowercase
- **Do not use an enum** if values change frequently → use a reference table

### Transactions

- **All multi-table operations MUST be in a transaction**
- **Isolation level**: `READ COMMITTED` by default (sufficient for 99% of cases)
- **Advisory locks** for critical concurrent operations

## Test conventions

- **TestContainers**: use a PostgreSQL container for integration tests
- **Each test creates and destroys its data** — no dependency between tests
- **Test migrations**: mount/unmount the full schema
- **Test constraints**: verify that CHECK / UNIQUE / FK reject invalid data
- **Use `TRUNCATE ... CASCADE`** for fast cleanup between tests

## Mandatory rules

1. **ALWAYS `TIMESTAMPTZ`** — never `TIMESTAMP` without timezone
2. **ALWAYS `UUID` for primary keys exposed in APIs** — no exposed auto-increment
3. **NEVER `FLOAT` or `DOUBLE` for amounts** — use `NUMERIC`
4. **NEVER `SELECT *`** in application code — list the columns
5. **ALWAYS an index on every foreign key**
6. **Each migration is reversible** — include the rollback
7. **No business logic in triggers** — only audit (`updated_at`) and simple constraints
8. **Seed data is separated from schema migrations**
9. **`JSONB` never `JSON`** — `JSON` does not support GIN indexes
10. **No table without a primary key** — even join tables have a composite PK or a UUID
