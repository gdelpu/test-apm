---
name: playwright-browser-automation
description: 'Browser automation via Playwright MCP — navigate, interact, inspect accessibility snapshots, record tests, and capture screenshots.'
triggers:
  - playwright browser
  - browser automation
  - web testing mcp
  - accessibility snapshot
  - browser interaction
  - e2e browser
---

# Skill: playwright-browser-automation

## Goal

Automate browser interactions via the Playwright MCP server for E2E test execution, accessibility inspection, test recording, and visual validation — all through structured accessibility snapshots rather than screenshots.

## MCP Server

- **Registry ID**: `playwright-mcp`
- **Repository**: https://github.com/microsoft/playwright-mcp
- **Auth**: None required
- **Install**: `npx @playwright/mcp@latest`

## Key features

- Uses Playwright's accessibility tree — no vision models needed
- LLM-friendly structured data output
- Deterministic tool application
- Supports headed and headless modes
- Test code generation (TypeScript)

## Platform detection

Auto-detected when repo contains `playwright.config.ts` or `playwright.config.js`.

## When to use

- Executing E2E test scenarios against a running application
- Inspecting page accessibility for compliance validation
- Recording user flows for test generation
- Validating that generated Playwright scripts work against the live app
- Taking screenshots for visual regression documentation

## When NOT to use

- For unit or integration tests (use standard test runners)
- For API-only testing (no browser needed)
- When the application under test is not running / reachable
- For high-throughput CI test execution (prefer Playwright CLI for token efficiency)

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `playwright-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute browser operation

Based on the user's request:
- **Navigate**: Open URLs (restricted to project domain or localhost)
- **Interact**: Click, type, select — using accessibility tree selectors
- **Inspect**: Take accessibility snapshots of current page state
- **Assert**: Validate page content, element states, text content (opt-in via `--caps=testing`)
- **Record**: Generate TypeScript test code from interactions (via `--codegen typescript`)
- **Screenshot**: Capture page state for documentation (opt-in via `--caps=vision`)

### Step 3 — Format results

Write test results, accessibility reports, or generated scripts to output files.

### Fallback (without MCP)

If `playwright-mcp` is unavailable:
1. Execute Playwright tests via CLI (`npx playwright test`) if Playwright is installed
2. Generate Playwright test scripts as static TypeScript files without live verification
3. Perform static HTML/accessibility analysis on local files
4. Warn that live browser interaction is unavailable
5. Instruct user to run tests manually: `npx playwright test --headed`

## Output

Use `edit/editFiles` to write:
- `outputs/specs/features/<feature>/e2e-test-results.md` (test execution reports)
- Generated test scripts: written to the project's test directory

## Security

- Restrict navigation to project domain, `localhost`, or user-specified URLs only
- Never navigate to arbitrary external URLs
- Never interact with login forms or enter credentials via MCP
- Do not enable `--allow-unrestricted-file-access` unless explicitly requested
- Screenshots may contain sensitive data — treat as confidential
