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

The link checker tested 30 distinct external destinations. Twenty-eight returned HTTP 200. The NUS-hosted BLOCKBENCH paper returned HTTP 403 to the automated request but remains a known publisher/university destination that requires browser review under the repository policy.

The original Berkeley URL for Eric Brewer's PODC 2000 keynote timed out repeatedly. This pass replaced it with the canonical ACM DOI landing page:

<https://doi.org/10.1145/343477.343502>

The DOI identifies "Towards robust distributed systems (abstract)," Eric A. Brewer, PODC 2000, and provides durable bibliographic metadata even if access or hosting changes.

## Chapter Reference Review

- Chapters 1-2 anchor scalability and distributed-systems framing in the original scalability paper, BLOCKBENCH, protocol papers, and the Brewer DOI.
- Chapters 3-4 cite EIP-4844, OP Stack specifications, Nightshade, IBC documentation, and Ethereum's sharding material for L1/L2 and sharding mechanisms.
- Chapter 5 cites the original Lightning, Sprites, and Plasma papers.
- Chapters 6-8 cite current Ethereum specifications and original data-availability work.
- Chapter 9 cites platform transaction specifications and the Block-STM paper.
- Chapter 10 cites the original HotStuff, Sync HotStuff, and Narwhal/Tusk papers.
- Chapter 11 cites current roadmap specifications for PeerDAS and state-tree evolution.

## Release Rule

Run `scripts/check-links.sh` immediately before tagging a release. Investigate every non-200 status manually. For mutable documentation, record the release audit date. If a primary source disappears, prefer its DOI, standards identifier, or official repository before selecting a third-party mirror. Preserve the title, authors, and publication venue so readers can recover the source independently of one URL.
