# **Review Questions and Design Exercises**

These questions are designed to test reasoning, not recall. A strong answer states its assumptions and distinguishes normal operation from failure recovery.

## **Chapters 1-2: Measuring Scalability and the Trilemma**

1. A chain reports 50,000 TPS. What information is needed before comparing it with Ethereum or a rollup?
2. Explain how throughput can increase while user latency becomes worse.
3. Why does adding validators to a fully replicated state machine improve redundancy without necessarily improving execution capacity?
4. Design a benchmark for an on-chain order book. Which workloads would expose hot-state contention?
5. Give one example in which a protocol improves the trilemma frontier and one in which it merely moves cost to a less visible layer.
6. Which forms of operational centralization are missed by validator count?

## **Chapters 3-5: Layers, Sharding, and Channels**

1. Follow one token transfer through an L1, a rollup, and a sidechain. At which point is each transfer final?
2. Why is a cross-shard transfer naturally asynchronous? What prevents its receipt from being replayed?
3. How does committee size affect both throughput and capture probability?
4. A channel counterparty publishes an old signed state. What evidence lets the contract choose the newer state?
5. Why can a payment route have sufficient graph connectivity but insufficient liquidity?
6. Compare the failure of a channel operator, a sidechain bridge, and a rollup sequencer. Which failures threaten safety and which threaten liveness?

## **Chapters 6-8: Rollups, Modularity, and Data Availability**

1. Separate sequencer confirmation, proof finality, and L1 finality for an optimistic and validity rollup.
2. Why does a validity proof not prove that users can reconstruct the state?
3. Describe the minimum escape hatch needed when a sequencer censors a withdrawal.
4. A modular rollup uses Celestia for data and Ethereum for settlement. What can each layer prove, and what can it not prove?
5. Derive the probability that 15 independent samples miss an attack hiding half the shares.
6. Compare L1 blobs, an external DA network, and a DAC across cost, validator integration, and withholding risk.
7. What observability should a wallet expose when a modular transaction is delayed?

## **Chapters 9-10: Parallel Execution and Consensus**

1. Construct three transactions where two can run in parallel and the third must retry. Identify all read/write conflicts.
2. Why is deterministic commitment required even if thread scheduling is nondeterministic?
3. Suggest two state-model changes that reduce contention in an on-chain game.
4. In a four-replica BFT system tolerating one Byzantine replica, explain why two quorums of three intersect in an honest replica.
5. How does pipelining improve throughput without reducing a transaction's finality latency?
6. Compare the network assumptions and fault thresholds of HotStuff and Sync HotStuff.
7. Why should consensus benchmarks include block payload and leader failures?

## **Chapter 11: Future Architecture**

1. Draw the dependency graph of a transaction using a solver, shared sequencer, validity rollup, external DA layer, and Ethereum settlement.
2. For each edge, identify a safety failure, a liveness failure, and a recovery mechanism.
3. What new concentration risks can shared sequencing or proof markets create?
4. How can chain abstraction hide complexity without hiding security assumptions?
5. Propose a reproducible benchmark for a multi-rollup system. Which finality boundary ends the timer?

## **Capstone Design Exercise**

Design a blockchain architecture for one of the following:

- a global micropayment network;
- an on-chain game with one million daily players;
- a high-value exchange with a central limit order book;
- a public registry whose data must remain retrievable for decades.

Your design must state:

1. transaction workload and latency target;
2. execution environment and concurrency model;
3. ordering and consensus mechanism;
4. settlement and finality rule;
5. data availability and archival strategy;
6. bridge or messaging assumptions;
7. upgrade and emergency controls;
8. user exit or recovery path;
9. benchmark method and hardware disclosure;
10. the trilemma cost the design accepts.

## **Quantitative Laboratory: Capacity and Finality**

Assume a rollup posts one batch every 10 seconds. Each batch contains 2,000 transactions, consumes 120 kB of compressed data, and takes a prover 24 seconds on one machine. The settlement chain finalizes a posted batch after 12 minutes. The sequencer has a 20-second forced-inclusion deadline.

1. Compute offered throughput when every batch is full.
2. Compute the sustained data rate in bytes per second, excluding commitment overhead.
3. How many independent prover workers are required to prevent an unbounded proof queue under steady load? Include utilization headroom rather than giving only the mathematical minimum.
4. Draw the user-visible milestones for sequencer receipt, batch publication, proof acceptance, and settlement finality.
5. Which milestone should a bridge use before releasing a high-value withdrawal, and why?
6. If the sequencer stops immediately after receipt, what evidence and deadline does a user need to invoke forced inclusion?
7. Repeat the capacity calculation when average compression worsens by 40 percent and the settlement data limit is fixed.

A strong submission shows units, separates offered load from completed throughput, and names assumptions about proof aggregation and parallelism.

## **Fault-Injection Laboratory**

Run an implementation or simulator through this sequence:

1. operate at 60 percent of measured saturation for ten minutes;
2. disconnect the current consensus leader for two views;
3. delay 10 percent of data chunks beyond their normal retrieval deadline;
4. stop the primary prover while proofs are queued;
5. submit one malformed cross-domain message and one replay;
6. restore all components without deleting persistent state.

Record p50, p95, and p99 latency; queue depth; time to view change; data-repair traffic; proof backlog; finalized height; and every user-visible status transition. The report must identify whether each fault affected safety, liveness, latency, or only cost. It must also explain which component detected the fault and which component initiated recovery.

## **Design Review Rubric**

Evaluate the capstone on five dimensions, each from 0 to 4:

- **Explicit assumptions:** network, trust, workload, finality, and failure assumptions are testable.
- **End-to-end correctness:** the transaction, message, withdrawal, and recovery paths are internally consistent.
- **Quantitative evidence:** calculations retain units, benchmarks reach saturation, and latency distributions are reported.
- **Adversarial depth:** censorship, withholding, equivocation, reorganization, upgrade compromise, and correlated outages are addressed.
- **User recovery:** escape paths are available, affordable under congestion, observable, and exercised in tests.

A score of 0 means the issue is absent. A score of 2 means it is described but not measured or tested. A score of 4 means another team could reproduce the evidence and challenge the assumptions.
