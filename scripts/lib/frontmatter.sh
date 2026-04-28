#!/usr/bin/env bash
# Extract YAML frontmatter from a Markdown file to stdout.
# Returns 0 if frontmatter found, 1 otherwise.
extract_frontmatter() {
  local file="$1"
  awk '
    BEGIN { in_fm = 0; saw_open = 0 }
    /^---[ \t]*$/ {
      if (!saw_open) { saw_open = 1; in_fm = 1; next }
      else if (in_fm) { in_fm = 0; exit }
    }
    in_fm { print }
    END { if (!saw_open) exit 1 }
  ' "$file"
}
