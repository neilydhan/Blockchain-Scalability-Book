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

For a rollup, the normal path may be wallet -> RPC -> sequencer -> batcher -> DA publication -> prover or challenger -> settlement contract. The recovery path may be wallet -> L1 force-inclusion contract -> timeout -> forced withdrawal. Both diagrams need identities for upgrade administrators and bridge relayers.

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

## **Worked Example: Evaluating a Rollup Exchange**

Consider a hypothetical validity rollup running a central-limit-order-book exchange. The operator claims 20,000 transactions per second and one-second confirmation. The number alone is not decision-ready.

### Workload

Define four transaction classes: limit-order placement, cancellation, market execution, and collateral update. Use at least two account distributions: uniform accounts and a concentrated market where many traders touch the same order book and price levels. Include signature verification, failed orders, and state growth.

Ramp offered load rather than selecting one favorable rate. At each step, run long enough for queues and compaction to stabilize. The sustainable point is the highest rate where input queue, proof queue, and DA publication backlog remain bounded and p99 latency stays within the objective.

### Resource budget

For rate `λ`, estimate:

- execution demand: `λ × CPU time per transaction`;
- data demand: `λ × compressed bytes per transaction`;
- proving demand: `λ × proving seconds per transaction-equivalent`;
- state growth: `λ × net new state bytes per transaction`;
- settlement demand: `batches per second × verification gas per batch`.

Do not add unlike units into one score. Compare each demand with the capacity of its resource and identify the first utilization ratio approaching one. Leave headroom for variance and recovery.

Suppose the measured mix averages 45 compressed bytes and 0.8 milliseconds of execution per transaction. At 20,000 transactions per second, the rollup generates 900 kB/s of data and 16 CPU-seconds of serial execution each second. The execution target therefore needs at least 16 fully utilized cores before database, scheduling, and operating-system overhead. A production target at 60 percent utilization needs roughly 27 equivalent cores. This is a lower bound, not a hardware promise.

### Finality timeline

Label four milestones:

1. the sequencer accepts and orders the transaction;
2. transaction data is published and recoverable;
3. the validity proof is accepted by settlement;
4. the settlement block reaches the application's chosen finality rule.

The advertised one second may describe only milestone 1. A wallet can display it as a provisional confirmation, but a high-value bridge should not represent it as settlement finality. Measure the distribution between every pair of milestones.

### Failure tests

Stop the sequencer and submit through forced inclusion. Stop the prover and observe whether unproven batches accumulate safely. Withhold one DA chunk and verify reconstruction or rejection. Reorganize an unfinalized settlement block. Corrupt an upgrade proposal and confirm the timelock and monitor alerts. Exhaust bridge and exit paths under base-layer congestion.

For every test, record detection time, safety outcome, recovery time, operator action, and user action. A test that recovers only after an undocumented administrator intervention reveals an additional trust assumption.

### Decision

The evaluation should finish with an operating envelope, not a winner label. For example: the exchange sustains a stated transaction mix at a stated rate on disclosed hardware; provisional confirmation stays below a latency target; proof and publication queues remain bounded; withdrawals reach settlement finality within a measured distribution; and the tested failure paths preserve funds while degrading service for a bounded period.

That conclusion is narrower than "20,000 TPS," but it is useful to an engineer, risk team, and user.

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

## **Incident Readiness and Postmortems**

A scaling system should be evaluated for diagnosability before an incident. When several layers are involved, the first visible symptom may be far from the failed component. A wallet reports a pending withdrawal, while the underlying cause is a DA retrieval gap, proof queue, settlement reorganization, or bridge verifier pause.

### Evidence to retain

Every component should emit durable identifiers that join one user action across layers:

```text
user transaction hash
sequencer request and L2 block
batch and data commitment
proof or dispute job
settlement transaction and state root
message and withdrawal nonce
destination execution
protocol, client, and verifier versions
```

Logs need synchronized clocks but must not treat timestamps as consensus truth. Retain signed protocol messages, state roots, commitments, queue transitions, and configuration changes. Protect private transaction content and prover witnesses according to the application's privacy model.

### Alert design

Alert on violated objectives, not every transient event. Examples include an oldest-unpublished batch beyond its deadline, proof queue work increasing for several intervals, finality lag beyond the recovery budget, sampling failure above threshold, force-inclusion backlog, or bridge messages past expiry.

Each alert should name the affected boundary, assets or batches at risk, safe automated actions, and operator actions requiring approval. A generic "rollup unhealthy" page forces responders to rediscover the architecture under pressure.

### Runbooks

A runbook for each critical dependency states:

