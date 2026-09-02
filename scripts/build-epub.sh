#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

command -v pandoc >/dev/null 2>&1 || {
  echo "error: pandoc is required to produce EPUB" >&2
  exit 1
}

python3 scripts/check-book.py
mkdir -p book
mapfile -t sources < <(python3 - <<'PY'
from pathlib import Path
import re
text=Path("SUMMARY.md").read_text()
for target in re.findall(r'\]\(([^)]+\.md)\)', text):
    if target not in {"README.md", "CONTRIBUTING.md", "LICENSE.md", "SAMPLE.md", "ACADEMIC.md"}:
        print(target)
PY
)

pandoc "${sources[@]}" \
  --from=gfm \
  --to=epub3 \
  --standalone \
  --toc \
  --metadata title="Blockchain Scalability Book" \
  --metadata subtitle="A mechanism-first guide to blockchain capacity, security, trust, and recovery" \
  --metadata author="Neil Han" \
  --metadata lang="en" \
  --metadata date="2026-09-02" \
  --metadata rights="CC BY-SA 4.0; build software separately licensed under MIT" \
  --resource-path=".:chapters:assets" \
  --output book/blockchain-scalability-book.epub

test -s book/blockchain-scalability-book.epub
unzip -t book/blockchain-scalability-book.epub >/dev/null
echo "EPUB book: book/blockchain-scalability-book.epub"
