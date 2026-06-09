# 월간 후보 채택(adopt) 자동화 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `automation.py adopt` 서브커맨드로 월간 후보 채택(fork → 토픽 → index → catalog → 점수 → 검증)을 자동화하고, 룰 기반 scope 가드 + 미러 중복탐지로 "성격에 맞는" 채택만 통과시킨다. 그리고 이번 이슈 #5의 31건을 처리한다.

**Architecture:** 기존 `automation.py`의 score/frontmatter 함수와 `seed_frontmatter.seed_one`, `sync-forks.sh`의 토픽 PUT 로직을 재사용한다. 신규는 순수 함수 3개(scope 가드, 미러 검사, fork-name suffix)와 이를 조립하는 `cmd_adopt`, 그리고 `_status/denylist.json`. 순수 함수는 stdlib `unittest`로 테스트, gh I/O는 실제 실행으로 검증.

**Tech Stack:** Python 3.10+ (stdlib only), `gh` CLI, bash. 테스트는 `python -m unittest`.

---

## File Structure

- **Modify** `scripts/automation.py` — scope 가드 상수+함수, `is_mirror`, `resolve_fork_name`, `append_source`, `cmd_adopt`, discover의 denylist/미러 통합, argparse `adopt` 등록
- **Create** `scripts/test_automation.py` — 순수 함수 unittest
- **Create** `_status/denylist.json` — 제외 repo 기록
- **Modify** `docs/scoring.md` 또는 `docs/contributing.md` — 채택 흐름에 adopt 추가
- **Create** `docs/adopt-and-scope-guard.md` — adopt/가드/denylist 규칙 + discover 결함 트러블슈팅

---

### Task 1: scope 가드 순수 함수

**Files:**
- Modify: `scripts/automation.py` (discover 상수 블록 아래, `cmd_discover` 위에 추가)
- Test: `scripts/test_automation.py`

- [ ] **Step 1: 테스트 작성**

`scripts/test_automation.py` 생성:

```python
import unittest
import automation as A


class TestClassifyScope(unittest.TestCase):
    def test_block_image_gen(self):
        v, _ = A.classify_scope("Nano Banana Pro prompts for image generation", [], "Python", "prompts")
        self.assertEqual(v, "BLOCK")

    def test_block_framework(self):
        v, _ = A.classify_scope("cloud-native Go microservice framework", ["go"], "Go", "spec-driven")
        self.assertEqual(v, "BLOCK")

    def test_block_desktop_app(self):
        v, _ = A.classify_scope("all-in-one Desktop AI application with RAG", [], "JavaScript", "mcp")
        self.assertEqual(v, "BLOCK")

    def test_pass_mcp_server(self):
        v, _ = A.classify_scope("The official GitHub MCP server", ["mcp"], "Go", "mcp")
        self.assertEqual(v, "PASS")

    def test_pass_claude_md(self):
        v, _ = A.classify_scope("Claude Code starter template with CLAUDE.md memory bank", [], "Python", "claude-md")
        self.assertEqual(v, "PASS")

    def test_warn_no_generic_signal(self):
        v, _ = A.classify_scope("3D digital twin visualization toolkit", ["vue"], "Vue", "spec-driven")
        self.assertEqual(v, "WARN")

    def test_warn_domain_keyword(self):
        v, _ = A.classify_scope("Claude Code skill for paid ad auditing and marketing", [], "Python", "skills")
        # ad audit는 BLOCK 패턴이므로 BLOCK이 우선 — career-ops류(domain만)를 위한 케이스는 아래
        self.assertEqual(v, "BLOCK")

    def test_warn_career_domain(self):
        v, _ = A.classify_scope("Claude Code based job-hunting system with skill modes", [], "JavaScript", "skills")
        self.assertEqual(v, "BLOCK")  # "job-hunting"은 product-app 패턴


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: FAIL — `AttributeError: module 'automation' has no attribute 'classify_scope'`

- [ ] **Step 3: 최소 구현**

`scripts/automation.py`의 `MIN_STARS`/`TOP_PER_CATEGORY` 상수 블록(382행 부근) 아래에 추가:

```python
# ─── scope guard (룰 기반 — docs/adopt-and-scope-guard.md) ────────────────────

