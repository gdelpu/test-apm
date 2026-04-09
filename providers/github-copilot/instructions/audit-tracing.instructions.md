---
name: audit-tracing
description: 'Instruction for all agents to emit structured audit trace metadata and maintain correlation IDs across workflow execution.'
applyTo: '**'
---

# Audit Tracing Instructions

## Correlation ID

Every workflow execution has a trace correlation ID.  When executing a workflow:

1. If a `TRACE_ID` is provided in the context, propagate it to all sub-invocations.
2. If no trace ID exists, generate a UUID and set it as `TRACE_ID` for the session.
3. Include `trace_id` in all station output frontmatter.

## Structured trace metadata

When completing a station, include this metadata in your output frontmatter:

```yaml
---
trace_id: <propagated correlation ID>
station: <station ID>
agent: <your agent role>
skill: <skill used>
timestamp: <ISO 8601 UTC>
---
```

## Input/output handling

- Never include raw PII in outputs.  Use `[REDACTED]` placeholders for any personal data encountered.
- When processing user-provided content (tickets, logs, documents), scan for sensitive data before including in your analysis.
- Report the types of data found (email, phone, etc.) without reproducing the values.

## Tool invocation logging

When invoking tools, summarise:
- Which tool was called
- Purpose of the invocation
- Whether the tool accessed external resources

## Risk awareness

When your station execution involves any of these factors, note them in your output:
- **Regulated client**: the project has compliance requirements
- **External MCP tools**: tools from external providers were used
- **Production data**: real production data was processed
- **Destructive actions**: file deletions, database modifications, deployments
- **Autonomous execution**: actions taken without explicit user confirmation