1. how to confirm the symptom from an independent source;
2. which safety invariant must not be violated while restoring liveness;
3. which actions are reversible and which require governance or user notice;
4. how to preserve forensic evidence;
5. how to fail over without processing an item twice;
6. when to stop new activity and when existing users can exit;
7. how to verify recovery end to end.

Do not make "restart everything" the default. Simultaneous restarts can remove consensus quorum, discard useful caches, create proof duplication, or erase the timing evidence needed to understand a split.

### Postmortem structure

A useful postmortem includes:

- user-visible impact and exact time interval;
- detection source and delay;
- normal path and recovery path affected;
- timeline using protocol identifiers and versions;
- triggering event, contributing conditions, and latent design weaknesses;
- why safeguards did or did not contain impact;
- manual and automated actions taken;
- verification that funds, state, messages, and queues reconciled;
- corrective actions with owners, tests, and completion evidence.

Avoid attributing a distributed failure to one operator mistake when missing validation, unsafe defaults, poor observability, or shared infrastructure allowed that mistake to become an incident.

## **Worked Adoption Decision**

Assume a team is choosing between a monolithic L1, an L1-settled validity rollup, and an appchain with external DA for a high-value exchange. The exchange expects 1,500 mixed transactions per second, sub-second trading feedback, and withdrawals whose final settlement can take several minutes.

Start with hard requirements:

| Requirement | Threshold |
|---|---|
| Trading acknowledgement | p99 below 800 ms |
| Canonical withdrawal | p99 below 10 min |
| Data recovery | independent reconstruction of every accepted batch |
| Safety | no single operator can create an unbacked withdrawal |
| Recovery | users can exit without the normal sequencer |
| Change control | routine upgrades delayed at least 7 days |

Then score evidence, not architecture labels:

| Evidence | Monolithic L1 | Validity rollup | Appchain + external DA |
|---|---|---|---|
| Mixed workload reaches 1,500 tx/s | measured result required | measured result required | measured result required |
| Sub-second feedback | block/preconfirmation policy | sequencer preconfirmation | appchain consensus/preconfirmation |
| Withdrawal safety | native state | verifier, bridge, and L1 finality | appchain consensus, bridge, DA, settlement |
| Forced path | native transaction submission | L1 inbox and escape path | chain/bridge-specific recovery |
| Independent reconstruction | L1 data/history | rollup data publication | DA proof plus retrieval and archive |
| Upgrade boundary | protocol governance | rollup contracts and verifier | appchain, bridge, DA integration |

A decision cannot be completed from this table alone. Run the same exchange generator against each candidate, disclose hardware and topology, and inject sequencer or leader loss, proof delay, DA withholding, settlement reorganization, and withdrawal congestion.

Suppose the monolithic L1 reaches only 900 transactions per second at the latency objective. The rollup reaches 2,000 but its proof queue becomes unstable after one prover loss. The appchain reaches 4,000 but its bridge uses an immediate small multisignature upgrade. None yet meets every requirement.

The next action is not to pick the largest number. For the rollup, add prover redundancy and repeat the failure test. For the appchain, require delayed bridge upgrades and an old-version exit. For the L1, decide whether workload partitioning or lower demand is acceptable. Adoption follows the first candidate that supplies evidence for the full operating envelope.

### Decision record

The final record names the selected commit and deployment, rejected alternatives, measured workload, finality policy, trust and key inventory, unresolved risks, launch limits, rollback trigger, and date for reassessment. A decision is temporary when protocols, control structures, or workloads change.

## **Upgrade Operations and User Exit Windows**

An upgrade changes the code or parameters that protect user state. Treat it as a protocol migration, not a software deployment. The operational goal is to prove that the proposed transition is authorized, understood, reproducible, reversible where possible, and gives users a meaningful chance to exit when trust assumptions change.

### Upgrade manifest

Publish one machine-readable manifest:

```text
UpgradeManifest {
  system_id,
  proposal_id,
  old_version,
  new_version,
  source_commit,
  build_digest,
  artifact_hashes[],
  verifier_or_contract_addresses[],
  state_migration_hash,
  activation_condition,
  activation_time_or_height,
  rollback_condition,
  governance_authority,
  user_exit_deadline
}
```

Signatures should authorize this exact manifest. A vote for prose that later resolves to different bytecode, initialization data, or activation height is not reproducible authorization.

### Classify the change

Label whether the upgrade changes:

- execution semantics or gas schedule;
- state encoding or commitment scheme;
- proof circuit, verifier, or trusted setup;
- sequencer, validator, or prover membership;
- bridge custody or message verification;
- DA provider or retention assumption;
- fee market, asset, or oracle;
- pause, upgrade, or emergency authority.

A minor API release can still be a major security change if it redirects a proof endpoint or bridge verifier. Classification follows effect, not version number.

### Pre-activation gates