# BLOCK: 명백한 scope 밖 — 자동 거부 (--force로만 우회)
SCOPE_BLOCK_PATTERNS: dict[str, list[str]] = {
    "image-gen":   ["nano banana", "nanobanana", "gpt-image", "text-to-image",
                    "diffusion", "image generation", "image-generation"],
    "product-app": ["desktop app", "desktop &", "desktop ai", "job search",
                    "job-hunting", "job hunting", "ad audit", "ad-audit",
                    "ad optimization", "advertising audit"],
    "framework":   ["microservice", "micro-service", "web framework",
                    "cloud-native", "cloud native"],
}

# 범용 하네스 신호 — 하나라도 있어야 PASS
SCOPE_GENERIC_SIGNALS: list[str] = [
    "claude.md", "claude-md", "claude code", "claude-code", "agents.md",
    "agents-md", "cursor", "copilot", "mcp", "skill", "subagent", "sub-agent",
    "spec-driven", "spec kit", "spec-kit", "prompt", "context engineering", "agent",
]

# 도메인 업무 키워드 — 제품성 의심, WARN으로 사람 확인
SCOPE_DOMAIN_KEYWORDS: list[str] = [
    "advertis", "marketing", "recruit", "career", "trading", "finance", "e-commerce",
]


def classify_scope(description: str | None, topics: list[str] | None,
                   language: str | None, category: str) -> tuple[str, str]:
    """Return ('PASS'|'WARN'|'BLOCK', reason).

    BLOCK: 명백 scope 밖. WARN: 범용 신호 없음 또는 도메인 키워드(제품성 의심).
    PASS: 범용 신호 있고 BLOCK/도메인 키워드 없음.
    """
    text = f"{description or ''} {' '.join(topics or [])} {language or ''}".lower()
    for label, pats in SCOPE_BLOCK_PATTERNS.items():
        for p in pats:
            if p in text:
                return "BLOCK", f"{label}: matched '{p}'"
    has_generic = any(s in text for s in SCOPE_GENERIC_SIGNALS)
    if not has_generic:
        return "WARN", "no generic harness signal in description/topics/language"
    has_domain = any(k in text for k in SCOPE_DOMAIN_KEYWORDS)
    if has_domain:
        return "WARN", "domain-specific keyword present — confirm reusable pattern, not a product"
    return "PASS", "generic harness signal present"
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS (8 tests)

- [ ] **Step 5: 커밋**

```bash
git add scripts/automation.py scripts/test_automation.py
git commit -m "adopt: 룰 기반 scope 가드 함수 추가 (classify_scope)"
```

---

### Task 2: 미러/중복 검사 + fork-name suffix 순수 함수

**Files:**
- Modify: `scripts/automation.py` (Task 1 함수 아래)
- Test: `scripts/test_automation.py`

- [ ] **Step 1: 테스트 추가**

`scripts/test_automation.py`에 클래스 추가:

```python
class TestMirrorAndForkName(unittest.TestCase):
    SOURCES = [
        {"name": "andrej-karpathy-skills",
         "upstream": "https://github.com/forrestchang/andrej-karpathy-skills",
         "fork": "https://github.com/glowElephant/andrej-karpathy-skills"},
        {"name": "open-multi-agent",
         "upstream": "https://github.com/JackChen-me/open-multi-agent",
         "fork": "https://github.com/glowElephant/open-multi-agent"},
    ]

    def test_mirror_detected_by_basename(self):
        hit = A.find_mirror("https://github.com/multica-ai/andrej-karpathy-skills", self.SOURCES)
        self.assertEqual(hit, "andrej-karpathy-skills")

    def test_no_mirror_for_new_repo(self):
        hit = A.find_mirror("https://github.com/github/github-mcp-server", self.SOURCES)
        self.assertIsNone(hit)

    def test_fork_name_no_collision(self):
        self.assertEqual(A.resolve_fork_name("github-mcp-server", {"skills", "gstack"}), "github-mcp-server")

    def test_fork_name_collision_suffix(self):
        self.assertEqual(A.resolve_fork_name("skills", {"skills"}), "skills-1")

    def test_fork_name_collision_multi(self):
        self.assertEqual(A.resolve_fork_name("skills", {"skills", "skills-1"}), "skills-2")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: FAIL — `find_mirror` / `resolve_fork_name` 없음

- [ ] **Step 3: 최소 구현**

`scripts/automation.py`의 `classify_scope` 아래에 추가:

```python
def _basename(url: str) -> str:
    return url.rstrip("/").split("/")[-1].removesuffix(".git").lower()


