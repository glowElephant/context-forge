# GeekNews 포스트 — context-forge

Channel: https://news.hada.io
**Reddit 포스트 후 24~48시간 뒤 등록** (트래픽 분산 방지 + 댓글 피드백 반영)
타이밍: 평일 09~11시 또는 21~23시 (오전 트래픽 강함)

---

## 제목 (3안)

**A. 결과-노출형 (추천)**
> context-forge - 5분 디스커션으로 하니스 엔지니어된 GitHub 저장소 부트스트랩 (82 카탈로그 소스 · 주간 자동 sync · 월간 자동 발굴)

**B. 도구-노출형 (차분)**
> context-forge - Claude Code 슬래시 커맨드로 새 프로젝트의 CLAUDE.md/AGENTS.md/skills/spec 자동 셋업

**C. 질문형**
> 새 프로젝트마다 CLAUDE.md 다시 짜고 있나요? 디스커션 → 자동 부트스트랩 도구를 만들었습니다.

---

## URL 입력란

```
https://github.com/glowElephant/context-forge
```

---

## 본문

> 새 프로젝트 시작할 때마다 CLAUDE.md / AGENTS.md / skills 셋업 / MCP 서버 고르기 / spec 워크플로우 정하기를 매번 다시 하고 있었습니다.
> 코드 한 줄 짜기 전에 반나절씩 사라지는 패턴.
> 그래서 만들었습니다.

```
/context-forge
```

Claude Code 슬래시 커맨드. 6-Phase 가이드 흐름으로 새 GitHub 저장소를 하니스 엔지니어된 상태로 생성합니다.

### 흐름

1. **고정 질문 4개** — 프로젝트 타입 / 스택 / solo·팀 / 멀티에이전트 필요?
2. **자유 디스커션** (최대 8 질문) — 목표·마일스톤·제약·도메인 지식·회피사항
3. **카탈로그 매칭** — 큐레이션된 82 소스에서 본 프로젝트에 적용 가능한 entries 자동 선별
4. **저장소 정보** — 이름·public/private·로컬 경로
5. **실제 생성 + 채우기** — `gh repo create` → clone → catalog entries 복사 → `CLAUDE.md`/`AGENTS.md`/`README.md`/`docs/spec.md` Phase 2 답변으로 합성 → commit → push
6. **Hand-off** — `cd <new-repo> && claude`로 새 세션 시작

### 카탈로그가 살아있는 이유

오늘 부트스트랩한 프로젝트가 한 달 묵은 best practice를 받지 않도록 자동화 3종 운영:

- **주간 fork sync** (월 04:00 UTC) — 82개 소스 fork를 upstream과 fast-forward sync
- **월간 자동 발굴** (1일 04:00 UTC) — GitHub Search로 9 카테고리 키워드 그룹 검색 → `★≥2000`, `popularity+activity≥7`, 카테고리당 상위 5 → Issue로 체크리스트 triage
- **월간 borderline rescore + 분기 full rescore** — 5팩터 점수 (popularity·activity 자동, reviews·quality·trust 수동), 6개월 미커밋 자동 archive

