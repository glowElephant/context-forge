# context-forge v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working `/context-forge` Claude Code skill that turns a 5-minute project discussion into a fully harness-engineered new GitHub repository.

**Architecture:** Single meta-repository (`glowElephant/context-forge`) houses (1) a catalog of know-how entries with frontmatter, (2) `sources/index.json` mapping forked source repos, (3) the `/context-forge` skill itself. The skill, when invoked, reads the catalog, runs a guided discussion, matches catalog entries to the user's project, and uses `gh repo create` to bootstrap a new repo populated with curated `CLAUDE.md`, `AGENTS.md`, `docs/spec.md`, `.claude/{skills,agents,rules}/`, and chosen know-how files.

**Tech Stack:** Markdown (catalog + skill), JSON (sources index + JSON Schema), Bash (helper scripts), `gh` CLI (forking, repo creation), Node.js 20+ (validation scripts only — keep tiny, optional).

**Scope of v1 (this plan):**
- Repository foundation files (sources index, contributing, scoring docs)
- Catalog schema + 15–20 hand-curated catalog entries (manual seed; full extraction is v1.5)
- `/context-forge` skill body covering discussion → match → repo creation
- Validation script for catalog frontmatter
- Manual end-to-end smoke test

**Out of scope (deferred to v1.5+):**
- Automated extraction of `.md` files from forked source repos into catalog entries
- Quarterly auto-discovery job (`schedule` skill integration)
- GitHub Issues auto-generation in target repos
- "sync" command to update existing harness-engineered repos when catalog evolves

---

## File Structure

```
context-forge/
├── README.md                           [exists]
├── README.ko.md                        [exists]
├── LICENSE                             [Task 1]
├── .gitignore                          [Task 1]
├── sources/
│   ├── index.schema.json               [Task 2]
│   ├── index.json                      [Task 3]
│   └── fork-log.txt                    [exists]
├── catalog/
│   ├── README.md                       [Task 4]
│   ├── _schema/
│   │   └── entry.schema.json           [Task 4]
│   ├── claude-md/                      [Task 6 fills]
│   ├── agents-md/                      [Task 6 fills]
│   ├── skills/                         [Task 6 fills]
│   ├── conventions/                    [Task 6 fills]
│   ├── multi-agent/                    [Task 6 fills]
│   ├── prompts/                        [Task 6 fills]
│   ├── spec-driven/                    [Task 6 fills]
│   └── boilerplate/                    [Task 6 fills]
├── scripts/
│   ├── validate-catalog.sh             [Task 7]
│   └── lib/
│       └── frontmatter.sh              [Task 7]
├── .claude/
│   └── skills/
│       └── context-forge/
│           └── SKILL.md                [Tasks 8–12]
├── docs/
│   ├── contributing.md                 [Task 14]
│   ├── scoring.md                      [Task 14]
│   ├── specs/                          [exists]
│   └── plans/                          [exists]
```

**Why this layout:**
- `sources/index.json` is the single source of truth for which repos are forked. The skill reads it; humans edit it via PRs.
- `catalog/<category>/<name>.md` mirrors the skills system pattern (frontmatter + body). Each file is independent — adding a new entry is just dropping a file.
- `scripts/` stays tiny — Bash only, no toolchain.
- The skill itself lives at the canonical Claude Code path so it auto-discovers when this repo is set as a plugin source.

---

## Task 1: Repository foundation files

**Files:**
- Create: `LICENSE`
- Create: `.gitignore`

- [ ] **Step 1.1: Create LICENSE (MIT)**

```
MIT License

Copyright (c) 2026 glowElephant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 1.2: Create .gitignore**

```
# Editor
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Node (only used by validation scripts)
node_modules/
*.log

