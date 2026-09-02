# Publication Grade Academic Review and Correction Report

Review date: 2026-09-02

Repository: <https://github.com/neilstripe/Blockchain-Scalability-Book>

Review branch: `academic-review-corrections-2026-09`

## 1. Executive Assessment

Scores use a five point scale. A score of five means the material is suitable for use in a graduate course with normal instructor curation, not that the subject has stopped evolving.

| Dimension | Before | After | Assessment |
| --- | ---: | ---: | --- |
| Conceptual correctness | 4.0 | 4.8 | The main blocker was the implication that one HotStuff quorum certificate establishes finality. Rollup, sharding, Sui, and bridge boundaries also needed narrower statements. |
| Security and assumption clarity | 4.1 | 4.8 | Commit rules, challenger assumptions, data availability, cross-domain recovery, and correlated faults are now more explicit. |
| Factual currency | 3.7 | 4.8 | PeerDAS, Polygon Chain naming, Sui Mysticeti, IBC channel ordering, and OP Alt-DA maturity were updated as of September 2026. |
| Readability | 4.3 | 4.7 | First-use acronyms were expanded and the generic rollup lifecycle now precedes named system traces. |
| Pedagogical progression | 4.3 | 4.8 | The sequence now moves more consistently from problem, to generic mechanism, to named deployment, to failure analysis. |
| Systems and mathematical depth | 4.5 | 4.8 | The committee example now computes the complete hypergeometric tail and states limits of the model. |
| Master's-program suitability | 4.3 | 4.8 | The corrected text consistently asks students to identify evidence, boundaries, assumptions, and recovery paths. |
| Exercises and supporting material | 4.5 | 4.9 | New questions test HotStuff commitment, Sui paths, MEV-Boost withholding, rollup boundaries, and committee capture probability. |

### Overall assessment

The original book already had unusually strong mechanism-first treatment, quantitative exercises, operational failure traces, and evaluation templates. The review found two conceptual areas that required coordinated correction across chapters, glossary, figures, and exercises: HotStuff commitment evidence and current Sui Mysticeti transaction paths. It also found several major currency and assumption issues in PeerDAS, rollup completion boundaries, modular data availability, cross-shard atomicity, and named deployment labels.

All identified P0 and P1 content issues were corrected. No known P0 or P1 content issue remains. The HTML edition is classroom-ready. PDF publication remains conditional because the repository PDF command did not complete under the managed macOS Chrome installation used for this review.

## 2. Baseline, Sources, and Concept Dependency Map

### Material reviewed

The complete 10,184 line pre-report source corpus was reviewed before the final verdict. It included every root Markdown file, every prior QA record, `book.toml`, all eighteen chapter and supporting-material files, all repository scripts, and all twelve course SVG files.

The review covered the 144 line Preface; Chapters 1 to 11, totaling 7,405 lines after correction; the 433 line glossary; the 234 line question and solution set; the 639 line evaluation handbook; the 143 line threat-model worksheets; and the 200 line benchmark template.

### Baseline failures

1. `./scripts/build-book.sh` initially failed because `mdbook` was not installed.
2. After installing mdBook 0.5.4, the build rejected the obsolete `multilingual = false` key in `book.toml`.
3. Repository links in `README.md`, `RELEASE.md`, and `book.toml` still used the former `neilydhan` repository owner.
4. The initial link audit contained publisher and bot-protection responses, including HTTP 403 responses from NUS, Medium, EigenDA documentation, and the ACM DOI.
5. The PDF script did not discover the normal macOS Google Chrome application path.

### Concept dependency map

