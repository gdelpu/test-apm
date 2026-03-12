#!/usr/bin/env python3
"""Extracts the first valid top-level JSON object from model output (stdin).

Supports two input formats:
1. Plain text (copilot --output-format text): searches for JSON objects in
   the raw text stream.
2. JSONL (copilot -s --output-format json): each line is a JSON event.
   The script concatenates all assistant.message content fields and then
   searches for JSON objects within the combined model response.

Improvements over the previous inline sed+jq approach:
- Handles multi-object model responses: emits a warning instead of silently
  returning only the first object, so callers can investigate unexpected output.
- Proper bracket-depth parser: correctly handles nested objects and arrays
  inside string values.
- Explicit exit code 1 on failure so all callers are fail-closed by default.

Usage:
    python3 extract_json.py < model_output.txt > parsed.json
"""

import json
import re
import sys


# JSONL envelope types that are never the model's answer.
_ENVELOPE_TYPES = frozenset({
    "session.tools_updated", "user.message", "assistant.turn_start",
    "assistant.turn_end", "assistant.reasoning_delta", "assistant.reasoning",
    "tool.execution_start", "tool.execution_complete",
    "tool.execution_partial_result", "assistant.message_delta",
    "subagent.started", "subagent.completed",
    "session.background_tasks_changed", "result",
})


def extract_jsonl_content(raw: str) -> str:
    """If input is JSONL from copilot --output-format json, concatenate all
    assistant.message content fields. Falls back to raw text if not JSONL."""
    lines = raw.splitlines()
    if not lines:
        return raw

    # Quick heuristic: if the first non-empty line is a JSON object with a
    # "type" key, treat the whole input as JSONL.
    first = ""
    for line in lines:
        line = line.strip()
        if line:
            first = line
            break

    try:
        probe = json.loads(first)
        if not isinstance(probe, dict) or "type" not in probe:
            return raw
    except (json.JSONDecodeError, ValueError):
        return raw

    # It's JSONL — collect assistant message content in order.
    parts: list[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        evt_type = evt.get("type", "")
        if evt_type == "assistant.message":
            content = evt.get("data", {}).get("content", "")
            if content:
                parts.append(content)
        elif evt_type == "session.task_complete":
            summary = evt.get("data", {}).get("summary", "")
            if summary:
                parts.append(summary)

    return "\n".join(parts) if parts else raw


def find_json_objects(text: str) -> list:
    objects = []
    depth = 0
    start = None
    in_string = False
    escape_next = False

    for i, ch in enumerate(text):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                candidate = text[start : i + 1]
                try:
                    obj = json.loads(candidate)
                    objects.append(obj)
                except json.JSONDecodeError:
                    pass
                start = None

    return objects


def main() -> None:
    raw = sys.stdin.read()
    content = extract_jsonl_content(raw)

    # Strip markdown code fences that models sometimes wrap JSON in.
    content = re.sub(r"```(?:json)?\s*\n?", "", content)

    objects = find_json_objects(content)

    if not objects:
        sys.stderr.write("ERROR: No valid JSON object found in model output\n")
        sys.exit(1)

    if len(objects) > 1:
        sys.stderr.write(
            f"WARNING: {len(objects)} JSON objects found; using the first. "
            "Model returned unexpected multi-block output — investigate raw response.\n"
        )

    print(json.dumps(objects[0]))


if __name__ == "__main__":
    main()
