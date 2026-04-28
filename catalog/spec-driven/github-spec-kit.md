---
name: github-spec-kit
category: spec-driven
domain: [general]
tags: [sdd, spec-driven, github]
source: https://github.com/glowElephant/spec-kit
upstream: https://github.com/github/spec-kit
when_to_use: Teams adopting spec-driven development with GitHub-native tooling (Issues, Projects, PRs). Especially good when leadership wants traceability from spec → PR.
priority: 5
---

# GitHub spec-kit — spec-driven development

`spec-kit` is GitHub's official toolkit for spec-driven development. The model:

1. **Spec first.** A short markdown spec lives in the repo (`docs/specs/...`) before any code.
2. **Plan derived from spec.** A separate plan document breaks the spec into bite-sized tasks.
3. **Code derived from plan.** The agent executes plan tasks, each ending with a commit.
4. **Review against spec.** PR description references the spec; reviewer can compare delta to spec.

## Quick start

In a new repo:

1. Create `docs/specs/` and `docs/plans/` directories
2. Write a 1–2 page spec for the first feature
3. Generate a plan from the spec (use `superpowers:writing-plans` or spec-kit's CLI)
4. Open issues mirroring plan tasks; link spec from each issue
5. PRs reference both the spec and the issue

## Notes

- spec-kit pairs especially well with `superpowers:brainstorming` (which already produces a spec doc).
- The "plan" stage is the critical correction point — if the plan deviates from the spec, fix the spec first.
- Avoid retrofitting specs to match shipped code; that defeats the purpose.

## Source

- Upstream: https://github.com/github/spec-kit
- Fork: https://github.com/glowElephant/spec-kit
