# Citation and Link Audit for 0.9.0

Audit date: 2026-09-02

## Method

The audit extracted every HTTP(S) destination from the Markdown source, deduplicated the list, and requested each destination with redirects enabled. It then reviewed the references at the end of Chapters 1-11 for source type and fit.

Primary-source preference for this edition is:

1. protocol specifications and standards;
2. official technical documentation and repositories;
3. original papers and project white papers;
4. official incident reports and measured engineering reports;
5. secondary explanation only when it adds necessary context.

A successful HTTP status proves reachability, not that a source supports every nearby claim. Editorial review must still check claim-to-source fit.

## Result

The final link checker tested 95 distinct external destinations. Eighty-nine returned HTTP 200. Six returned HTTP 403 and were accepted by the checker because the destinations use publisher or bot-protection controls:

1. the ACM DOI for Eric Brewer's PODC 2000 keynote;
2. the NUS-hosted BLOCKBENCH paper;
3. two official EigenDA documentation pages;
4. the official CryptoKitties incident post on Medium;
5. the official MetaMask incident post on Medium.

No destination returned a failing status under the repository policy. The six HTTP 403 destinations still require browser review before a release because an HTTP status alone cannot establish that the content remains readable or still supports the cited claim.

## Chapter Reference Review

- Chapters 1-2 anchor scalability and distributed-systems framing in the original scalability paper, BLOCKBENCH, protocol papers, and the Brewer DOI.
- Chapters 3-4 cite EIP-4844, EIP-7594, the Fusaka mainnet announcement, OP Stack specifications, Nightshade, and the current ICS-004 channel specification.
- Chapter 5 cites the original Lightning, Sprites, and Plasma papers.
- Chapters 6-8 cite current rollup documentation, Ethereum specifications, original data-availability work, the EigenDA security-parameter specification, and Avail implementation repositories.
- Chapter 9 cites platform transaction specifications, the Block-STM paper, and the Mysticeti paper.
- Chapter 10 cites the original HotStuff, Sync HotStuff, Narwhal/Tusk, and Mysticeti papers.
- Chapter 11 cites current implementation and roadmap sources for PeerDAS, MEV-Boost, Across, Espresso, and Succinct.

## Release Rule

Run `scripts/check-links.sh` immediately before tagging a release. Investigate every non-200 status manually. For mutable documentation, record the release audit date. If a primary source disappears, prefer its DOI, standards identifier, or official repository before selecting a third-party mirror. Preserve the title, authors, and publication venue so readers can recover the source independently of one URL.
