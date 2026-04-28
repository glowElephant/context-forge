---
name: context-forge
description: |
  Use when starting a brand-new project that needs AI-agent context (CLAUDE.md, AGENTS.md, skills, rules, MCP, spec workflow) set up from day one. Discusses goals → matches catalog know-how → creates a new GitHub repo with everything wired in. Keywords: harness engineering, bootstrap project, context engineering, scaffold repo, start project, agent-ready repo.
---

# context-forge

Auto-harness-engineering for AI coding agents. Turns a 5-minute project discussion into a fully context-engineered GitHub repository.

**Announce at start:** "Using context-forge to bootstrap a harness-engineered repo for your project."

## Hard prerequisites

Before doing anything else, verify ALL of these. If any fail, ask the user to fix and stop.

1. `gh` CLI is authenticated:
   ```bash
   gh auth status
   ```
   Expected: a logged-in account.

2. context-forge is checked out locally with the catalog present. The user should set `CONTEXT_FORGE_PATH` to their clone (default: `C:/Git/context-forge` or `~/code/context-forge`):
   ```bash
   test -d "$CONTEXT_FORGE_PATH/catalog" && test -f "$CONTEXT_FORGE_PATH/sources/index.json"
   ```
   If `CONTEXT_FORGE_PATH` is not set, ask the user where their context-forge clone is and persist it for the session.

3. The catalog passes validation:
   ```bash
   "$CONTEXT_FORGE_PATH/scripts/validate-catalog.sh"
   ```

If any step fails: stop and report the exact command that failed. Do NOT proceed.

---

## Phase 1: Fixed questions (always ask, in order)

Ask these one at a time. Wait for each answer before asking the next.

1. **Project type?** Multiple choice (single answer):
   - web (frontend / backend / fullstack)
   - game-engine (Unity, Unreal, Godot)
   - mobile (iOS, Android, cross-platform)
   - cli
   - library
   - mcp-server
   - other (free-text)

2. **Primary language / framework?** Free text (e.g., "Next.js + TypeScript", "Unity 6 / C#").

3. **Solo or team?** Multiple choice:
   - solo
   - small team (2–5)
   - larger team (6+)

4. **Multi-agent setup needed?** (Claude Code subagents, multi-IDE coordination, etc.) yes / no.

After all 4 are answered, **echo the answers back** in a single short summary so the user can correct any.

---

## Phase 2: Free discussion

After fixed questions, hold a focused conversation — **one question per turn**. Goal: understand goals, constraints, success criteria, and any domain knowledge that should land in `docs/spec.md`.

### What to extract (do NOT ask all at once — pull out as relevant)

- **Goal** — what does "done" look like in 1 sentence?
- **Top 3 milestones** — name each in 5–10 words.
- **Hard constraints** — deadlines, regulatory, perf budgets, target devices.
- **Domain knowledge** — vocabulary, prior incidents, who the users are.
- **What to avoid** — past failed approaches, anti-patterns the team rejects.

### Stop condition

Stop asking when you can write all five bullets above. If you've asked more than 8 questions and still can't, summarize what you have and ask the user "anything else essential before we move on?"

### Output of Phase 2

Internally produce:

```yaml
goal: ...
milestones: [..., ..., ...]
constraints: ...
domain: ...
avoid: ...
```

Do NOT show this YAML to the user yet. It feeds Phase 3.

---

## Phase 3: Catalog match

Read every `catalog/*/*.md` file's frontmatter from `$CONTEXT_FORGE_PATH/catalog/`. For each entry, decide whether it applies based on:

1. **Domain match** — at least one of `entry.domain` overlaps with the user's project type, OR `domain: [general]` is present.
2. **`when_to_use` semantic fit** — does the entry's `when_to_use` text describe this user's project? Use judgment.
3. **Multi-agent gating** — entries with `category: multi-agent` only apply if Phase 1 Q4 was "yes".
4. **Stack-specific gating** — if entry has `applies_to_files` (e.g., `[".cursorrules"]`) and the user's stack doesn't use those files, skip it.

Group results by category. Within each category, pick at most 3 (sort by `priority` field, fall back to alphabetical).

