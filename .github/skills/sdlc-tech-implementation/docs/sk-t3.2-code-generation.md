# Procedure: T3.2 — Code Generation

## Purpose

Produce or modify source code for the resolved task, following all project
conventions and upstream specifications exactly.

## Pre-conditions

- Resolved task file exists: `W{wave_id}/current-task-{item_id}.md`
- [STK-001] Stack Conventions is available
- Relevant upstream documents identified in the resolved task

## Steps

### 1. Load resolved task

Read `outputs/docs/2-tech/3-implementation/W{wave_id}/current-task-{item_id}.md` to get:
- Item metadata (type, scope, dependencies)
- Resolved context (ADRs, DAT, API, test IDs)
- Acceptance criteria
- Naming conventions

### 2. Load stack conventions

Read [STK-001] — extract:
- Project structure and module layout
- Naming conventions (packages, classes, files)
- Code patterns and idioms specific to the stack
- Framework-specific rules

### 3. Generate code per task type

#### Database tasks (migrations, entities)
1. Read [DAT-001] — exact column definitions, types, constraints, indexes
2. Generate migration file matching DAT-001 DDL exactly
3. Generate entity class with field mappings matching DAT-001
4. Verify FK references match DAT-001 relationship definitions

#### API controller tasks
1. Read [API-xxx] — endpoint URL, HTTP method, request/response DTOs, error codes, RBAC rules
2. Generate controller class matching API contract (URL, method, annotations)
3. Generate DTO classes matching API-xxx field definitions exactly
4. Generate service interface matching sequence diagram
5. Apply RBAC annotations as defined in [API-xxx]

#### Frontend tasks
1. Read [API-xxx] — expected request/response shapes for API calls
2. Read [STK-001] — frontend framework conventions, component patterns
3. Generate components following project conventions
4. Generate API client/hooks matching endpoint contracts

#### Enabler tasks (ENB-Cxx)
1. Read relevant [ADR-xxx] for decision context
2. Read [ENB-000] for enabler scope and included sub-tasks
3. Implement infrastructure/cross-cutting code per ADR decision

### 4. Run build

Execute the project build command to verify compilation:
- Only use commands from the project's `commandAllowlist`
- Build only affected modules when possible

### 5. Write implementation log

Create `outputs/docs/2-tech/3-implementation/W{wave_id}/impl-log-{item_id}.md` using the `tpl-impl-log.md` template with:
- Context loaded (documents read, sections referenced)
- Changes made (files created/modified with descriptions)
- Build result (output, status)
- ADR compliance check results
- Naming convention compliance

## Gate criteria

- [ ] Code compiles without errors
- [ ] Generated code adheres to [STK-001] naming conventions
- [ ] Database migrations match [DAT-001] column definitions exactly
- [ ] API controllers match [API-xxx] contracts (URL, method, DTOs, error codes)
- [ ] No files modified outside the task scope
