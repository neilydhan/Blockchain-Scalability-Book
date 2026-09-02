# **Chapter 6: Rollups**

## **Introduction**

Rollups move transaction execution away from the base chain while using it for settlement and data. Hundreds or thousands of transactions are compressed into a batch. The rollup publishes a new state commitment and enough information for the base layer to enforce correctness.

This design separates three questions: who orders transactions, who executes them, and how the result is proven. Understanding that separation is more useful than memorizing project names.

---

## **The Rollup Lifecycle**

<p align="center">
  <img src="../assets/course/ch06_rollup_lifecycle.svg" width="760" alt="Rollup transaction lifecycle and completion boundaries">
  <br>
  <em>Figure 6.1: A rollup transaction moves through sequencing, data publication, proof, and settlement. Applications should name which boundary they treat as complete. Original figure for this book.</em>
</p>


A typical transaction follows this path:

1. a user signs and submits a transaction to a sequencer;
2. the sequencer orders transactions and produces an L2 block;
3. an executor computes the new rollup state;
4. batch data or a data commitment is posted;
5. a state root is submitted to the settlement contract;
6. correctness is established by a fraud proof or validity proof;
7. the state becomes final under the rollup's rules.

The sequencer provides fast inclusion and a useful user experience, but its acknowledgement is normally **soft confirmation**. Settlement finality comes later. A centralized sequencer can censor or reorder transactions even when it cannot steal funds. Force-inclusion mechanisms and sequencer decentralization address this liveness risk.

---

## **Optimistic Rollups**

Optimistic rollups assume a proposed state is valid unless someone proves otherwise. After a batch is posted, a challenge period allows a verifier to submit a fraud proof.

A modern fault-proof system narrows disagreement to a specific execution step, then asks Layer 1 to evaluate that step. This avoids re-executing an entire batch on-chain.

### **Benefits**

- close compatibility with the EVM;
- relatively simple proving assumptions;
- computation is performed off-chain unless disputed;
- mature developer tooling and ecosystems.

### **Trade-Offs**

- canonical withdrawals can wait through the challenge period;
- at least one honest party must be able to reconstruct and challenge bad state;
- the fault-proof implementation and upgrade mechanism are security-critical;
- fast third-party bridges add liquidity and counterparty risk.

The honest verifier requirement does not mean every user must personally watch the chain. It means the system needs an open, economically sustainable set of watchers with access to the data and a working dispute path.[^1]

---

## **Validity Rollups**

Validity rollups, often called ZK rollups, attach a succinct proof that the new state was computed correctly. The Layer 1 verifier checks the proof rather than replaying the entire batch.

The proof may use a SNARK or STARK. These families differ in proof size, prover cost, verification cost, transparency, and cryptographic assumptions. The phrase "zero knowledge" describes the ability to hide witness data, but a validity rollup can use validity proofs without offering transaction privacy.

### **Benefits**

- invalid state cannot pass the verifier if the proof system and implementation are sound;
- withdrawals do not require a fraud-proof challenge window;
- verification cost can remain small even for a large computation;
- recursive proofs can aggregate many blocks.

### **Trade-Offs**

- proving is computationally demanding;
- circuits or zkVMs add implementation complexity;
- bugs in circuits, verifiers, or trusted setup procedures can be severe;
- EVM equivalence and rapid protocol upgrades are difficult engineering problems.

The course's STARK case study emphasizes **scalable proofs**: the verifier performs much less work than the prover, making it possible to amortize verification over a batch.

---

## **Where the Data Lives**

Validity proves that a transition is correct; it does not by itself make the underlying data available.

- A **rollup** publishes transaction data to the base layer.
- A **validium** stores data off-chain, often with a data availability committee.
- A **volition** lets users or applications choose between on-chain and off-chain data.

Validium can reduce cost, but an unavailable committee can prevent users from reconstructing balances or exiting, even if it cannot forge a validity proof. This is why state validity and data availability must be evaluated separately.

---

## **Compression and the Cost Model**

For many rollups, data publication is the largest variable cost. A batch saves money by:

- removing repeated signature and transaction fields;
- encoding values compactly;
- sharing one Layer 1 transaction across many L2 transactions;
- using blobs rather than expensive EVM calldata where supported.

EIP-4844 introduced blob-carrying transactions with their own fee market. Blobs are committed to by Ethereum consensus and retained for a limited period, which is sufficient for rollup reconstruction and challenges while avoiding permanent EVM storage.[^2]

A rollup's user fee can be viewed as:

> **L2 execution cost + allocated data-publication cost + proving/operation cost + margin**

High batch utilization lowers the data cost per user. Empty blocks or fragmented liquidity reduce those economies of scale.

---

## **Bridges and Forced Exits**

