#!/usr/bin/env bash
set -euo pipefail

if ! command -v mdbook >/dev/null 2>&1; then
  echo "error: mdbook is required (https://rust-lang.github.io/mdBook/guide/installation.html)" >&2
  exit 1
fi

rm -rf book
mdbook build

echo "HTML book: book/index.html"
echo "Print layout: book/print.html"
