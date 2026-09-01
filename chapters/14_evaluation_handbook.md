# **Practitioner's Evaluation Handbook**

A scaling architecture should be reviewed as a system, not as a collection of attractive components. This handbook turns the concepts in the book into a repeatable evaluation process for engineers, investors, researchers, and application teams.

## **1. Define the Workload Before the Architecture**

Start with actions users perform, not a target TPS. Record the expected and peak rates for transfers, contract calls, state reads, proof requests, deposits, withdrawals, and cross-domain messages. Measure transaction size and the number of state locations touched.

Separate independent traffic from contended traffic. Ten thousand transfers between distinct accounts may parallelize well. Ten thousand swaps against one pool may serialize. A game with one million daily users can still have a severe hot-state event during a popular mint.

Write latency objectives at the boundary users experience. A trading application may need a sequencer acknowledgement within 200 milliseconds but accept settlement after several minutes. A bridge releasing high-value collateral may require proof acceptance and L1 finality. These are different service-level objectives.

A workload statement should include:

- normal, peak, and burst arrival rates;
- transaction and batch sizes;
- read/write sets or expected contention;
- acceptable p50 and p99 latency;
- state growth and historical-query needs;
- deposit, withdrawal, and cross-chain volume;
- geographic distribution of users and validators;
- expected adversarial behavior.

## **2. Draw the Transaction and Trust Paths**

Draw two diagrams. The **transaction path** follows a normal transaction from signing to finality. The **recovery path** follows the same asset when each privileged service is offline or malicious.

For a rollup, the normal path may be wallet → RPC → sequencer → batcher → DA publication → prover or challenger → settlement contract. The recovery path may be wallet → L1 force-inclusion contract → timeout → forced withdrawal. Both diagrams need identities for upgrade administrators and bridge relayers.

At every edge, ask:

1. What message or commitment crosses the boundary?
2. How is it authenticated?
3. Which state or finality does the receiver assume?
4. Can the sender equivocate or withhold?
5. How is failure detected?
6. Can a user recover without the sender?

An architecture that has only a normal-path diagram is incomplete.

## **3. Identify the Capacity Equation**

Model each major resource independently. For a transaction class *i*, let:

- `e_i` be execution work;
- `d_i` be published bytes;
- `s_i` be state I/O;
- `p_i` be proving work;
- `c_i` be consensus or messaging work.

If the system has sustainable capacities `E`, `D`, `S`, `P`, and `C`, then a workload with transaction rates `x_i` must satisfy:

```text
Σ x_i e_i ≤ E
Σ x_i d_i ≤ D
Σ x_i s_i ≤ S
Σ x_i p_i ≤ P
Σ x_i c_i ≤ C
```

The first tight inequality is the current bottleneck. Optimization moves that bottleneck; it rarely removes all limits. A rollup compression improvement may free DA capacity and expose proving. A faster VM may expose state commitment or networking. This model prevents teams from optimizing the most visible component instead of the limiting one.

## **4. Benchmark in Layers**

### **Microbenchmarks**

Measure signature verification, VM instructions, state reads and writes, hashing, proof generation, proof verification, encoding, and network serialization independently. Microbenchmarks explain why the system behaves as it does, but cannot establish end-to-end capacity.

### **Component Benchmarks**

Run the execution engine against workloads with controlled conflict rates. Run consensus with realistic block payloads across realistic network delay. Run the prover with representative circuits and witness sizes. Run DA retrieval under missing peers and partial withholding.

### **End-to-End Benchmarks**

Submit signed transactions through the same interfaces users will use. Include batching, publication, proof generation, settlement, indexing, and receipt delivery. Report each finality milestone rather than stopping the timer at the first sequencer response.

### **Failure Benchmarks**

Remove the sequencer, prover, batch submitter, consensus leader, bridge relayer, or part of the DA network. Measure time to detect, time to recover, user action required, and cost of the recovery transaction. An escape hatch that has never been load-tested is a hypothesis.

## **5. Report Distributions, Not One Number**

Averages hide queues and failure. Report p50, p90, p95, and p99 latency. Plot offered load against completed throughput and tail latency. The useful capacity is near the point where latency or errors begin to rise sharply, not the largest transient sample observed before collapse.

Run tests long enough to expose database compaction, cache exhaustion, state growth, garbage collection, proof queues, and fee-market changes. Publish warm-up and measurement periods. Repeat experiments and include variance.

Hardware disclosure should include processor, core count, memory, storage device, network link, operating system, client commit, compiler, and configuration. For distributed tests, disclose locations and injected delay or packet loss.

## **6. Evaluate State Growth**

A chain can sustain high execution today while accumulating a state database that makes tomorrow's validator expensive. Measure bytes of new state per transaction, temporary data retention, history retention, snapshot size, synchronization time, and witness size.

Ask who pays for inactive state. Gas charged once may not cover decades of replication. Rent, expiry, stateless witnesses, and archival markets solve different parts of the problem. A plan to prune history is not a plan to serve historical queries.

## **7. Evaluate Data Availability Separately**

Record exactly where transaction data is published and for how long. If blobs or an external DA network are used, describe the commitment, erasure coding, sampling, retrieval, and retention assumptions. If a committee signs attestations, publish its membership, threshold, rotation, and slashing rules.