def find_mirror(candidate_url: str, sources: list[dict[str, Any]]) -> str | None:
    """기존 source 중 repo basename이 같은 게 있으면 그 name 반환 (미러/org-전송 의심).
    upstream URL 완전 일치는 호출부의 known_upstreams가 이미 거른다 — 여기는 basename 휴리스틱."""
    cand = _basename(candidate_url)
    for s in sources:
        if _basename(s.get("upstream", "")) == cand:
            return s.get("name")
    return None


def resolve_fork_name(base_name: str, existing: set[str]) -> str:
    """glowElephant에 이미 있는 fork 이름과 충돌하면 -N suffix."""
    if base_name not in existing:
        return base_name
    i = 1
    while f"{base_name}-{i}" in existing:
        i += 1
    return f"{base_name}-{i}"
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS (13 tests)

- [ ] **Step 5: 커밋**

```bash
git add scripts/automation.py scripts/test_automation.py
git commit -m "adopt: 미러 중복탐지(find_mirror) + fork-name suffix(resolve_fork_name) 추가"
```

---

### Task 3: index.json append + denylist 로드 순수 함수

**Files:**
- Modify: `scripts/automation.py`
- Create: `_status/denylist.json`
- Test: `scripts/test_automation.py`

- [ ] **Step 1: denylist.json 생성**

`_status/denylist.json`:

```json
{
  "version": 1,
  "updated_at": "2026-06-09",
  "note": "discover가 재발굴하지 않도록 제외할 upstream URL. reason: duplicate-mirror | out-of-scope | product-not-pattern",
  "entries": []
}
```

- [ ] **Step 2: 테스트 추가**

`scripts/test_automation.py`에 추가:

```python
class TestIndexAndDenylist(unittest.TestCase):
    def test_build_source_entry(self):
        e = A.build_source_entry(
            upstream="https://github.com/github/github-mcp-server",
            fork_name="github-mcp-server",
            name="github-mcp-server",
            category="mcp",
            notes="GitHub 공식 MCP 서버",
            today="2026-06-09",
        )
        self.assertEqual(e["upstream"], "https://github.com/github/github-mcp-server")
        self.assertEqual(e["fork"], "https://github.com/glowElephant/github-mcp-server")
        self.assertEqual(e["category"], "mcp")
        self.assertEqual(e["tier"], 1)
        self.assertEqual(e["added_at"], "2026-06-09")
        self.assertEqual(e["notes"], "GitHub 공식 MCP 서버")

    def test_denylist_urls(self):
        doc = {"entries": [{"url": "https://github.com/a/b", "reason": "out-of-scope"}]}
        self.assertEqual(A.denylist_urls(doc), {"https://github.com/a/b"})
```

- [ ] **Step 3: 테스트 실패 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: FAIL — `build_source_entry` / `denylist_urls` 없음

- [ ] **Step 4: 최소 구현**

`scripts/automation.py`에 추가(상수 `SOURCES_INDEX` 부근에 경로 추가, 함수는 Task 2 아래):

