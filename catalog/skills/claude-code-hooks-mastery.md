---
name: claude-code-hooks-mastery
category: skills
domain: [general]
tags: [hooks, automation, guardrails]
source: https://github.com/glowElephant/claude-code-hooks-mastery
upstream: https://github.com/disler/claude-code-hooks-mastery
when_to_use: Project that wants automated guardrails — block dangerous commands, enforce TDD, run formatters on save, log every tool call, etc. Hooks are how Claude Code automates "from now on always X."
priority: 3
applies_to_files: [.claude/settings.json, .claude/hooks]
---

# Claude Code hooks mastery

Claude Code hooks are shell commands the harness runs automatically on events (`PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`, `SessionStart`, …). They're how you turn "I keep telling Claude not to do X" into a hard rule.

Common hook patterns:

1. **PreToolUse `Bash`** — block dangerous commands (`rm -rf /`, `git push --force` to main)
2. **PostToolUse `Edit`** — auto-run formatter / linter
3. **PostToolUse `Write`** — sanity-check file headers
4. **Stop** — print a summary or play a sound
5. **SessionStart** — load project memory

## Quick start

1. Add `.claude/settings.json` with `hooks` section
2. Each hook is a shell command (executable) that gets event JSON on stdin
3. Exit non-zero from PreToolUse to BLOCK the action
4. Test hooks aggressively — a broken `PreToolUse` hook can lock you out of edits

Example:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/block-rm-rf.sh" }
    ],
    "PostToolUse": [
      { "matcher": "Edit", "command": "prettier --write \"$FILE\"" }
    ]
  }
}
```

## Notes

- Hooks run on the **harness**, not Claude. Memory/preferences cannot replace them.
- Keep hooks fast (under 1s); slow hooks block the agent.
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin-shipped hook scripts — it makes them portable.

## Source

- Upstream: https://github.com/disler/claude-code-hooks-mastery
- Fork: https://github.com/glowElephant/claude-code-hooks-mastery