모든 fork에 `context-forge-source` 토픽 부착 → GitHub UI에서 [한 줄 필터링](https://github.com/glowElephant?tab=repositories&q=topic%3Acontext-forge-source).

### 9 카테고리

| 카테고리 | 다루는 것 |
|---|---|
| claude-md | CLAUDE.md 패턴 (단일 vs sprawling, 솔로 vs 팀) |
| agents-md | AGENTS.md (IDE-agnostic, Cursor/Copilot/Codex 공통) |
| skills | Claude Code 스킬 프레임워크 (superpowers 등) |
| conventions | 코드/문서 컨벤션, context engineering |
| multi-agent | 서브에이전트 오케스트레이션, DAG 분해 |
| spec-driven | spec-kit, OpenSpec 등 SDD 워크플로우 |
| mcp | MCP 서버 부트스트랩 + 디스커버리 |
| prompts | 프롬프트 엔지니어링 기초 |
| boilerplate | 프로젝트 타입별 보일러플레이트 |

### 현재 상태 (정직)

v1.1.2 — MIT. 카탈로그 frontmatter 82/82 (수동 시드 15 + `scripts/seed_frontmatter.py` 자동 시드 67). 오늘 end-to-end **dogfood 검증** 완료 (버그 2건 발견·수정: 자동 시드 YAML quote 누설, Windows에서 `git branch -M main` 누락). **fresh Claude Code 세션에서 실제 사용자 1차 검증은 아직 안 됨** — 이 포스트도 그 piloting을 노립니다.

### 셋업

```bash
git clone https://github.com/glowElephant/context-forge ~/code/context-forge
export CONTEXT_FORGE_PATH=~/code/context-forge   # 또는 .claude/settings.json에 env 추가
```

Windows:
```powershell
[Environment]::SetEnvironmentVariable('CONTEXT_FORGE_PATH', 'C:\Git\context-forge', 'User')
```

Claude Code 세션에서:
```
/context-forge
```

### 링크

- Repo: https://github.com/glowElephant/context-forge
- 한국어 README: https://github.com/glowElephant/context-forge/blob/main/README.ko.md
- Release: https://github.com/glowElephant/context-forge/releases/tag/v1.1.0
- 카탈로그 82 소스 브라우즈: https://github.com/glowElephant?tab=repositories&q=topic%3Acontext-forge-source

### 피드백 받고 싶은 것

1. **9 카테고리 분류가 본인의 하니스 구성과 맞나요?** 빠진 카테고리는?
2. **수동으로 하니스 셋업해보신 적 있다면** — 가장 매번 잊어버리는 게 뭔지? context-forge가 정확히 그 "지난번에 빠뜨린 것"을 잡아내는 게 목표.
3. **실제 프로젝트 1개에 `/context-forge` 돌려보고 어디서 막혔는지 알려주실 분 환영** — Issue로 받습니다.

---

## 댓글 응대 메모

**"spec-kit / OpenSpec / superpowers와 뭐가 달라요?"**
> 그것들은 프레임워크/스킬 자체. context-forge는 그 위 레이어 — 본 프로젝트에 어떤 spec 시스템 + 어떤 스킬 프레임워크 + 어떤 MCP 조합이 맞을지 *고르고 부트스트랩하는* 도구. 카탈로그에 그 셋 모두 entries로 포함됨.

**"카탈로그에 정확히 뭐가 있죠?"**
> 82개의 upstream 하니스 know-how repos를 fork한 것. 각각 `catalog/<category>/<name>.md`에 frontmatter (`when_to_use`, `priority`, score) 보유. 슬래시 커맨드가 frontmatter 읽어서 본 프로젝트와 매칭.

**"코드 어디로 안 보내나요?"**
> 슬래시 커맨드는 `~/.claude/` 설정 메타데이터 + 본인 context-forge 클론의 `catalog/`만 읽음. 새 repo 생성은 `gh repo create`로 본인 계정에. 프로젝트 소스 코드 읽기·전송 0.

**"왜 fork? upstream 링크면 안 돼?"**
> 스냅샷 안정성 — upstream history rewrite 시 카탈로그 참조가 깨짐. 주간 자동 sync로 본인이 갱신 시점 통제. fast-forward만, divergence는 sync log에 표기.

**"카탈로그 매칭이 휴리스틱이던데 잘 골라주나요?"**
> 솔직히 1차 패스. 5팩터 rubric으로 `priority`·`domain`·`category-applicability` 우선순위. Phase 3가 *제안*하고 사용자가 confirm/remove. 더 똑똑하게 만들려면 사용자가 over-/under-recommend 케이스를 알려줘야.

**"Claude Code 외에 Cursor/Codex에선?"**
> 슬래시 커맨드 자체는 Claude Code 전용. 단, 출력물(`CLAUDE.md` + `AGENTS.md` + `.cursorrules` 패턴)은 multi-tool — 만들어진 프로젝트는 Cursor/Codex/Copilot에서도 동작. v1.5에서 Cursor 네이티브 wrapper 계획.

**"Claude Code도 아직 어색한데 굳이?"**
> 카탈로그 자체가 학습 자료로 쓰일 수 있음. `context-forge`로 부트스트랩 안 해도, 82 entries의 frontmatter `when_to_use`만 훑어도 "어떤 패턴이 어떤 상황에 맞는지" 학습 가능.

---

## 등록 직후 60분

- 차분히 응대. 비판 댓글 = 자료 (본문/README 보강 소재로 기록).
- 자추 금지. 다른 계정으로 댓글·추천 X (긱뉴스 룰).
- 본인 다른 프로젝트(harness-bench, Molten 등) 같은 thread에서 링크 X — 첫 인상이 광고로 박힘.

## 24h 후

- 댓글에서 잡힌 약점·FAQ → README 또는 SKILL.md 보강 PR
- 트래픽 좋으면 → Reddit r/ClaudeAI / Anthropic Discord #show-and-tell 다음 채널
- 결과 미지근하면 → Discussion 더 살리고 24~48h 뒤 다른 각도로 재시도