# Local overrides
.env
.env.local
*.local.md
```

- [ ] **Step 1.3: Commit**

```bash
git add LICENSE .gitignore
git commit -m "기본 메타 파일 추가 (LICENSE, .gitignore)"
```

---

## Task 2: sources/index.json schema

**Files:**
- Create: `sources/index.schema.json`

- [ ] **Step 2.1: Write JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/glowElephant/context-forge/sources/index.schema.json",
  "title": "context-forge sources index",
  "type": "object",
  "required": ["version", "updated_at", "sources"],
  "properties": {
    "version": { "type": "integer", "const": 1 },
    "updated_at": { "type": "string", "format": "date" },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["upstream", "fork", "category", "tier"],
        "properties": {
          "upstream": { "type": "string", "format": "uri" },
          "fork":     { "type": "string", "format": "uri" },
          "name":     { "type": "string" },
          "category": {
            "type": "string",
            "enum": [
              "claude-md", "agents-md", "skills", "conventions",
              "multi-agent", "prompts", "spec-driven", "mcp", "boilerplate"
            ]
          },
          "tier": { "type": "integer", "enum": [1, 2, 3] },
          "stars": { "type": "integer", "minimum": 0 },
          "pushed_at": { "type": "string", "format": "date" },
          "archived": { "type": "boolean" },
          "license":  { "type": "string" },
          "added_at": { "type": "string", "format": "date" },
          "notes":    { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  }
}
```

- [ ] **Step 2.2: Commit**

```bash
git add sources/index.schema.json
git commit -m "sources/index.json JSON Schema 추가"
```

---

## Task 3: sources/index.json initial population

**Files:**
- Create: `sources/index.json`

The fork log from earlier is the input. Each successfully forked repo becomes one entry.

- [ ] **Step 3.1: Generate index.json from fork-log.txt**

Run this from the repo root:

```bash
cat > /tmp/build-index.sh <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
USER="glowElephant"
DATE=$(date +%F)
out="sources/index.json"
{
  echo "{"
  echo "  \"version\": 1,"
  echo "  \"updated_at\": \"$DATE\","
  echo "  \"sources\": ["
  first=true
  while read -r line; do
    [[ "$line" =~ ^✓\ (.+)$ ]] || continue
    upstream="${BASH_REMATCH[1]}"
    name="${upstream##*/}"
    fork="https://github.com/$USER/$name"
    # Category inference from upstream slug (manual override allowed in PRs)
    cat=$(echo "$upstream" | tr '[:upper:]' '[:lower:]' | awk '
      /spec|prd/ {print "spec-driven"; exit}
      /mcp/ {print "mcp"; exit}
      /agent|orchestrat|swarm|maestro|ruflo|wshobson/ {print "multi-agent"; exit}
      /prompt/ {print "prompts"; exit}
      /skill/ {print "skills"; exit}
      /agents\.md|agents-md/ {print "agents-md"; exit}
      /design\.md|design-md/ {print "claude-md"; exit}
      /cursor|copilot|claude/ {print "claude-md"; exit}
      {print "skills"}')
    [[ "$first" == "true" ]] || echo ","
    first=false
    cat <<JSON
    {
      "upstream": "https://github.com/$upstream",
      "fork": "$fork",
      "name": "$name",
      "category": "$cat",
      "tier": 1,
      "added_at": "$DATE"
    }
JSON
  done < sources/fork-log.txt
  echo
  echo "  ]"
  echo "}"
} > "$out"
echo "wrote $out"
BASH
bash /tmp/build-index.sh
```

- [ ] **Step 3.2: Verify it parses**

```bash
node -e "JSON.parse(require('fs').readFileSync('sources/index.json'))"
```

Expected: no output (silent success).

- [ ] **Step 3.3: Verify count matches forks**

```bash
forks=$(grep -c '^✓ ' sources/fork-log.txt)
entries=$(node -e "console.log(JSON.parse(require('fs').readFileSync('sources/index.json')).sources.length)")
echo "forks=$forks entries=$entries"
test "$forks" = "$entries" && echo "✅ match"
```

Expected: `✅ match`.

- [ ] **Step 3.4: Manually adjust 5 obvious miscategorizations**

