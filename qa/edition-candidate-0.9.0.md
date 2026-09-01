# Edition Candidate 0.9.0 QA Record

This record documents the first release-layout audit of the 0.9.0 technical edition candidate. It is evidence for review, not a substitute for a full pre-1.0 copyedit and page-by-page inspection.

## Build Under Test

- Source commit: `496bd3b` (after publisher-depth pass 48)
- Build date: 2026-09-02
- Format: US Letter PDF
- Pages: 262
- File size: 2,301,816 bytes
- Integrity check: 21 summary entries and 11 figures
- Extracted replacement characters: 0

The PDF was rebuilt from source using `scripts/build-pdf.sh`. The non-fatal Chrome D-Bus diagnostic did not stop rendering; Chrome reported that it wrote the complete PDF.

## Automated Checks

- Repository integrity and mdBook HTML build passed.
- PDF metadata reported 262 Letter-sized pages.
- Text extraction found no Unicode replacement characters.
- A scan for unusually long unbroken extracted lines found no likely code-block clipping.
- A terminology scan was reviewed for `obviously`, `clearly`, `very`, `simply`, `just`, `trustless`, and `TPS`. Remaining uses of `trustless` and `TPS` are critical discussions of those labels rather than unsupported promotional claims.

## Visual Sample

The rendered pixels were inspected for:

- pages 1-3: title, chapter list, links, prose, code blocks, and repository metadata;
- page 26: Figure 2.1, caption, numbered list, footnote, and following heading;
- page 56: Figure 4.1, caption wrapping, bullets, and mathematical variables;
- page 95: Figure 6.1, caption, numbered lifecycle, emphasized term, and page rule;
- page 130: light-client bridge structures and numbered verification trace;
- page 142: Figure 8.1, probability notation, caption, footnote, and page rule;
- page 188: Figure 11.1, caption, paragraphs, and following heading;
- page 262: final code block, conclusion template, margins, and final page ending.

In the inspected sample, text and diagrams were legible; margins were consistent; captions stayed with figures; code blocks fit within their backgrounds; headings were not stranded at the page bottom; footnote markers rendered; and no content was clipped at page edges.

## Remaining Release Gates

Before version 1.0:

1. inspect all 262 pages at publication zoom, with special attention to every table, figure, code block, chapter opening, and reference list;
2. repeat the citation and link audit against live primary sources;
3. have an independent editor verify terminology, calculations, grammar, and accessibility text;
4. confirm the publisher's trim size, font embedding, cover, metadata, and accessibility requirements;
5. rebuild from the tagged commit and archive the manifest, checksums, logs, and signed release artifacts.