1. The Preface introduces Layer 1, Layer 2, data availability, finality, and the book's completion-boundary vocabulary.
2. Chapter 1 defines scalability through workload, resources, latency, security, and recovery. Those metrics are reused in every later comparison.
3. Chapter 2 introduces the trilemma as measurable trade-offs and supplies the fault-domain and governance vocabulary used in later threat models.
4. Chapter 3 defines architecture families. Chapters 4 and 5 then separate Layer 1 scaling from off-chain and independently secured systems.
5. Chapter 4 introduces asynchronous receipts, light-client evidence, committee sampling, state growth, and recovery. These concepts support later modular and bridge analyses.
6. Chapter 5 introduces channels, Plasma, sidechains, exits, and bridge verification. Chapter 6 builds on these prerequisites to compare optimistic and validity rollups.
7. Chapter 6 defines sequencing, publication, proof or challenge acceptance, settlement, forced inclusion, proving capacity, and canonical withdrawals.
8. Chapter 7 composes execution, settlement, consensus, and data availability into modular systems. Chapter 8 then deepens the data-availability component.
9. Chapter 9 separates deterministic semantics from concurrent execution. Chapter 10 supplies the consensus, quorum, synchrony, view-change, and commit-rule details needed to reason about ordering.
10. Chapter 11 combines the preceding layers into future-facing designs while explicitly labeling maturity.
11. Chapters 12 to 17 consolidate vocabulary, test reasoning, and provide practitioner, threat-model, and benchmark artifacts.

### Time-sensitive claims checked

The review dated mutable claims about PeerDAS activation, full danksharding, Polygon Chain naming, OP Stack Alt-DA maturity, Sui Mysticeti integration, Espresso, Succinct, MEV-Boost, and Across. These claims should be rechecked before each future release.

### Professor and researcher pass

This pass traced every major mechanism through its fault, timing, data, and governance assumptions. It identified the HotStuff and Sui conceptual blockers; recalculated committee capture; checked rollup proof and settlement boundaries; compared DA evidence; and reviewed named-system maturity against specifications, original papers, and official implementation documentation.

### Master's student pass

This pass reread the corrected sequence from the stated prerequisite level. It found that the generic rollup lifecycle appeared after named implementations and that several acronyms were used before expansion. The lifecycle was moved before the Arbitrum and ZKsync traces; TPS, EVM, NFT, BoLD, BFT, DAG, RPC, and ABCI were expanded at first use; and the RPC glossary entry now explains why an endpoint acknowledgement is not consensus evidence. Dense Chapters 4, 6, and 10 retain their technical depth, but their mechanism and failure traces now have clearer prerequisites.

## 3. Correction Log

