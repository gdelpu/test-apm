---
name: scenario-4-human-gate
description: 'Intentionally keeps blocking issues through 3 attempts to trigger human review gate'
---

# Scenario 4: Human Review Gate

Push this 3 times without fixing the companion workflow.yml.
The workflow intentionally stays blocking because it is missing the top-level `on` trigger.
On attempt 3, the pipeline should block with: "Human Review Gate - AI reached iteration 3".