### Present the proposal

Show the user a single message structured like this:

```
Based on our discussion, I'll include these from the catalog:

CLAUDE.md (claude-md):
  - karpathy-single-claude-md — Single careful CLAUDE.md
  - gstack-claude-toolkit — Garry Tan 23-tool stack

Skills:
  - superpowers-skills-pattern — Skills framework
  - cursor-rules-pattern (you mentioned Cursor)

Spec-driven:
  - github-spec-kit

MCP:
  - mcp-server-bootstrap

Prompts:
  - prompt-engineering-foundations

Anything to remove or any category you want me to add?
```

Wait for user response. If they ask to remove items, drop them. If they ask for items in a category that has none matched, search the catalog directly for that category.

---

## Phase 4: Collect repo info

Ask in one message (multiple-choice + free-text):

- **Repo name?** (free text, kebab-case suggested)
- **Public or private?** (default: private)
- **Local clone path?** (ask explicitly — never guess. Prefer the directory the user is currently working in.)
- **GitHub Issues for milestones?** (default: no — opt-in, since this is destructive in a brand-new repo)

---

## Phase 5: Create repo and populate

Run these in order. After each command, confirm the expected output before proceeding to the next.

```bash
# 1. Create remote + clone
gh repo create "<USER>/<NAME>" --private --clone --add-readme=false   # or --public
cd "<LOCAL_PATH>/<NAME>"

# 2. Make directory structure
mkdir -p docs/know-how .claude/skills .claude/agents .claude/rules

# 3. Copy chosen catalog entries
#    For each <entry> in the user-confirmed list:
cp "$CONTEXT_FORGE_PATH/catalog/<category>/<entry>.md" \
   "docs/know-how/<category>--<entry>.md"
```

Then **synthesize** these top-level files (do not just copy from catalog — these are written from scratch using Phase 2 inputs):

- **`CLAUDE.md`** — 30–80 lines. Sections: project goal (Phase 2), high-level architecture (if known), agent guardrails (`avoid` list), references to `docs/know-how/*.md`.
- **`AGENTS.md`** — Mirror of CLAUDE.md but tool-agnostic (no `/skill` references, no Claude Code specifics). Used by Cursor / Copilot / Codex.
- **`README.md`** — 1-line tagline + Goal + Quick start placeholder + Status section.
- **`docs/spec.md`** — Phase 2 YAML expanded into Markdown sections: Goal, Milestones, Constraints, Domain, Avoid.

Then add boilerplate (only if `catalog/boilerplate/<project-type>.md` exists):

```bash
# Optional - copy project-type .gitignore etc. if present
cp "$CONTEXT_FORGE_PATH/catalog/boilerplate/<type>.gitignore" .gitignore
```

Always-include minimal `.gitignore`:

```
.env
.env.local
node_modules/
.DS_Store
Thumbs.db
.vscode/
.idea/
```

Commit and push:

```bash
git add .
git commit -m "초기 하네스 셋업 (context-forge)"
git push -u origin main
```

Optional — set repo description and topics from Phase 2 goal:

```bash
gh repo edit <USER>/<NAME> --description "<one-line goal>"
# topics: derived from project type and key tech words
```

---

## Phase 6: Hand off

Print a final message in this exact shape:

```
✅ Done. Your harness-engineered repo:

  https://github.com/<USER>/<NAME>
  local: <LOCAL_PATH>/<NAME>

Included from catalog (<N> entries):
  <list>

Next steps:
  cd <LOCAL_PATH>/<NAME>
  claude       # start a fresh session in the new repo

Tip: Edit docs/spec.md as your project evolves; CLAUDE.md/AGENTS.md should stay short.
```

After printing, **stop**. Do not start working in the new repo from this session.

---

## Error handling

- **`gh repo create` fails with name collision** — ask user for an alternate name; do not silently rename.
- **`cp` fails because catalog file missing** — list the missing files and stop. Either the catalog wasn't synced or the entry name was misspelled.
- **`git push` fails** — show the error, do not retry. Common cause: branch protection or repo visibility mismatch.
- **User aborts mid-flow** — leave the partially-created repo in place; do not auto-delete.
