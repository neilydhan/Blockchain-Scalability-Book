# **Chapter 1: Understanding Blockchain Scalability Challenges**

## **Introduction**

Blockchain scalability is the ability to support increasing useful demand while keeping verification, participation, and failure recovery within acceptable resource and latency bounds. The definition deliberately includes more than transactions per second. It asks what work completed, when it became final, which machines and operators were required, and what happens when a component fails.

Public blockchains combine replicated execution and storage with adversarial consensus. That redundancy lets users verify shared state without trusting one database operator, but it also makes capacity expensive. The techniques in this book divide, compress, schedule, or prove the work while trying to preserve that independent check.

---
## **Why Naive Comparisons Fail**

A payment network, an exchange database, and a public blockchain perform different work under different trust assumptions. A card network may authorize a payment quickly while settlement, fraud handling, and bank reconciliation occur later. A public blockchain validates signatures, executes shared state, propagates data, and reaches Byzantine consensus before offering its strongest finality.

This does not make performance comparison useless. It means the comparison must hold the workload and completion boundary constant. A transfer-only TPS figure cannot be compared with arbitrary smart-contract execution. A sequencer acknowledgement cannot be compared with L1 finality. A laboratory cluster cannot be compared with a geographically distributed validator network without reporting the difference.

The immediate symptoms of insufficient capacity are familiar: transactions wait, fee markets rise, users retry, and applications become unreliable. Historic events such as the CryptoKitties congestion episode made those symptoms visible. Their precise fees and shares of network traffic are less important than the mechanism: demand exceeded scarce blockspace, so inclusion latency and price rose together.

## **Gas and the Price of Shared Computation**

Ethereum meters execution in **gas**. Every operation consumes a defined gas amount, and a transaction supplies a gas limit that bounds its work. This prevents a Turing-complete program from consuming validator resources forever.

Since EIP-1559, an Ethereum transaction pays a protocol-determined **base fee** that is burned and may add a **priority fee** to reward inclusion. The base fee changes with block utilization. The transaction's execution payment is approximately:

> `gas used × (base fee + priority fee)`

Blob-carrying transactions use a separate blob fee market. This separation matters for scaling: rollup data demand can change without pricing every EVM operation identically.

Gas is both metering and congestion pricing. It approximates execution and state cost well enough for the protocol to ration resources, but it is not a perfect hardware benchmark. An opcode's gas schedule is a governance and security parameter, while actual client performance changes with software and hardware.

## **Case Study: Congestion and Application Design**

When one popular application fills blocks, every application sharing the fee market competes for the same capacity. Users who need immediate inclusion bid more; users with low-value actions wait or leave. This is the practical consequence of synchronous composability: applications share one state and can interact atomically, but they also share congestion.

Scaling designs respond differently. A larger L1 block admits more shared activity but raises validator load. An application-specific chain isolates congestion but fragments state and security. A rollup batches application execution and shares the cost of data publication. A state channel avoids publishing repeated interactions but works only for a constrained participant set.

The right design depends on whether the application needs global synchronous state, how valuable its assets are, what latency users need, and how they recover from operator failure.

## **From Database Benchmarks to Blockchain Benchmarks**

Database benchmarks show why a workload must be specified. TPC-C, analytical queries, and key-value workloads exercise different resources. A result becomes meaningful through a transaction mix, dataset, concurrency, duration, hardware, tuning policy, and latency objective.

Blockchain evaluation keeps those controls and adds consensus topology, state replication, signature work, adversarial faults, finality, and recovery. BlockBench helped separate consensus, data, and execution behavior in permissioned blockchains.[^2] Gas per second is useful for comparing EVM execution because transactions consume different gas, but it remains only one resource metric: gas schedules approximate work and omit network consensus, data availability, proof generation, and long-run state costs.[^3]

The right output is not one universal score. It is an operating envelope showing which workloads a system sustains, on which resources, at which latency and finality boundary, and under which faults.

## **A Scalability Model for This Book**

The word *scalability* has long lacked one universally accepted systems definition.[^1] In blockchain discussions, it is often used when a team really means peak throughput. This book uses a stricter definition:

> A blockchain scales when it can support increasing useful demand while keeping verification, participation, and failure recovery within acceptable cost and latency bounds.

