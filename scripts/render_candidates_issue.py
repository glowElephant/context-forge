#!/usr/bin/env python3
"""Print _status/candidates.json entries as a Markdown checkbox list grouped by category.
Used by .github/workflows/monthly-rediscovery.yml to build the triage Issue body.
"""
import json
import pathlib
from collections import defaultdict

doc = json.loads(
    (pathlib.Path(__file__).resolve().parent.parent / "_status" / "candidates.json")
    .read_text(encoding="utf-8")
)

by_cat: dict[str, list] = defaultdict(list)
for x in doc["entries"]:
    by_cat[x["category"]].append(x)

for cat in sorted(by_cat):
    items = by_cat[cat]
    print(f"### {cat} ({len(items)})")
    print()
    for x in items:
        print(
            f"- [ ] **{x['name']}** — [GitHub]({x['url']}) · ★{x['stars']} · "
            f"push {x['pushed_at'][:10]} · Pop+Act={x['popularity']+x['activity']}"
        )
    print()
