# adopt 서브커맨드 + scope 가드

월간 후보(이슈 체크리스트)를 카탈로그에 채택하는 자동화. discover는 후보만 찾고, adopt가 실제 채택(fork → 토픽 → index → catalog → 점수)을 한 번에 처리한다.

## 사용법

```bash
python scripts/automation.py adopt <owner/repo> --category <cat> [--name <n>] [--notes "..."] [--force]
```

- `--category` (필수): 9개 enum 중 하나 — `claude-md, agents-md, skills, conventions, multi-agent, prompts, spec-driven, mcp, boilerplate`. `catalog/<cat>/` 디렉토리가 없으면 거부.
- `--name`: fork/catalog 이름 강제 지정. 생략 시 upstream repo 이름 사용, 충돌하면 `-N` suffix 자동.
- `--notes`: 한 줄 설명 → frontmatter `when_to_use` 시드 재료. 생략 시 upstream description 앞부분.
- `--force`: scope WARN/BLOCK과 미러 가드를 무시하고 강제 채택.

adopt가 하는 일(순서):
1. scope 가드 검사 (아래) — BLOCK/WARN이면 `--force` 없이 중단
2. `gh repo fork`로 glowElephant 계정에 fork (개인 계정이라 `--org` 없이)
3. fork에 `context-forge-source` 토픽 부착 (멱등)
4. `sources/index.json`에 엔트리 append (`tier:1`, `added_at`=today)
5. `seed_frontmatter.seed_one`으로 `catalog/<cat>/<name>.md` 생성
6. pop/act 자동 채점 + total/tier 계산해 frontmatter score 블록 작성
7. (호출자가 이어서) `validate-catalog.sh` + `render-index`로 검증·README 재생성

멱등: 이미 등록된 upstream이면 아무것도 안 하고 종료.

## scope 가드 (룰 기반)

입력: upstream의 `description` + `topics` + `language`. 판정 3단계:

| 판정 | 의미 | 동작 |
|---|---|---|
| **BLOCK** | 명백한 scope 밖 | 자동 거부 (`--force`로만 우회) |
| **WARN** | 범용 신호 없음, 또는 도메인 업무 키워드(제품성 의심) | 거부 + 사람 최종확인 필요 (`--force`) |
| **PASS** | 범용 하네스 신호 있고 BLOCK/도메인 키워드 없음 | 자동 진행 |

정책: **범용 하네스만 채택, 제품성/도메인특화는 제외.** CLAUDE.md/서브에이전트/스킬 형식이 맞아도 특정 업무 자동화 "제품"(광고 감사, 구직 시스템, 보안 에이전트, 데스크탑 앱)은 받지 않는다.

키워드(`scripts/automation.py`의 `SCOPE_*` 상수):
- **BLOCK**: 이미지 생성(`nano banana`, `gpt-image`, `text-to-image`, `diffusion`, `image generation`), 제품/앱(`desktop app`, `desktop ai`, `job search/hunting`, `ad audit/auditing/optimization`), 일반 프레임워크(`microservice`, `web framework`, `cloud-native`)
- **범용 신호(PASS 조건)**: `claude.md`, `claude code`, `agents.md`, `cursor`, `copilot`, `mcp`, `skill`, `subagent`, `spec-driven`, `prompt`, `context engineering`, `agent` …
- **도메인 키워드(WARN)**: `advertis`, `marketing`, `recruit`, `career`, `trading`, `finance`, `e-commerce`

룰이 늘면 상수를 `_status/scope-rules.json`으로 분리할 것(현재는 YAGNI로 상수).

## 미러/중복 검사

discover의 기존 dedup은 upstream URL 완전 일치만 봐서, **org-전송/미러된 repo를 신규로 오탐**했다(예: `multica-ai/andrej-karpathy-skills`는 기등록 `forrestchang/andrej-karpathy-skills`와 동일 repo, `open-multi-agent/open-multi-agent`는 기등록 `JackChen-me/open-multi-agent`와 동일).

보강: `find_mirror`가 후보의 repo basename(URL 마지막 segment)이 기존 source의 upstream basename과 같으면 미러로 판정해 차단. discover·adopt 양쪽에서 작동. 우연한 동명 프로젝트 오탐 여지가 있어 BLOCK이 아니라 `--force`로 우회 가능.

## denylist

`_status/denylist.json` — discover가 재발굴하지 않도록 제외할 upstream URL 목록.

```json
{ "entries": [ { "url": "...", "reason": "out-of-scope", "decided_at": "2026-06-09" } ] }
```

reason 3종:
- `duplicate-mirror`: 기등록 repo의 미러/org-전송
- `out-of-scope`: 카탈로그 범위 밖(이미지 프롬프트, 일반 프레임워크, LLM 앱 등)
- `product-not-pattern`: 형식은 하네스지만 도메인특화 "제품"(재사용 패턴 아님)

`cmd_discover`가 후보 필터링 시 이 url들을 제외한다.

## discover 결함과 대응 (트러블슈팅)

이슈 #5(2026-06) 31건 검증에서 드러난 discover 결함:

1. **미러/org-전송 오탐** — 위 미러 검사로 대응. 단 basename 휴리스틱이라 완벽하지 않음. 채택 전 사람이 한 번 확인.
2. **카테고리 오분류** — discover가 `matched_keyword`로 category를 자동 배정해서, `zeromicro/go-zero`가 `spec-driven`으로, `anything-llm`이 `mcp`로 잘못 들어온다. `validate-catalog.sh`가 `category` ≠ 디렉토리면 빌드를 깨뜨리므로, adopt 시 `--category`로 사람이 올바르게 지정해야 한다. adopt는 진입 시 category-디렉토리 정합성을 선검사한다.
3. **별점 스냅샷 시점 불일치** — 후보마다 표기 별점과 실제 별점 차이가 큼(발굴 스냅샷이 일관되지 않음). 채점은 adopt 시점에 `auto_score`로 다시 조회하므로 카탈로그 점수에는 영향 없음.
