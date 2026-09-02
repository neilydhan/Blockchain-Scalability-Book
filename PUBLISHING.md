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

The command first checks summary targets, local links, figure numbering, and footnote pairs. It then removes the prior generated directory, builds every entry in `SUMMARY.md`, and writes `book/index.html` and `book/print.html`. The `book/` directory is generated and is not committed.

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
8. Run `./scripts/check-links.sh`, investigate failures and redirects, and manually verify security-critical references. Some publisher sites return 403 to automated checks while remaining available in a browser.
9. Confirm figure credits, licenses, and permissions. Redraw or remove any element whose commercial reuse is unclear.
10. Treat protocol status, fee rules, deployment claims, and roadmaps as time-sensitive; verify them against primary sources at release time.
11. Name the files with edition, version, date, and commit, then retain the build log alongside the artifacts.

## Visual Review

A successful command does not prove that a PDF is publishable. Rendering can split captions from diagrams, clip wide tables, substitute fonts, or move a heading to the bottom of a page. Review the actual PDF pages after every layout-affecting change.

The HTML edition remains the canonical source output. Print rules live in `theme/print.css`. They keep headings, figures, code blocks, and tables from splitting when possible. If a printer requires a different trim size, adjust that file in a dedicated release branch and keep content changes separate from layout changes.

## Versioning

Use semantic edition tags such as `v1.0.0`. A patch release corrects prose, citations, or formatting without changing the book's architecture. A minor release adds substantial sections or updates protocol coverage. A major release changes the edition's scope or organization.

A release note should list the commit, word count, build versions, material technical changes, known rights limitations, and the date on which time-sensitive claims were checked.

## Package an Edition Candidate

Set the semantic version in `VERSION`, commit all source changes, and run:

```bash
./scripts/package-release.sh
```

The script requires a clean tree and creates `release/v<version>/` with the PDF, compressed HTML edition, JSON build manifest, and SHA-256 checksums. Review and archive the build log separately. Generated release artifacts are not source files and should normally be attached to a signed repository release rather than committed.

The packaging gate also reads the generated PDF with `pdfinfo` and `pdftotext`. It records the page count and page size in the manifest and refuses to package a PDF containing Unicode replacement characters. The reported word count covers all repository Markdown, including release and QA records; chapter-only editorial counts should be computed separately when needed.

mdBook inserts explicit page-break elements between source files in `print.html`. Do not add another unconditional `break-before` rule to every `h1`; the doubled break can produce blank pages. The release visual audit should scan extracted PDF pages for unexpectedly empty pages as well as inspect representative pixels.

## Build EPUB

Install Pandoc, then run:

```bash
./scripts/build-epub.sh
```

The command follows the chapter order in `SUMMARY.md`, writes an EPUB 3 file to `book/blockchain-scalability-book.epub`, and verifies the archive. Treat archive validity as a minimum gate, not an accessibility or device-compatibility review. Inspect navigation, code, tables, equations, diagrams, links, metadata, and reading order in representative EPUB readers before release.

## Web Deployment

GitHub Actions builds the mdBook web edition from `main` and deploys the generated `book/` directory to GitHub Pages. The build adds canonical links, publication metadata, `robots.txt`, and `sitemap.xml`. Repository Markdown is the canonical source; generated HTML is not committed.

Changing the production site still requires reviewing the Pages workflow result and the rendered URL. Check desktop and narrow mobile layouts, sidebar and search behavior, tables, code blocks, diagrams, and every primary reader path.

## Print Interior (7x10 KDP Paperback)

`./scripts/build-print.py` builds `print/blockchain-scalability-book-interior-7x10.pdf` from the rendered mdBook HTML. It selects the print sections (Preface, Chapters 1-11, glossary, review questions, evaluation handbook, figure credits, worksheets, benchmark template), adds the title page, copyright page, and table of contents, generates the back-of-book index from glossary terms and a curated system list, and typesets with `theme/print-7x10.css`: 7x10in pages, 0.8in top/bottom/inside and 0.65in outside margins, Noto Serif body at 10.5pt on 13.8pt, running heads, outside page numbers, and chapters opening on recto pages. SVG figures are rasterized at 2400px with cairosvg because WeasyPrint mis-renders some styled SVGs. Install dependencies from `requirements-pdf.txt` first.

Gates before KDP upload: confirm the final page count against KDP margin minimums, eyeball every figure in grayscale, order a proof copy, and only then approve distribution. The print ISBN (KDP free ISBN) goes on the copyright page at upload time.