The canonical bridge locks an asset on Layer 1 and represents it on Layer 2. Withdrawals burn or release the L2 representation and unlock the L1 asset after the required proof or challenge process.

The bridge contract is often the rollup's largest pool of value. Security depends on:

- correct message authentication;
- replay protection;
- the state-root acceptance rule;
- proof verification;
- upgrade and emergency powers;
- a usable escape path if the sequencer stops.

A rollup is not trustless merely because it has a proof system. Users should examine whether contracts are upgradeable, who controls the upgrade keys, whether there is a delay, and whether users can exit before a disputed upgrade takes effect.

---

## **Optimistic vs Validity Rollups**

| Feature | Optimistic Rollup | Validity Rollup |
|---|---|---|
| Correctness rule | Valid unless challenged | Proof required before acceptance |
| Main proof | Fraud/fault proof | SNARK or STARK |
| L1 computation | Mostly during disputes | Verify each aggregate proof |
| Canonical withdrawal | Delayed by challenge period | After proof and L1 finality |
| Prover burden | Lower in normal operation | Significant and continuous |
| Compatibility | Mature EVM compatibility | zkEVM/zkVM complexity |
| Core assumption | One honest challenger with data | Sound proof system and available data |

Neither design dominates every workload. Optimistic systems benefit from simple execution compatibility. Validity systems benefit from concise finality and proof aggregation. Both still face sequencing, governance, bridging, and data-availability choices.

---

## **From Rollups to Appchains**

The course asks why applications are becoming chains. A dedicated rollup can choose its fee token, block time, execution environment, governance, and sequencing policy. It can isolate congestion and capture more of the economics generated by its users.

The cost is fragmentation. Users must bridge assets, liquidity is split, and synchronous calls across rollups become asynchronous messages. Superchain and hyperchain designs try to standardize bridges, messaging, and upgrades across related rollups. Shared sequencers and proof aggregation aim to restore some atomicity and economies of scale.

## **Worked Example: From Transaction to Withdrawal**

Assume 1,000 users submit transfers to an optimistic rollup. The sequencer checks signatures and nonces, chooses an order, and returns quick receipts. It executes the batch, produces a new state root, and publishes compressed transaction data to Ethereum. The rollup contract records the proposed root.

A verifier re-executes the data. If its root differs, it opens a dispute. A bisection game narrows the disagreement until the contract checks one disputed machine step. A dishonest proposal is rejected and its bond can be penalized. If nobody challenges during the window, the root becomes final under the rollup contract.

A canonical withdrawal proves that finalized L2 state contains the withdrawal message. A liquidity bridge can pay earlier, but that is a separate service accepting delay and reorganization risk for a fee.

In a validity rollup, a prover generates a proof and the contract verifies it before accepting the root. The user avoids a fraud-proof window but may still wait for proving, batch publication, Ethereum inclusion, and L1 finality. "Instant finality" must be separated into sequencer confirmation, proof finality, and settlement finality.

## **Sequencer Failure and the Escape Hatch**

A sequencer outage should reduce convenience, not destroy ownership. Force inclusion lets a user submit data to Layer 1; after a timeout, the rollup must process it or permit an exit. This path must remain usable when many users need it simultaneously.

Upgrade control is part of the same threat model. If an administrator can replace the verifier immediately, the proof system cannot protect users from that administrator. Delayed upgrades and an exit window make the cryptographic guarantee operationally credible.

## **Rollup State Commitments and Inboxes**

A rollup contract usually maintains an ordered inbox and a sequence of accepted state commitments. The inbox binds the L2 to data posted on L1, including force-included transactions. A simplified commitment might be:

```text
BatchCommitment {
    previous_state_root
    new_state_root
    inbox_start
    inbox_end
    transaction_data_hash
    l2_block_range
}
```

The transition rule states that executing inbox items and batch data from `previous_state_root` must produce `new_state_root`. An optimistic rollup lets a proposer assert this relation subject to challenge. A validity rollup requires a proof of it.

This structure prevents a proposer from proving an arbitrary computation unrelated to user messages. It also lets bridge contracts authenticate an L2 withdrawal against an accepted root.

## **Interactive Fault Proofs**

Re-executing a large batch on Ethereum would remove the scaling benefit. An interactive game instead commits both parties to execution traces. If a trace contains `2^n` steps, repeated bisection isolates one disputed step in about `n` rounds.

Suppose the proposer claims a final machine state and the challenger computes another. They compare a midpoint commitment. Whichever half disagrees becomes the next interval. Eventually the L1 contract executes one instruction against an agreed pre-state and decides which trace is correct.

Implementation details matter:

- the machine state must have a canonical hash;
- instruction semantics on L1 must match L2 exactly;
- deadlines prevent one party from stalling;
- bonds cover verification cost and discourage spam;
- the challenger needs all batch data;
- the system needs at least one working path to submit the challenge.

A permissionless game can still be practically centralized if proof software is difficult to run or the bond is prohibitively large.

## **Validity-Proof Pipeline**

A validity rollup converts execution into an arithmetic statement. The witness contains transaction data, signatures or signature-verification inputs, prior state paths, and intermediate values. The circuit or zkVM constrains each transition and exposes public inputs such as old root, new root, and batch commitment.

A production pipeline includes:

1. **trace generation**, turning VM execution into witness data;
2. **witness generation**, filling circuit columns or zkVM memory;
3. **proving**, committing to the trace and producing the argument;
4. **aggregation**, recursively combining several proofs;
5. **verification**, checking one compact proof on the settlement layer.

The prover is an availability component even when it cannot violate safety. If only one prover implementation exists and it crashes on a valid block, finality stalls. Multiple provers, deterministic trace formats, and the ability to reproduce witnesses improve resilience.

### **Circuit Correctness**

Cryptographic soundness proves the encoded relation, not the intended protocol. If a circuit forgets to constrain a value, a proof can be valid for an invalid state transition. Teams use specification tests, differential execution against a reference VM, formal methods for critical gadgets, and independent audits.

Upgrading a zkVM changes the relation being proven. Settlement contracts must bind a proof to a verifier and program version. Upgrade delays give users time to examine new rules and exit.

## **Data Encoding and Fee Estimation**

Batchers reduce bytes by omitting values that can be inferred from order or state, replacing addresses with indices, compressing signatures, and aggregating repeated fields. The decoder must be canonical; two decodings of the same bytes would threaten consensus.

A rough rollup fee estimator is:

```text
user fee = L2 gas × L2 gas price
         + user data bytes × expected blob byte price
         + allocated proving and operation cost
         + risk margin
```

Blob prices vary with demand, so batchers estimate future publication cost and may delay low-priority batches. Delay improves compression and cost per transaction but increases latency and the amount of unposted state at risk during a sequencer failure.

## **Rollup Operations Checklist**

A production rollup should document and monitor:

- sequencer uptime, reorganization policy, and forced-inclusion delay;
- batch submission lag and unposted transaction volume;
- DA publication success and retrieval;
- proof or challenge status for every commitment;
- canonical bridge balances and pending withdrawals;
- contract implementation, administrator, and upgrade delay;
- prover diversity and backlog;
- the tested cost and capacity of forced exits.

A block explorer that shows only L2 blocks covers the first step of a longer settlement pipeline.

## **Deriving a Canonical Withdrawal**

Assume a rollup stores withdrawals in a Merkle tree. A user withdrawing 10 tokens receives a message leaf:

```text
leaf = hash(
    source_rollup,
    destination_chain,
    withdrawal_nonce,
    sender,
    recipient,
    token,
    amount
)
```

After the state root is accepted, the user submits the message, Merkle path, and root identifier to the bridge. The bridge verifies inclusion, confirms finality under the rollup rule, marks the nonce spent, and transfers the asset.

Marking consumption before transfer avoids reentrancy and replay. Binding both domains prevents the same proof from being reused on another chain. Token mapping must distinguish native assets from representations and handle tokens with unusual transfer behavior.

## **Fault-Proof Game Economics**

A challenger spends compute to replay batches and capital to post bonds. If rewards do not cover monitoring and transaction cost, "one honest challenger" may exist in theory but not operation.

The protocol can pay successful challengers from proposer bonds. Bonds must be large enough to deter false assertions and cover dispute cost, but not so large that only a few actors can participate. Challenge transactions also compete for L1 inclusion during congestion. Systems can sponsor challengers, run several independent watchers, and pre-fund accounts.

Permissionless participation should be tested: a new challenger using public software and ordinary infrastructure must be able to reproduce state, detect an invalid assertion, and complete the game.

## **Prover Performance Engineering**

Proof generation is a pipeline of CPU, GPU, memory, storage, and network work. Trace generation may be sequential even when polynomial commitments parallelize. Large witnesses may exceed accelerator memory and require partitioning.

Measure proofs per unit time, time to first proof, peak memory, accelerator count, energy, and cost. Report the program and workload because cryptographic operations, memory accesses, and control flow affect circuits differently.

Recursive proof systems split a block into segments, prove segments in parallel, and aggregate them. Segmentation shortens the critical path but adds recursive overhead. A scheduler balances segment size, available hardware, and settlement deadline.

## **Sequencer Architecture**

A sequencer commonly has an RPC/mempool layer, admission controls, ordering engine, execution engine, state database, block builder, and batch publisher. High availability can use an active-passive replica or a consensus group.

