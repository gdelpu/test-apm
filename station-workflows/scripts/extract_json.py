#!/usr/bin/env python3
"""Extracts the first valid top-level JSON object from model output (stdin).

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
import sys


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
    content = sys.stdin.read()
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
