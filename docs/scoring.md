# Scoring rubric for source repositories

This document defines how we evaluate candidate repositories before forking them into the context-forge catalog. It applies to both initial seeding and ongoing community proposals.

## Five-factor rubric

Each candidate is scored 1–5 on five factors. Total range: 5–25.

| Factor | What we look at | 1 (poor) | 5 (excellent) |
|--------|-----------------|----------|----------------|
| **Popularity** | GitHub stars, forks | <100 stars | >10,000 stars |
| **Activity** | Last commit, issue/PR cadence | >1 year stale | Commit in last week |
| **Real-world reviews** | Blog/HN/Reddit mentions, awesome-list inclusion | None / unclear | Cited as "the standard" repeatedly |
| **Content quality** | Depth of `.md` content, signal vs noise | Single-line stub or dead links | Comprehensive, well-structured, examples |
| **Maintainer reliability** | Solo / org, other reputable repos | Unknown solo, only repo | Known org or individual with track record |

### Scoring guidance

- **Popularity** is a lagging indicator — be willing to score a high-quality young repo a 3 even at 200 stars
- **Activity** does NOT mean "recent commit"; it means signs of life. A perfect spec doesn't need monthly commits
- **Reviews** count blog posts and conference talks, not just star counts
- **Content quality** rewards distillation. A 200-line `.md` that captures the core idea > a 2000-line that buries it
- **Maintainer reliability** is about the *next 12 months* — will this repo still be there?

## Time-sensitivity policy

The scoring rubric alone is not enough. Candidates fall into three categories with different freshness requirements:

| Category | Examples | Freshness rule |
|----------|----------|----------------|
| **AI/agent/tool ecosystem** | Claude Code, Cursor rules, Copilot agents, MCP servers | Must have commits in **last 6 months**; AI tooling moves too fast otherwise |
| **Language style/standard guides** | Effective Go, Airbnb JS, OWASP cheat sheets | Activity-agnostic; mark `archived` if true |
| **Classic patterns / security / architecture** | GoF design patterns, scalability primers | Time-agnostic; ageless content keeps value |

Anything in the first category that's archived OR has no commit in 6 months → automatic Tier 3 (excluded from auto-fork) regardless of other scores.

## Tier thresholds

After scoring + freshness check:

- **Tier 1 (auto-fork)** — total ≥ 20 OR (popularity ≥ 4 AND clearly relevant)
- **Tier 2 (curated review)** — total 13–19; included only after maintainer review and user confirmation
- **Tier 3 (excluded)** — total ≤ 12, or fails freshness rule

A Tier 1 candidate that loses points on freshness rolls down to Tier 2 or 3 even if other scores stay high.

## Domain taxonomy

Every catalog entry must declare at least one domain. Multiple are OK.

- `general` — applies to most projects regardless of stack
- `web` — frontend, backend, fullstack web apps
- `game-engine` — Unity, Unreal, Godot, custom engines
- `mobile` — iOS, Android, React Native, Flutter, KMP
- `ai-agent` — projects whose primary purpose is AI agent infra
- `backend` — server-side languages and infrastructure (Go, Rust, Python, Node, Java, K8s, DBs)
- `design` — UI/UX, design systems, design documents
- `documentation` — docs writing, README/CHANGELOG patterns
- `ml` — ML/MLOps, data engineering, LLM application patterns

When in doubt, prefer `general` plus one specific domain. Adding 5+ domains usually means the entry is too broad — split it.

## When the rubric disagrees with intuition

Sometimes a low-star repo is clearly excellent (a thoughtful 400-star coding convention guide is often better than a 30k-star list of links). When this happens:

1. Score honestly using the rubric
2. If the score puts it below your intuition, write your reasoning in the PR/discussion
3. The maintainer makes the final call — the rubric is a default, not a verdict

## Example scores

| Repo | Pop | Act | Rev | Qual | Trust | Total | Tier |
|------|-----|-----|-----|------|-------|-------|------|
| anthropics/skills | 5 | 5 | 5 | 5 | 5 | 25 | 1 |
| garrytan/gstack | 5 | 5 | 5 | 5 | 5 | 25 | 1 |
| Allar/ue5-style-guide | 4 | 3 | 5 | 5 | 4 | 21 | 1 |
| futurice/unity-good-practices | 2 | 1 | 4 | 4 | 5 | 16 | 2 (stale, but classic content) |
| github/swift-style-guide | 4 | 1 | 5 | 5 | 5 | 20 | 2 (archived → demoted) |
| obscure-2018-repo | 1 | 1 | 1 | 2 | 1 | 6 | 3 |

## Quarterly rediscovery

Every quarter, a discovery job (currently manual, target v1.5: scheduled) sweeps for new candidates using the keyword list in `docs/specs/2026-04-28-fork-candidates.md`. New finds are scored, opened as discussions for community input, and promoted via PR.
