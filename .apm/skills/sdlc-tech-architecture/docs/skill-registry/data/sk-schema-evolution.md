# Skill: PostgreSQL Schema Evolution (Brownfield)

## Objective

This skill provides the patterns and technical constraints for evolving an existing PostgreSQL database schema in production with real data. It is loaded by agents T-0.2, T-2.1 and T-2.3 when the project is a brownfield evolution.

This skill complements `sk-postgresql.md` (schema conventions) by focusing on **alteration operations** rather than initial creation.

---

## Core principle: Zero-Downtime First

Every migration MUST be classified according to its operational impact **before** being planned:

| Class | Definition | Examples |
|-------|-----------|---------|
| **Safe** | Executable without service interruption, without prolonged lock | ADD COLUMN nullable, CREATE INDEX CONCURRENTLY |
| **Careful** | Risk of short lock or volume-dependent behaviour | ADD COLUMN with DEFAULT (PostgreSQL ≥ 11: safe) |
| **Dangerous** | Possible prolonged table lock or data loss | SET NOT NULL without default, DROP COLUMN, RENAME |
| **Destructive** | Irreversible, data loss | DROP TABLE, TRUNCATE |

---

## 1. Adding a column

### Pattern: Nullable-first

The safe method for adding a column that will eventually be NOT NULL.

**Step 1 — Add the nullable column (Safe)**
```sql
ALTER TABLE orders ADD COLUMN validation_status VARCHAR(50) NULL;
```

**Step 2 — Backfill existing data (Safe, in batches)**
```sql
-- Run in batches to avoid a prolonged lock on large tables
UPDATE orders SET validation_status = 'pending' WHERE validation_status IS NULL;
```

**Step 3 — Switch to NOT NULL with DEFAULT (Careful)**
```sql
ALTER TABLE orders ALTER COLUMN validation_status SET NOT NULL;
ALTER TABLE orders ALTER COLUMN validation_status SET DEFAULT 'pending';
```

> ⚠️ Never run all 3 steps in the same migration in production. Split into separate migrations with validation between each step.

### Pattern: ADD COLUMN WITH DEFAULT (PostgreSQL ≥ 11 only)

For columns with a static default value, PostgreSQL 11+ handles the DEFAULT without rewriting the table:

```sql
-- Safe on PostgreSQL ≥ 11 (no table rewrite)
ALTER TABLE orders ADD COLUMN is_priority BOOLEAN NOT NULL DEFAULT FALSE;
```

> ⚠️ On PostgreSQL < 11, this operation rewrites the entire table → **Dangerous** on large tables.

---

## 2. Modifying a column

### Changing the type

```sql
-- SAFE if the conversion is implicit (e.g. VARCHAR(50) → VARCHAR(100))
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255);

-- DANGEROUS if the conversion requires a cast (e.g. VARCHAR → INTEGER)
-- First verify that existing data is convertible:
SELECT COUNT(*) FROM users WHERE email !~ '^[0-9]+$';
```

### Renaming a column

Renaming is a **breaking change** if external queries or ORMs use the column name.

**Safe 3-step rename strategy:**

1. Add the new column with the new name
2. Create a bidirectional synchronisation trigger
3. Migrate consumers to the new name
4. Remove the old name and the trigger

```sql
-- Step 1: New column
ALTER TABLE orders ADD COLUMN customer_ref VARCHAR(50) NULL;

-- Step 2: Synchronisation trigger (during transition)
CREATE OR REPLACE FUNCTION sync_customer_ref() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
    NEW.customer_ref = COALESCE(NEW.customer_ref, NEW.client_code);
    NEW.client_code = COALESCE(NEW.client_code, NEW.customer_ref);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 3: After full consumer migration
ALTER TABLE orders DROP COLUMN client_code;
DROP TRIGGER IF EXISTS sync_customer_ref_trigger ON orders;
```

---

## 3. Dropping a column (Soft Deprecation)

Never drop a column directly in production without a deprecation period.

### Pattern: Soft Deprecation

**Step 1 — Mark the column as deprecated in documentation**
```sql
COMMENT ON COLUMN orders.legacy_reference IS 'DEPRECATED: scheduled for removal after 2026-06-01. Replaced by order_ref.';
```

**Step 2 — Remove application reads/writes** (in code, not in SQL)

