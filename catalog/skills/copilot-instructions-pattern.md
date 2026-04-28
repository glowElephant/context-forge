---
name: copilot-instructions-pattern
category: skills
domain: [general]
tags: [copilot, github, instructions]
source: https://github.com/glowElephant/awesome-copilot
upstream: https://github.com/github/awesome-copilot
when_to_use: Project using GitHub Copilot or Copilot Chat. Use to bootstrap `.github/copilot-instructions.md` and per-task instruction files with patterns curated by GitHub themselves.
priority: 4
applies_to_files: [.github/copilot-instructions.md, .github/instructions]
---

# Copilot instructions pattern

`github/awesome-copilot` is GitHub's official curation of Copilot instructions, agents, and skills. It mirrors the structure of `awesome-cursorrules` but for Copilot's ecosystem.

GitHub's instruction system layers:

- **`.github/copilot-instructions.md`** — repo-wide always-included context
- **`.github/instructions/*.instructions.md`** — task-scoped (with `applyTo` glob frontmatter)
- **`.github/prompts/*.prompt.md`** — reusable prompt templates
- **`.github/agents/*.agent.md`** — Copilot Chat agents

## Quick start

1. Add `.github/copilot-instructions.md` with project goal + 3–5 anti-patterns
2. For language-specific guidance, add `.github/instructions/typescript.instructions.md` with `applyTo: "**/*.ts,**/*.tsx"`
3. Browse `awesome-copilot` for ready-made instruction files matching your stack

## Notes

- Copilot reads instructions even in non-chat completion contexts — keep them tight.
- Don't enable too many instruction files at once; each adds latency.
- These files coexist with `CLAUDE.md` and `AGENTS.md` — keep guidance consistent or one tool will diverge.

## Source

- Upstream: https://github.com/github/awesome-copilot
- Fork: https://github.com/glowElephant/awesome-copilot
