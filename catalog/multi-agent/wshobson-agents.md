---
name: wshobson-agents
category: multi-agent
domain: [ai-agent]
tags: [subagents, claude-code, automation]
source: https://github.com/glowElephant/agents
upstream: https://github.com/wshobson/agents
when_to_use: Projects that want pre-built Claude Code subagents covering common dev roles (code reviewer, debugger, explorer, planner, etc.) without writing each from scratch.
priority: 4
---

# wshobson/agents — Claude Code subagent collection

`wshobson/agents` is one of the largest curated collections of production-tested Claude Code subagents. Each agent is a single Markdown file with frontmatter (`name`, `description`, `tools`) and a system prompt body.

Agent roles typically included:

- **code-reviewer** — diff-focused review with confidence-based filtering
- **debugger** — systematic debugging with hypothesis tracking
- **explorer** — fast read-only codebase search
- **planner** — multi-step plan generation
- **test-writer** — TDD-style test generation

## Quick start

1. Drop the `agents/` directory into your project's `.claude/agents/`
2. Invoke an agent via the `Agent` tool with `subagent_type`: e.g., `Agent({subagent_type: "code-reviewer", prompt: "..."})`
3. Customize prompts in-place — these are starting points, not gospel

## Notes

- Some agents assume specific tools (`Grep`, `Bash`); verify your harness exposes them.
- Replace the default model frontmatter (`opus`/`sonnet`) to match your budget and latency needs.
- Don't ship more than ~10 agents to a project — agent sprawl hurts discoverability.

## Source

- Upstream: https://github.com/wshobson/agents
- Fork: https://github.com/glowElephant/agents
