# r/ClaudeAI post draft — context-forge

Channel: https://www.reddit.com/r/ClaudeAI
Best timing: Tue–Thu 09:00–11:00 ET (= Korea Wed–Fri 22:00–24:00).
**Required flair: "Built with Claude"** (Rule #7).
Stay in thread for first 60 min.

---

## Subreddit rules compliance (Rule #7 audit)

| Requirement | OK? | Where |
|---|---|---|
| Built FOR Claude/Claude Code, BY YOU | ✅ | "I built /context-forge..." in body |
| Clear description + how Claude helped + what it does | ✅ | 5-phase flow + dogfood note |
| Free to try, said so | ✅ | "MIT, free" |
| Promotional language minimal | ⚠️ | Variants B/C are safer |
| No referral links | ✅ | github/npm only |

---

## Title (pick one)

**A. Score/scope-bait (highest engagement)**
> I built a slash command that bootstraps a fully harness-engineered repo from a 5-minute discussion — 82 catalog sources, weekly auto-sync, monthly auto-discover

**B. Question-first**
> Tired of re-doing CLAUDE.md / AGENTS.md / skills setup for every new project? I made `/context-forge` to do it from a conversation.

**C. Tool-first (drier, safer)**
> context-forge: open-source slash command — discussion → curated catalog → new GitHub repo with CLAUDE.md/AGENTS.md/skills/docs wired in

---

## Body

Hey r/ClaudeAI 👋

Every time I start a new project, the same ritual: write CLAUDE.md, decide which skills to install, pick a spec workflow, set up MCP servers, write AGENTS.md so Cursor/Codex can read along, add hook patterns... It used to take half a day before I'd written a line of project code.

So I built [**context-forge**](https://github.com/glowElephant/context-forge) — a Claude Code slash command that turns that ritual into a 5-minute conversation:

```
/context-forge
```

It runs a 6-phase guided flow:

1. **4 fixed questions** — project type / stack / solo-vs-team / multi-agent needed?
2. **Free discussion** (≤8 questions) — goal, milestones, constraints, domain knowledge, anti-patterns
3. **Catalog match** — finds applicable entries from 82 curated sources (Claude Code skills, CLAUDE.md patterns, MCP infra, spec-driven workflows, multi-agent orchestration, agent conventions...)
4. **Repo info** — name, public/private, local path
5. **Create + populate** — `gh repo create` → clone → copy chosen catalog entries to `docs/know-how/` → **synthesize** `CLAUDE.md` / `AGENTS.md` / `README.md` / `docs/spec.md` from your Phase 2 answers → commit → push
6. **Hand off** — `cd <new-repo> && claude` to start coding

### How it stays current (the part I'm most proud of)

A new project bootstrapped today shouldn't get last month's best practices. So context-forge runs three automations on the catalog itself:

- **Weekly fork sync** (Mon 04:00 UTC) — all 82 source forks fast-forward synced from their upstreams
- **Monthly auto-discovery** (1st 04:00 UTC) — GitHub Search across 9 category keyword groups → filter `★≥2000`, `popularity+activity ≥ 7/10`, top 5 per category → opens an Issue with checkbox triage list
- **Monthly/quarterly rescore** — 5-factor rubric (popularity + activity auto, reviews/quality/trust manual), entries idle 6 months auto-archived

Every fork carries a `context-forge-source` topic so the catalog is filterable from the GitHub UI.

### Honesty about the state

v1.1.2, MIT. Catalog frontmatter exists for all 82 entries (15 hand-crafted + 67 auto-seeded via `scripts/seed_frontmatter.py`). End-to-end **dogfood-validated** today (2 bugs found and fixed in this session: YAML quote leak in auto-seeded frontmatter, `git branch -M main` missing for Windows). Full fresh-session validation by a real first-time user is still on my todo — that's why I'm posting here.

### What I'd love feedback on

1. **Does the 9-category split (claude-md / agents-md / skills / conventions / multi-agent / prompts / spec-driven / mcp / boilerplate) match how you actually organize harness know-how?** What's missing?
2. **If you've manually set up harness scaffolding before** — what was the hardest part to remember? I want context-forge to capture exactly those "I forgot this last time" lessons.
3. **Anyone willing to run `/context-forge` on a real project and tell me what broke?** Repro setup:
   ```bash
   git clone https://github.com/glowElephant/context-forge ~/code/context-forge
   export CONTEXT_FORGE_PATH=~/code/context-forge  # or set in .claude/settings.json
   # then in any Claude Code session:
   /context-forge
   ```

### Links

- Repo: https://github.com/glowElephant/context-forge
- Setup: [README](https://github.com/glowElephant/context-forge#quick-start)
- Catalog sources (browse 82): https://github.com/glowElephant?tab=repositories&q=topic%3Acontext-forge-source

MIT, Claude Code skill (works in any Claude Code session — no install beyond clone + env var).

---

## Comment-ready answers

**"How is this different from spec-kit / OpenSpec / superpowers?"**
> Those are skills/frameworks themselves — context-forge includes them in its catalog. The difference is `context-forge` *bootstraps* a project that uses any combination of those, picked based on your specific project's needs. It's the layer above: which spec system + which skill framework + which MCP combo for THIS project.

**"What does the catalog actually contain?"**
> 82 forks of upstream harness know-how repos, each with a Markdown frontmatter file at `catalog/<category>/<name>.md` that has `when_to_use`, `priority`, scoring. The slash command reads those frontmatters and matches against your project's stated goals/stack.

**"Privacy — does it send my code anywhere?"**
> The slash command reads only `~/.claude/` config metadata and the `catalog/` directory in your context-forge clone. It calls `gh repo create` for the new repo. No project source code is read or transmitted.

**"Why fork everything instead of just linking to upstreams?"**
> Snapshot stability — upstream history rewrites would otherwise break catalog references. Plus weekly auto-sync gives you control over WHEN updates land. Pure mirror, fast-forward only; if upstream diverges, the entry is reported in the sync log.

**"The catalog matching looks heuristic — does it actually pick well?"**
> Honestly it's a first pass. The 5-factor rubric prioritizes by `priority` × `domain` × `category-applicability`. Phase 3 *proposes*, you confirm or remove. I want to make the matching smarter as more users tell me where it over-/under-recommends.

**"What if my project type isn't in the 9 categories?"**
> v1 is intentionally narrow on AI-agent harness. v2 will broaden to domain conventions (game-engine, mobile, web, backend, ML, security). See [v2 candidates spec](https://github.com/glowElephant/context-forge/blob/main/docs/specs/2026-04-28-fork-candidates.md).

**"Will it work with Cursor / Codex / Aider?"**
> Slash command is Claude Code-only, but the output it creates (`CLAUDE.md` + `AGENTS.md` + `.cursorrules` patterns from the catalog) IS multi-tool — your project becomes runnable by Cursor/Codex/Copilot too. v1.5 plans a native Cursor command wrapper.

---

## Stay-in-thread rules (first 60 min)

- **If someone tries it and breaks**: thank them, ask for stack + error + which Phase. Don't ship a fix in the thread; file an Issue.
- **If someone says "this is just a wrapper around gh repo create"**: agree it's mechanical glue, but argue the *catalog curation* is the real value — the 82 entries are filtered from 277 candidates, weekly-fresh, scored.
- **If asked about catalog adding their pattern**: point to [GitHub Discussions — Source proposals](https://github.com/glowElephant/context-forge/discussions) (Rule #7 redirect).
- **No vote manipulation** — don't ask friends to upvote (instant ban per Rule #10).
- **Don't link harness-bench / Molten / other originals** in the same thread (looks promotional). Mention only if directly asked.

---

## Post-publish checklist

- [ ] Flair set to "Built with Claude"
- [ ] First comment by author with `/context-forge` setup snippet + sample run output
- [ ] Watch first 30 min — top comment determines thread direction
- [ ] If thread takes off: cross-post to r/AI_Agents (different framing — emphasize multi-agent harness)
- [ ] If thread flops (≤10 upvotes after 6h): wait 48h, post Variant B with different angle
