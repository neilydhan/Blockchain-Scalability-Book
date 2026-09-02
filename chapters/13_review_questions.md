# **Review Questions and Design Exercises**

These questions are designed to test reasoning, not recall. A strong answer states its assumptions and distinguishes normal operation from failure recovery.

## **Basic-Knowledge Warm-Up**

Use these questions before the chapter exercises. A reader should be able to answer them in plain language; formulas and protocol names are optional.

1. What is the difference between blockchain history and current state?
2. Why do many nodes repeat transaction checks instead of trusting one database?
3. What is the difference between a block being included and a transaction being final?
4. What evidence does a digital signature provide, and what does it not prove about a transaction's validity?
5. Why can raising transactions per second make latency or decentralization worse?
6. Explain safety and liveness using a system that must choose between halting and accepting conflicting payments.
7. Why is a sidechain bridge a separate security boundary?
8. In a payment channel, why must each participant keep the newest signed state?
9. What does a rollup post to its settlement or DA layers, and why is a state root alone insufficient for recovery?
10. Explain the difference between an optimistic fault proof and a validity proof.
11. Why can a validity proof establish correctness without establishing data availability?
12. Give an example of two transactions that can execute in parallel and two that conflict.
13. Why do two BFT quorums need to overlap in an honest participant?
14. For any future scaling claim, name one assumption and one failure state a wallet should expose.

### Warm-up answer guide

1. History is the ordered record of past blocks and transactions; state is the latest live balances, ownership, and contract data.
2. Replication lets independent parties detect an invalid update or dishonest operator, at the cost of repeated work.
3. Inclusion places a transaction in a current canonical candidate; finality adds evidence or depth that makes reversal forbidden or sufficiently unlikely under a stated model.
4. A signature proves authorization by the corresponding key for the signed bytes. It does not prove sufficient balance, correct contract execution, inclusion, or finality.
5. Larger or faster blocks can take longer to propagate and demand stronger hardware; batching can increase throughput while individual users wait longer.
6. Safety prevents two conflicting payments from both becoming accepted. Liveness ensures valid payments eventually progress. A partition may force a protocol to halt to preserve safety.
7. The bridge decides which sidechain evidence releases assets elsewhere. The base chain does not automatically verify every sidechain transition.
8. An old state may assign balances differently. The newest signature, revocation rule, or monotonic sequence is evidence against stale settlement.
9. A rollup posts ordered data or its commitment, state claims, and proof/dispute evidence according to its design. A root binds values but does not reveal them.
10. An optimistic system accepts after a challenge window unless a challenger proves a fault. A validity system requires a compact proof of correct execution before acceptance.
11. A verifier can check a proof over hidden or missing inputs without those inputs being available for users to reconstruct future state.
12. Transfers over disjoint accounts can run together; two transactions writing one balance or reading a value another writes conflict.
13. Overlap plus honest voting rules prevents certificates for incompatible commits under the fault bound.
14. Acceptable answers include a sequencer outage and "forced-inclusion pending," prover delay and "unproven," or bridge finality delay and "not withdrawable."

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

## **Instructor Notes and Solution Sketches**

These sketches identify the reasoning a strong answer should contain. They are not unique solutions. Quantitative answers should retain units and state assumptions.

### Chapters 1-2

A credible throughput comparison fixes transaction semantics, state size, offered-load curve, duration, hardware, network topology, validator independence, completion boundary, and fault behavior. Throughput can rise while latency worsens when batching waits longer, queues grow near saturation, or finality requires more stages. Adding replicas to a fully replicated state machine adds fault tolerance and read capacity, but each replica still executes the same ordered writes.

For the order-book benchmark, vary the number of markets, price-level concentration, cancellation ratio, market-order depth, account skew, and burst arrival. Hot price levels reveal serial state. A protocol improves the trilemma frontier when it lowers production or verification cost without changing the claim being measured; it only moves cost when it replaces broad verification with a committee, operator, expensive recovery path, or hidden subsidy.

### Chapters 3-5

An L1 transfer is complete under the L1's finality rule. A rollup transfer passes sequencer, publication, proof or challenge, and settlement milestones. A sidechain transfer follows its own consensus, and its bridge adds another finality rule.

Cross-shard execution is asynchronous because independent committees cannot atomically lock all state without coordination that erodes parallelism. The destination authenticates the source receipt and stores a consumed nonce or message identifier. Smaller committees improve parallel capacity while increasing capture probability. In a state channel, signatures authenticate updates and a monotonic nonce selects the newest state. Payment routes need directional balance on every hop, not only graph connectivity.

