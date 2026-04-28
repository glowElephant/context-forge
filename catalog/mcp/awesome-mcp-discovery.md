---
name: awesome-mcp-discovery
category: mcp
domain: [general]
tags: [mcp, catalog, discovery]
source: https://github.com/glowElephant/awesome-mcp-servers
upstream: https://github.com/punkpeye/awesome-mcp-servers
when_to_use: When choosing which MCP servers to install for a given stack. Use this as the discovery checklist; for canonical implementations of common services, defer to the official `modelcontextprotocol/servers` repo.
priority: 4
---

# Awesome MCP servers — discovery catalog

`punkpeye/awesome-mcp-servers` is the community-maintained catalog of MCP server implementations (official + third-party). Use it to find an MCP server for a less-common service before writing one yourself.

The catalog organizes servers by:

- **Category** (database, browser, file system, AI/ML, productivity, communication, finance, …)
- **Status** (official / community / experimental)
- **Auth** (none / token / OAuth)
- **Transport** (stdio / SSE / HTTP)

## Quick start

When bootstrapping a project:

1. List the external services your agent must reach
2. Search the catalog for each — prefer "official" tier when available
3. Add chosen servers to `.mcp.json`
4. For services with no MCP server, decide: write one (effort) or skip the integration (scope cut)

## Notes

- Community servers vary in maintenance — pin to a specific release.
- Some "experimental" servers are excellent in practice; check star/issue/PR activity before judging.
- For Korean/Chinese ecosystem servers, also check `yzfly/Awesome-MCP-ZH`.

## Source

- Upstream: https://github.com/punkpeye/awesome-mcp-servers
- Fork: https://github.com/glowElephant/awesome-mcp-servers
