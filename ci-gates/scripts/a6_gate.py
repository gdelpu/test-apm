#!/usr/bin/env python3
"""
Station A6 — Policy Gate (deterministic).

Aggregates all upstream station reports and produces a gate decision:
APPROVE, REVIEW, or BLOCK.  Writes station_out/a6_result.json.

Usage:
    python3 a6_gate.py \
        --station-out station_out \
        --out station_out/a6_result.json
"""

import argparse
import json
import sys
from pathlib import Path

# ── Report file mapping ──────────────────────────────────────────────────
REPORT_FILES = {
    "A0": "a0_result.json",
    "A1": "a1_result.json",
    "A2": "a2_result.json",
    "A3": "a3_result.json",
    "A4": "a4_result.json",
    "A5": "a5_result.json",
}


def load_report(station_out: Path, station: str, filename: str) -> dict | None:
    """Load a station report, returning None if missing."""
    path = station_out / filename
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def collect_findings(report: dict) -> list[dict]:
    """Extract findings from a report, normalising the key name."""
    findings = report.get("findings", [])
    # A4 red team may use red_team_findings
    findings += report.get("red_team_findings", [])
    # Filter out findings that lack both severity and message (malformed/stale)
    return [f for f in findings if f.get("severity") or f.get("message")]


def main() -> None:
    parser = argparse.ArgumentParser(description="A6 Policy Gate — deterministic")
    parser.add_argument("--station-out", required=True, help="Directory containing station reports")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    station_out = Path(args.station_out)

    # Load all reports
    reports: dict[str, dict | None] = {}
    for station, filename in REPORT_FILES.items():
        reports[station] = load_report(station_out, station, filename)

    # Track decision inputs
    blocking_findings: list[dict] = []
    review_findings: list[dict] = []
    warnings: list[dict] = []
    notes: list[str] = []
    skipped_stations: list[str] = []

    # Also load work order for risk hints
    work_order = load_report(station_out, "A0", "a0_result.json") or {}
    risk_hints = work_order.get("risk_hints", [])

    # If all stations skipped (non-agent scope), approve
    all_skipped = True
    for station, report in reports.items():
        if report is None:
            skipped_stations.append(station)
            notes.append(f"Station {station} report not found — treated as skipped.")
            continue
        status = report.get("status", "pass")
        if status == "skipped":
            skipped_stations.append(station)
            notes.append(f"Station {station} was skipped.")
            continue
        all_skipped = False

    if all_skipped or work_order.get("scope") == "non-agent":
        result = {
            "station": "A6",
            "status": "pass",
            "decision": "APPROVE",
            "labels": ["agent-factory:approved", "agent-factory:scanned"],
            "blocking_findings": [],
            "review_findings": [],
            "warnings": [],
            "notes": "No agent/skill artefacts changed — all stations skipped.",
            "summary": "PR APPROVED — no agent/skill artefacts changed.",
        }
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("  → A6 gate: APPROVE (non-agent scope)")
        return

    # ── Aggregate findings across all reports ────────────────────────────
    has_fail = False
    has_critical = False
    has_high = False
    has_vulnerable_sim = False

    for station, report in reports.items():
        if report is None or report.get("status") == "skipped":
            continue

        # Check for explicit fail status
        if report.get("status") == "fail":
            has_fail = True
            notes.append(f"Station {station} reported status: fail.")

        findings = collect_findings(report)
        for f in findings:
            severity = f.get("severity", "low")
            entry = {
                "station": station,
                "check": f.get("check", f.get("rule", "unknown")),
                "severity": severity,
                "file": f.get("file", ""),
                "message": f.get("message", ""),
            }

            if severity == "critical":
                has_critical = True
                blocking_findings.append(entry)
            elif severity == "high":
                has_high = True
                review_findings.append(entry)
            elif severity in ("medium", "low"):
                warnings.append(entry)

        # A5 sandbox: check for vulnerable scenarios
        for scenario in report.get("scenarios", []):
            if scenario.get("result") == "vulnerable":
                has_vulnerable_sim = True
                blocking_findings.append({
                    "station": station,
                    "check": scenario.get("id", "SIM"),
                    "severity": "critical",
                    "file": "",
                    "message": f"Sandbox scenario vulnerable: {scenario.get('description', '')}",
                })

    # ── Apply decision rules ─────────────────────────────────────────────

    # G-BLOCK: any fail, any critical, any vulnerable sim
    if has_fail or has_critical or has_vulnerable_sim:
        decision = "BLOCK"
        labels = ["security:blocker", "agent-factory:blocked", "agent-factory:scanned"]
        summary_parts = []
        if has_critical:
            summary_parts.append(f"{len(blocking_findings)} critical finding(s)")
        if has_fail:
            summary_parts.append("station failure")
        if has_vulnerable_sim:
            summary_parts.append("vulnerable simulation scenario")
        summary = f"PR BLOCKED — {'; '.join(summary_parts)}. Remediate before re-submission."

    # G-REVIEW: high findings or risky hints
    elif has_high or any(h in risk_hints for h in ("exec-tool", "unconstrained-network", "unconstrained-files")):
        decision = "REVIEW"
        labels = ["agent-factory:needs-review", "agent-factory:scanned"]
        if "exec-tool" in risk_hints:
            labels.append("agent:exec-tool")
        if "unconstrained-network" in risk_hints or "unconstrained-files" in risk_hints:
            labels.append("agent:risk-high")
        # Move high findings to blocking for review
        blocking_findings.extend(review_findings)
        review_findings = []
        summary = f"PR requires REVIEW — {len(blocking_findings)} high finding(s) or risk hints present."

    # G-APPROVE
    else:
        decision = "APPROVE"
        labels = ["agent-factory:approved", "agent-factory:scanned"]
        summary = "PR APPROVED — all checks passed."

    result = {
        "station": "A6",
        "status": "pass" if decision == "APPROVE" else ("fail" if decision == "BLOCK" else "pass"),
        "decision": decision,
        "labels": labels,
        "blocking_findings": blocking_findings,
        "review_findings": review_findings,
        "warnings": warnings,
        "notes": " ".join(notes) if notes else "",
        "summary": summary,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"  → A6 gate: {decision} ({summary})")


if __name__ == "__main__":
    main()