Replicating a sequencer introduces its own fork-choice problem. If two replicas issue conflicting soft confirmations, users need a rule for which survives. One approach gives only an elected leader signing authority; another uses a quorum certificate for each L2 block. The latter improves fault tolerance but adds latency.

Admission control protects the sequencer from transactions designed to consume simulation or storage resources without paying. Nonce gaps, replacement transactions, invalid signatures, and underpriced data must be bounded before they fill queues.

## **Decentralized Sequencing Trade-Offs**

Rotating sequencers reduce dependence on one operator but require consensus on L2 order and state. Permissionless participation needs stake or another Sybil-resistance mechanism, networking, penalties, and a way to distribute fees.

Decentralization can worsen latency and make reorganization behavior visible to users. A protocol may separate fast preconfirmations from final L2 consensus. Wallets and applications must know which promise they received.

Based sequencing inherits ordering from L1 proposers. Shared sequencing amortizes consensus across rollups. Each choice changes censorship, MEV, latency, and cross-rollup composition rather than producing one universal measure of sequencing decentralization.

## **Rollup Upgrade and Escape Testing**

Before an upgrade, operators should replay historical blocks against the new implementation, compare state roots, test bridge messages, and execute the forced path. A canary deployment or shadow prover can find divergence before activation.

The upgrade announcement should publish code hashes, verifier addresses, activation time, audit results, and user exit deadline. Emergency changes need narrower scope and a postmortem. An escape hatch that an upgrade can silently disable is not independent protection.

## **Fault-Proof Pipeline: From Assertion to One-Step Dispute**

An optimistic rollup accepts an assertion unless a challenger proves it inconsistent with the transition rules. The production system includes more than a challenge window: it needs an assertion graph, bonds, authenticated data, interactive narrowing, a one-step verifier, clocks, and permissionless participation.

### Assertion

A proposer submits a claim derived from a parent:

```text
Assertion {
  rollup_id,
  parent_assertion,
  l2_block_range,
  pre_state_root,
  post_state_root,
  data_commitment,
  inbox_position,
  vm_version,
  proposer_bond
}
```

The contract checks structural rules and starts a clock. It does not re-execute the batch. The data commitment and VM version must select the bytes and transition function a challenger will use.

An assertion may be valid or invalid independent of who proposed it. A trusted proposer is not a correctness proof; a permissioned proposer primarily controls liveness and censorship.

### Challenger reproduction

A challenger retrieves the committed batch data, reconstructs the pre-state or required witnesses, and executes the pinned VM. If its computed post-state differs, it opens a dispute before deadline and posts the required bond.

This path must be economically and operationally open. If data access, state snapshots, or a proprietary VM build are available only to the operator, "permissionless challenge" is nominal.

### Bisection

Re-executing an entire batch on L1 is too expensive. The parties commit to an execution trace and repeatedly narrow the disagreement.

If the trace has `N` steps, binary bisection takes approximately:

```text
ceil(log2(N))
```

rounds to isolate one transition. For `N = 2^30` machine steps, at most 30 bisection choices locate the disputed step, though each on-chain round also consumes confirmation and response time.

At each round, both sides bind their claimed intermediate state. The protocol chooses the half where commitments disagree. Domain separation includes game identity, round, interval, and trace commitment so a proof cannot be replayed into another dispute.

### Clocks and timing

A chess-clock design gives each side a total response budget rather than restarting a full window every round. The contract must define whose clock runs, when a move becomes effective, how L1 reorganizations affect inclusion, and what happens when both parties submit near a boundary.

Suppose each side has a 3.5-day clock and ordinary L1 inclusion p99 is two minutes. Thirty interactive rounds do not automatically require 60 minutes because parties may consume variable time, but automation needs enough margin for monitoring, proof construction, fee spikes, and reorgs. Timeout tests should target exact block boundaries and delayed transactions.

### One-step proof

After narrowing, the L1 verifier checks one transition from pre-step state to post-step state. Depending on design, it verifies a VM instruction, memory and register witnesses, Merkle proofs, inbox access, and output commitment.

The one-step verifier is a consensus-critical implementation of VM semantics. A mismatch between native rollup execution and this verifier can reject valid state or accept invalid state. Differential vectors must cover opcodes, exceptions, memory expansion, calls, precompiles, gas, and host inputs.

### Resolution and bonds

If the one-step proof shows the assertion invalid, the contract rejects it and descendants depending on it. If the challenge is invalid or times out, the assertion advances toward acceptance. Bond allocation rewards useful participation and deters spam, but must not price honest challengers out.

Economics need to cover:

- L1 gas across worst-case rounds;
- capital locked for the full game;
- data retrieval and state reconstruction;
- computation and monitoring;
- concurrent disputes and denial-of-service;
- volatility of the bonded asset.

