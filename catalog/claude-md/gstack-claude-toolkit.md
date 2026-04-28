---
name: gstack-claude-toolkit
category: claude-md
domain: [general, ai-agent]
tags: [toolkit, full-stack, claude-code]
source: https://github.com/glowElephant/gstack
upstream: https://github.com/garrytan/gstack
when_to_use: Greenfield project that wants Garry Tan's curated 23-tool Claude Code stack out of the box. Best fit for solo founders or small teams shipping a SaaS-style product where pragmatism beats novelty.
priority: 5
---

# gstack — Garry Tan's Claude Code stack

`gstack` packages Garry Tan's opinionated tool selection for Claude Code-driven development: 23 tools spanning code search, planning, execution, debugging, and shipping.

The selection philosophy:

- **One canonical tool per job.** No optional alternatives.
- **Bias toward observable side effects.** Tools that log what they did so the agent can self-correct.
- **Plan / execute split.** Planning happens in a separate skill from execution to prevent drift.

## Quick start

When bootstrapping a project that wants this stack:

1. Drop the `gstack` skill set into `.claude/skills/` (or include via plugin source)
2. Read `gstack`'s top-level `README.md` to learn the order of operations (plan → branch → execute → review → ship)
3. Adopt its `CLAUDE.md` template verbatim for the first sprint, then customize

## Notes

- The exact 23 tools shift quarterly — pin a commit SHA in your fork.
- gstack assumes you have `gh` CLI authed and a Postgres-style mental model. Other domains may swap a few tools.
- Pairs well with `github/spec-kit` for the planning side.

## Source

- Upstream: https://github.com/garrytan/gstack
- Fork: https://github.com/glowElephant/gstack
