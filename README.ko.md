# context-forge

> **AI 코딩 에이전트를 위한 오토 하네스 엔지니어링.**
> 프로젝트를 디스커션하고, 검증된 노하우를 큐레이션하고, 컨텍스트 엔지니어링이 완료된 저장소를 한 번에 생성하세요 — Claude Code, Cursor, Copilot 등 모든 AI 에이전트용.

[🇺🇸 English](./README.md) · [카탈로그](./catalog) · [Discussions](https://github.com/glowElephant/context-forge/discussions) · [기여 가이드](./docs/contributing.md)

---

## context-forge가 뭔가요?

**context-forge**는 흩어져 있는 AI 에이전트 노하우를 — `CLAUDE.md` 패턴, `AGENTS.md` 표준, `.cursorrules`, 에이전트 스킬, MCP 서버, 스펙 드리븐 워크플로우, 프롬프트 라이브러리, 컨벤션 가이드 — **하나의 큐레이션된 카탈로그**로 모아 새 프로젝트에 한 번에 적용해주는 메타 저장소입니다.

당신이 만들 프로젝트(웹 앱, Unity 게임, MCP 서버, CLI 도구…)를 가이드된 디스커션으로 설명하면, context-forge가 카탈로그에서 매칭되는 노하우를 골라 새 GitHub 저장소를 생성하고 모든 셋업을 자동으로 채워 넣습니다: `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/spec.md`, `.claude/skills/`, `.claude/agents/`, `.claude/rules/`, 보일러플레이트까지.

**AI 시대의 `create-react-app`** 이라고 보시면 됩니다 — 다만 고정 템플릿이 아니라, GitHub 최고의 에이전틱 엔지니어링 저장소들로부터 커뮤니티가 함께 큐레이션하는 살아있는 카탈로그입니다.

## 왜 필요한가요?

요즘 AI 코딩 에이전트(Claude Code, Cursor, Copilot, Codex, Aider, Windsurf …)를 제대로 쓰려면 본격적인 작업 전에 **컨텍스트 엔지니어링**이 필수입니다. 그런데 모든 프로젝트가 똑같은 보일러플레이트를 매번 다시 만들고 있습니다:

- 이 프로젝트엔 어떤 `CLAUDE.md` 패턴이 맞을까?
- 어떤 스킬/서브에이전트/훅을 깔아야 하지?
- 어떤 스펙 드리븐 워크플로우가 우리 팀에 맞을까?
- 어떤 MCP 서버가 필요할까?
- 언어별 컨벤션, 코드 리뷰 체크리스트, 커밋 규약은?

context-forge는 이 몇 시간짜리 의식을 **5분 가이드 대화**로 압축합니다. 그 다음엔 새 저장소로 `cd`해서 바로 코딩 시작.

## 작동 방식

```
[포크된 노하우 저장소들]                glowElephant/<fork>...
        ↓
[카탈로그]   ───────►   /context-forge 슬래시 커맨드
        ↓                  │
[디스커션]                  │ 짧은 고정 질문
        ↓                  │ 자유로운 목표/제약 대화
[매칭 + 컨펌]   ◄──────────┘
        ↓
[gh repo create user/<project>]   →   하네스 엔지니어링된 새 저장소
                                        ├── CLAUDE.md / AGENTS.md
                                        ├── README.md
                                        ├── docs/spec.md
                                        ├── docs/know-how/
                                        ├── .claude/skills,agents,rules/
                                        └── 보일러플레이트
```

## 카탈로그 범위 (v1)

v1 카탈로그는 의도적으로 **좁게** 가져갑니다 — AI 에이전트 하네스 그 자체에 집중:

| 카테고리 | 예시 |
|----------|------|
| Claude Code 코어 | `anthropics/skills`, `obra/superpowers`, `garrytan/gstack` |
| Cursor / Copilot 룰 | `PatrickJS/awesome-cursorrules`, `github/awesome-copilot` |
| 스펙 드리븐 개발 | `github/spec-kit`, `Fission-AI/OpenSpec` |
| 멀티에이전트 오케스트레이션 | `wshobson/agents`, `ruvnet/ruflo` |
| MCP 인프라 | `modelcontextprotocol/servers`, `punkpeye/awesome-mcp-servers` |
| 표준 | `agentsmd/agents.md`, `google-labs-code/design.md` |
| 프롬프트 엔지니어링 | `dair-ai/Prompt-Engineering-Guide`, `f/prompts.chat` |

v2에서는 도메인별 컨벤션(게임 엔진, 모바일, 웹, 백엔드, ML, 보안, 문서)으로 넓힐 예정. 전체 큐레이션 리스트는 [`docs/specs/2026-04-28-fork-candidates.md`](./docs/specs/2026-04-28-fork-candidates.md) 참고.

## 진행 상태

🚧 **개발 중.** 설계 단계 완료.

- [x] 설계 명세
- [x] 후보 저장소 큐레이션 완료 (v1 69개 + v2 210개)
- [ ] v1 카탈로그 소스 포크
- [ ] `/context-forge` 슬래시 커맨드 구현
- [ ] 카탈로그 frontmatter 작성
- [ ] 분기별 자동 발굴 잡

진행 추적: [`docs/specs/`](./docs/specs)

## 빠른 시작

> ⏳ 구현 진행 중. 출시되면:

```bash
# 어느 디렉토리에서든:
/context-forge

# 프로젝트 관련 몇 가지 질문에 답하세요.
# context-forge가 자동으로:
#  1. 당신의 스택과 목표에 카탈로그 노하우 매칭
#  2. 새 GitHub 저장소 생성
#  3. 큐레이션된 CLAUDE.md, 스킬, 룰, 문서 자동 생성
#  4. cd하여 바로 코딩 시작
```

## 기여하기

context-forge는 **커뮤니티 카탈로그**입니다. 좋아하는 저장소나 본인의 저장소를 추가해주세요:

- 💬 **GitHub Discussions** — 포크할 소스 저장소 제안 ([디스커션 열기](https://github.com/glowElephant/context-forge/discussions))
- 🛠 **Pull Request** — `sources/index.json`에 직접 항목 추가
- 📋 **스코어링 규칙** — [`docs/scoring.md`](./docs/scoring.md) 참고

모든 소스는 **인기도, 활성도, 실제 후기, 콘텐츠 품질, 유지보수자 신뢰도** 기준으로 평가 후 Tier 1 (자동 포크) 승격됩니다.

## 왜 "하네스 엔지니어링"인가요?

에이전틱 코딩 커뮤니티는 AI 모델을 감싸는 레이어 — 시스템 프롬프트, 도구, 메모리, 훅, 컨텍스트 — 를 **하네스(harness)** 라고 부르는 데 합의했습니다. **하네스 엔지니어링**은 그 레이어를 잘 설계하는 분야예요. context-forge는 그 작업을 코드 한 줄 쓰기 전에 자동으로 해주는 메타 도구입니다.

## 관련 프로젝트

context-forge는 다음 프로젝트들의 어깨 위에 서 있습니다:

- [obra/superpowers](https://github.com/obra/superpowers) — 에이전틱 스킬 프레임워크
- [garrytan/gstack](https://github.com/garrytan/gstack) — Claude Code 23-tool 스택
- [github/spec-kit](https://github.com/github/spec-kit) — 스펙 드리븐 개발
- [agentsmd/agents.md](https://github.com/agentsmd/agents.md) — `AGENTS.md` 오픈 표준
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro) — 컨텍스트 엔지니어링 입문

## 라이선스

MIT © glowElephant

---

**키워드**: claude code · claude skills · agent skills · cursor rules · copilot instructions · agents.md · claude.md · context engineering · spec-driven development · mcp servers · harness engineering · agentic coding · ai coding assistant · prompt engineering · meta repository · auto bootstrap · 하네스 엔지니어링 · 컨텍스트 엔지니어링 · AI 코딩 에이전트