**Step 3 — Verify zero usage**
```sql
-- Verify in application logs that the column is no longer accessed
-- Then verify in pg_stat_activity and column statistics
```

**Step 4 — Drop the column (after validation)**
```sql
ALTER TABLE orders DROP COLUMN IF EXISTS legacy_reference;
```

---

## 4. Dropping a table (DEPRECATE before DROP)

### Pattern: Table soft delete

```sql
-- Step 1: Rename the table to signal deprecation
ALTER TABLE paper_orders RENAME TO paper_orders_deprecated_20260601;

-- Step 2: Create a temporary compatibility view (if queries still exist)
CREATE VIEW paper_orders AS SELECT * FROM paper_orders_deprecated_20260601;

-- Step 3: After validation (end of deprecation window)
DROP VIEW IF EXISTS paper_orders;
DROP TABLE IF EXISTS paper_orders_deprecated_20260601;
```

---

## 5. Creating indexes on production tables

### CREATE INDEX CONCURRENTLY

In production, **always** use `CONCURRENTLY` to avoid the read/write lock:

```sql
-- CORRECT: no lock on the table during creation
CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders (customer_id);

-- INCORRECT in production: exclusive lock on the table
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
```

> ⚠️ `CREATE INDEX CONCURRENTLY` **cannot** be run inside a transaction (`BEGIN ... COMMIT`). It must be a standalone SQL statement in the migration.

### Managing Flyway / Prisma / TypeORM migrations

Some ORM tools automatically wrap migrations in a transaction. For `CREATE INDEX CONCURRENTLY`:

**Flyway:**
```sql
-- flyway:acceptMigrationChecksumWithoutVerifyVersion(true) -- disable transaction
-- @formatter:off
-- Put the CREATE INDEX CONCURRENTLY in a separate script with runInTransaction=false
```

**Prisma**: use `db execute` for non-transactional operations

**TypeORM**: use `queryRunner.createIndex()` or raw migrations with `transaction: false`

---

## 6. Constraints on existing tables

### ADD CHECK CONSTRAINT

On a table with existing data, a CHECK constraint is **validated against all rows** when added, which can be slow or fail.

```sql
-- Step 1: Add the constraint as NOT VALID (does not validate existing rows)
ALTER TABLE orders ADD CONSTRAINT chk_amount_positive CHECK (amount > 0) NOT VALID;

-- Step 2: Validate existing data in the background (does not acquire an exclusive lock)
ALTER TABLE orders VALIDATE CONSTRAINT chk_amount_positive;
```

### ADD FOREIGN KEY

```sql
-- Step 1: Add NOT VALID to avoid an immediate full scan
ALTER TABLE order_lines ADD CONSTRAINT fk_order_lines_order_id
  FOREIGN KEY (order_id) REFERENCES orders(id) NOT VALID;

-- Step 2: Validate (will take longer but without exclusive lock)
ALTER TABLE order_lines VALIDATE CONSTRAINT fk_order_lines_order_id;
```

---

## 7. Backfill strategy on large tables

For tables with > 100,000 rows, backfills MUST be performed in **batches** to avoid prolonged locks and WAL overload:

```sql
-- Batch backfill script (adapt based on volume)
DO $$
DECLARE
  batch_size INT := 1000;
  offset_val INT := 0;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE orders
    SET validation_status = 'pending'
    WHERE id IN (
      SELECT id FROM orders
      WHERE validation_status IS NULL
      LIMIT batch_size
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    PERFORM pg_sleep(0.1); -- Pause between batches to reduce load
  END LOOP;
END $$;
```

---

## 8. Brownfield migration checklist

Before delivering an `ALTER` or `DROP` migration in `[GAP-001]`:

- [ ] Each operation is classified: Safe / Careful / Dangerous / Destructive
- [ ] `Dangerous` operations have a defined rollback strategy
- [ ] `Destructive` operations are validated and flagged as irreversible
- [ ] `CREATE INDEX` on production tables uses `CONCURRENTLY`
- [ ] ADD FOREIGN KEY and CHECK CONSTRAINT use `NOT VALID` + `VALIDATE`
- [ ] Backfills on > 100k rows are in batch mode
- [ ] Migration order respects FK dependencies (no FK referencing a table not yet created)
- [ ] `SET NOT NULL` migrations are preceded by a verified backfill
- [ ] Column removals are preceded by a deprecation period