Edit `sources/index.json`. For each of these, set `category` to the correct value:
- `agentsmd/agents.md` → `agents-md`
- `google-labs-code/design.md` → `claude-md` (DESIGN.md sibling)
- `VoltAgent/awesome-design-md` → `claude-md`
- `dair-ai/Prompt-Engineering-Guide` → `prompts`
- `f/prompts.chat` → `prompts`
- `modelcontextprotocol/servers` → `mcp`
- `punkpeye/awesome-mcp-servers` → `mcp`
- `appcypher/awesome-mcp-servers` → `mcp`
- `yzfly/Awesome-MCP-ZH` → `mcp`
- `jaw9c/awesome-remote-mcp-servers` → `mcp`
- `github/spec-kit` → `spec-driven`
- `Fission-AI/OpenSpec` → `spec-driven`
- `Pimzino/spec-workflow-mcp` → `spec-driven`
- `gsd-build/get-shit-done` → `spec-driven`
- `shotgun-sh/shotgun` → `spec-driven`

- [ ] **Step 3.5: Commit**

```bash
git add sources/index.json
git commit -m "sources/index.json 초기 시드 67개 등록"
```

---

## Task 4: Catalog schema + README

**Files:**
- Create: `catalog/_schema/entry.schema.json`
- Create: `catalog/README.md`

- [ ] **Step 4.1: Write catalog entry JSON Schema**

This validates frontmatter only. Body is free Markdown.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/glowElephant/context-forge/catalog/_schema/entry.schema.json",
  "title": "Catalog entry frontmatter",
  "type": "object",
  "required": ["name", "category", "domain", "when_to_use", "source"],
  "properties": {
    "name":        { "type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$" },
    "category": {
      "type": "string",
      "enum": [
        "claude-md", "agents-md", "skills", "conventions",
        "multi-agent", "prompts", "spec-driven", "mcp", "boilerplate"
      ]
    },
    "domain": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "general", "web", "game-engine", "mobile", "ai-agent",
          "backend", "design", "documentation", "ml"
        ]
      },
      "minItems": 1
    },
    "tags":      { "type": "array", "items": { "type": "string" } },
    "source":    { "type": "string", "format": "uri" },
    "upstream":  { "type": "string", "format": "uri" },
    "when_to_use": { "type": "string", "minLength": 10 },
    "priority":  { "type": "integer", "minimum": 1, "maximum": 5 },
    "applies_to_files": { "type": "array", "items": { "type": "string" } }
  }
}
```

- [ ] **Step 4.2: Write catalog/README.md**

```markdown
# Catalog

