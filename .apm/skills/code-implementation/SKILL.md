# Skill: code-implementation

## Goal

Execute implementation tasks from a task breakdown, producing or modifying code while following project conventions, and verifying changes through build and test commands.

## When to use

- When the implementer agent needs to execute tasks from `tasks.md`
- When code changes need to be made according to an implementation plan
- When build and test verification is needed after code changes

## Procedure

### 1. Read context

- Load `tasks.md` for the task list
- Load `plan.md` for architectural decisions and constraints
- Load `constitution.md` for coding standards and quality expectations
- Identify the target project's build and test commands

### 2. Process tasks

For each task in dependency order:

    a. Read task description and acceptance criteria
    b. Identify affected files and modules
    c. Check that prerequisite tasks are completed
    d. Implement the change (create, modify, or delete files)
    e. Run build command if available
    f. Run test command if available
    g. Record result in implementation log

### 3. Produce implementation log

Write `implementation-log.md` with results for each task.

## Implementation discipline

- Follow existing code style and patterns
- Make minimal changes — only what the task requires
- Do not refactor unrelated code
- Do not add features beyond what is specified
- Prefer small, testable increments

## Build and test commands

The skill looks for project-specific commands:

| Signal | Build | Test |
|--------|-------|------|
| `package.json` | `npm run build` | `npm test` |
| `pom.xml` | `mvn compile` | `mvn test` |
| `build.gradle` | `gradle build` | `gradle test` |
| `Cargo.toml` | `cargo build` | `cargo test` |
| `pyproject.toml` / `setup.py` | — | `pytest` |
| `*.sln` / `*.csproj` | `dotnet build` | `dotnet test` |

If the project has a custom build/test script, prefer that over the default.

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/implementation-checklist.md` | Pre/post implementation verification checklist |
