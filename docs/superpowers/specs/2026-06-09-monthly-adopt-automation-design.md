# 월간 후보 채택(adopt) 자동화 설계

- 날짜: 2026-06-09
- 트리거: 이슈 #5 (월간 신규 후보 31건, 2026-06)
- 상태: 설계 승인됨, 구현 대기

## 1. 배경과 문제

`automation.py discover` + `monthly-rediscovery.yml`는 매월 GitHub Search로 신규 후보를 긁어 이슈 체크리스트를 만든다. 이 부분은 완전 자동이다.

그러나 **채택(adopt)은 수동**이다. 사람이 직접 ① glowElephant로 fork 생성, ② `sources/index.json` 1줄 등록을 해야 하고, 그 뒤(토픽 부착, frontmatter, 점수, README 재생성)는 기존 스크립트가 자동 처리한다.

이슈 #5의 31건을 실제로 검증해보니 두 가지 문제가 드러났다:

1. **discover가 scope 밖 후보를 다수 끌어온다.** 카테고리 키워드 매칭만으로 긁어서, 이미지 생성 프롬프트(`nano banana`, `gpt-image`), 일반 프레임워크(`zeromicro/go-zero`), 제품/앱(`anything-llm`, `career-ops`)이 섞인다. 무지성 전체 fork하면 카탈로그 품질이 망가진다.
2. **discover의 중복 탐지가 upstream URL만 비교한다.** org-전송/미러된 repo를 신규로 오탐한다. 이번에 `multica-ai/andrej-karpathy-skills`(= 기등록 `forrestchang/andrej-karpathy-skills`), `open-multi-agent/open-multi-agent`(= 기등록 `JackChen-me/open-multi-agent`) 2건이 여기 걸렸다(★/desc/push 완전 일치).

## 2. 목표

- `automation.py adopt` 서브커맨드를 추가해 채택의 수동 게이트(fork + index 등록)를 자동화한다.
- **"저장소의 성격에 맞게"** 채택하도록 룰 기반 scope 가드를 넣는다. 명백한 오탐은 자동 거부, 애매하면 사람 최종확인.
- discover의 중복(미러/org-전송) 탐지를 보강한다.
- 이번 이슈 #5의 31건을 이 도구로 처리한다(채택 12 / 제외 19).

## 3. 정책 결정

- **채택 철학**: 사람이 선별하고 adopt가 실행하되, 룰 기반 scope 가드로 명백한 오탐을 사전 차단한다(완전 LLM 무인화는 하지 않음 — 오판 시 불필요 fork + 카탈로그 오염 위험).
- **scope 경계**: **범용 하네스만 채택, 제품성/도메인특화는 제외**한다. CLAUDE.md/서브에이전트/스킬 *형식*이 맞아도 특정 업무 자동화 "제품"(광고 감사 `claude-ads`, 구직 시스템 `career-ops`, 보안 에이전트 `raptor`, 데스크탑 앱 `golutra`)은 제외한다. 어떤 프로젝트에도 이식 가능한 범용 패턴만 받는다.

## 4. 설계

### 4.1 `automation.py adopt` 서브커맨드

```
adopt <owner/repo> --category <cat> [--name <n>] [--notes "..."] [--force]
```

내부 시퀀스(멱등 — 이미 등록된 upstream이면 skip):

1. **scope 가드 검사**(§4.2) → BLOCK이면 사유 출력 후 중단(`--force`로만 우회), WARN이면 `--force` 없을 때 중단.
2. `gh repo fork <owner/repo> --org glowElephant` → fork 생성. 이름 충돌 시 `-N` suffix 자동 부여, 실제 fork URL 회수.
3. `context-forge-source` 토픽 PUT (`sync-forks.sh:57-62` 로직 이식 — `gh api -X PUT repos/<fork>/topics`).
4. `sources/index.json`에 엔트리 append: `upstream / fork / name / category / tier:1 / added_at:today / notes`.
5. `seed_frontmatter.seed_one(name)` 호출 → `catalog/<cat>/<name>.md` 생성(기존 함수 재사용).
6. 점수 계산: `auto_score()` + `compute_total_and_tier()` 호출 → frontmatter score 블록(pop/act 자동 + total/tier) 채움(기존 함수 재사용).
7. `validate-catalog.sh` → 통과 못 하면 롤백 안내.
8. `render-index` → `catalog/<cat>/README.md` 재생성(기존 함수 재사용).

**신규로 짜는 코드는 1·2·4번(가드, fork+suffix, index append)뿐.** 나머지는 기존 함수 조합.

### 4.2 scope 가드 (룰 기반, discover·adopt 공용)

입력: `gh repo view`의 `description` + `repositoryTopics` + `primaryLanguage`.

판정 3단계:

- **BLOCK**(자동 거부): 명백한 scope 밖. → 거부 + denylist 후보로 출력.
  - 이미지 생성: `nano banana`, `gpt-image`, `text-to-image`, `diffusion`, `image generation`
  - 제품/앱: `desktop app`, `local-first … app`, `job search`, `ad … audit/optimization`
  - 일반 프레임워크: `microservice`, `web framework`, `cloud-native`
