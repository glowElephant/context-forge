# Catalog

This directory holds curated know-how entries. Each entry is one Markdown file with YAML frontmatter, mirroring the [Claude Code skills](https://docs.anthropic.com/) pattern.

## Entry format

```yaml
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
```

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

Run `scripts/validate-catalog.sh` from the repo root before committing new entries.
