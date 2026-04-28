# context-forge — 설계 문서 (v1)

작성일: 2026-04-28
상태: 디스커션 완료, 사용자 리뷰 대기

## 1. 목적

프로젝트 시작 전, AI 에이전트(Claude Code, Cursor, GPT 등)가 잘 작동하도록 컨텍스트/노하우/규약/스킬을 미리 셋업해주는 자동화 시스템. 사용자가 디스커션을 거치면 Claude가 카탈로그된 노하우 중 적합한 것을 골라 새 GitHub 저장소에 통합 셋업한다.

별명: **오토 하네스 엔지니어링.**

## 2. 시스템 구성

```
┌─────────────────────────────────────────────────┐
│  [포크 저장소들]  glowElephant/<fork>            │
│   - awesome-design-md, gstack 등                 │
│   - 정기 검색 잡으로 추가됨                      │
└──────────────────┬──────────────────────────────┘
                   │ 카탈로그
                   ▼
┌─────────────────────────────────────────────────┐
│  [메타 저장소]  glowElephant/context-forge       │
│   ├── catalog/                                   │
│   │   ├── skills/                                │
│   │   ├── conventions/                           │
│   │   ├── multi-agent/                           │
│   │   ├── claude-md/                             │
│   │   ├── prompts/                               │
│   │   └── boilerplate/                           │
│   ├── sources/                                   │
│   │   └── index.json     (포크 저장소 목록)      │
│   ├── docs/                                      │
│   │   ├── specs/                                 │
│   │   ├── contributing.md                        │
│   │   └── scoring.md                             │
│   ├── .claude/skills/context-forge/SKILL.md      │
│   └── README.md                                  │
└──────────────────┬──────────────────────────────┘
                   │ /context-forge 호출
                   ▼
┌─────────────────────────────────────────────────┐
│  [디스커션] (D + C 무드)                         │
│   1. 짧은 고정 질문 (타입/스택/팀/멀티에이전트)  │
│   2. 자유 디스커션 (목표/제약/성공 기준)         │
│   3. Claude 카탈로그 매칭 → 사용자 컨펌          │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  [하네스된 신규 저장소]  user/<project-name>     │
│   ├── CLAUDE.md / AGENTS.md                      │
│   ├── README.md (프로젝트 소개)                  │
│   ├── docs/                                      │
│   │   ├── spec.md (목표/마일스톤)                │
│   │   └── know-how/ (선택된 노하우 .md들)        │
│   ├── .claude/                                   │
│   │   ├── skills/                                │
│   │   ├── rules/                                 │
│   │   └── agents/                                │
│   ├── .gitignore, LICENSE, (옵션) CI            │
└─────────────────────────────────────────────────┘
```

## 3. 카탈로그 항목 구조

스킬 시스템과 동일한 패턴 (폴더 + frontmatter).

```yaml
---
name: tdd-workflow
category: conventions
domain: [web, game-engine, general]
tags: [testing, methodology]
source: https://github.com/glowElephant/awesome-design-md/blob/main/tdd.md
upstream: https://github.com/VoltAgent/awesome-design-md
when_to_use: 테스트 우선 개발이 가능한 프로젝트. Unity는 EditMode 한정.
priority: 3   # 같은 이름 충돌 시 우선순위
---
(본문...)
```

## 4. 디스커션 흐름

1. **고정 질문 (3~4개)**
   - 프로젝트 타입? (web / unity / unreal / mobile / cli / library / mcp / 기타)
   - 주 언어/프레임워크?
   - 혼자 / 팀?
   - 멀티에이전트 셋업?
2. **자유 디스커션** — superpowers:brainstorming 패턴, 한 번에 한 질문
   - 목표, 제약, 성공 기준, 도메인 지식 파악
3. **카탈로그 매칭**
   - Claude가 카탈로그 frontmatter 다 읽고 후보 리스트업
   - 사용자에게 "이거이거 넣을게요" 제시 → 빼고 싶은 거 컨펌
4. **저장소 정보 수집**
   - 저장소 이름, public/private, 로컬 경로

## 5. 실행 시퀀스

```
1. /context-forge 입력
2. 메타 저장소 카탈로그 로드 (clone or pull)
3. 디스커션
4. 카탈로그 매칭 + 사용자 컨펌
5. 저장소 정보 수집
6. gh repo create <user>/<name> --private --clone
7. 파일 채우기:
   - 카탈로그 항목 복사 (frontmatter 유지, source URL 박힘)
   - CLAUDE.md / AGENTS.md / README.md / docs/spec.md 디스커션 기반 합성
8. git add . && commit && push
9. (옵션) 보일러플레이트, GitHub Issues 생성
10. 완료 메시지 + 다음 세션 진입 안내
```

## 6. 파일 충돌/머지 정책