- **WARN**(`--force` 필요, 사람 최종확인): 명백한 오탐은 아니지만 사람이 확정해야 함.
  - 범용 신호(`CLAUDE.md`/`AGENTS.md`/`cursor`/`copilot`/`mcp`/`skill`/`subagent`/`spec`/`prompt`/`context engineering`)가 **하나도 없음**
  - 또는 도메인 업무 키워드 탐지(보안/광고/구직 등 특정 도메인 + skill/agent)
- **PASS**: 범용 신호 ≥1 + BLOCK 키워드 없음 + category 정합 → 자동 진행.

**category 정합성**: `--category`가 9개 enum(claude-md, agents-md, skills, conventions, multi-agent, prompts, spec-driven, mcp, boilerplate) 중 하나이고 `catalog/<cat>/` 디렉토리가 존재하는지 선검사(validate가 잡기 전에 — go-zero가 spec-driven으로 새던 오분류 차단).

**룰 데이터 위치**: 키워드 패턴은 `automation.py` 상수로 시작. 유지보수가 늘면 `_status/scope-rules.json`으로 분리(YAGNI — 지금은 상수).

### 4.3 중복/미러 검사 (discover·adopt 공용 보강)

현재 discover는 `known_upstreams`(upstream URL 집합)로만 dedup한다. 보강:

- upstream URL 일치 → 중복(기존)
- **추가**: 기존 index 엔트리와 `repo basename(이름의 마지막 segment)` 일치 **AND** `(stargazerCount, pushedAt)` 동일 → 미러/org-전송으로 판정해 차단.

adopt도 같은 검사를 진입 시 수행한다.

### 4.4 denylist

- 파일: `_status/denylist.json` — `{ url, reason, decided_at }` 엔트리 배열.
- discover가 후보 필터링 시 denylist의 url을 제외한다(다음 달 재발굴 방지).
- 제외 사유 분류: `duplicate-mirror` / `out-of-scope` / `product-not-pattern`.

## 5. 이번 31건 처리 분류

### 채택 확정 12건

| category | repos |
|---|---|
| claude-md | my-claude-code-setup, claude-token-efficient |
| mcp | playwright-mcp, github-mcp-server, mcp-toolbox |
| multi-agent | awesome-codex-subagents |
| prompts | Awesome-Context-Engineering |
| skills | graphify, Understand-Anything, awesome-openclaw-skills |
| spec-driven | gsd-core, agent-os |

### 제외 19건 (denylist 등록)

- **duplicate-mirror (2)**: multica-ai/andrej-karpathy-skills, open-multi-agent/open-multi-agent
- **product-not-pattern (7)**: claude-ads, career-ops, raptor, golutra, activepieces, Backlog.md, SkillOpt
- **out-of-scope (10)**: anything-llm, open-design, agency-swarm, solace-agent-mesh, EvoLink awesome-gpt-image-2, awesome-nano-banana-pro-prompts, awesome-nanobanana-pro, go-zero, three-vue-tres, ai-boost/awesome-prompts

> 주: `name` 식별자와 `category` 재분류는 adopt 실행 시 candidates.json 기준으로 확정하되, 이슈에 적힌 category가 틀린 경우(go-zero=spec-driven 등) 교정한다. 채택 12건은 모두 category 정합.

## 6. 실행 + 이슈 마감 절차

1. adopt 구현 + 가드/중복검사/denylist 추가 → 채택 1건으로 dry-run, `validate-catalog.sh` 통과 확인.
2. **채택 12건 일괄 adopt** (실행 직전 최종 목록 사용자 재확인 — fork는 외부 상태 변경이라 되돌리기 번거로움).
3. 제외 19건 → `_status/denylist.json` 등록.
4. `validate-catalog.sh` + `render-index` 최종 1회 → 전체 정합성 확인.
5. **커밋**: 코드(automation.py, denylist.json) + 데이터(index.json, catalog/) + 문서 함께. 메시지 한글.
6. **이슈 #5 마감**: 처리 결과 코멘트(채택 12 / 제외 19 + 사유표) + 채택분 체크박스 체크 → close.

## 7. 문서화 (커밋 동반, AI 파악용)

- `docs/`의 채택 흐름에 `adopt` 서브커맨드 추가, scope 가드/denylist 규칙 기록.
- discover 결함(미러 오탐, 카테고리 오분류)과 대응을 트러블슈팅으로 남김.

## 8. 검증 기준 (완료 정의)

- `automation.py adopt <repo> --category <cat>`가 fork~README까지 한 번에 처리하고 `validate-catalog.sh`를 통과한다.
- BLOCK 케이스(예: go-zero, nano-banana 류)에 adopt 실행 시 `--force` 없이 거부된다.
- 미러(andrej-karpathy multica-ai 버전)가 중복으로 차단된다.
- 채택 12건이 index.json + catalog + README에 반영되고 fork 12개에 `context-forge-source` 토픽이 붙는다.
- 제외 19건이 denylist.json에 등록되어 다음 discover에서 제외된다.
