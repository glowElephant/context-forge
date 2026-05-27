#!/usr/bin/env python3
"""Generate catalog frontmatter stubs for every sources/index.json entry that doesn't have one yet.

context-forge의 슬래시 커맨드(/context-forge)는 `catalog/*/*.md` frontmatter만 읽어서 매칭하므로,
sources/index.json에는 등록됐지만 catalog 파일이 없는 entry는 부트스트랩 추천에서 빠진다.

이 스크립트는 그 갭을 메운다:
  - sources/index.json의 모든 entry 순회
  - catalog/{category}/{name}.md 이미 있으면 skip
  - 없으면 gh API로 upstream description/topics 가져와 frontmatter + 본문 생성
  - validate-catalog.sh가 통과하는 최소 형식 보장

Claude Code가 갱신·정제할 수 있는 "충분히 정확한 시드"가 목표. 사람이 직접 안 써도 동작.

사용:
  python scripts/seed_frontmatter.py            # 누락된 것만 시드
  python scripts/seed_frontmatter.py --force    # 기존 파일도 덮어쓰기 (재시드)
  python scripts/seed_frontmatter.py --name X   # 특정 entry만
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
SOURCES = ROOT / "sources" / "index.json"

# 카테고리별 기본 domain (catalog/_schema/entry.schema.json enum 안에서)
CATEGORY_DOMAIN = {
    "skills": ["general", "ai-agent"],
    "claude-md": ["general", "ai-agent"],
    "agents-md": ["general", "ai-agent"],
    "multi-agent": ["general", "ai-agent"],
    "spec-driven": ["general"],
    "mcp": ["general", "ai-agent"],
    "prompts": ["general"],
    "conventions": ["general"],
    "boilerplate": ["general"],
}

# 카테고리별 when_to_use 보조 한 줄 (notes가 너무 짧을 때 prepend)
CATEGORY_HINT = {
    "skills": "Claude Code/Codex skills 또는 agent 스킬을 채택할 때 참고",
    "claude-md": "프로젝트의 CLAUDE.md 구조를 결정할 때 참고",
    "agents-md": "AGENTS.md(IDE-agnostic) 컨벤션이 필요할 때 참고",
    "multi-agent": "여러 에이전트가 협업·오케스트레이션될 때 참고",
    "spec-driven": "Spec-Driven Development 워크플로우를 도입할 때 참고",
    "mcp": "MCP 서버를 추가하거나 발굴할 때 참고",
    "prompts": "프롬프트 엔지니어링 패턴이 필요할 때 참고",
    "conventions": "전체 코드/문서 규약을 정할 때 참고",
    "boilerplate": "프로젝트 부트스트랩 보일러플레이트가 필요할 때 참고",
}


def gh_api(path: str) -> dict[str, Any] | None:
    """gh api wrapper. 실패 시 None."""
    try:
        r = subprocess.run(
            ["gh", "api", path], capture_output=True, text=True, timeout=15
        )
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)
    except Exception:
        return None


def upstream_path(url: str) -> str:
    """https://github.com/owner/repo → owner/repo"""
    return url.replace("https://github.com/", "").rstrip("/")


def derive_tags(category: str, description: str | None, topics: list[str]) -> list[str]:
    """카테고리 + 토픽 + 설명의 핵심 키워드로 최대 6개 태그."""
    seen: set[str] = set()
    tags: list[str] = []

    def push(t: str) -> None:
        t = t.lower().strip()
        if not t or t == "context-forge-source":
            return
        if t in seen:
            return
        seen.add(t)
        tags.append(t)

    push(category)
    for t in topics[:5]:
        push(t)

    # description에서 의미 있는 키워드 추출 (보조)
    if description:
        for kw in ["claude", "agent", "mcp", "skills", "cursor", "codex", "prompt",
                   "rag", "tool", "harness", "spec", "boilerplate", "template"]:
            if re.search(rf"\b{kw}\b", description, re.IGNORECASE):
                push(kw)

    return tags[:6] or [category]


def derive_when_to_use(notes: str, category: str, description: str | None) -> str:
    """when_to_use 문자열 생성. 스키마 최소 10자 보장."""
    base = notes.strip() if notes else ""
    if len(base) < 10 and description:
        base = description.strip().split(". ")[0]
    hint = CATEGORY_HINT.get(category, "AI 코딩 에이전트 하니스 구성 시 참고")
    if len(base) >= 10:
        # notes/description이 충분하면 그것 + 카테고리 힌트
        return f"{base}. {hint}"
    # 둘 다 부족하면 카테고리 힌트만
    return hint + "."