A proposer bond lower than extractable bridge value may still work if invalid assertions cannot finalize while one honest challenger acts. The bond funds deterrence and operations; cryptographic/game correctness protects the state. However, challenger rewards must support an actual monitoring market.

### Multiple games and denial of service

An attacker may create many claims or challenges to exhaust honest capital and computation. Limit policies must avoid giving one administrator power to suppress a valid challenge. Defenses include per-claim bonds, bounded game trees, shared computation, proof caching, and priority for games closest to finalization.

Game implementations need garbage collection. Resolved descendants, bonds, and trace data should be finalized without deleting evidence before appeals or monitoring complete.

### Fault-proof assertions

A release test should assert:

1. an invalid state root cannot pass when one challenger has data and responds on time;
2. a valid assertion survives malicious challenges;
3. every bisection round shrinks the disputed interval and binds one trace;
4. timeout results are deterministic at block boundaries and through shallow reorgs;
5. the one-step verifier agrees with native execution on generated and adversarial vectors;
6. duplicate and concurrent games cannot settle the same bond or assertion twice;
7. parent rejection invalidates dependent state safely;
8. any qualified challenger can participate without operator credentials;
9. worst-case gas, time, and capital fit the published challenge assumptions.

Run the complete game periodically in production-like staging. A deployed contract that has never resolved an intentionally invalid assertion remains an untested safety mechanism.

## **Proving Pipeline: From Execution Trace to L1 Verification**

A validity rollup does not prove "the block" as an informal object. It proves that a precisely encoded program accepted private witness data and public inputs. The engineering pipeline must keep execution, trace generation, arithmetization, proof creation, and contract verification on the same version.

### Statement and witness

Public inputs commonly bind:

```text
rollup identity
protocol and circuit version
parent and post-state roots
transaction-data commitment
inbox and withdrawal roots
batch number or range
```

The witness contains transaction fields, signatures or signature-verification auxiliaries, Merkle paths, pre-state values, execution intermediates, and any tables needed by the proof system. Data may be private to the proof while still needing separate publication for rollup availability.

A proof that omits the rollup identity may replay across deployments. A proof that omits the data commitment can establish a state transition without tying it to the bytes users downloaded. A proof that omits the program version may verify under rules different from the batch's declared semantics.

### Constraint generation

An execution trace is converted into algebraic constraints. Each row or step encodes machine state, opcode semantics, memory, storage, gas, and transitions to the next step. Lookup arguments can prove that values belong to fixed tables such as byte ranges or opcode metadata without repeating every constraint.

The prover must constrain failure paths as carefully as success. A signature failure, out-of-gas exception, revert, and invalid opcode each have deterministic effects on state and receipts. An unconstrained branch can let a prover choose a convenient result not produced by the VM.

Circuit capacity is often measured in rows or constraints, not transactions. One cryptographic operation can consume more proving work than many transfers. A batcher therefore tracks execution gas, published bytes, and proving shape separately.

### Witness generation and proving

Witness generation re-executes or instruments the block to fill every constrained cell. It is frequently memory- and storage-intensive. Proof generation then commits to the trace, derives challenges, constructs polynomial or hash-based arguments, and emits a succinct proof.

A production job record includes:

```text
ProofJob {
  job_id,
  batch_range,
  program_hash,
  public_input_hash,
  witness_commitment,
  priority,
  deadline,
  attempts,
  prover_build,
  result_proof_hash
}
```

Jobs must be idempotent. A worker restart should either resume safely or reproduce the same public statement. Different valid proofs may have different bytes because of proof randomness, so compare their verified public inputs and result, not only proof hashes.

### Recursion and aggregation

When one batch exceeds circuit capacity, a rollup can prove segments, then recursively verify segment proofs inside an aggregation circuit. Aggregation amortizes L1 verification but introduces another program version and dependency graph.

The aggregator must bind segment order, continuity of state roots, complete batch coverage, and absence of duplicate segments. If segment `i` ends at root `R`, segment `i+1` must begin at `R`. Sorting proofs by an untrusted job identifier without constraining root continuity can combine individually valid pieces into the wrong history.

### On-chain verification

The settlement contract reads the proof and public inputs, selects the correct verifier, checks that the parent root equals the last accepted root, and updates state only after successful verification. Verifier upgrades need a timelock and explicit circuit-version activation.

Verification gas should be measured with worst-case public inputs and contract storage behavior. A cheap cryptographic verifier can still become expensive if it writes many roots, messages, or accounting records.

### Prover failure and fallback

