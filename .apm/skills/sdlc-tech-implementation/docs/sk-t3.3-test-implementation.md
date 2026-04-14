# Procedure: T3.3 — Test Implementation

## Purpose

Generate tests traceable to BA test scenarios and the TST-001 catalogue,
ensuring full coverage of the implemented item.

## Pre-conditions

- Resolved task file exists: `current-task-{item_id}.md`
- Implementation log exists: `impl-log-{item_id}.md` (code is generated)
- [TST-001] Test Strategy is available

## Steps

### 1. Identify mapped test IDs

From the resolved task's "Test IDs" section, extract all test IDs that correspond to this item:
- UT-xxx (unit tests)
- IT-xxx (integration tests)
- UFE-xxx (frontend unit tests)
- E2E-xxx (end-to-end tests)
- SEC-xxx (security tests)

### 2. Generate tests per type

#### Unit tests (UT-xxx)
1. Read test description from [TST-001]
2. Generate test class following [TST-001] naming conventions
3. Include BA traceability comment: `// Implements: [BR-xxx], [US-xxx]`
4. Use project-standard mocking framework for isolation

#### Integration tests (IT-xxx)
1. Read test description from [TST-001]
2. Generate test class extending project's integration test base
3. Use appropriate test containers or stubs for external dependencies
4. Include traceability comment linking to BA artifacts

#### Frontend tests (UFE-xxx)
1. Read test description from [TST-001]
2. Generate test co-located with the component under test
3. Use project-standard testing library for DOM assertions
4. Mock API calls using project-standard HTTP mocking
5. Include traceability comment: `// Implements: [TS-xxx], [BR-xxx]`

#### E2E tests (E2E-xxx)
1. Read E2E scenario from [TST-001]
2. Generate E2E test script using project-standard E2E framework
3. Include traceability comment linking to BA scenario [SCE-xxx]

#### Security tests (SEC-xxx)
1. Read security test descriptions from [TST-001]
2. Generate security-focused tests (authentication/authorization matrix)
3. Verify expected 401/403 responses for unauthorized access

### 3. Run tests

Execute the project test command for affected modules.

### 4. Write test log

Create `outputs/docs/2-tech/3-implementation/test-log-{item_id}.md` with:
- Test IDs implemented (linking to TST-001)
- Test files created
- Test execution results
- BA traceability mapping
- Coverage delta (if available)

## Gate criteria

- [ ] Every test ID from [TST-001] mapped to this item has a corresponding test file
- [ ] Tests pass (build green)
- [ ] Each test contains a BA traceability comment
- [ ] Test naming follows [TST-001] conventions
