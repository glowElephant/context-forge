---
name: cursor-rules-pattern
category: skills
domain: [general]
tags: [cursor, rules, mdc]
source: https://github.com/glowElephant/awesome-cursorrules
upstream: https://github.com/PatrickJS/awesome-cursorrules
when_to_use: Project where Cursor is the primary editor (or one of multiple editors). Use to bootstrap `.cursorrules` and `.cursor/rules/*.mdc` with battle-tested patterns.
priority: 4
applies_to_files: [.cursorrules, .cursor]
---

# Cursor rules pattern

Cursor's `.cursorrules` (and the newer `.cursor/rules/*.mdc` format) is the equivalent of `CLAUDE.md` for Cursor's agent. The `awesome-cursorrules` catalog has hundreds of community-tested rule files for popular stacks.

Two formats:

1. **`.cursorrules`** (legacy, single file) — one global rule file, repo-wide
2. **`.cursor/rules/*.mdc`** (new, per-file glob) — multiple rule files, each scoped to file globs (e.g., `apps/web/**/*.tsx`)

## Quick start

1. Browse `awesome-cursorrules` for your stack (Next.js, Django, Rails, Unity, etc.)
2. Copy the closest match into your repo as `.cursorrules` or split into `.cursor/rules/*.mdc`
3. Trim — most rules are too long; keep only what catches actual mistakes
4. Add 3–5 project-specific anti-patterns at the top

## Notes

- Don't duplicate `CLAUDE.md` content; reference shared sections via `AGENTS.md` if both must coexist.
- `.mdc` files have YAML frontmatter (`description`, `globs`) that auto-targets them.
- Keep total rule budget under ~5KB; Cursor truncates aggressively.

## Source

- Upstream: https://github.com/PatrickJS/awesome-cursorrules
- Fork: https://github.com/glowElephant/awesome-cursorrules
