# Instructor and Course Adoption Guide

## Why Use This Book

*Mastering Blockchain Scalability* treats scalability as a resource, systems, security, and recovery problem. It is designed for courses that need more than a list of protocols or a comparison of advertised transactions-per-second figures. Students trace complete transaction and failure paths, calculate resource bounds, state trust assumptions, analyze recovery, and evaluate benchmark claims.

The complete web and PDF editions are free. Instructors can assign individual chapters, reuse and adapt the worksheets under CC BY-SA 4.0, and pin a class to a versioned release so page numbers and exercises remain stable.

## Suitable Courses

Neil Han developed the book from his teaching context for SC6019 at Nanyang Technological University (NTU). This is a factual authorship and teaching context, not an NTU endorsement.

The material fits master's-level courses in blockchain systems, distributed systems, computer security, cryptography engineering, and computer architecture. It can also support advanced professional training for protocol engineers and technical decision-makers.

## Prerequisites

Students should understand basic data structures, networking, public-key signatures, and asymptotic reasoning. Prior smart-contract development is useful but not required. Chapter 1 establishes the blockchain transaction, state, execution, consensus, finality, safety, and liveness vocabulary used later.

## Learning Outcomes

After completing the core sequence, students should be able to:

1. decompose a scalability claim into execution, bandwidth, storage, state, data-availability, and consensus constraints;
2. trace normal and failure paths through L1, L2, rollup, bridge, and modular systems;
3. identify security, trust, liveness, governance, and recovery assumptions;
4. reproduce throughput, sampling, committee, and contention calculations with explicit units;
5. distinguish execution throughput from consensus throughput and data publication from archival storage;
6. design an honest benchmark and identify misleading comparisons;
7. compare systems using threat models and operational recovery rather than headline TPS.

## Proposed 12-Week Sequence

| Week | Topic | Reading | Applied work |
|---|---|---|---|
| 1 | What scalability means | Preface, Chapter 1 | Decompose one TPS claim into resources and assumptions |
| 2 | Trilemma and measurement | Chapter 2 | Calculate node and committee costs under two designs |
| 3 | L1 and L2 boundaries | Chapter 3 | Trace who verifies, orders, stores, and recovers |
| 4 | L1 execution and sharding | Chapter 4 | Analyze cross-shard receipts and failure states |
| 5 | Channels, sidechains, and Plasma | Chapter 5 | Build a dispute and timeout state machine |
| 6 | Optimistic and validity rollups | Chapter 6 | Compare proof, data, bridge, and forced-exit paths |
| 7 | Modular architectures | Chapter 7 | Map settlement, execution, ordering, and DA providers |
| 8 | Data availability | Chapter 8 | Work an erasure-coding and sampling calculation |
| 9 | Parallel execution | Chapter 9 | Measure contention and scheduler behavior |
| 10 | Consensus scaling | Chapter 10 | Compare quorum, finality, and communication costs |
| 11 | Evaluation and benchmarking | Chapters 14, 16, 17 | Audit a public benchmark or architecture claim |
| 12 | Synthesis and future directions | Chapter 11, review questions | Present a capstone architecture and recovery plan |

For a 13-week term, split Week 6 into optimistic rollups and validity rollups, or reserve the final week for capstone defenses.

## Assessment Options

- **Mechanism memos:** short analyses that draw the normal path, failure path, and recovery boundary of a named system.
- **Calculation labs:** reproduce a worked example with changed parameters, units, and sensitivity analysis.
- **Benchmark audit:** evaluate workload, hardware, state, network, finality, fault model, and omitted costs.
- **Threat-model review:** use the worksheets to test a bridge, rollup, DA layer, or execution system.
- **Capstone:** propose a scalable architecture for a specified workload and defend its security and recovery tradeoffs.

The repository includes graduate-level review questions and solution sketches. Instructors should avoid publishing full solutions in a public course repository when those questions are graded.

## Primary-Source Policy

Protocol details change. Course staff should check cited specifications, repositories, governance documents, and production status before each term. Students should date every time-sensitive claim and distinguish specification, implementation, testnet, mainnet, and roadmap evidence.

## Review Copies and Course Use

The free versioned release is the instructor review copy: https://github.com/neilydhan/Blockchain-Scalability-Book/releases/latest

For a syllabus review, correction, or course-adoption discussion, open a GitHub issue with the label or title prefix `course adoption`. Do not include student personal data or private course records. A private instructor contact route will be added only after the author approves its account and data-handling process.

## Recommended Citation

> Han, Neil. *Mastering Blockchain Scalability*. Version 1.1.1, 2026. GitHub. https://github.com/neilydhan/Blockchain-Scalability-Book/releases/tag/v1.1.1
