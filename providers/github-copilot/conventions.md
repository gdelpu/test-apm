# GitHub Copilot — File Format Conventions

Copilot recognizes specific file formats in `.github/`. Each format has its own
YAML frontmatter schema and naming convention.

---

## Agent files (`.github/agents/*.agent.md`)

**Naming**: `<agent-name>.agent.md` — the `<agent-name>` becomes the `@agent-name`
invocation in Copilot Chat.

**Frontmatter** (required):

```yaml
---
name: '<Display Name>'
description: '<one-liner>'
tools:
  - codebase
  - edit/editFiles
  - runCommands
commandAllowlist: ['<allowed-command-1>', '<allowed-command-2>']
allowedFilePaths: ['<glob-1>', '<glob-2>']
---
```

**Body**: Markdown describing purpose, decision policy, skills to invoke,
guardrails. The body is the system prompt Copilot uses when the agent is active.

**Security constraints**: Every agent must include anti-impersonation,
argument-injection prevention, content sanitisation, and processing-limit
sections in its body.

**Example**: `.github/agents/brand-styler.agent.md`

---

## Prompt files (`.github/prompts/*.prompt.md`)

**Naming**: `<prompt-name>.prompt.md` — the `<prompt-name>` becomes the `/prompt-name`
slash command in Copilot Chat.

**Frontmatter** (required):

```yaml
---
mode: agent
description: '<one-liner>'
---
```

**Body**: Markdown instructions executed when the user invokes the slash command.
Should specify what to do, what outputs to produce, and what to ask the user.

**Workflow prompts** use the naming pattern `workflow-<name>.prompt.md` to become
`/workflow-<name>` slash commands.

**Example**: `.github/prompts/workflow-feature.prompt.md`

---

## Instruction files (`.github/instructions/*.instructions.md`)

**Naming**: `<domain>.instructions.md` — descriptive name for the instruction scope.

**Frontmatter** (required):

```yaml
---
applyTo: '<glob-pattern>'
---
```

**Body**: Markdown with rules, conventions, and guidelines that are injected into
Copilot's context whenever the user is working on files matching the `applyTo`
pattern.

**Example**: `.github/instructions/apm-layer.instructions.md` with `applyTo: .apm/**`

---

## Hub-wide context (`.github/copilot-instructions.md`)

Single file loaded for **every** Copilot chat in this repository. Contains
repository layout, working rules, and workflow catalog. No frontmatter needed.

---

## Naming rules

| Type | Pattern | Example |
|------|---------|---------|
| Agent | `<kebab-case>.agent.md` | `brand-styler.agent.md` |
| Prompt | `<kebab-case>.prompt.md` | `create-one-pager.prompt.md` |
| Workflow prompt | `workflow-<name>.prompt.md` | `workflow-feature.prompt.md` |
| Instruction | `<domain>.instructions.md` | `apm-layer.instructions.md` |
| Hub context | `copilot-instructions.md` | *(exactly this name)* |
