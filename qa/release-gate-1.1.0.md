# Version 1.1.0 Release Gate

Gate run: 2026-09-02

## Source and Scope

- Source commit at gate preparation: `34d7dc6` plus the footnote-rendering fix in this gate commit
- Summary entries: 21
- Original figures: 12
- Chapter-only Markdown word count: 96,055 before this gate note
- Scope: named production and pilot protocol case studies added to Chapters 1, 2, and 4-11

## Material Additions

- Chapter 1: CryptoKitties congestion and a production Arbitrum workload
- Chapter 2: fixed-workload Bitcoin, Ethereum, and Solana comparison
- Chapter 4: NEAR receipt trace and IBC packet lifecycle
- Chapter 5: Polygon PoS sidechain and checkpoint/bridge contrast
- Chapter 6: Arbitrum Nitro/BoLD and ZKsync Era end-to-end traces; six-rollup comparison
- Chapter 7: OP Stack deployment using Celestia data availability
- Chapter 8: same-batch Celestia, EigenDA, and Avail comparison
- Chapter 9: Solana, Sui, and Aptos execution traces
- Chapter 10: HotStuff/Diem/AptosBFT, Narwhal/Bullshark/Mysticeti, and PBFT/Tendermint/CometBFT lineages
- Chapter 11: ERC-4337, MEV-Boost, Espresso, Across/CoW, and Succinct Prover Network maturity map

Every added case study states an architecture, transaction or batch trace, trust and upgrade assumptions, observable evidence, and a failure path. Time-sensitive claims were checked against linked official documentation on the gate date. Historical CryptoKitties evidence uses primary project and wallet accounts plus a Consensys retrospective; L2BEAT is identified as an independent deployment view.

## Automated Result

- repository integrity: passed
- local links and footnote pairs: passed
- external link check: passed; expected 403 responses from sites that block automated HEAD requests were treated as reachable and the corresponding pages were fetched during research
- clean mdBook 0.4.52 HTML build: passed
- Chrome 151 PDF build: passed
- PDF page size: US Letter
- PDF pages: 416
- PDF replacement characters: 0
- PDF blank pages: 0
- Markdown whitespace check: passed
- mdBook footnote warnings: 0 after separating adjacent citation markers

## Visual Review

Rendered pages were inspected at the opening of every new named case study: 17, 37, 71, 110, 132-133, 199, 233, 260, 286, and 323. The new Figure 6.2 was rendered separately in Chrome and again in the PDF. The final two PDF pages were also inspected. Headings, tables, prose, and Figure 6.2 are readable and remain inside the print area in the sampled pages.

The source tree remains the canonical edition. The generated PDF candidate is `book/blockchain-scalability-book.pdf`; release artifacts are not committed.

## Release Boundary

This gate prepares the v1.1 candidate but does not create a tag or public GitHub release. Public tagging and attachment of the updated PDF require Neil's explicit final go-ahead after he receives the candidate summary.
