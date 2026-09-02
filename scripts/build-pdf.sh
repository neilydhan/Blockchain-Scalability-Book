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
output="$root/book/blockchain-scalability-book.pdf"
profile="$(mktemp -d)"
trap 'rm -rf "$profile"' EXIT
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

test -s "$output"
echo "PDF book: $output"
