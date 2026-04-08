#!/usr/bin/env python3
"""
CLI entry point for the hook framework.

Called by the CLI workflow runner (station-runner.sh) as:
    python -m hooks --phase pre  --trace-id <uuid> --station <id> --input <file> [options]
    python -m hooks --phase post --trace-id <uuid> --station <id> --output <file> [options]
    python -m hooks --retroactive --path <dir-or-file>    # scan existing artifacts
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import generate_trace_id, run_pre_hooks, run_post_hooks
from .pii_scanner import scan_retroactive


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SSG AI SDLC hook framework",
        prog="python -m hooks",
    )
    parser.add_argument("--phase", choices=["pre", "post"], help="Hook phase")
    parser.add_argument("--trace-id", default="", help="Correlation ID (UUID)")
    parser.add_argument("--station", default="", help="Station ID")
    parser.add_argument("--workflow", default="", help="Workflow name")
    parser.add_argument("--agent", default="", help="Agent role")
    parser.add_argument("--skill", default="", help="Skill name")
    parser.add_argument("--provider", default="cli", help="Provider name")
    parser.add_argument("--input", dest="input_file", help="Input file to scan (pre)")
    parser.add_argument("--output", dest="output_file", help="Output file to scan (post)")
    parser.add_argument("--trace-file", help="Path to audit-trace.jsonl")
    parser.add_argument("--config", help="Path to hook-config.json")
    parser.add_argument("--pre-result", help="Path to pre-hook result JSON (post phase)")
    parser.add_argument("--retroactive", action="store_true", help="Scan existing files for PII")
    parser.add_argument("--path", help="File or directory to scan (retroactive mode)")
    parser.add_argument("--json", dest="json_output", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.retroactive:
        return _retroactive(args)

    if not args.phase:
        parser.error("--phase is required (unless --retroactive)")

    trace_id = args.trace_id or generate_trace_id()

    if args.phase == "pre":
        return _run_pre(args, trace_id)
    else:
        return _run_post(args, trace_id)


def _run_pre(args: argparse.Namespace, trace_id: str) -> int:
    content = ""
    if args.input_file:
        content = Path(args.input_file).read_text(encoding="utf-8")

    result = run_pre_hooks(
        content=content,
        trace_id=trace_id,
        workflow=args.workflow,
        station=args.station,
        agent=args.agent,
        skill=args.skill,
        provider=args.provider,
        config_path=args.config,
    )

    # Write result for post-phase consumption
    result_path = Path(args.trace_file or ".").parent / f".pre-result-{args.station}.json"
    if args.trace_file:
        result_path = Path(args.trace_file).parent / f".pre-result-{args.station}.json"

    serialisable = {
        k: v for k, v in result.items()
        if k != "spans"  # spans are internal
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(serialisable, default=str), encoding="utf-8")

    if args.json_output:
        print(json.dumps(serialisable, indent=2, default=str))
    else:
        if result["blocked"]:
            print(f"BLOCKED: {result['block_reason']}")
        elif result["pii_findings"].get("found"):
            types = result["pii_findings"]["types"]
            print(f"PII detected and redacted: {', '.join(types)}")
        else:
            print("pre-hooks: pass")

    # Write redacted content back if modified
    if args.input_file and result["content"] != content:
        Path(args.input_file).write_text(result["content"], encoding="utf-8")

    return 1 if result["blocked"] else 0


def _run_post(args: argparse.Namespace, trace_id: str) -> int:
    output = ""
    if args.output_file:
        output = Path(args.output_file).read_text(encoding="utf-8")

    # Load pre-result
    pre_result: dict = {}
    if args.pre_result:
        pre_result = json.loads(Path(args.pre_result).read_text(encoding="utf-8"))
    elif args.trace_file:
        candidate = Path(args.trace_file).parent / f".pre-result-{args.station}.json"
        if candidate.exists():
            pre_result = json.loads(candidate.read_text(encoding="utf-8"))

    result = run_post_hooks(
        output=output,
        pre_result=pre_result,
        trace_id=trace_id,
        workflow=args.workflow,
        station=args.station,
        agent=args.agent,
        skill=args.skill,
        provider=args.provider,
        trace_file=args.trace_file,
        config_path=args.config,
    )

    if args.json_output:
        print(json.dumps(result, indent=2, default=str))
    else:
        risk = result.get("risk", {})
        score = risk.get("score", 0)
        level = risk.get("level", "low")
        review = risk.get("human_review_required", False)
        print(f"post-hooks: risk={score} ({level})"
              + (f" — HUMAN REVIEW REQUIRED: {risk.get('human_review_reason', '')}"
                 if review else ""))

    # Write redacted output back if modified
    if args.output_file and result["output"] != output:
        Path(args.output_file).write_text(result["output"], encoding="utf-8")

    return 0


def _retroactive(args: argparse.Namespace) -> int:
    target = args.path
    if not target:
        print("ERROR: --path required for retroactive mode")
        return 1

    p = Path(target)
    files = list(p.rglob("*.md")) + list(p.rglob("*.json")) if p.is_dir() else [p]

    total_findings = 0
    for f in files:
        result = scan_retroactive(str(f))
        if result["found"]:
            total_findings += result["count"]
            types = ", ".join(result["types"])
            print(f"  {f}: {result['count']} findings ({types})")

    if total_findings == 0:
        print("No PII found.")
    else:
        print(f"\nTotal: {total_findings} PII findings across {len(files)} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
