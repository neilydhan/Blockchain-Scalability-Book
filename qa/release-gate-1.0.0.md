# Version 1.0.0 Release Gate

Gate run: 2026-09-02

## Source and Scope

- Version declared: 1.0.0
- Summary entries: 21
- Original figures: 11
- Scope: preface, Chapters 1-11, glossary, exercises and instructor solutions, practitioner handbook, figure credits, threat-model worksheets, and benchmark template

## Automated Result

- repository integrity: passed
- clean mdBook HTML build: passed
- PDF build: passed
- PDF page size: US Letter
- PDF pages: 302
- PDF replacement characters: 0
- Markdown whitespace check: passed

## Prior Review Evidence

The repository retains separate 0.9.0 QA records for PDF pixel sampling, citation/link review, and the whole-book engineering copyedit. The technical additions after the first PDF audit were each rebuilt through the same integrity and HTML pipeline. The 1.0 PDF is rebuilt again in this gate.

## Release Boundary

This gate establishes an internally reproducible first-edition release candidate. A commercial publisher may still impose a separate trim size, cover, font embedding, accessibility, indexing, legal, or independent technical-review process. Those production choices should not silently change protocol claims or source content.

## Tagging Procedure

After merging this gate:

1. fetch and check out the exact authoritative main commit;
2. verify a clean tree;
3. run scripts/package-release.sh;
4. inspect the generated manifest and SHA-256 checksums;
5. visually sample the packaged PDF;
6. create the signed v1.0.0 tag and attach artifacts only after the package matches this gate.

A tag and public release are external publication actions and remain separate from merging the source-ready release gate.
