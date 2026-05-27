# `_status/` — automation state

Auto-generated and auto-consumed by GitHub Actions in `.github/workflows/`.
Do **not** hand-edit unless you know what you're doing.

| File | Owner | Purpose |
|------|-------|---------|
| `borderline.json` | `monthly-borderline-rescore.yml` / `quarterly-full-rescore.yml` | Catalog entries within ±2 of a tier boundary (18–21 or 11–14). The monthly job only rescore these. |
| `history.jsonl` | rescore + rediscovery jobs | Append-only log of every score change, archive/unarchive, and new candidate. One JSON object per line. |
| `candidates.json` | `monthly-rediscovery.yml` | Newly discovered repositories not yet in the catalog. Refreshed every month; entries are overwritten on each run. An Issue with a checkbox triage list is opened alongside. |

(`sources/sync-log.md` lives under `sources/`, not here — it tracks weekly fork-sync results.)

## History event schema

```json
{
  "ts": "2026-07-01T03:00:00Z",
  "event": "rescore" | "archive" | "unarchive" | "discover",
  "name": "claude-code-hooks-mastery",
  "category": "skills",
  "before": { "total": 19, "tier": 2, "status": "active" },
  "after":  { "total": 12, "tier": 3, "status": "archived" },
  "reason": "freshness rule: no commit in 6 months"
}
```
