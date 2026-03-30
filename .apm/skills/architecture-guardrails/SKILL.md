# Skill: architecture-guardrails

## Goal

Apply architecture guardrails relevant to the chosen or existing architecture style and stack.

## When to use

- During plan review to validate architecture choices against established guardrails
- When the spec-orchestrator needs NFR and architecture validation
- When evaluating modernization target architectures

## Procedure

1. Identify the project's architecture style (monolith, microservice, etc.)
2. Identify the primary stack (.NET, Java, etc.)
3. Load the matching guardrail resource(s) from `resources/`
4. Evaluate the plan or spec against the guardrail criteria
5. Report violations, warnings, and recommendations

## Output

Architecture guardrail assessment included in the quality gate or review output.

## Resources

| Resource | Purpose |
|----------|----------|
| `resources/dotnet-guardrails.md` | .NET stack guardrails |
| `resources/java-guardrails.md` | Java stack guardrails |
| `resources/microservice-guardrails.md` | Microservice architecture guardrails |
| `resources/monolith-guardrails.md` | Monolith architecture guardrails |
