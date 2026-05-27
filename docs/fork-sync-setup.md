# Fork Sync — Setup

`scripts/sync-forks.sh` 가 `sources/index.json`의 67개 fork를 upstream과 fast-forward sync한다.
로컬에서는 `gh auth login` 한 번이면 동작하고, GitHub Actions로 매주 자동화하려면 **Personal Access Token (PAT)** 한 번 등록이 필요하다.

기본 `GITHUB_TOKEN`은 워크플로우가 도는 repo(context-forge)만 만질 수 있어서, **다른 repo(=67개 fork)에 push 불가**. 그래서 PAT 필요.

## 1. PAT 발급

1. GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. **Generate new token (classic)**
3. 설정:
   - **Note**: `context-forge fork sync`
   - **Expiration**: 1 year (만료 직전 알림 옴)
   - **Scopes**: ✅ `repo` (Full control of private repositories)
     - 이 한 개면 충분. `workflow`, `admin:org` 등은 불필요
4. **Generate token** → 값 복사 (한 번만 보임)

## 2. context-forge에 secret 등록

1. https://github.com/glowElephant/context-forge/settings/secrets/actions
2. **New repository secret**
3. 설정:
   - **Name**: `FORK_SYNC_TOKEN`
   - **Secret**: 위에서 복사한 토큰 값
4. **Add secret**

## 3. 워크플로우 동작 확인

1. https://github.com/glowElephant/context-forge/actions/workflows/link-check.yml
2. **Run workflow** (수동 트리거)
3. 1~3분 후 결과 확인:
   - 성공: `sources/sync-log.md`에 새 entry 추가 + auto-commit
   - 실패: Actions 탭에서 로그 확인. `FORK_SYNC_TOKEN secret is not set` 에러면 위 2단계 다시.

## 4. 자동 스케줄

- **매주 월요일 04:00 UTC** (= 13:00 KST) cron으로 자동 실행 — `link-check.yml`에 통합
- 같은 워크플로우의 `check-source-urls` job과 병렬로 돔
- `.github/workflows/link-check.yml`의 `schedule.cron` 수정으로 변경 가능

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 모든 fork가 `❌ fork not found` | PAT scope 부족 | `repo` scope 확인. fine-grained PAT보다 classic PAT 권장 (fork 67개 일괄 권한이 단순) |
| 특정 fork만 `⚠️ failed: divergent` | 그 fork에 직접 커밋한 적 있음 | 1) 해당 fork 직접 visiting → upstream에서 manual sync, 또는 2) `index.json`에서 제거 |
| `upstream`이 삭제된 경우 | 원본 repo 사라짐 | `index.json`에서 해당 entry 삭제 |
| PAT 만료 | 1년 경과 | 새 PAT 발급 → secret 갱신 |

## 로컬 1회 실행 (PAT 없이)

```bash
cd context-forge
gh auth login   # 한 번만
bash scripts/sync-forks.sh
```

워크플로우 가동 전 67개를 한 번에 따라잡고 싶을 때 사용. 결과는 워크플로우와 동일하게 `sources/sync-log.md`에 박힘.