- **CLAUDE.md / AGENTS.md / README.md** — 디스커션 기반 새로 작성. 카탈로그 그대로 복사 X.
- **`.claude/skills/`, `.claude/agents/`, `.claude/rules/`** — 항목별 별개 파일. 같은 이름이면 frontmatter `priority`로 결정.
- **`docs/know-how/`** — 노하우 .md 그대로 복사. 파일명 충돌 시 `<category>-<name>.md` prefix.
- **보일러플레이트** — 프로젝트 타입에서 1개만 선택 (충돌 차단).

## 7. 결과물 산출물 (v1 기본 + 옵션)

**기본**:
- `CLAUDE.md` / `AGENTS.md`
- `README.md`
- `docs/spec.md`
- `docs/know-how/` (선택된 노하우들)
- `.claude/skills/`, `.claude/rules/`, `.claude/agents/`
- `.gitignore`, `LICENSE`

**옵션 (디스커션에서 묻기)**:
- 보일러플레이트 (프로젝트 타입별 — package.json, tsconfig, ProjectSettings 등)
- GitHub Issues 자동 생성 (마일스톤별)
- CI 설정

## 8. 포크 저장소 발굴 정책

### 8.1 다요소 스코어링

각 후보 저장소를 5개 요소로 평가 (각 1~5점):

| 요소 | 평가 기준 |
|------|-----------|
| 인기도 | 스타 수, 포크 수 |
| 활성도 | 최근 커밋(6개월), 이슈/PR 활동 |
| 실용 후기 | 블로그/Reddit/HN 언급, awesome list 등재 |
| 콘텐츠 품질 | 실제 .md 내용 깊이, 단순 링크 모음 X |
| 유지보수자 신뢰도 | 개인/조직, 다른 평판 |

### 8.2 티어 분류

- **Tier 1 (자동 포크)**: 합산 20점 이상 OR ⭐ 1000+ AND 명확히 관련
- **Tier 2 (큐레이션 검토)**: 합산 13~19점, 사용자 컨펌 후 포크
- **Tier 3 (제외)**: 합산 12점 이하

### 8.3 분야별 분류

`domain` 태그로 카테고리화:
- `web` — 프론트/백/풀스택
- `game-engine` — Unity, Unreal, Godot
- `mobile` — iOS, Android, 태블릿
- `ai-agent` — Claude/Cursor rules, prompts
- `general-dev` — 언어 무관
- `backend/infra` — DevOps, k8s, MCP
- `design` — UI/UX, design system
- `documentation` — 작성 가이드

### 8.4 정기 업데이트

- **주기**: 분기 1회 (3개월)
- **방법**: `schedule` 스킬로 크론 잡 등록 → 서브에이전트가 신규 저장소 발굴 → `sources/index.json`에 후보 추가 → 사용자 PR 리뷰 후 머지
- **자동 포크 조건**: Tier 1만 자동, Tier 2는 PR로 사용자 컨펌

### 8.5 커뮤니티 기여 채널

- **GitHub Discussions** — "내 저장소도 추가해주세요" 카테고리
- **PR** — `sources/index.json` 직접 추가 PR 환영
- **검토 기준**: `docs/scoring.md`에 명시

## 9. 메타 저장소 부트스트랩 (시드)

v1 시작 시점 시드 후보:
- VoltAgent/awesome-design-md (Tier 1 확정)
- garrytan/gstack (Tier 1 확정)
- 추가 후보 — 서브에이전트 발굴 결과로 채워짐 (별첨)

## 10. v1 스코프 vs 후속

**v1 (포함):**
- `/context-forge` 슬래시 커맨드 + 디스커션
- 카탈로그 매칭 + 사용자 컨펌
- GitHub repo 생성 + 파일 채우기 + 푸시
- 파일 단순 복사 (frontmatter source URL)
- 보일러플레이트 (프로젝트 타입별)
- 분기 1회 정기 발굴 잡

**v2 이후:**
- GitHub Issues 자동 생성 (v1은 `docs/spec.md`에 마일스톤만)
- 메타 저장소 업데이트 → 기존 하네스된 repo sync 명령
- 카탈로그 추천 학습 (자주 쓰이는 조합 분석)
- 다른 에이전트 도구(Cursor, Copilot) 직접 지원

## 11. 열린 이슈 / 후속 결정

- 카탈로그 매칭 알고리즘 세부 (단순 frontmatter 매칭? 임베딩 검색?)
- 정기 발굴 잡 실행 환경 (로컬 / GitHub Actions / 외부)
- 사용자 GitHub 인증 (`gh` CLI 의존)

## 12. 별첨

- 별첨 A: 포크 후보 저장소 리스트 — 서브에이전트 결과로 채워짐 (별도 파일: `docs/specs/2026-04-28-fork-candidates.md`)
