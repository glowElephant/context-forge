---
name: mcp-server-bootstrap
category: mcp
domain: [general]
tags: [mcp, integration, official]
source: https://github.com/glowElephant/servers
upstream: https://github.com/modelcontextprotocol/servers
when_to_use: Any project that will integrate at least one MCP server. The official Anthropic-maintained collection is the safest starting point — file system, GitHub, Postgres, Slack, etc.
priority: 5
---

# MCP server bootstrap (official)

`modelcontextprotocol/servers` is the official Anthropic-maintained collection of MCP server reference implementations. Use it as the starting point for any agent that needs structured access to external services.

Servers in the collection cover:

- **filesystem** — sandboxed file access
- **github** — repos, issues, PRs
- **postgres** / **sqlite** — read-only DB access
- **fetch** — HTTP client
- **memory** — long-term memory store
- **slack** — channels, messages
- **time**, **search**, and others

## Quick start

In your project's `.mcp.json` or equivalent:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

Pick MCP servers based on which external systems your agent must reach. Each server adds tools to the agent's tool set, which costs context — be selective.

## Notes

- MCP servers run as separate processes. Logs and crashes are easy to miss; wire them to your dev workflow.
- Use `${CLAUDE_PLUGIN_ROOT}` (or equivalent) for plugin-based MCP configs to keep paths portable.
- For exotic services (e.g., a vector DB or a SaaS API), check `punkpeye/awesome-mcp-servers` first; if nothing fits, write a custom one.

## Source

- Upstream: https://github.com/modelcontextprotocol/servers
- Fork: https://github.com/glowElephant/servers
