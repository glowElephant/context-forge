---
name: agents-md-standard
category: agents-md
domain: [general]
tags: [agents-md, standard, multi-tool]
source: https://github.com/glowElephant/agents.md
upstream: https://github.com/agentsmd/agents.md
when_to_use: Multi-agent or multi-tool projects where Claude, Cursor, Copilot, Codex, and other agents must read the same instructions. Use AGENTS.md as the neutral, tool-agnostic source of truth.
priority: 5
---

# AGENTS.md — the open standard

`AGENTS.md` is the open, vendor-neutral standard for "how an AI coding agent should operate in this repo." Where `CLAUDE.md` is Claude Code-specific, `AGENTS.md` is meant to be read by any agent — Claude, Cursor, Copilot, Codex, Aider, etc.

Key rules from the spec:

1. **One file at the repo root.** Not per-folder.
2. **No tool-specific syntax.** No `/skill`, no Cursor MDC blocks, no Copilot directives.
3. **Imperative, declarative, short.** Prefer "Run tests with `pnpm test`" over "Tests should be run."
4. **Sections are conventional but not required**: Setup, Build, Test, Code style, Architecture, Caveats.

## Quick start

Add a top-level `AGENTS.md` with these sections:

- `## Setup` — exact commands to bootstrap the dev environment
- `## Build` — exact build commands
- `## Test` — exact test commands plus where tests live
- `## Code style` — only the 3–5 rules linters can't enforce
- `## Architecture` — 1 paragraph
- `## Caveats` — known footguns

Mirror essential content into `CLAUDE.md` if you also want Claude-Code-specific guidance, but keep the tool-agnostic version canonical.

## Notes

- If both `CLAUDE.md` and `AGENTS.md` exist, prefer keeping `AGENTS.md` shorter and more authoritative.
- The standard is still evolving — pin to the spec version you adopted.

## Source

- Upstream: https://github.com/agentsmd/agents.md
- Fork: https://github.com/glowElephant/agents.md