| Severity | Confidence | File and section | Issue | Correction made | Source | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P0, Conceptual blocker | High | `chapters/10_consensus_scaling.md`, Safety, Liveness, and the Finality Boundary, lines 69 to 104 | The text allowed readers to infer that one HotStuff QC gives deterministic finality. | Distinguished a one-phase QC from the protocol commit rule and explained the later certified chain required by chained HotStuff. Updated the glossary, style guide, figure description, questions, and solutions. | [HotStuff paper](https://arxiv.org/abs/1803.05069) | Fixed |
| P0, Conceptual blocker | High | `chapters/09_parallel_execution.md`, Sui sections, lines 98 and 176 to 188; `chapters/10_consensus_scaling.md`, lines 193 to 199 | The Sui explanation reflected an older separation between a consensusless owned-object path and consensus, rather than the current integrated Mysticeti design. | Explained Mysticeti-FPC and Mysticeti-C, their shared DAG communication, different ordering requirements, certificate evidence, object versioning, and checkpoint role. Updated comparison tables, glossary, questions, and solutions. | [Mysticeti paper](https://docs.sui.io/paper/mysticeti.pdf), [Sui transaction lifecycle](https://docs.sui.io/concepts/sui-architecture/transaction-lifecycle) | Fixed |
| P1, Major | High | `chapters/04_layer_1_on_chain_scalability.md`, Ethereum roadmap, lines 196 to 200; related Chapter 8, Chapter 11, and glossary text | PeerDAS was described as future work after its mainnet activation. | Dated Fusaka activation to December 3, 2025, described cells, columns, custody, sampling, and reconstruction, and kept full danksharding as later roadmap work. | [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594), [Fusaka announcement](https://blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement) | Fixed |
| P1, Major | High | `chapters/10_consensus_scaling.md`, lines 69 to 89 and comparison table at lines 230 to 236 | Safety, liveness, and finality were presented as three parallel properties without a sufficiently explicit application decision boundary. | Separated protocol properties from the finality rule and qualified fault and timing assumptions for each consensus family. | [HotStuff paper](https://arxiv.org/abs/1803.05069), [Sync HotStuff paper](https://arxiv.org/abs/2005.13432) | Fixed |
| P1, Major | High | `chapters/06_rollups.md`, completion boundaries and lifecycle, lines 47 to 90 and 319 | Validity-rollup withdrawal text compressed proof acceptance and settlement finality; optimistic acceptance was also too generic. | Separated sequencer confirmation, data publication, proof or challenge acceptance, deployment-specific delays, and L1 finality. Replaced “proof finality” with “proof acceptance.” | [Ethereum validity rollups](https://ethereum.org/developers/docs/scaling/zk-rollups/), [Arbitrum transaction lifecycle](https://docs.arbitrum.io/how-arbitrum-works/deep-dives/transaction-lifecycle) | Fixed |
| P1, Major | High | `chapters/04_layer_1_on_chain_scalability.md`, Cross-Shard Transfer Atomicity, lines 218 to 222 | “Economically atomic” could conceal intermediate states and double-credit or refund races. | Reframed the flow as authenticated asynchronous messaging with explicit credit, rejection, cancellation, refund, and late-receipt rules. | [IBC lifecycle](https://docs.cosmos.network/ibc/next/learn/ibc-lifecycle), [NEAR transaction execution](https://docs.near.org/protocol/transactions/transaction-execution) | Fixed |
| P1, Major | High | `chapters/04_layer_1_on_chain_scalability.md`, Committee Security by Calculation, lines 224 to 239 | The example named the mean and attack threshold but omitted the required tail calculation. | Added the exact hypergeometric sum, the result `0.02144`, the roughly one-in-47 interpretation, multi-committee extension, and limitations involving stake, correlation, dependence, and adaptive corruption. | Hypergeometric calculation reproduced locally from stated inputs | Fixed |
| P1, Major | High | `chapters/07_modular_vs_monolithic.md`, OP Stack with Celestia DA, lines 129 to 173 | The integration was labeled production-capable even though the governing OP specification identifies Alt-DA mode as beta. | Changed the section to an architecture trace, dated the maturity check, quoted the beta status, and required chain-specific verification of fallback, proof, bridge, and governance configuration. | [OP Stack Alt-DA specification](https://specs.optimism.io/experimental/alt-da.html) | Fixed |
| P1, Major | High | `chapters/08_data_availability_scaling.md`, EigenDA path, lines 185 to 193 | The comparison did not expose threshold relationships, trusted disperser liveness, or intersubjective recovery. | Added confirmation, safety, liveness, and reconstruction thresholds; the required inequality; quorum scope; trusted disperser assumption; and the alarm and token-fork recovery path. | [EigenDA security parameters](https://layr-labs.github.io/eigenda/protocol/architecture/security-parameters.html), [EigenDA security model](https://docs.eigencloud.xyz/eigenda/core-concepts/security/security-model) | Fixed |
| P1, Major | High | `chapters/05_layer_2_off_chain_scalability.md`, Polygon case study, lines 120 to 140 | The title reduced the case to a label dispute and the architecture count treated Ethereum contracts as an operating Polygon layer. | Updated current Polygon Chain naming, described Heimdall-v2 and Bor as two operating layers, and clarified that Ethereum custody and checkpoints do not confer rollup execution verification. | [Polygon Chain overview](https://docs.polygon.technology/pos/overview) | Fixed |
| P1, Major | High | `chapters/11_future_directions.md`, MEV-Boost, line 385 | The fallback text implied that a proposer could safely switch payloads after signing a blinded header. | Stated that fallback must be selected before signing and that late substitution risks equivocation. | [MEV-Boost block proposal](https://docs.flashbots.net/flashbots-mev-boost/architecture-overview/block-proposal), [MEV-Boost risks](https://docs.flashbots.net/flashbots-mev-boost/architecture-overview/risks) | Fixed |
| P1, Major | High | `chapters/11_future_directions.md`, Across, line 401 | The one-of-N honest-monitor statement omitted the separate DVM decision assumption after a dispute. | Separated dispute detection and initiation from UMA token-holder resolution and bond settlement. | [Across security model](https://docs.across.to/introduction/security) | Fixed |
| P2, Moderate | High | `chapters/03_layer_1_vs_layer_2.md`, taxonomy, lines 56 to 90 | Sharding, channels, Plasma, optimistic rollups, and validity rollups were accurate only at survey level and omitted key assumptions. | Rewrote the entries around assigned work, participant and monitoring constraints, exit games, data publication, challenge assumptions, circuit scope, upgrades, and settlement. | [Lightning paper](https://lightning.network/lightning-network-paper.pdf), [Plasma paper](https://plasma.io/plasma.pdf), [Ethereum validity rollups](https://ethereum.org/developers/docs/scaling/zk-rollups/) | Fixed |
| P2, Moderate | High | `chapters/04_layer_1_on_chain_scalability.md`, IBC trace, line 173 | The text described only ordered and unordered channels. | Added `ordered_allow_timeout` and distinguished its receive-or-timeout sequencing from strict ordered-channel closure. | [ICS-004](https://docs.cosmos.network/ibc/latest/spec/core/ics-004-channel-and-packet-semantics/README) | Fixed |
| P2, Moderate | High | `chapters/08_data_availability_scaling.md`, Sampling Probability, line 258 | Sampling independence was described too loosely and could suggest that one malicious peer merely weakens confidence numerically. | Explained that selective service violates the fixed hidden-set model and added custody, peer diversity, authenticated coding, and incompatible-view concerns. | [Fraud and Data Availability Proofs](https://arxiv.org/abs/1809.09044), [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594) | Fixed |
| P2, Moderate | High | `chapters/02_blockchain_trilemma.md`, Ethereum trace, line 125 | The EVM was said to apply every transfer in a way that blurred protocol balance updates and recipient bytecode execution. | Distinguished externally owned account transfers from calls to contract recipients. | [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf), [Ethereum transactions](https://ethereum.org/developers/docs/transactions/) | Fixed |
| P2, Moderate | High | `chapters/06_rollups.md`, lines 69 to 90 | Named projects preceded the generic rollup lifecycle, forcing a student to infer generic stages from implementation detail. | Moved the generic lifecycle and completion-boundary figure before Arbitrum and ZKsync traces. | Student review; internal dependency analysis | Fixed |
| P2, Moderate | High | `chapters/01_introduction.md`, first-use terminology; related Chapters 3, 9, 10, and glossary | TPS, EVM, NFT, BoLD, BFT, DAG, RPC, and ABCI were used without adequate first-use expansion in the learning sequence. | Expanded each acronym at first use and added an RPC glossary entry that distinguishes endpoint responses from consensus evidence. | Internal terminology audit | Fixed |
| P2, Moderate | High | All twelve `assets/course/*.svg` files and `STYLE.md`, Figures | SVG source files lacked internal accessibility metadata. | Added `title` and `desc` elements to every course SVG and made the requirement explicit in the style guide. | Internal accessibility audit | Fixed |
| P3, Minor | High | `chapters/01_introduction.md`, `chapters/15_figure_credits.md`, Chapter 6 figure order | Figure 1 was numbered 1.4, and Chapter 6 figure numbering did not support the corrected teaching order. | Corrected Figure 1.1 and made the lifecycle Figure 6.1 and named rollup traces Figure 6.2 in text and credits. | Internal figure audit | Fixed |
| P2, Moderate | High | `book.toml`, lines 1 to 15; `README.md`; `RELEASE.md` | mdBook 0.5.4 rejected the obsolete multilingual key and canonical repository links used the previous owner. | Removed the obsolete key and updated release, clone, canonical-source, repository, and edit URLs. | [mdBook documentation](https://rust-lang.github.io/mdBook/), [canonical repository](https://github.com/neilstripe/Blockchain-Scalability-Book) | Fixed |
| P2, Moderate | High | `scripts/build-pdf.sh`, browser discovery and isolation | The script did not discover macOS Chrome and could reuse a desktop browser profile. | Added macOS application discovery and an isolated temporary profile with background services disabled. The managed Chrome process still failed to finish the large print render in this environment. | Local execution evidence | Partially fixed |

## 4. Files Changed

1. `README.md`: corrected release and clone URLs. This is mechanical and does not change teaching outcomes.
2. `RELEASE.md`: corrected the canonical repository URL. This is mechanical and does not change teaching outcomes.
3. `STYLE.md`: strengthened finality language and SVG accessibility requirements. This affects terminology discipline across future editions.
4. `book.toml`: restored mdBook 0.5.4 compatibility and corrected repository links.
5. `scripts/build-pdf.sh`: added macOS Chrome discovery and isolated headless-profile handling. The environmental render hang remains documented.
6. `qa/citation-audit-0.9.0.md`: updated the audit to the final 95-link result and current source mix.
7. `qa/academic-review-2026-09-02.md`: records the two review passes, corrections, sources, scorecards, and verification results.
8. `chapters/01_introduction.md`: corrected Figure 1.1 and expanded first-use terminology. This improves entry-level readability.
9. `chapters/02_blockchain_trilemma.md`: clarified Ethereum execution, MEV terminology, and unqualified security language. This sharpens architectural comparison.
10. `chapters/03_layer_1_vs_layer_2.md`: deepened sharding, channel, Plasma, optimistic-rollup, and validity-rollup definitions. Related references were added.
11. `chapters/04_layer_1_on_chain_scalability.md`: updated PeerDAS and IBC, corrected cross-shard atomicity, and added the committee-capture calculation. Related questions and solutions were updated.
12. `chapters/05_layer_2_off_chain_scalability.md`: updated the Polygon Chain case and its security boundary.
13. `chapters/06_rollups.md`: separated proof acceptance from settlement, improved withdrawal semantics, and moved the generic lifecycle before named cases. Figures and credits were updated.
14. `chapters/07_modular_vs_monolithic.md`: corrected the maturity label and claims for OP Stack Alt-DA with Celestia.
15. `chapters/08_data_availability_scaling.md`: updated PeerDAS, EigenDA assumptions, DAS sampling language, and Avail sources.
16. `chapters/09_parallel_execution.md`: replaced the older Sui path model with Mysticeti-FPC and Mysticeti-C and updated comparison tables.
17. `chapters/10_consensus_scaling.md`: corrected finality, HotStuff commitment, Sui Mysticeti, and comparison-table assumptions.
18. `chapters/11_future_directions.md`: updated PeerDAS, MEV-Boost fallback, Across dispute resolution, and end-to-end security wording.
19. `chapters/12_glossary.md`: corrected finality, challenge period, and QC entries and added PeerDAS, fast path, and RPC.
20. `chapters/13_review_questions.md`: added quantitative and failure-analysis questions with solution sketches for the corrected mechanisms.
21. `chapters/15_figure_credits.md`: synchronized Figure 1.1, Figure 6.1, Figure 6.2, and Figure 11.1 credits.
22. `assets/course/ch01_scalability_stack.svg`: added internal title and description metadata.
23. `assets/course/ch02_trilemma_tradeoffs.svg`: added internal title and description metadata.
24. `assets/course/ch03_l1_l2_architecture.svg`: added internal title and description metadata.
25. `assets/course/ch04_sharding_receipt.svg`: added internal title and description metadata.
26. `assets/course/ch05_channel_state_machine.svg`: added internal title and description metadata.
27. `assets/course/ch06_named_rollup_traces.svg`: added internal title and description metadata.
28. `assets/course/ch06_rollup_lifecycle.svg`: added internal title and description metadata.
29. `assets/course/ch07_modular_message.svg`: added internal title and description metadata.
30. `assets/course/ch08_das_sampling.svg`: added internal title and description metadata.
31. `assets/course/ch09_parallel_scheduler.svg`: added internal title and description metadata.
32. `assets/course/ch10_hotstuff_flow.svg`: added internal title and description metadata.
33. `assets/course/ch11_appchain_tradeoff.svg`: added internal title and description metadata.

`SUMMARY.md`, the Preface, the practitioner evaluation handbook, the threat-model worksheets, and the benchmark reporting template were reread but did not require a supported content correction. Their existing sequencing and graduate-level tasks remain consistent with the corrected chapters.

## 5. Chapter Scorecard

| Chapter | Correctness | Readability | Depth | Exercises | Remaining concern |
| --- | ---: | ---: | ---: | ---: | --- |
| Preface | 4.9 | 4.9 | 4.5 | Not applicable | The reading-path choices remain important because the complete book is long. |
| 1. Introduction | 4.8 | 4.8 | 4.7 | 4.8 | Historical incident links hosted on Medium require browser review. |
| 2. Blockchain Trilemma | 4.8 | 4.7 | 4.8 | 4.8 | Concentration measurements remain time-sensitive by definition. |
| 3. Layer 1 vs Layer 2 | 4.8 | 4.8 | 4.6 | 4.8 | The chapter is a taxonomy and appropriately defers implementation depth. |
| 4. Layer 1 Scalability | 4.9 | 4.6 | 4.9 | 4.9 | The chapter is dense and benefits from instructor-selected subsections. |
| 5. Layer 2 Scalability | 4.8 | 4.7 | 4.8 | 4.8 | Named bridge and sidechain configurations can change. |
| 6. Rollups | 4.9 | 4.6 | 5.0 | 5.0 | At 1,493 lines, it should normally be taught across several sessions. |
| 7. Modular vs Monolithic | 4.8 | 4.6 | 4.9 | 4.8 | Every real deployment still requires configuration-specific verification. |
| 8. Data Availability | 4.9 | 4.7 | 4.9 | 4.9 | Two EigenDA sources use bot protection and need manual release review. |
| 9. Parallel Execution | 4.9 | 4.8 | 4.9 | 4.9 | Sui implementation terminology is likely to continue evolving. |
| 10. Consensus Scaling | 4.9 | 4.7 | 5.0 | 5.0 | Students need introductory distributed-systems preparation before this chapter. |
| 11. Future Directions | 4.7 | 4.6 | 4.8 | 4.9 | This chapter has the highest rate of maturity and roadmap change. |
| Glossary and questions | 4.9 | 4.9 | 4.8 | 5.0 | Recheck glossary synchronization when protocol terms change. |
| Practitioner materials | 4.9 | 4.8 | 5.0 | 5.0 | Effective use requires access to realistic workloads and fault-injection environments. |

## 6. Deferred Issues

### PDF rendering in the current environment

Status: Deferred, environment verification required.

The PDF script now discovers the macOS Chrome application and uses an isolated temporary profile. HTML generation completed, but managed Chrome did not finish `--print-to-pdf` after more than 600 seconds. The process was stopped and no PDF artifact was produced. The author should run the script in the release environment with a known headless Chromium version and inspect page breaks, formulas, tables, and figure sizing before publishing a PDF.

### Manual browser review of HTTP 403 sources

Status: Deferred, release verification required.

Six authoritative or first-party destinations returned HTTP 403 to automated HEAD requests: the ACM DOI, the NUS BLOCKBENCH paper, two EigenDA documentation pages, and two official Medium posts. The checker accepts 403 responses by policy, and no URL returned a failing status. A human browser check remains required before release.

No content issue was deferred for an author decision. If a future source conflicts with a dated maturity label, the new evidence should replace the dated statement rather than be added as an undifferentiated disclaimer.

## 7. Verification Results

| Check | Result |
| --- | --- |
| `python3 scripts/check-book.py` | Passed: 21 summary entries and 12 figures; no missing local links, duplicate figure numbers, or footnote-definition mismatches. |
| `mdbook --version` | `mdbook v0.5.4`. |
| `./scripts/build-book.sh` | Passed. Generated `book/index.html` and `book/print.html`. |
| `./scripts/check-links.sh` | Passed under repository policy. Checked 95 destinations: 89 HTTP 2xx, 6 HTTP 403, 0 failures. |
| Rendered HTML structural audit | Passed: 22 H1 elements, 391 H2 elements, 48 tables, 12 images, and 1,192 identifiers. No missing image alt text, duplicate identifiers, missing internal anchor targets, stale Figure 1.4, or stale “proof finality” phrase. |
| SVG accessibility audit | Passed for all 12 files. Every SVG has an internal `title` and `desc`. |
| Finality terminology search | Passed. Remaining “instant finality” use is explicitly decomposed into confirmation, proof acceptance, and settlement finality. |
| Throughput-claim search | Passed. Numerical throughput examples state or request workload, hardware, resource, latency, or completion context. |
| `./scripts/build-pdf.sh` | Did not complete under managed macOS Chrome. HTML rebuilt successfully; PDF generation was stopped after the second attempt exceeded 600 seconds. |

The final content diff contains targeted replacements, added evidence and exercises, accessibility metadata, and one moved lifecycle section. The review found no accidental deletion of substantive teaching material.

## 8. Evidence Excerpts for Central Corrected Claims

1. PeerDAS mechanism and reconstruction. [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594) states: “PeerDAS ... allows nodes to perform data availability sampling ... while downloading only a subset of the data,” and “A node can reconstruct the entire data matrix if it acquires at least 50% of all the columns.”
2. PeerDAS deployment date. The [Fusaka mainnet announcement](https://blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement) states: “The Fusaka network upgrade is scheduled to activate on the Ethereum mainnet ... December 3, 2025,” and identifies PeerDAS as the headlining feature.
3. HotStuff commitment. The [HotStuff paper](https://arxiv.org/html/1803.05069v4) states: “Finally, if b* forms a Three-Chain, the commit phase of b has succeeded, and b becomes a committed decision.”
4. Mysticeti fast-path evidence. The [Mysticeti paper](https://docs.sui.io/paper/mysticeti.pdf) states that a transaction is certified after `2f + 1` votes from distinct validators and is finalized either through `2f + 1` validators supporting a certificate or through a Mysticeti-C commit containing that certificate in its causal history.
5. Current Sui general path. The [Sui transaction lifecycle](https://docs.sui.io/concepts/sui-architecture/transaction-lifecycle) states: “All transactions are sequenced by Sui's Mysticeti DAG consensus,” and separately describes certified effects and certified checkpoints as finality evidence.
6. OP Alt-DA maturity. The [OP Stack specification](https://specs.optimism.io/experimental/alt-da.html) states: “Alt-DA Mode is a Beta feature ... still undergoing testing, and may have bugs or other issues.”
7. IBC channel ordering. [ICS-004](https://docs.cosmos.network/ibc/latest/spec/core/ics-004-channel-and-packet-semantics/README) states that an `ordered_allow_timeout` channel processes packets in order, permits a timed-out packet to execute its timeout logic, continues with later packets, and does not close on timeout.
8. EigenDA threshold relationship. The [EigenDA security-parameter specification](https://layr-labs.github.io/eigenda/protocol/architecture/security-parameters.html) requires `ConfirmationThreshold - SafetyThreshold >= ReconstructionThreshold`.
9. Across dispute boundary. The [Across security model](https://docs.across.to/introduction/security) states that a disputed bundle is escalated to UMA's Data Verification Mechanism and that UMA token holders vote on whether it was valid.
10. MEV-Boost operational assumptions. The [Flashbots risk documentation](https://docs.flashbots.net/flashbots-mev-boost/architecture-overview/risks) identifies liveness and local fallback, builder centralization, builder and relay collusion, malicious relays, and MEV hiding as separate risks.
11. Polygon architecture. The [Polygon Chain overview](https://docs.polygon.technology/pos/overview) states that Polygon Chain has two operating layers: Heimdall as the consensus layer and Bor as the execution layer.

## 9. Final Teaching Verdict

The corrected HTML book is ready for classroom use. Its strongest qualities are the explicit separation of execution, ordering, proof, data availability, settlement, finality, and recovery; the repeated use of end-to-end traces; and the combination of mathematical, adversarial, and operational exercises.

Its most serious remaining weakness is not conceptual correctness but breadth and maintenance cost. Several long chapters combine material that would require multiple class meetings, and the deployment-heavy sections need a dated source audit before each edition. The unverified PDF artifact is also a release blocker for print distribution, although it does not block use of the HTML edition.

The expected student background is data structures, computer networking, introductory distributed systems, public-key signatures, cryptographic hashes, transactions, and smart contracts. Familiarity with probability, queues, and basic performance measurement is helpful; the book supplies the blockchain-specific vocabulary.

The material has sufficient depth for a one-semester master's course. A practical syllabus should use Chapters 1 to 3 as foundations, select core sections from Chapters 4 to 10 for weekly technical units, use Chapter 11 as a research seminar, and assign the threat-model and benchmark artifacts as recurring laboratories.