Proof correctness protects safety; prover availability controls liveness. A queue can grow because of hardware loss, a pathological transaction, witness-service outage, circuit bug, or demand burst. Operators should expose oldest unproved batch, queue work in constraint-seconds, attempt count, GPU/CPU utilization, witness generation time, and estimated settlement delay.

Redundant workers help only if they do not share one code build, cloud region, witness database, or coordinator. A fallback prover should be exercised before an incident. If the protocol permits an escape mode after prolonged proof failure, the activation condition and state reconstruction data must be public and testable.

### Proving capacity calculation

Suppose batches arrive every 12 seconds. Average proof time is 42 GPU-seconds, but p95 is 72 seconds. Mean offered proving load is:

```text
42 / 12 = 3.5 GPU equivalents
```

Four workers provide only 12.5 percent mean headroom and cannot absorb long p95 jobs or one-worker failure. At six workers, mean utilization is about 58 percent. If one worker fails, utilization becomes 70 percent. Queue simulation should use the measured proof-time distribution and correlated batches, not only the average.

If recursion aggregates 32 batch proofs and takes an additional 180 GPU-seconds, its amortized load is:

```text
180 / (32 × 12) ≈ 0.47 GPU equivalents
```

That stage needs its own queue and redundancy. A stable leaf-proof queue can coexist with an unstable aggregation queue.

### Differential and adversarial testing

For each VM test vector, compare native execution, witness generation, proof verification, and a second independent implementation where available. Mutate every public input and confirm verification fails. Generate invalid traces for signature, nonce, balance, gas, memory, storage, logs, and withdrawal roots.

Test circuit boundaries: zero transactions, maximum rows, one step over capacity, largest lookup table, deepest call stack, maximum public inputs, and version transition. Crash workers after witness generation, during proof creation, after upload, and before coordinator acknowledgement. The coordinator should avoid duplicate state acceptance while allowing redundant proof production.

A proof system is production-ready when the statement is complete, execution and circuit semantics agree, every version is pinned, queues remain stable under realistic distributions, and independent parties can reproduce verification. Succinct proof size alone establishes none of those properties.

## **Rollup Fee Market and Batch-Packing Trace**

A rollup fee pays for more than execution. The operator must recover local execution and storage cost, the cost of publishing compressed data, settlement transactions, proof or dispute infrastructure, and a risk margin for volatile base-layer prices.

A useful fee decomposition is:

```text
user fee = L2 execution fee
         + allocated DA fee
         + proof or dispute fee
         + settlement overhead
         + operator margin
         - explicit subsidy
```

Each component should be observable or governed by a documented estimator. A single opaque gas price hides which resource is scarce.

### Two-dimensional demand

A transaction may be cheap to execute but expensive to publish, or expensive to execute with little data. Model at least:

- L2 execution gas or compute units;
- compressed bytes added to the batch;
- state writes or persistent storage burden;
- proof cost, when transaction shape changes proving work.

One scalar fee can still be presented to users, but its calculation should price each constrained resource and avoid cross-subsidies that attackers can exploit.

### Worked fee estimate

Suppose a transaction uses 90,000 L2 gas at 0.02 gwei per gas:

```text
90,000 × 0.02 gwei = 1,800 gwei
```

Its batch contribution is estimated at 140 compressed bytes. If L1 or DA publication costs 18 gwei per byte after the protocol's conversion and safety margin:

```text
140 × 18 gwei = 2,520 gwei
```

Allocate another 300 gwei for proof and settlement overhead:

```text
estimated fee = 1,800 + 2,520 + 300 = 4,620 gwei
              = 0.00000462 ETH
```

This is an illustrative estimator, not a live network quote. The wallet should show the fee asset, maximum charged amount, refund rule, and which base-layer price observation the estimate used.

### Compression is contextual

The marginal compressed size of a transaction depends on its neighbors. Repeated addresses and zero bytes may compress well; random signatures and high-entropy calldata may not. Measuring one transaction alone can overstate or understate its batch contribution.

A deterministic protocol may calculate charges from uncompressed bytes or a stable proxy while the operator bears compression variance. If fees use actual compressed output, transaction ordering could alter what each user pays. Define attribution so a builder cannot move compression benefits to favored transactions.

### Batch-packing policy

A batcher chooses transactions subject to several limits:

```text
execution_gas <= G_max
compressed_bytes <= B_max
proof_complexity <= P_max
state_writes <= S_max
```

A transaction fits only if it leaves all limits valid. Greedy sorting by fee per gas can fill execution capacity while wasting scarce DA bytes. Sorting only by fee per byte can starve compute-heavy, data-light work.

One approach calculates expected revenue against the transaction's vector of resource use, then packs while maintaining reserves for system messages, forced transactions, and proof constraints. The exact optimization may be heuristic, but consensus must define the resulting batch validity independently of the heuristic.

