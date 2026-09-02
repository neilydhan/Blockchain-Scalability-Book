#!/usr/bin/env bash
set -euo pipefail

"$(dirname "$0")/build-book.sh"

browser="${CHROME:-}"
if [[ -z "$browser" ]]; then
  for candidate in google-chrome chromium chromium-browser; do
    if command -v "$candidate" >/dev/null 2>&1; then
      browser="$(command -v "$candidate")"
      break
    fi
  done
fi
if [[ -z "$browser" && -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  browser="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
fi
if [[ -z "$browser" ]]; then
  echo "error: Chrome or Chromium is required to produce the PDF" >&2
  exit 1
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
output="$root/book/mastering-blockchain-scalability.pdf"
toc_map="$root/book/pdf-toc.json"
helper="$root/scripts/pdf_toc.py"

python3 - <<'PY2'
try:
    import fitz, pypdf
except ImportError as exc:
    raise SystemExit("error: PDF TOC build requires pymupdf and pypdf (python3 -m pip install pymupdf pypdf)") from exc
PY2

print_pdf() {
  local profile
  profile="$(mktemp -d)"
  "$browser" \
    --headless=new \
    --no-sandbox \
    --disable-gpu \
    --disable-background-networking \
    --disable-component-update \
    --disable-extensions \
    --disable-sync \
    --no-first-run \
    --user-data-dir="$profile" \
    --allow-file-access-from-files \
    --print-to-pdf="$output" \
    --no-pdf-header-footer \
    "file://$root/book/print.html"
  rm -rf "$profile"
}

# Chrome cannot render target page numbers directly. Print once to resolve every
# heading link, fill those page numbers into the HTML, then print the final PDF.
python3 "$helper" prepare --html "$root/book/print.html" --map "$toc_map" --version "$(cat "$root/VERSION")"
print_pdf
python3 "$helper" fill --html "$root/book/print.html" --map "$toc_map" --pdf "$output"
print_pdf
python3 "$helper" paginate --map "$toc_map" --pdf "$output"
python3 "$helper" outline --map "$toc_map" --pdf "$output"
python3 "$helper" verify --map "$toc_map" --pdf "$output"

test -s "$output"
echo "PDF book: $output"