This definition has four consequences. First, the workload must be specified. Ten thousand independent transfers are not equivalent to ten thousand swaps that all modify one liquidity pool. Second, resources must be specified: CPU model, core count, memory, storage, network bandwidth, validator count, and geographic distribution. Third, security must remain comparable. A system that replaces 1,000 independent validators with one database has increased capacity but has not demonstrated blockchain scalability. Fourth, the result must survive failure. Normal-path TPS says little about a sequencer outage, leader change, data withholding attack, or mass exit.

### **Throughput, Latency, and Capacity**

*Throughput* is completed work per unit time. *Latency* is the time one request takes. *Capacity* is the maximum sustainable load before latency or failure rate becomes unacceptable. They interact but are not interchangeable.

A batching system illustrates the distinction. Waiting to collect 1,000 transactions may increase throughput and reduce cost per transaction, but the first user in the batch waits longer. A pipelined consensus protocol may commit one block per round after warming up even though each block needs several rounds to reach finality. Always ask which quantity improved.

### **Vertical and Horizontal Scaling**

Vertical scaling extracts more work from one machine by using faster hardware or better software. Horizontal scaling divides work among machines. Blockchains need both, but horizontal scaling is harder because machines may be faulty or adversarial and must agree on shared state.

A useful mental model is a replicated state machine. If every validator executes every transaction, adding validators increases redundancy and security but does not add execution capacity. Sharding, rollups, and parallel execution change which work is repeated, where it is performed, or how independent work is scheduled.

## **A Transaction as a Resource Vector**

TPS treats every transaction as one unit. In reality, a transaction consumes several resources:

- signature verification and EVM computation;
- state reads and writes;
- bytes propagated across the network;
- bytes retained temporarily or permanently;
- consensus votes and block space;
- proof generation or verification in a validity system.

Represent a workload as a vector rather than a count. A calldata-heavy rollup batch stresses data bandwidth. A zero-knowledge application may stress proving. A hot DeFi contract stresses sequential state access. The sustainable transaction rate is bounded by the first exhausted resource.

Ethereum gas captures part of computation and storage cost, which makes gas per second more informative than transfer TPS. It is still not a universal metric because gas schedules approximate resource usage and exclude consensus and off-chain proving.

## **Worked Example: Benchmarking Two Chains**

Chain A reports 20,000 TPS using simple transfers on eight validator machines in one data center. Chain B reports 4,000 TPS using contract calls across 200 geographically distributed validators. Chain A is faster for the measured workload, but the headline does not establish that its architecture is more scalable.

A fair experiment fixes or reports the transaction mix, validator hardware, network topology, state size, block size, duration, client version, and tolerated failure rate. It measures p50 and p99 latency, not only the average. It runs long enough to expose state growth and database compaction. It introduces a faulty leader or network delay and records recovery.

The output should be a curve. At low load, latency is stable. As offered load approaches capacity, queues form and tail latency rises. Beyond the knee, throughput may flatten while failures increase. The knee of that curve under a realistic workload is more useful than one peak number.

## **The Four-Layer Evaluation Framework**

<p align="center">
  <img src="../assets/course/ch01_scalability_stack.svg" width="760" alt="Execution, settlement, consensus, and data availability">
  <br>
  <em>Figure 1.4: A blockchain transaction depends on execution, settlement, consensus, and data availability. Monolithic chains combine them; modular systems separate some roles. Original figure for this book.</em>
</p>


The chapters ahead repeatedly separate four functions:

1. **Execution** computes state transitions.
2. **Settlement** decides which transition is accepted and resolves disputes.
3. **Consensus** orders data and finalizes a history.
4. **Data availability** ensures that the information needed for verification can be obtained.

A monolithic chain performs all four together. A rollup may execute elsewhere while Ethereum supplies settlement, consensus, and data. A modular DA layer may order and publish data without knowing an application's execution rules. Keeping these functions separate prevents category errors, such as assuming a validity proof also proves data availability or assuming a bridge gives a sidechain Layer 1 security.

## **Security and Decentralization Measurements**

Decentralization is not a raw node count. Nodes operated by one company, hosted in one cloud, or controlled by one key do not provide independent failure domains. Relevant measures include stake or hash-power concentration, client diversity, hosting and geographic distribution, hardware requirements, governance power, and the ability of an ordinary user to verify and exit.

Security should be expressed as an adversary model. What fraction of validators can be Byzantine? Can the attacker delay the network, corrupt participants adaptively, or withhold data? Which guarantees fail first: liveness, safety, censorship resistance, or data retrieval? A protocol is secure only relative to those assumptions.

## **How to Read Performance Claims**

When a project claims a large scalability gain, ask:

- What transactions were executed?
- Was the number measured, simulated, or projected?
- Which hardware and network were used?
- How many independent validators participated?
- Which finality boundary ended the timer?
- Was data publication included?
- Did the test include proof generation, state storage, and failures?
- Can users recover if the normal operator disappears?

These questions do not dismiss performance work. They make results reproducible and comparable.

## **From Transaction Submission to Finality**

A blockchain performance measurement needs a precise start and finish. A transaction passes through construction and signing, RPC admission, peer-to-peer propagation, block inclusion, execution and fork choice, then finality. "Transaction latency" may stop at any one of these boundaries.

A wallet often shows block inclusion because it is fast and useful. A bridge waits for stronger finality because releasing assets against a reverted source transaction can create an unbacked claim. A rollup adds further milestones: sequencer acknowledgement, L2 inclusion, data publication, proof acceptance, and settlement finality.

This path explains why VM throughput is not chain throughput. The result still has to be encoded, propagated, agreed upon, committed to state, indexed, and served back to users.

## **Queueing and the Capacity Knee**

When transactions arrive more slowly than the system processes them, queues remain short. Near capacity, ordinary variance produces bursts faster than blocks or batches can absorb. Waiting time rises even before average demand exceeds average service.

Let work arrive at rate `λ` and be processed at sustainable rate `μ`. A basic queue becomes unstable when `λ ≥ μ`. Blockchains add batches, heterogeneous transactions, and fee priority, but the lesson holds: running continuously at advertised peak throughput creates poor tail latency.

A sound capacity plan reserves headroom for larger witnesses, failed leaders, prover retries, database compaction, and recovery traffic. Fee markets act as admission control. When demand exceeds scarce blockspace, users bid for priority while low-value work waits. The fee spike is the mechanism allocating congestion, not an unrelated symptom.

## **State, History, and Working Sets**

**History** is the ordered record of blocks and transactions. **State** is the latest value of live accounts, contracts, or objects. The **working set** is the portion current execution touches. Pruning history does not shrink live state. Stateless validation reduces a validator's need to store state by supplying witnesses, but a builder or state provider still needs data to produce those witnesses.

Benchmark duration matters because caches hide storage cost. A short test may keep its working set in memory. A long-running chain reads cold state, compacts databases, creates snapshots, and serves synchronization. Sustainable performance includes these tasks.

## **A Reproducible Benchmark Procedure**

1. Define completion: execution, inclusion, optimistic confirmation, proof acceptance, or consensus finality.
2. Publish transaction templates, state size, locality, and conflict rate.
3. Record client commits, protocol parameters, validator count, hardware, geography, and network shaping.
4. Warm representative state under a published rule.
5. Sweep offered load while measuring queue depth, failures, resource usage, fees, and p50/p95/p99 latency.
6. Inject a faulty leader, sequencer outage, delayed region, data withholding event, and prover crash.
7. Report the highest load meeting the latency and error objective, not the largest transient burst.

### **Worked Benchmark: A Rollup Exchange**

Suppose an exchange sees 60% limit-order placements, 30% cancellations, and 10% market orders. Placements write an order and one price level. Market orders can touch many levels and accounts. A transfer benchmark misses this shared state.

A realistic generator samples prices and sizes, creates bursts around market moves, and records sequencer acknowledgement, L2 inclusion, publication, proof completion, and settlement. The first limit may be a hot price level. After partitioning markets, blob publication may dominate. After compression, proof generation may queue. Each optimization requires another end-to-end test.

## **Scalability Claims as Falsifiable Statements**

A useful claim states workload, duration, validator topology, hardware, latency, finality, and failure behavior. "This system sustains the published mixed workload for one hour across 100 distributed validators while p99 finality stays below ten seconds and one leader failure recovers within thirty seconds" can be tested. "Up to 100,000 TPS" cannot.

## **Worked Capacity Envelope**

Assume a chain targets a mixed workload of 70 percent transfers, 20 percent swaps, and 10 percent contract deployments. Measurements on disclosed hardware produce these per-transaction averages:

| Transaction | Execution gas | Published bytes | Net state growth |
|---|---:|---:|---:|
| Transfer | 21,000 | 110 | 16 B |
| Swap | 140,000 | 260 | 80 B |
| Deployment | 1,200,000 | 8,000 | 6,000 B |

The weighted average execution demand is:

```text
0.70 × 21,000 + 0.20 × 140,000 + 0.10 × 1,200,000
= 162,700 gas/transaction
```

