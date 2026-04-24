---
name: mslearn-docs-lookup
description: 'Query Microsoft Learn documentation via MCP — fetch up-to-date .NET, Azure, M365, and PowerShell API references and guides.'
triggers:
  - microsoft learn
  - mslearn docs
  - dotnet documentation
  - azure documentation
  - microsoft api reference
---

# Skill: mslearn-docs-lookup

## Goal

Query Microsoft Learn documentation via the MsLearn MCP server to fetch up-to-date API references, guides, and best practices for .NET, Azure, M365, and PowerShell.

## MCP Server

- **Registry ID**: `mslearn-mcp`
- **Repository**: https://github.com/MicrosoftDocs/mcp
- **Auth**: None required
- **Install**: `npx @microsoftdocs/mcp@latest`

## Platform detection

Auto-detected when repo contains `*.csproj`, `*.sln`, or `global.json`.

## When to use

- Looking up .NET API documentation during code generation
- Referencing Azure service documentation for architecture decisions
- Checking PowerShell cmdlet documentation for script generation
- Validating code examples against current Microsoft documentation
- Enriching technical architecture documents with official references

## When NOT to use

- For non-Microsoft technologies (use `context7-docs` skill)
- For general library documentation (use `context7-docs` skill)
- When offline documentation is sufficient

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `mslearn-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Query documentation

Based on the user's request:
- **API reference**: Look up specific class, method, or namespace documentation
- **Guide search**: Find how-to guides and tutorials for a topic
- **Best practices**: Retrieve Microsoft's recommended patterns for a scenario
- **Version-specific**: Query docs for a specific .NET / Azure SDK version

### Step 3 — Integrate results

Include relevant documentation excerpts in the current workflow deliverable. Always cite the source URL.

### Fallback (without MCP)

If `mslearn-mcp` is unavailable:
1. Use agent's training knowledge for Microsoft technology guidance
2. Warn that documentation may not reflect the latest API versions
3. Add `[DOCS-NOT-VERIFIED]` marker to any Microsoft-specific code examples
4. Suggest user verify against https://learn.microsoft.com manually

## Output

Integrates into the calling workflow's output files. Documentation references are woven into specifications, architecture documents, and implementation guides.

## Security

- Do not include any authentication tokens in documentation queries
- Documentation content is public — no redaction needed
