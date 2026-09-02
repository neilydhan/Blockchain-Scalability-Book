# Whole-Book Copyedit Pass for 0.9.0

Audit date: 2026-09-02

This pass checked the complete Markdown manuscript and release material for mechanical and terminology defects after the major technical additions through publisher-depth pass 59.

## Checks Performed

- inconsistent top-level section formatting;
- duplicate consecutive words;
- whitespace before punctuation;
- unresolved `TODO`, `TBD`, `FIXME`, and `XXX` markers;
- complexity-hiding words such as "obviously," "clearly," "simply," and "just";
- absolute safety language such as "always," "never," "guarantee," and "trustless";
- repository integrity, summary coverage, figure numbering, local links, and footnotes;
- Markdown diff whitespace.

## Changes

- Standardized Chapter 2's introduction, conclusion, and reference headings with the other numbered chapters.
- Replaced "obviously conflicting speculation" with a claim about conflicts predicted by scheduling history.
- Replaced a positive use of "trustless" in migration guidance with the narrower claim that correctness can be cryptographically verified while availability still depends on providers.

Remaining appearances of "trustless" occur only where the manuscript criticizes or qualifies the term. Remaining uses of "never" and "guarantee" were retained when they state explicit invariants, describe a bounded protocol property, or warn against a forbidden transition. `TPS` remains where the text teaches why transaction-count headlines require workload and finality context.

## Result

No unresolved editorial markers, duplicate consecutive words, or punctuation-spacing faults were found. The repository checks and HTML build passed after the edits. This is an engineering copyedit, not independent proof correction; calculations and security arguments still require subject-matter review before a publisher calls the edition final.
