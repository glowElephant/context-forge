---
name: orchestration-pattern
category: multi-agent
domain: [ai-agent]
tags: [orchestration, dag, decomposition]
source: https://github.com/glowElephant/open-multi-agent
upstream: https://github.com/JackChen-me/open-multi-agent
when_to_use: Projects with goals that decompose into a DAG of subtasks (build pipeline, multi-stage data processing, complex feature with parallelizable parts). When a single linear plan won't capture the actual dependencies.
priority: 3
---

# Open multi-agent orchestration pattern

The orchestration pattern: a top-level **planner** agent decomposes a goal into a directed acyclic graph (DAG) of subtasks. Each leaf task is dispatched to a specialized **worker** agent. A **synthesizer** agent merges results.

When this pattern shines:

- The goal has natural parallelism (e.g., 5 unrelated investigations)
- Subtasks have clear inputs/outputs (no shared mutable state)
- The synthesis step is well-defined (concatenation, voting, ranking)

When it does NOT shine:

- Tasks are deeply sequential (planning gets in the way)
- Subtasks need shared context (overhead of passing data between agents > savings)

## Quick start

1. Identify the goal and write it as a single sentence
2. List 3–8 subtasks; check that each is independent
3. Define the synthesis rule before dispatching (otherwise you'll get incompatible outputs)
4. Use `Agent` tool calls in parallel from the orchestrator

## Notes

- The `superpowers:dispatching-parallel-agents` skill encodes this pattern with safety rails.
- Orchestrators should NOT also do work — pure delegation prevents context bloat.
- For 2 or fewer subtasks, the overhead usually beats the savings.

## Source

- Upstream: https://github.com/JackChen-me/open-multi-agent
- Fork: https://github.com/glowElephant/open-multi-agent
