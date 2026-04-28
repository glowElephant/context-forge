---
name: karpathy-single-claude-md
category: claude-md
domain: [general]
tags: [claude-md, single-file, observation-based]
source: https://github.com/glowElephant/andrej-karpathy-skills
upstream: https://github.com/forrestchang/andrej-karpathy-skills
when_to_use: Solo developer or small team that wants one carefully-crafted CLAUDE.md instead of a sprawling skill/rules tree. Especially relevant when the project codebase is small enough to articulate "here's how to write code in this repo" in one document.
priority: 4
---

# Karpathy-style single CLAUDE.md

Andrej Karpathy's observation: most LLM coding pitfalls are predictable, and a single well-curated `CLAUDE.md` covers more ground than a sprawling tree of rules and skills.

The pattern is:

1. **Lead with anti-patterns.** "When I ask for X, do not also do Y." Concrete failure modes you've seen.
2. **State the project mental model.** A paragraph that orients the agent — what the code does, who uses it, what the constraints are.
3. **Code style is short.** Don't replicate the linter; only flag things tools can't catch.
4. **Stop when uncertain.** Make explicit that asking is preferred over guessing.

## Quick start

Start the project's `CLAUDE.md` as one short file (under 200 lines) with these sections:

- **Project goal** (3–5 sentences)
- **Architecture mental model** (one paragraph)
- **Anti-patterns I've observed** (bulleted, concrete)
- **When to stop and ask** (3–5 triggers)

Resist the urge to grow it past one screen.

## Notes

- This style **complements** but does not replace task-specific skills; `CLAUDE.md` is the always-loaded context.
- Update it after every "I shouldn't have to repeat that" moment. That's the signal a rule should live in CLAUDE.md.
- Don't write rules linters can enforce — those waste context budget.

## Source

- Upstream: https://github.com/forrestchang/andrej-karpathy-skills
- Fork: https://github.com/glowElephant/andrej-karpathy-skills
