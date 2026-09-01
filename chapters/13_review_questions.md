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
