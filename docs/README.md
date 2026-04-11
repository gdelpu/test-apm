# Documentation Hub

> Navigate the AI SDLC Foundation docs by audience.

---

## For Consumers

Teams installing and using the foundation in their own repositories.

| Document | What it covers |
|----------|---------------|
| [Quick Start](consumer/quick-start.md) | Install in 60 seconds, Hub Orchestrator, common workflows, per-provider usage |
| [APM Consumer Guide](consumer/apm-consumer-guide.md) | Install modes, customization, `providers-local/` overlay, CI integration, troubleshooting |

---

## Reference

Catalogs of all available agents, skills, workflows, hooks, and prompts — useful for both consumers and contributors.

| Document | What it covers |
|----------|---------------|
| [Agents](reference/agents.md) | All 23 agents with descriptions and key skills |
| [Skills](reference/skills.md) | All 94 skills organized by category |
| [Workflows](reference/workflows.md) | All 19 workflows with detailed station tables |
| [Hooks](reference/hooks.md) | 7 hook definitions + Python engine spec |
| [Prompts & Knowledge](reference/prompts.md) | 4 prompts and knowledge base areas |

---

## For Contributors

Maintainers developing, extending, or operating the foundation itself.

| Document | What it covers |
|----------|---------------|
| [Architecture](contributor/architecture.md) | Three-layer design, repository layout, source of truth rules |
| [Contributing](contributor/contributing.md) | Adding agents/skills/workflows, self-maintenance checklist, naming conventions, prerequisites |
| [Provider Setup](contributor/provider-setup.md) | Copilot three-layer projection, Claude Code, CLI configuration |
| [CI Pipeline](contributor/ci-pipeline.md) | PR validation pipeline (A0–A7), deterministic validators, local testing |
| [Local Testing](contributor/local-testing.md) | Run the full CI pipeline locally with Podman, environment variables, troubleshooting |
| [Distribution](contributor/distribution.md) | APM bundle build, publish, registry, consumer install channels |

---

## Shared

| Document | What it covers |
|----------|---------------|
| [Concepts & Glossary](concepts.md) | Building blocks: agents, workflows, skills, prompts, instructions, hooks, templates, contexts, scripts |
| [Output Metadata](output-metadata.md) | Mandatory YAML frontmatter for all `outputs/` files |