```python
DENYLIST = STATUS / "denylist.json"
GLOWELEPHANT = "glowElephant"


def build_source_entry(*, upstream: str, fork_name: str, name: str,
                       category: str, notes: str, today: str) -> dict[str, Any]:
    return {
        "upstream": upstream.rstrip("/"),
        "fork": f"https://github.com/{GLOWELEPHANT}/{fork_name}",
        "name": name,
        "category": category,
        "tier": 1,
        "added_at": today,
        "notes": notes,
    }


def denylist_urls(doc: dict[str, Any]) -> set[str]:
    return {e["url"].rstrip("/") for e in doc.get("entries", [])}


def load_denylist() -> dict[str, Any]:
    if DENYLIST.exists():
        return json.loads(DENYLIST.read_text(encoding="utf-8"))
    return {"version": 1, "entries": []}
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS (15 tests)

- [ ] **Step 6: 커밋**

```bash
git add scripts/automation.py scripts/test_automation.py _status/denylist.json
git commit -m "adopt: index 엔트리 빌더 + denylist 로드 + _status/denylist.json 추가"
```

---

### Task 4: discover에 denylist + 미러 필터 통합

**Files:**
- Modify: `scripts/automation.py` (`cmd_discover`, 405행 부근)

- [ ] **Step 1: cmd_discover 수정**

`cmd_discover`의 `known_upstreams` 정의 직후(388행)에 denylist 로드 추가:

```python
    known_upstreams = {s["upstream"].rstrip("/") for s in sources.get("sources", [])}
    denied = denylist_urls(load_denylist())
    source_list = sources.get("sources", [])
```

그리고 후보 루프의 `if url in known_upstreams: continue`(405행) 아래에 추가:

```python
                if url in known_upstreams:
                    continue
                if url in denied:
                    continue
                mirror_of = find_mirror(url, source_list)
                if mirror_of:
                    continue
```

- [ ] **Step 2: 회귀 확인 (구문/동작)**

Run: `cd scripts && python -c "import automation; print('import ok')"`
Expected: `import ok`

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS (15 tests — 회귀 없음)

- [ ] **Step 3: 커밋**

```bash
git add scripts/automation.py
git commit -m "discover: denylist + 미러 basename 필터 통합 (org-전송/미러 오탐 차단)"
```

---

### Task 5: `cmd_adopt` 조립 + argparse 등록

**Files:**
- Modify: `scripts/automation.py` (`cmd_render_index` 아래 `cmd_adopt` 추가, `main`에 파서 등록, 파일 상단에 `seed_frontmatter` import)

- [ ] **Step 1: seed_frontmatter import 추가**

`scripts/automation.py` 상단 import 블록(36행 `from typing import Any` 아래)에 추가:

```python
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import seed_frontmatter  # noqa: E402  (같은 scripts/ 디렉토리)
```

- [ ] **Step 2: gh I/O 헬퍼 + cmd_adopt 추가**

`cmd_render_index` 아래(493행 부근)에 추가:

```python
# ─── subcommand: adopt ───────────────────────────────────────────────────────

def gh_run(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True,
                          input=input_text, check=False)


def ensure_topic(fork_path: str, topic: str = "context-forge-source") -> None:
    """sync-forks.sh:57-62 이식 — 토픽 멱등 부착."""
    cur = gh_run(["api", f"repos/{fork_path}/topics",
                  "--jq", ".names | join(\" \")"])
    names = cur.stdout.split() if cur.returncode == 0 else []
    if topic in names:
        return
    payload = json.dumps({"names": sorted(set(names + [topic]))})
    gh_run(["api", "-X", "PUT", f"repos/{fork_path}/topics", "--input", "-"],
           input_text=payload)