Test a withholding event. Can an independent node reconstruct the batch? Can an optimistic verifier build a fault proof? Can a validity-rollup user recover the current state? Which service holds historical copies after the consensus retention window?

Avoid the phrase "data is on-chain" unless the chain, data type, and retention rule are named.

## **8. Evaluate Sequencing and MEV**

Document how transactions enter the system, how they are ordered, and whether users can bypass the normal sequencer. Measure censorship time, reordering power, downtime, and recovery after conflicting sequencer views.

If there is a decentralized sequencer set, analyze its own consensus and membership. If sequencing is based on the L1 proposer, explain latency and inclusion. If a shared sequencer orders several rollups, define atomicity and what happens when only one rollup accepts the ordered batch.

MEV analysis should cover front-running, back-running, sandwiching, liquidations, cross-domain timing, and privileged order flow. More throughput does not remove ordering value.

## **9. Evaluate Proof Systems**

For validity systems, record the statement being proven, circuit or VM version, proof system, cryptographic assumptions, setup procedure, verifier contract, prover hardware, proof time, memory, proof size, and verification cost.

Measure worst-case and average proving. A block filled with cryptographically expensive operations may be harder to prove than a transfer block with the same execution gas. Define what happens if proof generation misses its deadline or the only prover fails.

Circuit audits and differential testing matter as much as proof-system soundness. A proof can perfectly establish the wrong program if the circuit does not match intended execution.

For optimistic systems, document the fault-proof game, bond, challenge window, data dependency, game duration, and permission to challenge. Exercise the complete game against an intentionally invalid transition.

## **10. Evaluate Consensus Under Its Real Model**

State whether the protocol assumes synchrony, partial synchrony, or another network model. Record its Byzantine threshold, quorum rule, leader-selection method, timeout behavior, view-change path, signature aggregation, and validator admission.

Benchmark the full block, not an empty proposal. Introduce slow and equivocating leaders. Partition a minority of validators. Test clock skew and delayed certificates. Report safety outcomes separately from liveness degradation.

Validator count should be accompanied by stake distribution, operator independence, client diversity, hosting, geography, and delegation. A thousand keys controlled by ten operators do not create a thousand independent failure domains.

## **11. Evaluate Bridges as Security-Critical Systems**

Inventory every bridge contract, message verifier, relayer, committee, light client, upgrade key, rate limit, and pause mechanism. Follow deposits and withdrawals in both directions. Confirm replay protection, source and destination domain separation, nonce handling, and finality assumptions.

Model the largest credible loss, not only daily volume. A bridge may accumulate years of locked collateral. Rate limits and delayed large withdrawals can bound damage, but emergency controls create governance power that must be secured and disclosed.

Test recovery when one chain reorganizes, stops finalizing, or upgrades its message format. Cross-chain systems inherit the failure modes of both chains plus the bridge.

## **12. Evaluate Upgrades and Governance**

List every address or governance process that can change execution code, proof verification, bridge rules, sequencer membership, fees, or emergency state. Record signature thresholds, signer independence, hardware security, timelocks, monitoring, and user exit periods.

An upgradeable rollup has two protocols: the code users see now and the process that can replace it. The second can dominate the first. A useful maturity report distinguishes immediate emergency powers from delayed routine upgrades and states whether a user can exit under old rules.

## **13. Make Recovery Affordable**

Failure recovery often moves activity back to a scarce base layer. Estimate the cost of force inclusion, mass withdrawal, state reconstruction, and proof submission under congestion. Simulate many users invoking the path together.

A mechanism that is correct but unaffordable does not give ordinary users meaningful sovereignty. Batching recovery claims, rate-limited exits, proof aggregation, and pre-funded watchdogs can improve practicality, but each introduces new coordination rules.

## **14. Produce a Comparable Result**

A professional evaluation report should publish:

1. architecture and recovery diagrams;
2. source code and client commits;
3. workload generator and transaction mix;
4. hardware and network configuration;
5. offered-load versus throughput curves;
6. latency distributions at each finality boundary;
7. state, data, and proof growth;
8. failure-injection results;
9. trust, upgrade, and bridge assumptions;
10. raw results and scripts needed to reproduce the test.

The conclusion should name the operating envelope: the workload and conditions under which the architecture meets its objective. It should also name the first bottleneck and the failure that creates the largest user burden.

## **Evaluation Template**

Use this short form before adopting or comparing a scaling system:

| Question | Evidence |
|---|---|
| What workload was tested? | Transaction mix, contention, duration |
| Where does execution happen? | VM, hardware, determinism rule |
| Where is data published? | Commitment, retention, retrieval |
| Who orders transactions? | Sequencer/consensus and bypass path |
| How is state proven? | Fault/validity proof and implementation |
| What is finality? | Milestones and fault assumptions |
| How do users exit? | Normal and forced paths, measured cost |
| What can be upgraded? | Keys, threshold, delay, exit window |
| What fails under load? | Capacity curves and queues |
| What happens during failure? | Injection results and recovery time |

## **Conclusion**

Scalability engineering begins after the headline number. A defensible evaluation starts with workload, traces the transaction and recovery paths, models each resource, tests the real stack under failure, and publishes enough detail for another team to reproduce the result.

This method does not produce one universal winner. It produces an operating envelope and a visible set of trade-offs. That is the information builders need to choose an architecture responsibly.
