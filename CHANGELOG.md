# Changelog

## v1.1.1 — 2026-05-27 (same day patch)

### Added

- **`scripts/seed_frontmatter.py`** — `sources/index.json` 순회하며 누락된 `catalog/<cat>/<name>.md` 자동 생성. gh API로 upstream description/topics 가져와 frontmatter + 본문 시드. upstream URL 기반 중복 체크로 manual semantic-name 시드와 충돌 방지. `.md`로 끝나는 name(예: `agents.md`)의 이중 확장자 방지.
- **`link-check.yml` sync-forks job**에 seed step + validate-catalog step 통합 — 매주 sync 직후 누락 frontmatter 자동 채움, catalog 변경분도 같은 commit에.
- **`context-forge-source` 토픽 일괄 부착** — 82개 fork 전부. `sync-forks.sh`에 토픽 자동 보장 로직 추가 (멱등). 외부에서 `topic:context-forge-source`로 originals와 분리 식별 가능.
- **글로벌 프로필 README** (`glowElephant/glowElephant`)에 `CATALOG_SOURCES` 섹션 신설 — originals와 catalog source forks 시각적 분리.

### Changed

- catalog frontmatter 보유 entries: 15 → **82 (전부)**. `/context-forge` 슬래시 커맨드 Phase 3 매칭 풀이 5.5배 확장, Phase 5 `cp` 누락 가능성 0.
- 자동 시드 13개가 manual semantic-name 시드와 같은 upstream을 가리키는 중복 발견 → 자동본 삭제, manual을 정본으로 유지.
- `docs/scoring.md` "Quarterly rediscovery" → "Monthly rediscovery"로 갱신 (v1.1에서 cron 변경 반영 + seed_frontmatter 흐름 명시).
- README/README.ko 사전 조건 섹션 보강: Windows PowerShell·Claude Code settings.json 환경변수 등록 가이드 추가. v1.0 → v1.1 갱신.
- `docs/fork-sync-setup.md` 하드코딩된 "67개"를 count-agnostic 표현으로.

### Why

v1.1.0 직후 슬래시 커맨드 end-to-end 흐름 검토 중 발견: catalog frontmatter가 v1 시드 15개로 좁아서 sources/index.json 82 entries 중 67개가 슬래시 커맨드 매칭 풀에서 누락. 자동화의 데이터 측면이 비어있어서 "사람이 손으로 67개 frontmatter 써야" 했던 상태.

`seed_frontmatter.py` + 주간 자동 hook으로 이 갭을 영구 해소 — 앞으로 새 채택은 다음 주 sync에서 자동 frontmatter 시드. Claude Code가 슬래시 커맨드 사용자 경험에서 사람 손 의존 없이 동작 가능.

## v1.1.0 — 2026-05-27

### Added

- **주간 fork sync 자동화** — `scripts/sync-forks.sh` + `link-check.yml`의 sync-forks job. 67개 fork를 매주 월요일 04:00 UTC에 upstream과 fast-forward sync. 결과는 `sources/sync-log.md`에 누적, `sources/index.json.updated_at` 자동 갱신. PAT(`FORK_SYNC_TOKEN`, `repo` + `workflow` scope) 필요 — 셋업은 [`docs/fork-sync-setup.md`](./docs/fork-sync-setup.md).
- **`scripts/render_candidates_issue.py`** — 신규 후보를 카테고리별 체크박스 list로 렌더링 (Issue 본문용).

### Changed

- **`monthly-rediscovery.yml`** (개명: `quarterly-rediscovery.yml`에서) — cron 분기→월간 (`0 4 1 * *`), 결과 출력 PR→Issue (`gh issue create`, `discovery` 라벨). 검토 부담을 낮추고 검토 주기를 짧게.
- **`automation.py` discover 필터 강화** — `MIN_STARS` 500→2000, `TOP_PER_CATEGORY=5` 신규 (카테고리당 상위 5개만 유지). 첫 실행 기준 138 → 32로 감소.
- **`link-check.yml`** — 워크플로우 이름 `weekly-maintenance`로 개명, sync-forks job 흡수. PR 트리거에선 sync-forks skip (link-check만 실행), 스케줄/수동에선 둘 다 병렬.

### Fixed

- `monthly-rediscovery.yml`의 `run: |` 블록 안에 `python -c "..."` 다중행 heredoc 인해 YAML 파싱 실패 → workflow_dispatch 트리거 등록 불가. 별도 스크립트(`render_candidates_issue.py`)로 분리해 해결.
- `package.json` 류 정합성 케이스는 해당 없음 (context-forge는 패키지 배포 X).

### Why

v1.0 직후 운영 중 발견된 두 가지 문제를 해결:

1. **fork 67개 stale** — 4/28 일괄 포크 후 한 달간 upstream과 벌어진 상태로 방치. 매주 자동 sync로 해소.
2. **분기 1회 발굴이 너무 길고 한 번에 너무 많음** — 첫 실행에서 138개 후보 발생, 검토 부담 과중. 월간 + 임계값 강화로 한 회 ~30개로 cap.

자세한 작동 원리는 README의 "Status" 섹션 + [`docs/fork-sync-setup.md`](./docs/fork-sync-setup.md).

## v1.0.0 — 2026-04-28

초기 릴리스. [release notes](https://github.com/glowElephant/context-forge/releases/tag/v1.0.0) 참고.

- 67개 v1 카탈로그 소스 포크 + `sources/index.json`
- `/context-forge` Claude Code 슬래시 커맨드
- 카탈로그 frontmatter 스키마 (`catalog/_schema/entry.schema.json`) + 9 카테고리
- 5팩터 점수 시스템 (popularity / activity 자동, reviews / quality / trust 수동)
- 자동화 워크플로우 7종: link-check, monthly-borderline-rescore, quarterly-full-rescore, quarterly-rediscovery, update-readme-index, validate-catalog (+ 봇 PR 자동 머지)
