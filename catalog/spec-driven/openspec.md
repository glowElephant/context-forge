---
name: openspec
category: spec-driven
domain: [general]
tags: [sdd, open-source, cli]
source: https://github.com/glowElephant/OpenSpec
upstream: https://github.com/Fission-AI/OpenSpec
when_to_use: Spec-driven projects that prefer an open-source, CLI-first tool over GitHub-tied workflows. Good fit for self-hosted Git, GitLab, or teams that want spec linting and validation locally.
priority: 4
---

# OpenSpec — open-source spec-driven CLI

`OpenSpec` is a CLI tool for spec-driven development that doesn't depend on GitHub. It treats the spec as a first-class artifact with linting, schema validation, and traceability hooks.

Differences from `spec-kit`:

- **CLI-first.** Spec validation runs locally and in CI, not just on GitHub.
- **Spec schema.** Specs follow a defined schema (sections, required fields, link types) that the CLI validates.
- **Traceability links.** Specs explicitly reference plans/PRs/issues; the CLI walks the graph.

## Quick start

```bash
# install
npm i -g openspec    # or pnpm/yarn

# init in a repo
openspec init

# validate all specs
openspec validate

# show the trace from spec to PRs
openspec trace docs/specs/2026-04-28-feature.md
```

## Notes

- OpenSpec's schema is opinionated — adopt early or you'll spend time migrating.
- Works well alongside `superpowers:writing-plans` (the plan format is compatible).
- For teams already on GitHub Issues, `spec-kit` is usually less friction.

## Source

- Upstream: https://github.com/Fission-AI/OpenSpec
- Fork: https://github.com/glowElephant/OpenSpec
