Architecture: “Agent Factory” with Station Gates (PR-driven)
What happens on a PR that adds/changes an agent or skill
Station A0 — Intake
Pull PR context: changed files, diff, metadata
Output: outputs/station_out/work_order.json
Station A1 — Policy & Structure Validation (deterministic)
Validate agent/skill manifests against JSON Schema
Enforce rules: tool allowlists, no “wildcard exec”, required safety fields
Output: outputs/station_out/policy_report.json
Station A2 — Security Static Checks (deterministic)
Secret scan (repo + diff)
Dependency scan (if code changed)
“Dangerous patterns” scan (shell injection, curl|bash, eval, unrestricted file reads)
Output: outputs/station_out/security_report.json
Station A3 — Prompt Injection & Exfil Hardening Checks (deterministic + optional agent)
Deterministic scanners:
Look for jailbreak phrases / instruction override patterns
Ensure agent prompts contain required “non-negotiables” (system constraints)
Ensure skills declare data access boundaries
Ensure tools are constrained (paths, network, repo scope)
Optional read-only “Red Team Agent”:
tries to generate exploit prompts / tool misuse scenarios
outputs structured findings (no code execution)
Output: outputs/station_out/promptsec_report.json
Station A4 — Red Team Agent
Station A5 — Sandbox Simulation (deterministic)
Run the agent/skill in a locked sandbox against test fixtures:
malicious user inputs
prompt injection payloads
“exfiltrate secrets” attempts
“modify CI pipeline” attempts
Output: outputs/station_out/sim_report.json
Station A6 — Policy Gate
Block PR if any “critical” finding or missing mandatory fields
Apply risk label / require human approval for “high-risk agent”
Output: outputs/station_out/gate_decision.json
Station A7 — GitLab Update
Comment on PR with a short report + links to artifacts
Add labels like security:blocker, agent:risk-high, needs:manual-review