### Forced-inclusion reserve

If users can place transactions in an L1 inbox, ordinary batches need capacity to consume them before the force deadline. Reserving zero capacity until the deadline lets a sequencer fill every batch with profitable private traffic and then face an impossible backlog.

Let maximum forced-inbox growth be 200 kB per L1 interval and safe rollup consumption be 250 kB. Only 50 kB of recovery margin remains. A short DA-price spike or missed batch can make the queue grow. Monitor arrival and service rates, oldest-message age, and the number of batches needed to clear the queue.

A force path should specify whether inbox work has prepaid L1 cost, pays L2 execution later, or can fail for insufficient funds. Invalid forced messages must not block later messages forever; define skippable failure semantics while preserving order commitments.

### Price volatility

The sequencer estimates a future publication cost but may post the batch after the base-layer fee changes. Use a bounded moving estimate, explicit safety margin, and a reconciliation rule. Overcharging without refunds can become a hidden margin; undercharging can make the operator delay publication and weaken user guarantees.

Separate a user's fee cap from the operator's publication decision. A transaction accepted under one quote should have a deadline or cancellation policy if base-layer prices make timely publication uneconomic.

If the system smooths prices across batches, maintain a reserve and publish its accounting. A reserve can absorb short spikes but should not silently socialize persistent losses or let governance redirect user prepayments.

### Fee tokens and conversion risk

Charging in a token other than the settlement asset introduces an exchange rate. State the oracle, update frequency, stale-price rule, spread, and who bears conversion risk. During a rapid token decline, an old conversion rate can make fees too low and expose liveness to spam.

Fallback should be deterministic: reject new transactions, require the settlement asset, or apply a bounded conservative rate. An emergency operator quote with no on-chain rule adds discretionary access control.

### Congestion and priority

A fee market needs a clear inclusion objective. First-price priority is easy to explain but exposes users to estimation error. Posted prices smooth user experience but need an adjustment rule. Auctions or MEV-aware ordering add complexity and information leakage.

Whatever the policy, system deposits, withdrawals, forced messages, proof updates, and escape transactions may require protected capacity. Document these lanes and prevent operators from labeling arbitrary private traffic as system-critical.

### Refunds and failed execution

A reverted transaction still consumes execution and publication resources. Charge measured work up to the failure boundary, but refund unused fee cap under a canonical rule. Ensure the sequencer cannot manufacture a different refund by changing a non-consensus execution limit.

Deposits that fail on L2 need a recoverable credit or retry path. Users should not lose funds merely because the destination call ran out of gas. Separate asset custody from destination-call success.

### Fee-market tests

Replay realistic mixed workloads while varying L1/DA price, compressibility, proof complexity, forced-inbox arrivals, and fee-token exchange rate. Inject missed publications and sequencer restarts. For each transaction, reconcile:

```text
maximum authorized
- actual charged
- canonical refund
= zero unexplained remainder
```

Assert that resource limits never overflow, forced work meets its deadline under the stated arrival envelope, failed transactions cannot block the queue, and restarting does not forget prepaid fees or issue duplicate refunds.

Publish estimator error distributions, not only averages: quoted versus charged fee at p50, p95, and p99; operator surplus or deficit; batch utilization by each resource; forced-queue age; and time from sequencer acceptance to DA publication.

A rollup fee market is credible when it prices the resources users consume, preserves mandatory safety traffic under congestion, reconciles every payment, and does not turn base-layer volatility into an undisclosed right for the operator to delay finality.

## **End-to-End Implementation Example: A Rollup Payment**

Consider a minimal account-based rollup supporting deposits, transfers, and withdrawals. The example is intentionally small enough to audit, but its boundaries match production systems.

### State and transaction format

The L2 state maps an account identifier to a balance, nonce, and public key. A transfer contains:

```text
Transfer {
  chain_id,
  rollup_contract,
  sender,
  receiver,
  amount,
  fee,
  nonce,
  expiry,
  signature
}
```

`chain_id` and `rollup_contract` prevent the signature from being replayed on another deployment. The nonce prevents replay within this rollup. Expiry bounds how long a censored or delayed transaction remains valid. The signed payload includes fee and receiver so an intermediary cannot change either.

A deposit is not an ordinary signed L2 transfer. It begins as an L1 event emitted after the bridge receives funds. The rollup derives a unique deposit identifier from the source block, transaction, and event position. The state transition marks that identifier consumed before crediting the account. A reorganization policy defines how much L1 finality is required before the deposit can enter a batch.

### Batch construction

The sequencer validates syntax and signatures, rejects stale nonces, selects an order, and executes against a parent state root. It creates a batch header:

