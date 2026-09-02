#!/usr/bin/env bash
set -euo pipefail

if ! command -v mdbook >/dev/null 2>&1; then
  echo "error: mdbook is required (https://rust-lang.github.io/mdBook/guide/installation.html)" >&2
  exit 1
fi

python3 "$(dirname "$0")/check-book.py"

rm -rf book
mdbook build

# With the repository root as mdBook source, remove source-control, CI, QA, and
# local metadata that must never ship in the Pages artifact.
rm -rf book/.git book/.github book/qa book/release book/.DS_Store

# Mark unusually wide tables for compact print-only styling.
python3 - <<'PY2'
from pathlib import Path
from bs4 import BeautifulSoup
p = Path("book/print.html")
soup = BeautifulSoup(p.read_text(), "html.parser")
for table in soup.find_all("table"):
    columns = max((len(row.find_all(["th", "td"], recursive=False)) for row in table.find_all("tr")), default=0)
    if columns >= 6:
        table["class"] = list(table.get("class", [])) + ["wide-table"]
p.write_text(str(soup))
PY2

python3 "$(dirname "$0")/enrich-html.py"

echo "HTML book: book/index.html"
echo "Print layout: book/print.html"
