#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

if [[ -n $(git status --porcelain --untracked-files=normal) ]]; then
  echo "refusing to package a dirty working tree" >&2
  exit 1
fi

version=$(tr -d '[:space:]' < VERSION)
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
  echo "VERSION must contain a semantic version such as 1.2.3" >&2
  exit 1
}

commit=$(git rev-parse HEAD)
built_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
repository_markdown_word_count=$(find . -name '*.md' -not -path './book/*' -not -path './release/*' -not -path './.git/*' -print0 | xargs -0 cat | wc -w | tr -d ' ')
mdbook_version=$(mdbook --version 2>/dev/null || echo unavailable)

./scripts/build-pdf.sh

browser=${CHROME:-}
if [[ -z "$browser" ]]; then
  for candidate in chromium chromium-browser google-chrome google-chrome-stable; do
    if command -v "$candidate" >/dev/null 2>&1; then browser=$(command -v "$candidate"); break; fi
  done
fi
browser_version=$(${browser:-false} --version 2>/dev/null || echo unavailable)

out="release/v${version}"
rm -rf "$out"
mkdir -p "$out"
pdf="book/blockchain-scalability-book.pdf"
pages=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
page_size=$(pdfinfo "$pdf" | awk -F: '/^Page size:/{sub(/^[[:space:]]*/, "", $2); print $2}')
replacement_characters=$(pdftotext "$pdf" - | grep -o $'�' | wc -l || true)
[[ "$pages" =~ ^[1-9][0-9]*$ ]] || { echo "could not verify PDF page count" >&2; exit 1; }
[[ "$replacement_characters" -eq 0 ]] || { echo "PDF contains replacement characters" >&2; exit 1; }
cp "$pdf" "$out/blockchain-scalability-book-v${version}.pdf"
tar -czf "$out/blockchain-scalability-book-v${version}-html.tar.gz" -C book --exclude='blockchain-scalability-book.pdf' .

cat > "$out/manifest.json" <<JSON
{
  "title": "Blockchain Scalability Book",
  "author": "Neil Han",
  "version": "$version",
  "commit": "$commit",
  "built_at_utc": "$built_at",
  "repository_markdown_word_count": $repository_markdown_word_count,
  "mdbook_version": "$mdbook_version",
  "browser_version": "$browser_version",
  "pdf_pages": $pages,
  "pdf_page_size": "$page_size",
  "pdf_replacement_characters": $replacement_characters
}
JSON
(
  cd "$out"
  sha256sum *.pdf *.tar.gz manifest.json > SHA256SUMS
)

echo "release package: $out"
cat "$out/manifest.json"
cat "$out/SHA256SUMS"
