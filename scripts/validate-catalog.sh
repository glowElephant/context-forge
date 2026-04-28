#!/usr/bin/env bash
# Validate every catalog/*/*.md file:
#  1. has frontmatter
#  2. frontmatter has required keys: name, category, domain, when_to_use, source
#  3. category matches its parent directory
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/frontmatter.sh"

REQUIRED_KEYS=(name category domain when_to_use source)
fail=0
checked=0

shopt -s nullglob
for file in catalog/*/*.md; do
  base="$(basename "$file")"
  # Skip README.md and dotfiles, only validate real entries
  [[ "$base" == "README.md" ]] && continue
  [[ "$base" == _* ]] && continue
  parent_cat="$(basename "$(dirname "$file")")"
  [[ "$parent_cat" == "_schema" ]] && continue

  checked=$((checked+1))
  fm="$(extract_frontmatter "$file" || true)"
  if [[ -z "$fm" ]]; then
    echo "✗ $file — missing frontmatter"
    fail=$((fail+1))
    continue
  fi
  for key in "${REQUIRED_KEYS[@]}"; do
    if ! echo "$fm" | grep -qE "^${key}:"; then
      echo "✗ $file — missing key: $key"
      fail=$((fail+1))
    fi
  done
  decl_cat="$(echo "$fm" | sed -nE 's/^category:[ ]*([a-z-]+).*/\1/p')"
  if [[ -n "$decl_cat" && "$decl_cat" != "$parent_cat" ]]; then
    echo "✗ $file — category=$decl_cat but in directory $parent_cat/"
    fail=$((fail+1))
  fi
done

if [[ "$fail" -eq 0 ]]; then
  echo "✅ all catalog entries valid (checked: $checked)"
  exit 0
fi
echo "❌ $fail issue(s) found"
exit 1
