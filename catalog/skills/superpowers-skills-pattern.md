---
name: superpowers-skills-pattern
category: skills
domain: [general, ai-agent]
tags: [skills, framework, methodology]
source: https://github.com/glowElephant/superpowers
upstream: https://github.com/obra/superpowers
when_to_use: Any project where Claude Code skills will be the primary harness layer. Especially good when the team wants pre-made skills for brainstorming, plan writing, plan execution, debugging, code review, and TDD.
priority: 5
---

# Superpowers skills pattern

The `superpowers` framework is the de-facto standard for organizing reusable Claude Code skills. It defines:

- A **skill manifest** format (`SKILL.md` with YAML frontmatter `name` + `description` that triggers automatic invocation)
- Skill **types** — rigid (TDD, debugging — follow exactly) vs flexible (patterns — adapt to context)
- A **skill priority** order — process skills first (brainstorming, debugging) then implementation skills (frontend-design, mcp-builder)
- Anti-patterns and red flags ("This is too simple to need a design") that prevent skipping discipline

## Quick start

Drop `superpowers` into your project as a plugin/skill source and invoke `superpowers:brainstorming` before any creative work, `superpowers:writing-plans` after the brainstorm, `superpowers:executing-plans` to ship.

For greenfield work the loop is:

1. `brainstorming` → design doc
2. `writing-plans` → step-by-step plan
3. `executing-plans` (or `subagent-driven-development`) → implementation
4. `finishing-a-development-branch` → wrap up

## Notes

- Treat `superpowers` skills as **rigid** unless explicitly marked flexible.
- User CLAUDE.md instructions always win over a skill, but the skill still must be invoked first.
- Skills evolve — don't rely on memory; let the Skill tool re-load each session.

## Source

- Upstream: https://github.com/obra/superpowers
- Fork: https://github.com/glowElephant/superpowers