Require reproducible builds, independent artifact hashes, differential execution, state migration rehearsal, security review, and rollback testing. Run old and new versions in shadow against the same finalized inputs and compare state roots, receipts, logs, fees, and messages.

Expected differences need machine-readable exceptions tied to test cases. "Roots differ because of the upgrade" is not an explanation. Enumerate which transactions or state fields change and prove that all other behavior remains equal.

For a verifier upgrade, generate valid and invalid proof vectors across both versions. Test old proofs pending at activation, new proofs submitted early, recursive proofs embedding the old verifier, and malformed version tags.

### Timelock and exit window

A timelock is useful only if users can understand the change and complete an exit before activation. The window must include monitoring delay, challenge or proof time, settlement finality, bridge withdrawal, and congestion under simultaneous exits.

Suppose monitoring may take 24 hours, an optimistic withdrawal needs 7 days, settlement policy adds 20 minutes, and a mass-exit capacity model requires 2 days. A 48-hour upgrade delay is not a meaningful exit window. A conservative bound is at least:

```text
24 h + 7 d + 20 min + 2 d ≈ 10 days and 20 minutes
```

Add operational margin. If emergency upgrades can bypass the delay, disclose exactly who can invoke that path and which loss it is intended to contain.

### State migration

Bind the pre-state root, migration program hash, parameters, and expected post-state root. Run the migration on a production-sized snapshot with constrained hardware. Measure wall time, peak memory, disk amplification, and downtime.

Make migration idempotent or persist phases so a restart cannot apply transformations twice. Validate supply, ownership, nonces, permissions, pending messages, and consumed replay identifiers before activation.

If rollback is possible after new transactions execute, define how those transactions are replayed or compensated. Database rollback alone can duplicate external messages or withdrawals. Often the safe recovery is a forward fix from a frozen state, not a silent binary downgrade.

### Activation

Use an objective height, finalized timestamp, or governance state visible to every component. Confirm clock and chain assumptions. Freeze configuration changes that could alter the manifest near activation.

At activation, monitor version adoption, state-root agreement, block production, proof acceptance, bridge queues, forced messages, fee behavior, and user errors. Define abort thresholds before the event; do not invent them while under pressure.

An activation runbook assigns named roles for command authority, observation, communications, bridge/prover/sequencer operations, and independent safety review. One person should not both execute and attest that all checks passed.

### Rollback and halt matrix

| Condition | Safe response | Forbidden shortcut |
|---|---|---|
| artifact hash mismatch | stop activation | rebuild unreviewed binary live |
| state roots diverge in shadow | investigate and delay | label difference expected without vector |
| migration stops before commit | resume from verified phase or restore snapshot | rerun blindly over partial state |
| new verifier rejects valid proofs | halt unsafe frontier; preserve old accepted state | accept proofs off-chain by operator judgment |
| bridge messages diverge | pause release and reconcile identifiers | replay all pending messages |
| liveness degrades but safety holds | use bounded rollback/forward-fix rule | weaken validation to regain throughput |
| conflicting accepted state appears | halt finalization and preserve evidence | choose a root based on convenience |

### Governance key operations

Inventory every key and threshold that can schedule, cancel, accelerate, pause, or execute an upgrade. Verify device access, signer identity, transaction simulation, nonce, chain ID, and destination contract. Conduct a dry run with the same signer path.

A multisignature threshold is not independent if signers share custody software or one administrator can reset all accounts. Exercise loss of one signer and loss of the largest correlated signer group.

After activation, revoke obsolete roles, rotate temporary keys, and verify old implementation contracts cannot be reinitialized or called through an alternate proxy path.

### User communication

Publish plain-language and technical notices from authenticated channels. State the exact effect, trust changes, hashes, activation boundary, exit deadline, known limitations, and where status updates will appear.

Wallets and interfaces should surface pending upgrades that affect custody or verification. Avoid claiming "no action required" when a user must accept a new governance, DA, bridge, or proof assumption by remaining in the system.

### Post-activation proof

Record actual activation height, transaction, code hashes, post-migration root, signer set, tests, incidents, and any deviation from the manifest. Reconcile assets and messages. Keep the old and new artifacts plus migration inputs long enough for independent review.

An upgrade is complete only after the observation window passes, queues normalize, proofs and exits work, obsolete authority is removed, and the evidence package lets an outsider reproduce what changed.

## **Conclusion**

Scalability engineering begins after the headline number. A defensible evaluation starts with workload, traces the transaction and recovery paths, models each resource, tests the real stack under failure, and publishes enough detail for another team to reproduce the result.

This method does not produce one universal winner. It produces an operating envelope and a visible set of trade-offs. That is the information builders need to choose an architecture responsibly.