Operator failure has different effects: a channel counterparty can delay cooperative close but the adjudicator preserves funds; a sidechain bridge compromise may violate safety; a sequencer outage should affect liveness if forced inclusion and exit remain intact.

### Chapters 6-8

An optimistic rollup has fast soft confirmation but final state waits through publication, challenge, and settlement. A validity rollup replaces the challenge period with proof generation and verification, while settlement finality still comes later. A validity proof establishes a transition statement; unavailable inputs can still prevent users from reconstructing state or exiting.

A minimum escape path authenticates forced transactions through L1, defines a bounded inclusion deadline, and permits state advancement or withdrawal without the sequencer. For an external DA design, the DA layer can prove that bytes were ordered and available under its rules; settlement verifies only the commitment or proof its contract understands.

If each independent sample has probability `1/2` of missing a half-hidden block, 15 samples all miss with probability:

```text
(1/2)^15 = 1/32768 ≈ 0.00305%
```

The calculation assumes uniform unpredictable samples, independent observations, valid encoding, honest header authentication, and peers that cannot selectively identify and deceive the sampler.

A wallet should distinguish waiting for sequencing, data publication, proof, settlement finality, and destination execution. "Pending" alone does not tell a user whether retrying is safe.

### Chapters 9-10

One conflict example is `T1: read A, write B`; `T2: read C, write D`; `T3: read B, write C`. `T1` and `T2` can speculate together from the same snapshot, while `T3` depends on both and must wait or retry. A parallel schedule must commit a state equivalent to canonical order; otherwise validators can calculate different roots from identical blocks.

Reduce contention by partitioning per-player or per-market state, replacing one global counter with mergeable local counters, and avoiding synchronous writes to shared metadata. In a four-replica BFT system, two quorums of three intersect in two replicas; with at most one Byzantine, at least one overlap is honest. Pipelining overlaps different consensus stages across blocks, improving steady-state block rate without shortening one block's commit chain.

HotStuff assumes eventual network bounds for liveness and tolerates fewer than one-third Byzantine replicas in the common model. A synchronous variant uses a known bound and derives different protocol guarantees from that stronger assumption. Benchmarks must include payload dissemination and leader failures because empty-block voting hides bandwidth and view-change cost.

### Chapter 11

A dependency graph should show user, solver, sequencer, execution rollup, DA network, prover, settlement chain, and destination bridge. Each edge needs authenticated data, finality, timeout, and recovery. Shared sequencing can concentrate order flow; proof markets can concentrate specialized hardware and witness access; solver markets can concentrate routing and censorship power.

Chain abstraction is safe when the interface hides mechanics but still exposes assets, maximum spend, destination, finality status, fees, and recovery. A multi-rollup benchmark fixes workload and route, records every domain boundary, and ends at a named milestone such as settlement finality or destination execution rather than the first sequencer response.

### Quantitative Laboratory

With 2,000 transactions every 10 seconds, offered throughput is:

```text
2,000 / 10 s = 200 transactions/s
```

The mean compressed data rate is:

```text
120 kB / 10 s = 12 kB/s
```

One proof job consumes 24 prover-seconds and arrives every 10 seconds, so minimum steady capacity is `24/10 = 2.4` workers. Three workers give only 80 percent utilization under uniform jobs and no failures. Four workers give 60 percent and more useful headroom. A production answer should examine proof-time variance, aggregation, restart cost, and correlated hardware loss.

The bridge should normally wait for proof acceptance plus the chosen settlement finality, not sequencer receipt. Forced inclusion needs the signed transaction, evidence or timing rule showing the sequencer deadline expired, and enough L1 capacity to submit it.

If compression worsens by 40 percent, a batch uses `168 kB` and mean data rate becomes `16.8 kB/s`. With a fixed 12 kB/s limit, only about `12/16.8 = 71.4%` of the former transaction rate fits, or roughly 143 transactions/s under the same mix. The exact result depends on whether the stated limit was already saturated and whether batch overhead is fixed.

### Capstone Review

A complete capstone has two diagrams: the normal transaction/finality path and the degraded recovery path. It includes capacity arithmetic for execution, data, proving, consensus, and state; a role and key inventory; at least one safety and one liveness failure per external dependency; a measured mass-recovery test; and a clear statement of the accepted trade-off.