def cmd_adopt(args: argparse.Namespace) -> int:
    today = dt.date.today().isoformat()
    repo = args.repo  # owner/repo
    category = args.category
    if category not in AI_CATEGORIES:
        print(f"✗ category '{category}' not in {sorted(AI_CATEGORIES)}")
        return 1
    if not (CATALOG / category).is_dir():
        print(f"✗ catalog/{category}/ directory missing")
        return 1

    sources_doc = json.loads(SOURCES_INDEX.read_text(encoding="utf-8"))
    source_list = sources_doc.get("sources", [])
    upstream_url = f"https://github.com/{repo}"

    # 멱등: 이미 등록된 upstream이면 skip
    if upstream_url.rstrip("/") in {s["upstream"].rstrip("/") for s in source_list}:
        print(f"= already adopted: {repo}")
        return 0

    # 미러 검사
    mirror_of = find_mirror(upstream_url, source_list)
    if mirror_of and not args.force:
        print(f"✗ mirror suspected (basename matches existing '{mirror_of}'). Use --force to override.")
        return 1

    # repo 메타 조회 + scope 가드
    info = gh_api(f"repos/{repo}")
    verdict, reason = classify_scope(info.get("description"), info.get("topics", []),
                                     info.get("language"), category)
    if verdict == "BLOCK" and not args.force:
        print(f"✗ scope BLOCK ({reason}). Use --force to override.")
        return 1
    if verdict == "WARN" and not args.force:
        print(f"✗ scope WARN ({reason}). Use --force to confirm adoption.")
        return 1
    print(f"  scope {verdict}: {reason}")

    # fork 이름 결정
    base = repo.split("/")[-1]
    existing_forks = {_basename(s["fork"]) for s in source_list}
    fork_name = args.name or resolve_fork_name(base, existing_forks)

    # fork 생성
    print(f"  forking {repo} → {GLOWELEPHANT}/{fork_name} ...")
    fr = gh_run(["repo", "fork", repo, "--org", GLOWELEPHANT,
                 "--fork-name", fork_name, "--clone=false"])
    if fr.returncode != 0:
        print(f"✗ fork failed: {fr.stderr.strip()}")
        return 1

    # 토픽 부착
    ensure_topic(f"{GLOWELEPHANT}/{fork_name}")

    # index.json append
    notes = args.notes or (info.get("description") or "")[:120]
    entry = build_source_entry(upstream=upstream_url, fork_name=fork_name,
                               name=fork_name, category=category, notes=notes, today=today)
    source_list.append(entry)
    sources_doc["sources"] = source_list
    sources_doc["updated_at"] = today
    SOURCES_INDEX.write_text(json.dumps(sources_doc, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")

    # catalog frontmatter 시드
    seed_frontmatter.seed_one(entry, force=False, upstream_index=seed_frontmatter.existing_upstreams())

    # 점수 채우기
    path = CATALOG / category / f"{fork_name}.md"
    fm, fm_text, body = read_frontmatter(path)
    auto = auto_score(repo)
    new_score = {"popularity": auto["popularity"], "activity": auto["activity"],
                 "reviews": 3, "quality": 3, "trust": 3}
    total, tier = compute_total_and_tier(new_score, category, auto["archived"])
    new_score["total"] = total
    new_score["tier"] = tier
    new_score["last_scored"] = today
    update_frontmatter(path, fm_text, body, score=new_score, status="active" if tier != 3 else "archived")

    log_history({"event": "adopt", "name": fork_name, "category": category,
                 "after": {"total": total, "tier": tier}})
    print(f"✓ adopted {repo} as {category}/{fork_name} (total={total}, tier={tier})")
    return 0
```

`main()`의 `p_render` 등록(514행) 아래에 추가:

```python
    p_adopt = sub.add_parser("adopt", help="Adopt a candidate: fork + topic + index + catalog + score")
    p_adopt.add_argument("repo", help="owner/repo")
    p_adopt.add_argument("--category", required=True, help="catalog category")
    p_adopt.add_argument("--name", help="override fork/catalog name")
    p_adopt.add_argument("--notes", help="one-line notes (→ when_to_use seed)")
    p_adopt.add_argument("--force", action="store_true", help="override scope WARN/BLOCK and mirror guard")
    p_adopt.set_defaults(func=cmd_adopt)
```

- [ ] **Step 3: import/구문 확인**

Run: `cd scripts && python -c "import automation; print('import ok')"`
Expected: `import ok`

Run: `cd scripts && python automation.py adopt --help`
Expected: adopt 서브커맨드 usage 출력

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS (15 tests)

- [ ] **Step 4: dry-run 검증 (BLOCK 동작)**

Run: `cd scripts && python automation.py adopt zeromicro/go-zero --category spec-driven`
Expected: `✗ scope BLOCK (framework: ...)` — fork 안 함, 종료코드 1

Run: `cd scripts && python automation.py adopt multica-ai/andrej-karpathy-skills --category claude-md`
Expected: `✗ mirror suspected (basename matches existing 'andrej-karpathy-skills')` — 종료코드 1

- [ ] **Step 5: 커밋**

```bash
git add scripts/automation.py
git commit -m "adopt: cmd_adopt 조립 (가드→fork→토픽→index→seed→score) + argparse 등록"
```

---

### Task 6: 채택 1건 실제 실행으로 통합 검증

**Files:** (실데이터 변경 — index.json, catalog/mcp/)

- [ ] **Step 1: 가장 안전한 1건 채택 (PASS 확실)**

Run: `cd scripts && python automation.py adopt github/github-mcp-server --category mcp --notes "GitHub 공식 MCP 서버"`
Expected: `scope PASS` → fork 생성 → `✓ adopted ... mcp/github-mcp-server (total=..., tier=...)`

- [ ] **Step 2: 산출물 확인**

Run: `cd /c/Git/context-forge && git status --short`
Expected: `sources/index.json` 수정 + `catalog/mcp/github-mcp-server.md` 신규

Run: `bash scripts/validate-catalog.sh`
Expected: 통과 (0 failures)

Run: `gh api repos/glowElephant/github-mcp-server/topics --jq '.names'`
Expected: `context-forge-source` 포함

- [ ] **Step 3: README 재생성 확인**

Run: `cd scripts && python automation.py render-index`
Expected: `rendered N category READMEs` — `catalog/mcp/README.md`에 github-mcp-server 행 등장

- [ ] **Step 4: 커밋**

```bash
git add sources/index.json catalog/mcp/
git commit -m "adopt: github-mcp-server 채택 (통합 검증 1건)"
```

> 이후 나머지 11건은 Task 8에서 사용자 최종확인 뒤 일괄.

---

### Task 7: 문서화

**Files:**
- Create: `docs/adopt-and-scope-guard.md`
- Modify: `docs/scoring.md` (채택 흐름 섹션에 adopt 한 줄 추가)

- [ ] **Step 1: docs/adopt-and-scope-guard.md 작성**

내용: `adopt` 사용법(`python scripts/automation.py adopt <owner/repo> --category <cat> [--name --notes --force]`), 가드 3단계(BLOCK/WARN/PASS) 키워드 표, 미러 basename 휴리스틱, denylist 운영(reason 3종), 그리고 discover 결함 트러블슈팅(① 미러/org-전송 오탐 → basename 필터로 대응, ② 카테고리 오분류 → adopt 진입 시 category-디렉토리 선검사 + 사람이 `--category`로 교정).

- [ ] **Step 2: docs/scoring.md 채택 흐름에 adopt 추가**

기존 채택 흐름 설명 줄 아래에: "채택은 `automation.py adopt`로 자동화됨 — fork·토픽·index·catalog·점수를 한 번에. scope 가드가 범용 하네스만 통과시킴(docs/adopt-and-scope-guard.md)."

- [ ] **Step 3: 커밋**

```bash
git add docs/adopt-and-scope-guard.md docs/scoring.md
git commit -m "docs: adopt 서브커맨드 + scope 가드/denylist 규칙 + discover 결함 트러블슈팅"
```

---

### Task 8: 이번 31건 일괄 처리 + 이슈 마감

**Files:** (실데이터 — index.json, catalog/, denylist.json)

- [ ] **Step 1: 사용자 최종확인 게이트**

채택 확정 11건(github-mcp-server는 Task 6에서 완료) 목록을 사용자에게 다시 보여주고 일괄 실행 승인받는다. fork는 외부 상태 변경.

- [ ] **Step 2: 채택 11건 일괄 adopt**

```bash
cd /c/Git/context-forge/scripts
python automation.py adopt centminmod/my-claude-code-setup --category claude-md --notes "Claude Code 스타터 템플릿 + CLAUDE.md 메모리뱅크"
python automation.py adopt drona23/claude-token-efficient --category claude-md --notes "응답을 간결하게 만드는 단일 CLAUDE.md"
python automation.py adopt microsoft/playwright-mcp --category mcp --notes "Playwright MCP 서버 (MS 공식)"
python automation.py adopt googleapis/mcp-toolbox --category mcp --notes "DB용 MCP 서버 (Google 공식)"
python automation.py adopt VoltAgent/awesome-codex-subagents --category multi-agent --notes "Codex 서브에이전트 130+ 컬렉션"
python automation.py adopt Meirtz/Awesome-Context-Engineering --category prompts --notes "Context Engineering 서베이"
python automation.py adopt safishamsi/graphify --category skills --notes "코드→지식그래프 멀티-CLI 코딩 에이전트 스킬"
python automation.py adopt Lum1104/Understand-Anything --category skills --notes "코드→인터랙티브 지식그래프 스킬"
python automation.py adopt VoltAgent/awesome-openclaw-skills --category skills --notes "OpenClaw 스킬 5400+ 큐레이션"
python automation.py adopt open-gsd/gsd-core --category spec-driven --notes "Git Ship Done — spec-driven/meta-prompting"
python automation.py adopt buildermethods/agent-os --category spec-driven --notes "코드베이스 표준 주입 + spec-driven 시스템"
```

각 명령이 `scope PASS` 후 `✓ adopted`로 끝나는지 확인. WARN/BLOCK이 나면 멈추고 사유 검토(graphify/Understand-Anything의 "knowledge graph"는 BLOCK 패턴 아님 → PASS 예상).

- [ ] **Step 3: 제외 19건 denylist 등록**

`_status/denylist.json`의 `entries`에 19건 추가(url + reason + decided_at=2026-06-09). reason 분류는 spec §5 기준:
- duplicate-mirror: multica-ai/andrej-karpathy-skills, open-multi-agent/open-multi-agent
- product-not-pattern: claude-ads(AgriciDaniel), career-ops(santifer), raptor(gadievron), golutra, activepieces, MrLesk/Backlog.md, microsoft/SkillOpt
- out-of-scope: anything-llm, open-design(nexu-io), agency-swarm(VRSEN), solace-agent-mesh, EvoLinkAI/awesome-gpt-image-2-API-and-Prompts, YouMind-OpenLab/awesome-nano-banana-pro-prompts, ZeroLu/awesome-nanobanana-pro, zeromicro/go-zero, hawk86104/three-vue-tres, ai-boost/awesome-prompts

- [ ] **Step 4: 전체 검증 + README 재생성**

Run: `bash scripts/validate-catalog.sh`
Expected: 0 failures

Run: `cd scripts && python automation.py render-index`
Expected: 카테고리 README들에 신규 12건 반영

Run: `cd scripts && python -m unittest test_automation -v`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add sources/index.json catalog/ _status/denylist.json _status/history.jsonl
git commit -m "월간 후보 채택: 12건 카탈로그 등록 + 제외 19건 denylist (이슈 #5)"
```

- [ ] **Step 6: 푸시 + 이슈 마감**

```bash
git push -u origin feat/monthly-adopt-automation
```

이슈 #5에 처리 결과 코멘트(채택 12 / 제외 19 + 사유표) 작성, 채택분 체크박스 체크, close. PR 생성 여부는 사용자에게 확인.

---

## Self-Review

**Spec coverage:**
- §4.1 adopt 시퀀스 → Task 5 ✓
- §4.2 scope 가드 → Task 1 ✓
- §4.3 미러 검사 → Task 2 + Task 4 ✓
- §4.4 denylist → Task 3 + Task 8 Step 3 ✓
- §5 31건 분류 → Task 8 ✓
- §6 실행/이슈 마감 → Task 6 + Task 8 ✓
- §7 문서화 → Task 7 ✓
- §8 검증 기준 → Task 5 Step 4(BLOCK/미러), Task 6(통합), Task 8 Step 4(전체) ✓

**Type consistency:** `classify_scope`(4-arg) / `find_mirror`(url, sources) / `resolve_fork_name`(base, set) / `build_source_entry`(kwargs) / `denylist_urls`(doc) / `ensure_topic`(fork_path) / `cmd_adopt` — Task 정의와 호출부 일치 확인됨. `seed_one(entry, force, upstream_index)` 시그니처는 seed_frontmatter.py:204와 일치.

**Placeholder scan:** 모든 코드 스텝에 실제 코드 포함. docs(Task 7)는 산문 문서라 내용 요지만 기술 — 작성 시 실제 채움.

**Note:** Task 8 Step 2의 graphify/Understand-Anything는 description에 "knowledge graph"가 있으나 BLOCK 패턴(image-gen/product-app/framework)에 없고 "skill"/"claude code" 범용 신호가 있어 PASS 예상. 실행 중 WARN이면 `--force`로 확정(이미 사람이 채택 판정한 건들).
