#!/usr/bin/env python3
"""
context-forge automation toolkit.

Subcommands:
  score     <owner/repo>            Print Pop+Act score JSON for a single repo.
  rescore   [--borderline-only]     Recompute Pop+Act scores for catalog entries,
                                    update frontmatter, append history, refresh
                                    _status/borderline.json. Sets status=archived
                                    when freshness rule trips.
  discover                          Search GitHub for new candidates, filter
                                    against sources/index.json, append to
                                    _status/candidates.json.
  render-index                      Regenerate catalog/<cat>/README.md tables
                                    from frontmatter.

Conventions follow docs/scoring.md (5-factor rubric, freshness rule, tiers).
Only popularity and activity are computed automatically. Other factors
(reviews, quality, trust) keep whatever the maintainer last set in frontmatter
(default 3 if missing).

Requires: python 3.10+, gh CLI on PATH, GITHUB_TOKEN env (gh handles auth).
No third-party deps — frontmatter is parsed by hand.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
STATUS = ROOT / "_status"
SOURCES_INDEX = ROOT / "sources" / "index.json"

# Tier 1 ≥20, Tier 2 13–19, Tier 3 ≤12 (docs/scoring.md)
TIER1_MIN = 20
TIER2_MIN = 13
# Borderline = ±2 of each tier boundary
BORDERLINE_TIER1 = (18, 21)
BORDERLINE_TIER3 = (11, 14)
# AI/agent freshness: activity = 1 (no commit in 6 months) forces Tier 3
FRESHNESS_MONTHS = 6
# v1 categories — entire catalog is AI-tool ecosystem, freshness rule applies to all
AI_CATEGORIES = {
    "claude-md", "agents-md", "skills", "conventions",
    "multi-agent", "prompts", "spec-driven", "mcp", "boilerplate",
}

# ─── frontmatter helpers ─────────────────────────────────────────────────────

FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def read_frontmatter(path: pathlib.Path) -> tuple[dict[str, Any], str, str]:
    """Return (frontmatter_dict, frontmatter_text, body)."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return {}, "", text
    fm_text = m.group(1)
    body = text[m.end():]
    return parse_yaml_lite(fm_text), fm_text, body


def parse_yaml_lite(text: str) -> dict[str, Any]:
    """Tiny YAML subset: scalar key: value, list `[a, b, c]`, nested object via 2-space indent."""
    out: dict[str, Any] = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.startswith("  "):  # nested handled by caller path
            i += 1
            continue
        if ":" not in raw:
            i += 1
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            # nested object — collect indented lines
            sub: dict[str, Any] = {}
            j = i + 1
            while j < len(lines) and (lines[j].startswith("  ") or not lines[j].strip()):
                if lines[j].strip() and ":" in lines[j]:
                    sk, _, sv = lines[j].strip().partition(":")
                    sub[sk.strip()] = _coerce(sv.strip())
                j += 1
            out[key] = sub
            i = j
            continue
        out[key] = _coerce(value)
        i += 1
    return out


def _coerce(v: str) -> Any:
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [s.strip().strip('"').strip("'") for s in inner.split(",")]
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def update_frontmatter(path: pathlib.Path, fm_text: str, body: str,
                       *, score: dict[str, Any], status: str) -> None:
    """Replace ONLY the `score:` block and `status:` line in the original
    frontmatter text. All other fields (URLs, multi-line scalars, key order,
    comments) are preserved byte-for-byte. Adds the keys at the end if missing.
    """
    new_fm = _replace_or_append(fm_text, "status", _format_status_line(status))
    new_fm = _replace_or_append(new_fm, "score", _format_score_block(score), block=True)
    path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")


def _format_status_line(status: str) -> str:
    return f"status: {status}"


def _format_score_block(score: dict[str, Any]) -> str:
    lines = ["score:"]
    order = ("popularity", "activity", "reviews", "quality", "trust", "total", "tier", "last_scored")
    for k in order:
        if k in score:
            lines.append(f"  {k}: {score[k]}")
    return "\n".join(lines)


