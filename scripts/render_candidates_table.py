#!/usr/bin/env python3
"""Print _status/candidates.json entries as a Markdown table row per line.
Used by .github/workflows/quarterly-rediscovery.yml to build the PR body.
"""
import json
import pathlib

doc = json.loads((pathlib.Path(__file__).resolve().parent.parent / "_status" / "candidates.json").read_text(encoding="utf-8"))
for e in doc["entries"]:
    print(f"| {e['category']} | [{e['name']}]({e['url']}) | {e['stars']} | {e['pushed_at'][:10]} | {e['popularity']}+{e['activity']} |")
