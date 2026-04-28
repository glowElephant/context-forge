---
name: context-engineering-intro
category: conventions
domain: [general, ai-agent]
tags: [context-engineering, methodology, onboarding]
source: https://github.com/glowElephant/context-engineering-intro
upstream: https://github.com/coleam00/context-engineering-intro
when_to_use: Onboarding a team to context engineering as a discipline. Especially when team members come from a "just write a great prompt" mindset and need to internalize that context (memory, retrieval, tools, examples) is the actual leverage.
priority: 4
---

# Context engineering — the discipline

Context engineering is the discipline of designing the **non-prompt** parts of an LLM system: what's in memory, what's retrieved, which tools are exposed, which examples are visible, how state flows between turns.

Three claims:

1. **Most LLM failures are context failures, not prompt failures.** The model didn't have the right info, not the right phrasing.
2. **Context is finite.** Every byte spent on irrelevant info is a byte stolen from the actual task. Curation matters.
3. **Tools change the game.** A retrieval tool, a write-to-file tool, a search tool — each shifts what the model can do without changing the prompt.

## Quick start

Before tuning prompts, ask:

1. **What's in the context window right now?** Skim it.
2. **What's missing?** Often: the file the user is editing, recent error logs, the spec doc.
3. **What's noise?** Often: long file dumps, irrelevant past turns, framework boilerplate.
4. **Which tools should the model have?** Add ones that let it self-correct (run tests, grep code).
5. **Then** revisit the prompt.

## Notes

- Context engineering benefits compound: skills, memory, hooks, MCP — they all add up.
- Pair this with `superpowers:brainstorming` for projects — the skill bakes context engineering into the workflow.
- Without context engineering, scaling up to harder tasks just produces louder hallucinations.

## Source

- Upstream: https://github.com/coleam00/context-engineering-intro
- Fork: https://github.com/glowElephant/context-engineering-intro
