# context-forge

> **Auto harness engineering for AI coding agents.**
> Discuss your project, curate battle-tested know-how, and bootstrap a fully context-engineered repository — for Claude Code, Cursor, Copilot, and beyond.

[🇰🇷 한국어](./README.ko.md) · [Catalog](./catalog) · [Discussions](https://github.com/glowElephant/context-forge/discussions) · [Contributing](./docs/contributing.md)

---

## What is context-forge?

**context-forge** is a meta repository that turns scattered AI-agent know-how — `CLAUDE.md` patterns, `AGENTS.md` standards, `.cursorrules`, agent skills, MCP servers, spec-driven workflows, prompt libraries, and convention guides — into a **single curated catalog** that you can apply to a brand-new project in one go.

You describe what you're building (web app, Unity game, MCP server, CLI tool…) through a guided discussion. context-forge picks the matching know-how from the catalog, creates a new GitHub repository, and writes everything in: `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/spec.md`, `.claude/skills/`, `.claude/agents/`, `.claude/rules/`, boilerplate, and more.

Think of it as **`create-react-app` for AI-augmented codebases** — except instead of a fixed template, it's a living catalog crowd-curated from the best agentic-engineering repos on GitHub.

## Why?

The current state of AI coding agents (Claude Code, Cursor, Copilot, Codex, Aider, Windsurf, …) demands serious context engineering before useful work begins. Every project re-solves the same boilerplate:

- Which `CLAUDE.md` patterns apply here?
- Which skills / subagents / hooks should be installed?
- Which spec-driven workflow fits this team?
- Which MCP servers do we need?
- Which language conventions, code-review checklists, commit standards?

context-forge collapses that hours-long ritual into a guided 5-minute conversation. Then you `cd` into the new repo and start coding.

## How it works

```
[Forked know-how repos]                glowElephant/<fork>...
        ↓
[Catalog]   ───────►   /context-forge slash command
        ↓                  │
[Discussion]               │ Brief fixed questions
        ↓                  │ Free-form goal/constraint chat
[Match + Confirm]   ◄──────┘
        ↓
[gh repo create user/<project>]   →   New harness-engineered repo
                                        ├── CLAUDE.md / AGENTS.md
                                        ├── README.md
                                        ├── docs/spec.md
                                        ├── docs/know-how/
                                        ├── .claude/skills,agents,rules/
                                        └── boilerplate
```

## Catalog scope (v1)

The v1 catalog is intentionally **narrow** — focused on the AI-agent harness itself:

| Category | Examples |
|----------|----------|
| Claude Code core | `anthropics/skills`, `obra/superpowers`, `garrytan/gstack` |
| Cursor / Copilot rules | `PatrickJS/awesome-cursorrules`, `github/awesome-copilot` |
| Spec-driven development | `github/spec-kit`, `Fission-AI/OpenSpec` |
| Multi-agent orchestration | `wshobson/agents`, `ruvnet/ruflo` |
| MCP infrastructure | `modelcontextprotocol/servers`, `punkpeye/awesome-mcp-servers` |
| Standards | `agentsmd/agents.md`, `google-labs-code/design.md` |
| Prompt engineering | `dair-ai/Prompt-Engineering-Guide`, `f/prompts.chat` |

v2 will broaden to domain conventions (game engines, mobile, web, backend, ML, security, documentation). See [`docs/specs/2026-04-28-fork-candidates.md`](./docs/specs/2026-04-28-fork-candidates.md) for the full curated list.

## Status

🚧 **Active development.** Design phase complete.

- [x] Design specification
- [x] Candidate repositories curated (69 v1 + 210 v2)
- [ ] Forking the v1 catalog sources
- [ ] `/context-forge` slash command implementation
- [ ] Catalog frontmatter authoring
- [ ] Quarterly auto-discovery job

Track progress in [`docs/specs/`](./docs/specs).

## Quick start

> ⏳ Implementation in progress. Once shipped:

```bash
# In any directory, run:
/context-forge

# Answer a few questions about your project.
# context-forge will:
#  1. Match catalog know-how to your stack and goals
#  2. Create a new GitHub repository
#  3. Populate it with curated CLAUDE.md, skills, rules, docs
#  4. cd into it and start coding
```

## Contributing

context-forge is a **community catalog**. Add your favorite repository or your own:

- 💬 **GitHub Discussions** — propose a source repo to fork ([open a discussion](https://github.com/glowElephant/context-forge/discussions))
- 🛠 **Pull request** — directly add an entry to `sources/index.json`
- 📋 **Scoring rubric** — see [`docs/scoring.md`](./docs/scoring.md)

All sources are evaluated on **popularity, activity, real-world reviews, content quality, and maintainer reliability** before promotion to Tier 1 (auto-fork).

## Why "harness engineering"?

The agentic coding community has converged on the term **harness** for the layer that wraps an AI model — system prompt, tools, memory, hooks, context. **Harness engineering** is the discipline of designing that layer well. context-forge is the meta tool that does this for you, automatically, before you write a single line of code.

## Related work

context-forge stands on the shoulders of these projects:

- [obra/superpowers](https://github.com/obra/superpowers) — agentic skills framework
- [garrytan/gstack](https://github.com/garrytan/gstack) — Claude Code 23-tool stack
- [github/spec-kit](https://github.com/github/spec-kit) — spec-driven development
- [agentsmd/agents.md](https://github.com/agentsmd/agents.md) — `AGENTS.md` open standard
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro) — context engineering primer

## License

MIT © glowElephant

---

**Keywords**: claude code · claude skills · agent skills · cursor rules · copilot instructions · agents.md · claude.md · context engineering · spec-driven development · mcp servers · harness engineering · agentic coding · ai coding assistant · prompt engineering · meta repository · auto bootstrap
