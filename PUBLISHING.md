# Publishing Guide

This repository produces a browsable HTML edition and a print-ready PDF candidate. The PDF is an editorial artifact, not the final press file for every printer. A publisher may still change trim size, fonts, bleeds, metadata, and color handling.

## Prerequisites

- mdBook 0.4.52 or a tested compatible release;
- Chrome or Chromium for PDF output;
- a shell environment that can run the scripts in `scripts/`.

Install mdBook using the official installation instructions linked from the project README. Record tool versions when producing a release so a later editor can reproduce the result.

## Build HTML

```bash
./scripts/build-book.sh
```

The command removes the prior generated directory, builds every entry in `SUMMARY.md`, and writes `book/index.html` and `book/print.html`. The `book/` directory is generated and is not committed.

## Build PDF

```bash
./scripts/build-pdf.sh
```

The script first performs a clean HTML build, then asks a headless Chrome or Chromium process to print `book/print.html` to:

```text
book/blockchain-scalability-book.pdf
```

Set `CHROME=/path/to/browser` when the browser binary is not on the normal path.

## Release Checklist

1. Pull the intended commit from `main` and record its full hash.
2. Record `mdbook --version` and the browser version.
3. Run the HTML and PDF builds from a clean checkout.
4. Confirm the build contains every item in `SUMMARY.md`.
5. Inspect the PDF cover, table of contents, first and last page, and every figure page at 100 percent zoom.
6. Check headings for stranded lines and code blocks or tables for clipping.
7. Search the PDF for replacement characters, missing glyphs, unresolved footnote markers, and raw HTML.
8. Run a link checker over the HTML edition and manually verify security-critical references.
9. Confirm figure credits, licenses, and permissions. Redraw or remove any element whose commercial reuse is unclear.
10. Treat protocol status, fee rules, deployment claims, and roadmaps as time-sensitive; verify them against primary sources at release time.
11. Name the files with edition, version, date, and commit, then retain the build log alongside the artifacts.

## Visual Review

A successful command does not prove that a PDF is publishable. Rendering can split captions from diagrams, clip wide tables, substitute fonts, or move a heading to the bottom of a page. Review the actual PDF pages after every layout-affecting change.

The HTML edition remains the canonical source output. If a printer requires a different page size, adjust print CSS in a dedicated release branch and keep content changes separate from layout changes.

## Versioning

Use semantic edition tags such as `v1.0.0`. A patch release corrects prose, citations, or formatting without changing the book's architecture. A minor release adds substantial sections or updates protocol coverage. A major release changes the edition's scope or organization.

A release note should list the commit, word count, build versions, material technical changes, known rights limitations, and the date on which time-sensitive claims were checked.
