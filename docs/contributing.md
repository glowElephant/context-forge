# Contributing to context-forge

Thanks for considering a contribution. context-forge is a community catalog — every entry is curated, and your additions help everyone shipping AI-augmented projects.

There are three kinds of contributions:

1. **Propose a new source repository** to fork into the catalog
2. **Add a catalog entry** distilling know-how from an already-forked source
3. **Improve the toolchain** (skill body, validator, docs)

## 1. Proposing a new source

A "source" is an upstream GitHub repository with `.md` know-how that we'd consider forking.

### Option A — GitHub Discussions (lower friction)

Open a discussion in the **"Source proposals"** category with this template:

```markdown
**Upstream URL:** https://github.com/<owner>/<name>

**Why it belongs in context-forge:**
(1–2 sentences)

**Category fit:**
- [ ] claude-md
- [ ] agents-md
- [ ] skills
- [ ] conventions
- [ ] multi-agent
- [ ] prompts
- [ ] spec-driven
- [ ] mcp
- [ ] boilerplate

**Score (rough — see docs/scoring.md):**
- Popularity: ⭐ <stars>
- Activity: last commit <date>
- Reviews/mentions: (links if any)
- Content depth: high / medium / low
- Maintainer reliability: organization / individual / unclear

**Estimated tier:** 1 / 2 / 3
```

A maintainer will evaluate, fork if appropriate, and add an entry to `sources/index.json` via PR.

### Option B — Direct PR (faster if you know the rubric)

Add an entry to `sources/index.json` matching the schema in `sources/index.schema.json`. Open a PR with the same template above as the description. The maintainer will fork the upstream and merge.

## 2. Adding a catalog entry

Catalog entries distill the actionable know-how from a forked source into a single Markdown file with frontmatter.

### Steps

1. Pick a forked source from `sources/index.json` that has no catalog entry yet
2. Create `catalog/<category>/<kebab-name>.md` using this template:

```markdown
---
name: <kebab-case-name>
category: <category>
domain: [<domain1>, <domain2>]
tags: [<tag1>, <tag2>]
source: https://github.com/glowElephant/<fork-name>
upstream: https://github.com/<original-owner>/<original-name>
when_to_use: <one or two sentences describing when to include this in a new project>
priority: <1-5>
---

# <Title>

(2–4 paragraphs summarizing the core idea, drawn from the upstream README/docs.)

## Quick start

(Concrete bullet list — what to do in a new project.)

## Notes

(Caveats, when not to use, version pinning if relevant.)

## Source

- Upstream: <upstream URL>
- Fork: <fork URL>
```

3. Run the validator:
   ```bash
   ./scripts/validate-catalog.sh
   ```
4. Submit a PR with title `catalog: add <name>` and a 2–3 sentence description in the body

### Style guidelines

- Keep entries **under 100 lines**. The catalog is a curated digest, not a copy-paste of upstream READMEs.
- `when_to_use` is the most important field — it drives matching. Be specific about WHEN to include this entry, not WHAT it is.
- Lead with the core insight, not the marketing copy. Imagine you have 30 seconds to convince another dev this matters.
- Pin `priority` 1–5 honestly. 5 = "almost every project of this domain should consider this". 3 = "useful for the right project". 1 = niche.

### Worked example PR description

> **Title:** catalog: add tdd-guard-hooks
>
> Adds a `skills/tdd-guard-hooks` entry distilling the hook-based TDD enforcement pattern from `nizos/tdd-guard`. The entry covers the PreToolUse hook setup, the test-first fail mode, and how to opt out for hotfixes. Priority 3 because it's high-value for greenfield TDD adoption but unsuitable for legacy migrations.
>
> Validator: ✅ passes

## 3. Improving the toolchain

PRs against the skill (`.claude/skills/context-forge/SKILL.md`), validator, schema, or docs are welcome. Open an issue first for non-trivial changes — the skill body especially is a load-bearing surface.

### Local development

```bash
git clone https://github.com/<your-fork>/context-forge
cd context-forge
./scripts/validate-catalog.sh   # should already pass on main
```

There is no build step — everything is plain Markdown / shell / JSON.

## Code of conduct

Be kind. Disagreements happen — keep them about the work, not the person.

## Questions?

Open a discussion. The maintainers prefer public Q&A so the answer benefits everyone.