def render_body(name: str, source: dict[str, Any], description: str | None,
                topics: list[str]) -> str:
    desc = description or "(no upstream description)"
    return f"""# {name}

> Auto-seeded from `sources/index.json`. Refine when human-reviewed.

{desc}

## When to apply

{source.get('notes', '').strip() or '(see frontmatter `when_to_use`)'}

## Source

- Upstream: {source['upstream']}
- Fork (auto-synced weekly): {source['fork']}
- Category: `{source['category']}`
"""


def yaml_block(d: dict[str, Any]) -> str:
    """frontmatter용 간단 YAML 직렬화 (jq/yaml 무의존)."""
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            inner = ", ".join(repr(x) if isinstance(x, str) else str(x) for x in v)
            lines.append(f"{k}: [{inner}]")
        elif isinstance(v, str):
            # 안전한 문자 안에 있으면 quote 없이, 아니면 double-quote
            if any(ch in v for ch in ":#-{}[]&*!|>'\"%@`,"):
                escaped = v.replace("\\", "\\\\").replace('"', '\\"')
                lines.append(f'{k}: "{escaped}"')
            else:
                lines.append(f"{k}: {v}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def existing_upstreams() -> dict[str, pathlib.Path]:
    """이미 catalog 안에서 다루는 upstream URL → 파일 경로 매핑.
    seed가 같은 upstream에 중복 파일 만드는 것 차단용."""
    import re
    mapping: dict[str, pathlib.Path] = {}
    for f in CATALOG.rglob("*.md"):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^upstream:\s*[\"']?([^\"'\s]+)[\"']?", text, re.MULTILINE)
        if m:
            mapping[m.group(1).strip().rstrip("/")] = f
    return mapping


def seed_one(source: dict[str, Any], force: bool = False,
             upstream_index: dict[str, pathlib.Path] | None = None) -> str:
    """단일 entry를 시드. 결과 상태 문자열 반환."""
    cat = source["category"]
    name = source["name"]
    target = CATALOG / cat / f"{name}.md"
    upstream = source["upstream"].rstrip("/")

    # 같은 upstream을 가리키는 기존(또는 manual) catalog 파일이 있으면 skip
    if upstream_index is not None and upstream in upstream_index:
        existing = upstream_index[upstream]
        if existing.resolve() != target.resolve():
            return f"skip   {cat}/{name} (upstream already in {existing.relative_to(ROOT)})"

    if target.exists() and not force:
        return f"skip   {cat}/{name}"

    # gh API로 description + topics 시도 (실패 OK)
    info = gh_api(f"repos/{upstream_path(source['upstream'])}")
    description = info.get("description") if info else None
    topics = info.get("topics", []) if info else []

    fm = {
        "name": name,
        "category": cat,
        "domain": CATEGORY_DOMAIN.get(cat, ["general"]),
        "tags": derive_tags(cat, description, topics),
        "source": source["fork"],
        "upstream": source["upstream"],
        "when_to_use": derive_when_to_use(source.get("notes", ""), cat, description),
        "priority": 3,
        "status": "active",
    }

    body = render_body(name, source, description, topics)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml_block(fm) + "\n\n" + body, encoding="utf-8")
    return f"create {cat}/{name}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="기존 파일도 덮어쓰기")
    ap.add_argument("--name", help="특정 entry만 시드 (sources/index.json의 name)")
    args = ap.parse_args()

    idx = json.loads(SOURCES.read_text(encoding="utf-8"))
    targets = idx["sources"]
    if args.name:
        targets = [s for s in targets if s["name"] == args.name]
        if not targets:
            print(f"no entry named '{args.name}'", file=sys.stderr)
            return 1

    upstream_index = existing_upstreams()
    created = skipped = 0
    for s in targets:
        result = seed_one(s, force=args.force, upstream_index=upstream_index)
        print(f"  {result}")
        if result.startswith("create"):
            created += 1
            # 새로 만든 catalog의 upstream을 인덱스에 등록 (같은 호출 안에서 또 안 만들어짐)
            upstream_index[s["upstream"].rstrip("/")] = CATALOG / s["category"] / f"{s['name']}.md"
        else:
            skipped += 1

    print(f"\n결과: {created} 생성 / {skipped} skip / total {len(targets)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