This directory holds curated know-how entries. Each entry is one Markdown file with YAML frontmatter, mirroring the [Claude Code skills](https://docs.anthropic.com/) pattern.

## Entry format

\`\`\`yaml
---
name: tdd-workflow
category: conventions
domain: [general]
tags: [testing, methodology]
source: https://github.com/glowElephant/awesome-design-md/blob/main/tdd.md
upstream: https://github.com/VoltAgent/awesome-design-md
when_to_use: Greenfield projects where TDD is feasible. Skip for hotfixes or exploration spikes.
priority: 3
---

(Body — actual know-how content, copied from upstream and lightly adapted.)
\`\`\`

## Categories

- `claude-md` — patterns and templates for `CLAUDE.md`
- `agents-md` — patterns for `AGENTS.md` (the open standard)
- `skills` — reusable Claude Code skills
- `conventions` — coding/review/commit conventions
- `multi-agent` — orchestration patterns
- `prompts` — system/user prompt templates
- `spec-driven` — spec-driven development workflows
- `mcp` — MCP server configs and integration guides
- `boilerplate` — project-type starters (.gitignore, tsconfig, etc.)

## Validation

Run `scripts/validate-catalog.sh` before committing new entries.
```

- [ ] **Step 4.3: Create empty category directories**

```bash
mkdir -p catalog/{claude-md,agents-md,skills,conventions,multi-agent,prompts,spec-driven,mcp,boilerplate}
# Add .gitkeep so empty dirs are tracked
for d in catalog/claude-md catalog/agents-md catalog/skills catalog/conventions catalog/multi-agent catalog/prompts catalog/spec-driven catalog/mcp catalog/boilerplate; do
  touch "$d/.gitkeep"
done
```

- [ ] **Step 4.4: Commit**

```bash
git add catalog/
git commit -m "카탈로그 스키마 + 카테고리 디렉토리 구조 추가"
```

---

## Task 5: Catalog frontmatter validator

**Files:**
- Create: `scripts/validate-catalog.sh`
- Create: `scripts/lib/frontmatter.sh`

- [ ] **Step 5.1: Write frontmatter parser helper**

`scripts/lib/frontmatter.sh`:

```bash
#!/usr/bin/env bash
# Extract YAML frontmatter from a Markdown file to stdout.
# Returns 0 if frontmatter found, 1 otherwise.
extract_frontmatter() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0; saw_open = 0 }
    /^---[ \t]*$/ {
      if (!saw_open) { saw_open = 1; in_fm = 1; next }
      else if (in_fm) { in_fm = 0; exit }
    }
    in_fm { print }
    END { if (!saw_open) exit 1 }
  ' "$file"
}
```

- [ ] **Step 5.2: Write validator**

`scripts/validate-catalog.sh`:

```bash
#!/usr/bin/env bash
# Validate every catalog/*/*.md file:
#  1. has frontmatter
#  2. frontmatter has required keys: name, category, domain, when_to_use, source
#  3. category matches its parent directory
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/frontmatter.sh"

REQUIRED_KEYS=(name category domain when_to_use source)
fail=0

for file in catalog/*/*.md; do
  [[ "$file" == *"/_schema/"* ]] && continue
  parent_cat="$(basename "$(dirname "$file")")"
  fm="$(extract_frontmatter "$file" || true)"
  if [[ -z "$fm" ]]; then
    echo "✗ $file — missing frontmatter"
    fail=$((fail+1))
    continue
  fi
  for key in "${REQUIRED_KEYS[@]}"; do
    if ! echo "$fm" | grep -qE "^${key}:"; then
      echo "✗ $file — missing key: $key"
      fail=$((fail+1))
    fi
  done
  decl_cat="$(echo "$fm" | sed -nE 's/^category:[ ]*([a-z-]+).*/\1/p')"
  if [[ -n "$decl_cat" && "$decl_cat" != "$parent_cat" ]]; then
    echo "✗ $file — category=$decl_cat but in directory $parent_cat/"
    fail=$((fail+1))
  fi
done

if [[ "$fail" -eq 0 ]]; then
  echo "✅ all catalog entries valid"
  exit 0
fi
echo "❌ $fail issue(s) found"
exit 1
```

Make executable:

```bash
chmod +x scripts/validate-catalog.sh scripts/lib/frontmatter.sh
```

- [ ] **Step 5.3: Run validator on empty catalog (sanity check)**

```bash
./scripts/validate-catalog.sh
```

Expected: `✅ all catalog entries valid` (no .md files yet, so trivially passes).

- [ ] **Step 5.4: Write a deliberately broken entry and confirm validator catches it**

```bash
cat > catalog/skills/_test-broken.md <<'MD'
---
name: test
---
body
MD
./scripts/validate-catalog.sh && echo "should have failed!" || echo "✅ caught broken entry"
rm catalog/skills/_test-broken.md
```

Expected: `✅ caught broken entry`.

- [ ] **Step 5.5: Commit**

```bash
git add scripts/
git commit -m "catalog 검증 스크립트 + frontmatter 파서"
```

---

## Task 6: Hand-curate 15 catalog entries

**Files:** create one Markdown file per entry. List of entries below.

This is the v1 manual seed. Each entry is small (50–150 lines). Body is a tight summary of the upstream's core idea, not a full copy.

The 15 entries to write (one per step). For each, use the template under Step 6.0.

- [ ] **Step 6.0: Entry template**

Use this for every step below. Replace placeholders:

```markdown
---
name: <kebab-case-name>
category: <category>
domain: [<domain1>, <domain2>]
tags: [<tag1>, <tag2>]
source: https://github.com/glowElephant/<fork-repo>
upstream: https://github.com/<upstream>
when_to_use: <one or two sentences>
priority: 3
---

# <Human-readable title>

(2–4 paragraphs summarizing the core idea, drawn from the upstream README/docs.)

## Quick start

(Concrete bullet list — what to do in a new project.)

## Notes

(Caveats, when not to use, version pinning if relevant.)

## Source

- Upstream: <upstream URL>
- Fork: <fork URL>
```

- [ ] **Step 6.1: `catalog/skills/superpowers-skills-pattern.md`** — based on `obra/superpowers`. Domain: `general, ai-agent`. when_to_use: "Any project where Claude Code skills will be used as the primary harness."

- [ ] **Step 6.2: `catalog/claude-md/karpathy-single-claude-md.md`** — based on `forrestchang/andrej-karpathy-skills`. Domain: `general`. when_to_use: "Solo or small-team projects that benefit from one carefully-crafted CLAUDE.md."

- [ ] **Step 6.3: `catalog/claude-md/gstack-claude-toolkit.md`** — based on `garrytan/gstack`. Domain: `general, ai-agent`. when_to_use: "Greenfield project that wants Garry Tan's 23-tool Claude Code stack."

- [ ] **Step 6.4: `catalog/agents-md/agents-md-standard.md`** — based on `agentsmd/agents.md`. Domain: `general`. when_to_use: "Multi-agent (Claude/Cursor/Codex) projects needing a single neutral instruction file."

- [ ] **Step 6.5: `catalog/spec-driven/github-spec-kit.md`** — based on `github/spec-kit`. Domain: `general`. when_to_use: "Teams adopting spec-driven development with GitHub-native tooling."

- [ ] **Step 6.6: `catalog/spec-driven/openspec.md`** — based on `Fission-AI/OpenSpec`. Domain: `general`. when_to_use: "Spec-driven projects preferring an open-source CLI over GitHub-tied tools."

- [ ] **Step 6.7: `catalog/multi-agent/wshobson-agents.md`** — based on `wshobson/agents`. Domain: `ai-agent`. when_to_use: "Projects needing pre-built Claude Code subagents for common dev roles."

- [ ] **Step 6.8: `catalog/multi-agent/orchestration-pattern.md`** — based on `JackChen-me/open-multi-agent`. Domain: `ai-agent`. when_to_use: "Projects with goals that decompose into a DAG of subtasks."

- [ ] **Step 6.9: `catalog/mcp/mcp-server-bootstrap.md`** — based on `modelcontextprotocol/servers`. Domain: `general`. when_to_use: "Any project that will integrate at least one MCP server."

- [ ] **Step 6.10: `catalog/mcp/awesome-mcp-discovery.md`** — based on `punkpeye/awesome-mcp-servers`. Domain: `general`. when_to_use: "Bootstrapping checklist of which MCP servers to install for a given stack."

- [ ] **Step 6.11: `catalog/prompts/prompt-engineering-foundations.md`** — based on `dair-ai/Prompt-Engineering-Guide`. Domain: `general, ai-agent`. when_to_use: "Any project where the team is new to prompt engineering."

- [ ] **Step 6.12: `catalog/skills/cursor-rules-pattern.md`** — based on `PatrickJS/awesome-cursorrules`. Domain: `general`. when_to_use: "Project where Cursor is the primary editor."

- [ ] **Step 6.13: `catalog/skills/copilot-instructions-pattern.md`** — based on `github/awesome-copilot`. Domain: `general`. when_to_use: "Project using GitHub Copilot or Copilot Chat."

- [ ] **Step 6.14: `catalog/conventions/context-engineering-intro.md`** — based on `coleam00/context-engineering-intro`. Domain: `general, ai-agent`. when_to_use: "Onboarding context engineering as a discipline."

- [ ] **Step 6.15: `catalog/skills/claude-code-hooks-mastery.md`** — based on `disler/claude-code-hooks-mastery`. Domain: `general`. when_to_use: "Project that wants automated guardrails via Claude Code hooks."

- [ ] **Step 6.16: Run validator after every 5 entries**

```bash
./scripts/validate-catalog.sh
```

Expected: `✅ all catalog entries valid` after each batch.

- [ ] **Step 6.17: Commit in 3 batches (5 entries each)**

```bash
git add catalog/
git commit -m "카탈로그 시드 1차 5개 추가"
# repeat for batches 2 and 3
```

---

## Task 7: Skill manifest header

**Files:**
- Create: `.claude/skills/context-forge/SKILL.md`

- [ ] **Step 7.1: Write SKILL.md frontmatter + intro section**

The skill file is one Markdown file. Subsequent tasks fill in body sections in order.

```markdown
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
   \`\`\`bash
   gh auth status
   \`\`\`
   Expected: a logged-in account.

2. context-forge is checked out locally with the catalog present:
   \`\`\`bash
   test -d "$CONTEXT_FORGE_PATH/catalog" && test -f "$CONTEXT_FORGE_PATH/sources/index.json"
   \`\`\`
   If `CONTEXT_FORGE_PATH` is not set, ask the user where their context-forge clone is.

3. The catalog passes validation:
   \`\`\`bash
   "$CONTEXT_FORGE_PATH/scripts/validate-catalog.sh"
   \`\`\`

If any step fails: stop and report the exact command that failed. Do NOT proceed.
```

- [ ] **Step 7.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "context-forge 스킬 매니페스트 + 사전조건 섹션"
```

---

## Task 8: Skill body — fixed-question phase

**Files:**
- Modify: `.claude/skills/context-forge/SKILL.md` (append)

- [ ] **Step 8.1: Append "Fixed questions" section**

```markdown

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
```

- [ ] **Step 8.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "스킬: 고정 질문 단계 추가"
```

---

## Task 9: Skill body — free-discussion phase

**Files:**
- Modify: `.claude/skills/context-forge/SKILL.md` (append)

- [ ] **Step 9.1: Append "Free discussion" section**

```markdown

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

\`\`\`yaml
goal: ...
milestones: [..., ..., ...]
constraints: ...
domain: ...
avoid: ...
\`\`\`

Do NOT show this YAML to the user yet. It feeds Phase 3.
```

- [ ] **Step 9.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "스킬: 자유 디스커션 단계 추가"
```

---

## Task 10: Skill body — catalog matching + confirmation

**Files:**
- Modify: `.claude/skills/context-forge/SKILL.md` (append)

- [ ] **Step 10.1: Append "Match" section**

```markdown

## Phase 3: Catalog match

Read every `catalog/*/*.md` file's frontmatter. For each entry, decide whether it applies based on:

1. **Domain match** — at least one of `entry.domain` overlaps with the user's project type, OR `domain: [general]` is present.
2. **`when_to_use` semantic fit** — does the entry's `when_to_use` text describe this user's project? Use judgment.
3. **Multi-agent gating** — entries with `category: multi-agent` only apply if Phase 1 Q4 was "yes".
4. **Stack-specific gating** — if entry has `applies_to_files` (e.g., `["package.json"]`) and the user's stack doesn't use those files, skip it.

Group results by category. Within each category, pick at most 3 (sort by `priority` field, fall back to alphabetical).

### Present the proposal

Show the user a single message structured like this:

\`\`\`
Based on our discussion, I'll include these from the catalog:

CLAUDE.md:
  - karpathy-single-claude-md — One careful CLAUDE.md
  - gstack-claude-toolkit — Garry Tan 23-tool stack

Skills:
  - superpowers-skills-pattern — Skills framework
  - cursor-rules-pattern — (you mentioned Cursor)

Spec-driven:
  - github-spec-kit

MCP:
  - mcp-server-bootstrap

Prompts:
  - prompt-engineering-foundations

Anything to remove or any category you want me to add?
\`\`\`

Wait for user response. If they ask to remove items, drop them. If they ask for items in a category that has none matched, search the catalog directly for that category.
```

- [ ] **Step 10.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "스킬: 카탈로그 매칭 + 컨펌 단계 추가"
```

---

## Task 11: Skill body — repo creation + file generation

**Files:**
- Modify: `.claude/skills/context-forge/SKILL.md` (append)

- [ ] **Step 11.1: Append "Create repo" section**

```markdown

## Phase 4: Collect repo info

Ask in one message (multiple-choice + free-text):

- **Repo name?** (free text, kebab-case suggested)
- **Public or private?** (default: private)
- **Local clone path?** (default: same directory as the user's existing project root, ask explicitly — never guess)
- **GitHub Issues for milestones?** (default: no — opt-in, since this is destructive in a brand-new repo)

## Phase 5: Create repo and populate

Run, in order, exactly these commands. After each, confirm the expected output before proceeding.

\`\`\`bash
# 1. Create remote + clone
gh repo create "<USER>/<NAME>" --<public|private> --clone --add-readme=false
cd "<LOCAL_PATH>/<NAME>"

# 2. Copy chosen catalog entries into the new repo
mkdir -p docs/know-how .claude/{skills,agents,rules}
for entry in <list of selected catalog files>; do
  cp "$CONTEXT_FORGE_PATH/$entry" "docs/know-how/$(basename $entry)"
done

# 3. Generate top-level files (CLAUDE.md, AGENTS.md, README.md, docs/spec.md)
#    These are SYNTHESIZED from the discussion + chosen entries — see "Synthesis rules" below.

# 4. .gitignore for the project type (copy from catalog/boilerplate/<type>.gitignore if it exists)

# 5. Commit and push
git add .
git commit -m "초기 하네스 셋업 (context-forge)"
git push -u origin main

# 6. Optional: gh repo edit to set description / topics derived from goals
\`\`\`

### Synthesis rules

For each generated file, follow these rules. Never copy-paste a catalog entry into these top-level files — they are syntheses.

- **`CLAUDE.md`** — 30–80 lines. Sections: project goal (from Phase 2), high-level architecture if known, agent guardrails ("don't do X" from Phase 2 'avoid' list), references to `docs/know-how/*.md` files.
- **`AGENTS.md`** — Mirror of CLAUDE.md but tool-agnostic (no `/skill` references, no `Claude Code` specifics). Used by Cursor/Copilot/Codex.
- **`README.md`** — 1-line tagline + Goal (from Phase 2) + Quick start placeholder + Status section.
- **`docs/spec.md`** — full Phase 2 YAML expanded into Markdown sections: Goal, Milestones, Constraints, Domain, Avoid.
```

- [ ] **Step 11.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "스킬: 저장소 생성 + 파일 합성 단계 추가"
```

---

## Task 12: Skill body — completion + handoff

**Files:**
- Modify: `.claude/skills/context-forge/SKILL.md` (append)

- [ ] **Step 12.1: Append "Done" section**

```markdown

## Phase 6: Hand off

Print a final message in this exact shape:

\`\`\`
✅ Done. Your harness-engineered repo:

  https://github.com/<user>/<name>
  local: <path>

Included from catalog (<N> entries):
  <list>

Next steps:
  cd <path>
  claude       # start a fresh session in the new repo

Tip: Edit docs/spec.md as your project evolves; CLAUDE.md/AGENTS.md should stay short.
\`\`\`

After printing, **stop**. Do not start working in the new repo from this session.
```

- [ ] **Step 12.2: Commit**

```bash
git add .claude/skills/context-forge/SKILL.md
git commit -m "스킬: 완료 메시지 + 핸드오프 단계 추가"
```

---

## Task 13: Skill smoke test (manual)

**Files:** none. Documentation step.

This is an end-to-end manual test. The plan executor performs it and records the result in `docs/specs/2026-04-28-smoke-test-results.md`.

- [ ] **Step 13.1: Set CONTEXT_FORGE_PATH and load the skill**

```bash
export CONTEXT_FORGE_PATH=/c/Git/context-forge
```

In a fresh Claude Code session in any directory, type `/context-forge` (or invoke the skill via `Skill` tool if running headless).

- [ ] **Step 13.2: Run through with a known scenario**

Test scenario: "I'm building a small Next.js + TypeScript SaaS, solo, multi-agent yes."

Expected behavior:
- 4 fixed questions asked
- 5–8 free-discussion questions
- Catalog match shows: gstack-claude-toolkit, superpowers-skills-pattern, github-spec-kit, mcp-server-bootstrap, prompt-engineering-foundations, agents-md-standard
- New repo `<user>/<test-name>` is created with the files described in Task 11

- [ ] **Step 13.3: Verify the new repo contents**

```bash
cd <new-repo-path>
ls CLAUDE.md AGENTS.md README.md docs/spec.md
ls docs/know-how/   # 5–7 files
git log --oneline   # 1 commit "초기 하네스 셋업 (context-forge)"
```

Expected: all listed files exist, commit log shows the initial commit.

- [ ] **Step 13.4: Record results**

Create `docs/specs/2026-04-28-smoke-test-results.md` with:
- date / scenario / what worked / what failed / fixes applied
- screenshots optional but encouraged

- [ ] **Step 13.5: Commit**

```bash
git add docs/specs/2026-04-28-smoke-test-results.md
git commit -m "스모크 테스트 결과 기록"
```

---

## Task 14: Contributing + scoring docs

**Files:**
- Create: `docs/contributing.md`
- Create: `docs/scoring.md`

- [ ] **Step 14.1: Write `docs/contributing.md`** — explains how to:
  - Propose a new source repo (Discussions or PR to `sources/index.json`)
  - Add a catalog entry (drop file in `catalog/<category>/`, run validator)
  - Suggest a category split / new category (Discussions only, never silent)

  Concrete length target: 80–120 lines. Include a worked example PR description.

- [ ] **Step 14.2: Write `docs/scoring.md`** — verbatim copy of the spec's section 8 "포크 저장소 발굴 정책" (5-factor rubric, tier thresholds, domain taxonomy). Translate to English alongside Korean. Length: 100–150 lines.

- [ ] **Step 14.3: Link from READMEs**

Verify both `README.md` and `README.ko.md` already link to these files (they do, from earlier writeup). Run:

```bash
grep -E '(contributing|scoring)\.md' README.md README.ko.md
```

Expected: matches in both.

- [ ] **Step 14.4: Commit**

```bash
git add docs/contributing.md docs/scoring.md
git commit -m "기여 가이드 + 스코어링 규칙 문서 추가"
```

---

## Task 15: Push and tag v1.0.0

**Files:** none.

- [ ] **Step 15.1: Push all work**

```bash
git push origin main
```

- [ ] **Step 15.2: Tag**

```bash
git tag -a v1.0.0 -m "v1.0.0 — initial harness-engineering release"
git push origin v1.0.0
```

- [ ] **Step 15.3: Create GitHub release**

```bash
gh release create v1.0.0 --title "v1.0.0 — context-forge initial release" --notes "First public release. v1 catalog seeded with 15 hand-curated entries spanning Claude/Cursor/Copilot, spec-driven development, multi-agent orchestration, MCP, and prompts. /context-forge skill ready for end-to-end use. See docs/specs/ for design and v2 roadmap."
```

---

## Open items deferred to v1.5+

Track as GitHub Issues after v1.0.0 ships.

- Catalog auto-extraction from forked repos (currently manual)
- Quarterly auto-discovery job (use `schedule` skill)
- "sync" command to update existing harness-engineered repos when catalog changes
- GitHub Issues auto-generation in target repos (one Issue per Phase 2 milestone)
- v2 catalog expansion (use the v2 pool in `docs/specs/2026-04-28-fork-candidates.md`)
- Additional language stylistic guides for non-AI categories
