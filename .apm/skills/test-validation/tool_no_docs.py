#!/usr/bin/env python3
# No documentation file for this script - will trigger test_gap_detector

def process_data(items):
    """Process items without any markdown docs explaining this script."""
    result = []
    for item in items:
        result.append(item.upper())
    return result

if __name__ == "__main__":
    data = ["a", "b", "c"]
    print(process_data(data))
