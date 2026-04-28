---
name: prompt-engineering-foundations
category: prompts
domain: [general, ai-agent]
tags: [prompts, foundations, learning]
source: https://github.com/glowElephant/Prompt-Engineering-Guide
upstream: https://github.com/dair-ai/Prompt-Engineering-Guide
when_to_use: Any project where the team is new to prompt engineering, or when designing a complex prompt that needs few-shot examples, chain-of-thought, or structured output.
priority: 3
---

# Prompt engineering foundations

`dair-ai/Prompt-Engineering-Guide` is the most widely cited educational resource on prompt engineering, RAG, and AI agents. It's a guide, not a recipe book — read it once and refer back.

Core concepts to internalize:

1. **Zero-shot vs few-shot.** When examples help vs hurt.
2. **Chain-of-thought.** Explicit reasoning steps for hard tasks.
3. **Structured output.** When and how to require JSON / tool calls.
4. **System vs user vs assistant roles.** What each is for.
5. **Decomposition.** Breaking a hard task into subtasks the model handles reliably.

## Quick start

When designing a new prompt:

1. Start with zero-shot — does the model do it?
2. If unreliable, add 1–3 examples (few-shot)
3. If still unreliable, add chain-of-thought ("think step by step before answering")
4. If output is hard to parse, switch to structured output (tool calls or JSON schema)
5. If task is just hard, decompose into multiple prompts

## Notes

- Prompt engineering changes fast. Anchor on principles, not specific phrasings.
- For Claude specifically, `anthropics/claude-cookbooks` has more current recipes.
- Don't over-engineer prompts that already work — readability matters.

## Source

- Upstream: https://github.com/dair-ai/Prompt-Engineering-Guide
- Fork: https://github.com/glowElephant/Prompt-Engineering-Guide