```text
BatchHeader {
  rollup_id,
  batch_number,
  parent_state_root,
  post_state_root,
  transaction_data_commitment,
  inbox_cursor,
  timestamp,
  protocol_version
}
```

The batch number and parent root make the state chain explicit. The inbox cursor proves which forced L1 messages and deposits have been consumed. The protocol version chooses one deterministic transition function. The data commitment binds the encoded transactions used to reproduce the post-state root.

Before signing the header, an implementation checks three invariants: the parent is the last accepted state, every mandatory inbox item through the cursor was processed exactly once, and re-execution from published data produces the proposed post-state root.

### Publication and proof

The operator publishes compressed transaction data to the chosen DA path and submits the header to the settlement contract. These actions must be linked. A contract that accepts a state root without binding it to available transaction data can leave users unable to reconstruct state.

An optimistic design starts a challenge window. Challengers download the data, reproduce execution, and dispute an invalid transition. A validity design proves a statement equivalent to:

```text
given parent_state_root and committed batch data,
valid decoding + signatures + nonce rules + balance rules
produce post_state_root and inbox_cursor
```

The public inputs must bind the rollup identity, protocol version, roots, data commitment, and inbox position. Omitting one can make a proof valid for the wrong deployment, program, or batch.

### Withdrawal lifecycle

A withdrawal transition debits L2 funds and inserts a message leaf containing source rollup, destination chain, recipient, asset, amount, and unique nonce. After the batch is accepted under the rollup's proof rule, the user supplies a Merkle proof to the L1 bridge.

The bridge verifies the accepted state or message root, checks domain separation and finality, marks the message consumed, then transfers the asset. Marking before transfer follows checks-effects-interactions and blocks reentrancy-based replay. The consumed key should bind every field that distinguishes one withdrawal from another.

A wallet should not show one undifferentiated "complete" state. Useful statuses are:

1. **received** - sequencer accepted the signed transfer;
2. **included** - transaction appears in an L2 block;
3. **data published** - independent nodes can reconstruct it;
4. **state accepted** - proof or challenge rule accepted the batch;
5. **settlement final** - the relevant L1 block is final under policy;
6. **withdrawal executed** - the destination bridge consumed the message.

### Failure and recovery table

| Failure | Safe behavior | Recovery path |
|---|---|---|
| Sequencer stops before inclusion | User funds and nonce remain unchanged | Submit through forced inbox or another sequencer |
| Sequencer equivocates on soft confirmations | Conflicting promises are visible but not final | Follow canonical published batch; apply preconfirmation penalty if defined |
| Batch data is missing | Do not accept a state that depends on unavailable data | Reconstruct from DA network or reject/halt under protocol rule |
| Optimistic batch is invalid | Challenger prevents final acceptance | Execute fault-proof game before deadline |
| Validity proof is unavailable | State cannot advance, but prior accepted state remains safe | Fail over to another prover or use delayed escape mode |
| Settlement chain reorganizes | Do not release against the reverted commitment | Re-evaluate batch and message after required finality |
| Bridge transaction is replayed | Consumed-message check rejects it | No recovery needed; retain evidence and alert |
| Upgrade changes transition rules | Old and new versions must not silently diverge | Timelocked activation, shadow execution, and user exit window |

### Test harness

An end-to-end test starts from a known L1 and L2 genesis, deposits funds, transfers them, publishes a batch, proves or challenges it, withdraws, and verifies final balances on both layers. Repeat the flow after process restarts and at every persistence boundary.

Then inject faults: reorder inbox messages, duplicate a deposit, change one encoded amount after commitment, prove against the wrong program version, withhold data, stop the primary prover, reorganize an unfinalized deposit, replay a withdrawal, and activate an incompatible upgrade. Assert both a safety result and an observable status. "The transaction failed" is insufficient; the user and operator need to know which boundary failed and which recovery action is valid.

This small example demonstrates why rollup correctness is not one proof or contract. It is an agreement among transaction encoding, deterministic execution, data publication, proof rules, settlement finality, bridge replay protection, operator persistence, and user-facing status.

## **Conclusion**

Rollups scale execution by batching work and turning Layer 1 into a verifier and data-publication layer. Optimistic rollups use disputes; validity rollups use cryptographic proofs. Their real security also depends on sequencers, bridges, data availability, upgrades, and exit mechanisms.

Rollups do not remove the need to scale Layer 1. They make Layer 1 data capacity more valuable. The next chapters study the modular architecture behind this relationship and the data-availability problem that makes it possible.

## **References**

[^1]: Ethereum.org. "Optimistic Rollups." <https://ethereum.org/developers/docs/scaling/optimistic-rollups/>.
[^2]: Buterin, Vitalik, et al. "EIP-4844: Shard Blob Transactions." <https://eips.ethereum.org/EIPS/eip-4844>.