The weighted published data is:

```text
0.70 × 110 + 0.20 × 260 + 0.10 × 8,000
= 929 bytes/transaction
```

The weighted state growth is:

```text
0.70 × 16 + 0.20 × 80 + 0.10 × 6,000
= 627.2 bytes/transaction
```

Suppose the measured system sustains 60 million execution gas per second, 500 kB/s of canonical data, and 25 kB/s of acceptable long-run state growth. Each resource implies a different transaction ceiling:

```text
execution: 60,000,000 / 162,700 ≈ 369 tx/s
data:        500,000 / 929     ≈ 538 tx/s
state:        25,000 / 627.2   ≈ 40 tx/s
```

Under these assumptions, long-run state growth is the tightest policy limit even though CPU and block data could support much more short-term throughput. If the state-growth budget is a governance objective rather than a hard protocol limit, the report should say so and project the resulting database size.

At 40 transactions per second, annual net state growth is approximately:

```text
40 × 627.2 B × 31,536,000 s ≈ 791 GB/year
```

That result should trigger questions: can inactive state expire, do updates overwrite existing values rather than add new ones, how large are witnesses, who serves snapshots, and is the 10 percent deployment mix realistic? A surprising calculation is a reason to inspect the workload, not hide the number.

### Add latency and headroom

Capacity is not the same as a safe operating target. If the state database, block propagation, and leader changes become unstable above 70 percent of the measured limit, target load should remain below that knee. Use the minimum across resources after applying their own headroom policies:

```text
safe rate = min(
  execution capacity × execution headroom,
  data capacity × data headroom,
  state budget × state headroom,
  consensus capacity × consensus headroom,
  proving capacity × proving headroom
)
```

Headroom is resource-specific. Data publication may need burst capacity after an outage. Consensus needs time for a failed leader. A prover fleet needs capacity after one worker fails. State growth is cumulative and may need a policy margin rather than an operational utilization target.

### Workload sensitivity

If deployments fall from 10 percent to 1 percent while swaps increase to 29 percent, both average gas and state growth change sharply. Report a sensitivity table instead of one mix:

| Scenario | Transfer | Swap | Deployment | Purpose |
|---|---:|---:|---:|---|
| Typical | 70% | 20% | 10% | Expected mean |
| Mature application | 70% | 29% | 1% | Fewer deployments |
| Launch burst | 45% | 35% | 20% | Contract-heavy stress |
| Hot market | 20% | 80% | 0% | Shared-state contention |

A weighted average also hides variance. One maximum-size deployment can delay many transfers even when the mean fits. Run burst and adversarial scenarios, and publish p50, p95, and p99 completion latency at each offered load.

### Reproducibility record

A reviewer should be able to reconstruct every number from:

```text
client commit and protocol parameters
transaction generator and random seed
initial state snapshot and working-set distribution
hardware, storage, operating system, and compiler
validator count, regions, latency, loss, and bandwidth
run duration, warm-up, offered-load schedule, and errors
raw block, queue, resource, and finality measurements
calculation script and unit conventions
```

Keep decimal and binary byte units distinct. State whether `kB` means 1,000 bytes and `KiB` means 1,024. Define whether throughput counts submitted, included, executed, successful, or finalized transactions. Unit discipline catches many performance claims that are numerically correct but semantically incomparable.

## **Chapter Summary**

Blockchain scalability is sustained useful capacity under explicit workload, resource, security, and recovery assumptions. TPS alone omits transaction complexity, latency, hardware, decentralization, and data. The central difficulty comes from globally replicated execution and storage plus the communication required for Byzantine consensus.

The rest of the book studies ways to divide or compress that work: sharding at Layer 1, channels and rollups at Layer 2, modular data availability, parallel execution, and more efficient consensus.


## **References**

[^1]: Hill, Mark D. "What is Scalability?" *ACM SIGARCH Computer Architecture News* 18, no. 4 (1990). <https://minds.wisconsin.edu/bitstream/handle/1793/9676/file_1.pdf?sequence=1&isAllowed=y>.
[^2]: Dinh, Tien Tuan Anh, et al. "BLOCKBENCH: A Framework for Analyzing Private Blockchains." SIGMOD 2017. <https://www.comp.nus.edu.sg/~ooibc/blockbench.pdf>.
[^3]: Konstantopoulos, Georgios. "Reth's path to 1 gigagas per second, and beyond." Paradigm, 2024. <https://www.paradigm.xyz/writing/reth-perf>.
