# 스모크 테스트 결과 (Task 13)

작성일: 2026-04-28
상태: **PENDING** — 이 단계는 fresh Claude Code 세션에서 사용자가 직접 수행해야 함

## 테스트 시나리오

### 시나리오 1 — 솔로 SaaS 부트스트랩

**입력:**
- 프로젝트 타입: web (fullstack)
- 언어/프레임워크: Next.js + TypeScript
- 솔로
- 멀티에이전트: yes

**기대 결과:**
- Phase 1: 4개 고정 질문 모두 답함
- Phase 2: 5~8개 자유 디스커션 질문
- Phase 3: 다음 카탈로그 항목 매칭 후보 제시
  - claude-md/karpathy-single-claude-md
  - claude-md/gstack-claude-toolkit
  - skills/superpowers-skills-pattern
  - skills/cursor-rules-pattern (사용자 컨펌 시)
  - spec-driven/github-spec-kit
  - multi-agent/wshobson-agents
  - mcp/mcp-server-bootstrap
  - prompts/prompt-engineering-foundations
  - agents-md/agents-md-standard
- Phase 4: 저장소 정보 수집
- Phase 5: `gh repo create` → clone → 파일 채우기 → 커밋 → 푸시
- Phase 6: 완료 메시지 출력

**검증 명령:**

```bash
cd <new-repo-path>
ls CLAUDE.md AGENTS.md README.md docs/spec.md
ls docs/know-how/   # 약 5~9개 파일
git log --oneline   # "초기 하네스 셋업 (context-forge)"
```

### 시나리오 2 — 게임 엔진 프로젝트 (분야 매칭 검증)

**입력:**
- 프로젝트 타입: game-engine (Unity)
- 언어/프레임워크: Unity 6 / C#
- 소규모 팀 (2~5)
- 멀티에이전트: no

**기대 결과:**
- Phase 3에서 `multi-agent` 카테고리 항목은 자동 제외됨 (Q4 = no)
- 일반(general) domain 항목들은 매칭됨
- 게임 엔진 특화 항목은 v1 시드에 없으므로 매칭 안됨 (이는 정상 — v2에서 추가)

## 실행 절차

1. **CONTEXT_FORGE_PATH 설정**
   ```bash
   export CONTEXT_FORGE_PATH=/c/Git/context-forge
   ```

2. **Fresh Claude Code 세션 시작**
   - 어떤 디렉토리에서든 `claude` 실행
   - context-forge를 플러그인 소스로 등록했다면 자동 로드됨

3. **`/context-forge` 호출** (또는 자연어로 "새 프로젝트 셋업해줘")

4. **시나리오 1 진행**

5. **결과 캡쳐 후 이 문서 업데이트**:
   - 무엇이 작동했나
   - 무엇이 실패했나
   - 어떻게 고쳤나

## 결과 (실행 후 채워주세요)

> _이 섹션은 사용자가 실제 스모크 테스트 후 작성_

- [ ] 시나리오 1 통과 / 실패 — 메모: ...
- [ ] 시나리오 2 통과 / 실패 — 메모: ...
- [ ] 발견된 버그: ...
- [ ] 적용된 수정: ...

## 알려진 한계 (v1)

- 카탈로그 매칭은 frontmatter + `when_to_use` 기반 휴리스틱 (의미 검색 X)
- 보일러플레이트는 v1에 없음 (catalog/boilerplate/ 는 빈 디렉토리)
- 동일 카테고리에서 충돌 시 priority 휴리스틱 단순함
- 정기 발굴 잡 미구현 (v1.5)