def _replace_or_append(fm_text: str, key: str, replacement: str, *, block: bool = False) -> str:
    """Replace the existing key (single line, or block if `block=True` — block
    spans through indented continuation lines until a non-indented non-blank
    line). If key missing, append to the end."""
    lines = fm_text.split("\n")
    # find key at column 0
    start = next((i for i, ln in enumerate(lines) if re.match(rf"^{re.escape(key)}\s*:", ln)), None)
    if start is None:
        # append (strip trailing blanks first)
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines + [replacement])
    if not block:
        end = start + 1
    else:
        end = start + 1
        while end < len(lines) and (lines[end].startswith(" ") or lines[end].startswith("\t") or not lines[end].strip()):
            # stop on blank only if next non-blank is non-indented
            if not lines[end].strip():
                # peek
                k = end + 1
                while k < len(lines) and not lines[k].strip():
                    k += 1
                if k >= len(lines) or not (lines[k].startswith(" ") or lines[k].startswith("\t")):
                    break
            end += 1
    return "\n".join(lines[:start] + [replacement] + lines[end:])


# ─── GitHub API via gh CLI ───────────────────────────────────────────────────

def gh_api(path: str) -> dict[str, Any]:
    """Call gh api <path>; return parsed JSON."""
    proc = subprocess.run(
        ["gh", "api", path, "-H", "Accept: application/vnd.github+json"],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {path} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def gh_search(query: str, per_page: int = 30) -> list[dict[str, Any]]:
    path = f"search/repositories?q={query}&per_page={per_page}&sort=stars&order=desc"
    data = gh_api(path)
    return data.get("items", [])


def repo_from_url(url: str) -> str | None:
    m = re.search(r"github\.com/([^/]+/[^/?#]+)", url)
    if not m:
        return None
    return m.group(1).removesuffix(".git")


# ─── scoring ─────────────────────────────────────────────────────────────────

def score_popularity(stars: int) -> int:
    if stars < 100: return 1
    if stars < 500: return 2
    if stars < 2000: return 3
    if stars < 10000: return 4
    return 5


def score_activity(last_push_iso: str) -> int:
    last = dt.datetime.fromisoformat(last_push_iso.replace("Z", "+00:00"))
    age = dt.datetime.now(dt.timezone.utc) - last
    days = age.days
    if days <= 7: return 5
    if days <= 30: return 4
    if days <= 90: return 3
    if days <= 30 * FRESHNESS_MONTHS: return 2
    return 1


def auto_score(repo_full_name: str) -> dict[str, Any]:
    info = gh_api(f"repos/{repo_full_name}")
    pop = score_popularity(info.get("stargazers_count", 0))
    act = score_activity(info["pushed_at"])
    return {
        "stars": info.get("stargazers_count", 0),
        "pushed_at": info["pushed_at"],
        "archived": info.get("archived", False),
        "popularity": pop,
        "activity": act,
    }


def compute_total_and_tier(score: dict[str, int], category: str, archived_upstream: bool) -> tuple[int, int]:
    total = sum(score[k] for k in ("popularity", "activity", "reviews", "quality", "trust"))
    if category in AI_CATEGORIES and (score["activity"] == 1 or archived_upstream):
        return total, 3
    if total >= TIER1_MIN: return total, 1
    if total >= TIER2_MIN: return total, 2
    return total, 3


# ─── history log ─────────────────────────────────────────────────────────────

def log_history(event: dict[str, Any]) -> None:
    STATUS.mkdir(exist_ok=True)
    event = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), **event}
    with (STATUS / "history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ─── subcommand: score ──────────────────────────────────────────────────────

def cmd_score(args: argparse.Namespace) -> int:
    print(json.dumps(auto_score(args.repo), indent=2))
    return 0


# ─── subcommand: rescore ────────────────────────────────────────────────────

def iter_catalog_entries():
    for cat_dir in sorted(CATALOG.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("_"):
            continue
        for f in sorted(cat_dir.glob("*.md")):
            if f.name == "README.md" or f.name.startswith("_"):
                continue
            yield f


def cmd_rescore(args: argparse.Namespace) -> int:
    today = dt.date.today().isoformat()
    borderline_path = STATUS / "borderline.json"
    borderline_doc = json.loads(borderline_path.read_text(encoding="utf-8"))
    borderline_names = {e["name"] for e in borderline_doc.get("entries", [])}

    new_borderline: list[dict[str, Any]] = []
    rescored = 0

    rescored_borderline: dict[str, dict[str, Any]] = {}

    for path in iter_catalog_entries():
        fm, fm_text, body = read_frontmatter(path)
        if not fm:
            continue
        name = fm.get("name", path.stem)
        category = fm.get("category", path.parent.name)
        if args.borderline_only and name not in borderline_names:
            continue
        upstream = fm.get("upstream") or fm.get("source")
        repo = repo_from_url(upstream) if upstream else None
        if not repo:
            print(f"skip {name}: no upstream URL")
            continue
        try:
            auto = auto_score(repo)
        except Exception as e:
            print(f"skip {name}: {e}")
            continue

        prev = fm.get("score") or {}
        new_score = {
            "popularity": auto["popularity"],
            "activity": auto["activity"],
            "reviews": int(prev.get("reviews", 3)),
            "quality": int(prev.get("quality", 3)),
            "trust": int(prev.get("trust", 3)),
        }
        total, tier = compute_total_and_tier(new_score, category, auto["archived"])
        new_score["total"] = total
        new_score["tier"] = tier
        new_score["last_scored"] = today

        prev_status = fm.get("status", "active")
        new_status = "archived" if tier == 3 else "active"

        prev_total = int(prev.get("total", 0))
        prev_tier = int(prev.get("tier", 0))
        if prev_total != total or prev_tier != tier or prev_status != new_status:
            log_history({
                "event": "rescore",
                "name": name,
                "category": category,
                "before": {"total": prev_total, "tier": prev_tier, "status": prev_status},
                "after":  {"total": total, "tier": tier, "status": new_status},
                "reason": "freshness rule" if (tier == 3 and new_score["activity"] == 1) else "rescore",
            })

        update_frontmatter(path, fm_text, body, score=new_score, status=new_status)
        rescored += 1

        in_borderline = (BORDERLINE_TIER1[0] <= total <= BORDERLINE_TIER1[1] or
                         BORDERLINE_TIER3[0] <= total <= BORDERLINE_TIER3[1])
        if in_borderline:
            new_borderline.append({"name": name, "category": category, "total": total, "tier": tier})
            rescored_borderline[name] = {"name": name, "category": category, "total": total, "tier": tier}
        else:
            # explicit removal mark for borderline-only mode
            rescored_borderline[name] = None  # type: ignore[assignment]

    if args.borderline_only:
        # patch existing borderline list: drop entries that left the bands,
        # update scores for entries that stayed
        kept = []
        for entry in borderline_doc.get("entries", []):
            patched = rescored_borderline.get(entry["name"], entry)
            if patched is not None:
                kept.append(patched)
        borderline_doc["updated_at"] = today
        borderline_doc["entries"] = sorted(kept, key=lambda e: e["total"])
    else:
        borderline_doc["updated_at"] = today
        borderline_doc["entries"] = sorted(new_borderline, key=lambda e: e["total"])
    borderline_path.write_text(json.dumps(borderline_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"rescored {rescored} entries; borderline={len(borderline_doc['entries'])}")
    return 0


# ─── subcommand: discover ───────────────────────────────────────────────────

# v1 scope keyword presets — keep narrow per user decision
DISCOVERY_QUERIES: dict[str, list[str]] = {
    "skills":      ["claude-code-skills", "claude-skills", "agent-skills"],
    "claude-md":   ["claude-md", "claude.md", "claude-code-template"],
    "agents-md":   ["agents-md", "agents.md"],
    "multi-agent": ["claude-subagents", "subagents-collection", "multi-agent-orchestration"],
    "spec-driven": ["spec-driven-development", "spec-kit", "openspec"],
    "mcp":         ["awesome-mcp", "mcp-servers"],
    "prompts":     ["awesome-prompts", "prompt-engineering-guide"],
    "conventions": ["claude-code-best-practice", "agent-conventions"],
    "boilerplate": ["claude-code-boilerplate", "ai-coding-template"],
}

MIN_STARS = 500
MIN_POP_ACT = 7  # 10점 만점 중


def cmd_discover(args: argparse.Namespace) -> int:
    today = dt.date.today().isoformat()
    sources = json.loads(SOURCES_INDEX.read_text(encoding="utf-8"))
    known_upstreams = {s["upstream"].rstrip("/") for s in sources.get("sources", [])}

    found: list[dict[str, Any]] = []
    first = True
    for category, keywords in DISCOVERY_QUERIES.items():
        for kw in keywords:
            # GitHub Search API is 10 req/min for authenticated calls — pace at 7s between calls
            if not first:
                time.sleep(7)
            first = False
            try:
                results = gh_search(f"{kw}+stars:>={MIN_STARS}+pushed:>={_six_months_ago()}", per_page=20)
            except Exception as e:
                print(f"search {kw}: {e}")
                continue
            for repo in results:
                url = repo["html_url"].rstrip("/")
                if url in known_upstreams:
                    continue
                if any(c["url"] == url for c in found):
                    continue
                pop = score_popularity(repo.get("stargazers_count", 0))
                act = score_activity(repo["pushed_at"])
                if pop + act < MIN_POP_ACT:
                    continue
                found.append({
                    "url": url,
                    "name": repo["full_name"],
                    "category": category,
                    "matched_keyword": kw,
                    "stars": repo.get("stargazers_count", 0),
                    "pushed_at": repo["pushed_at"],
                    "popularity": pop,
                    "activity": act,
                    "discovered_at": today,
                })

    candidates_path = STATUS / "candidates.json"
    doc = json.loads(candidates_path.read_text(encoding="utf-8"))
    doc["updated_at"] = today
    doc["entries"] = sorted(found, key=lambda e: -(e["popularity"] + e["activity"]))
    candidates_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for c in found:
        log_history({"event": "discover", "name": c["name"], "category": c["category"],
                     "after": {"popularity": c["popularity"], "activity": c["activity"]}})

    print(f"discovered {len(found)} new candidates")
    return 0


def _six_months_ago() -> str:
    return (dt.date.today() - dt.timedelta(days=30 * FRESHNESS_MONTHS)).isoformat()


# ─── subcommand: render-index ───────────────────────────────────────────────

def cmd_render_index(args: argparse.Namespace) -> int:
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for path in iter_catalog_entries():
        fm, _, _ = read_frontmatter(path)
        if not fm:
            continue
        cat = fm.get("category", path.parent.name)
        by_cat.setdefault(cat, []).append({
            "name": fm.get("name", path.stem),
            "file": path.name,
            "when_to_use": fm.get("when_to_use", ""),
            "status": fm.get("status", "active"),
            "score": fm.get("score", {}),
            "source": fm.get("source", ""),
        })

    written = 0
    for cat, entries in by_cat.items():
        readme = CATALOG / cat / "README.md"
        lines = [f"# `{cat}` catalog\n",
                 f"Auto-generated by `scripts/automation.py render-index`. Do not hand-edit.\n",
                 "| Status | Name | Tier | Total | When to use |",
                 "|--------|------|------|-------|-------------|"]
        for e in sorted(entries, key=lambda x: (x["status"] == "archived", x["name"])):
            score = e["score"] or {}
            tier = score.get("tier", "—")
            total = score.get("total", "—")
            display_name = f"~~{e['name']}~~" if e["status"] == "archived" else f"[{e['name']}]({e['file']})"
            when = (e["when_to_use"] or "").replace("|", "\\|").splitlines()[0][:120]
            lines.append(f"| {e['status']} | {display_name} | {tier} | {total} | {when} |")
        readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written += 1

    print(f"rendered {written} category READMEs")
    return 0


# ─── main ────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="Auto-score a single repo (Pop+Act)")
    p_score.add_argument("repo", help="owner/repo")
    p_score.set_defaults(func=cmd_score)

    p_rescore = sub.add_parser("rescore", help="Recompute Pop+Act for catalog entries")
    p_rescore.add_argument("--borderline-only", action="store_true",
                           help="Only rescore entries listed in _status/borderline.json")
    p_rescore.set_defaults(func=cmd_rescore)

    p_discover = sub.add_parser("discover", help="Search for new candidate repos")
    p_discover.set_defaults(func=cmd_discover)

    p_render = sub.add_parser("render-index", help="Regenerate catalog/<cat>/README.md tables")
    p_render.set_defaults(func=cmd_render_index)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
