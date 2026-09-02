# **Chapter 4: Layer 1 On-Chain Scalability**

## **Introduction**

Layer 1 scaling changes the base blockchain itself. Instead of moving work to a separate protocol, it asks how the network can process more computation, store more state, publish more data, and reach agreement faster while preserving open verification.

The simplest ideas are larger blocks and shorter block times. Both can raise headline throughput, but they increase bandwidth, storage, and CPU requirements. If fewer people can validate the chain independently, scalability has been purchased by weakening decentralization. Good Layer 1 design aims for more capacity per unit of validator resource, or divides work so that no validator must process everything.

The course frames the problem around replicated computation, replicated storage, and consensus communication. Layer 1 techniques attack these bottlenecks through protocol optimization, sharding, and interoperability.

---

## **A Map of Layer 1 Work**

A base-layer transaction passes through several resources. Separating them makes the later techniques easier to understand.

1. **Propagation:** transaction and block bytes travel between nodes.
2. **Execution:** each validator applies program instructions to current state.
3. **State access:** the client reads and writes its database.
4. **Consensus:** validators decide which proposed block is canonical.
5. **Storage and synchronization:** nodes retain enough data and help new or recovering nodes catch up.

Raising a limit in one stage can move the bottleneck to another. A faster virtual machine does not help if blocks cannot reach validators before the next round. More bandwidth does not help if every transaction contends for one state entry.

A useful analogy is a warehouse. Trucks deliver orders, workers pick items, a ledger records inventory, supervisors approve each batch, and archives let a replacement warehouse reconstruct the ledger. Buying faster forklifts improves only the picking stage. Layer 1 scaling measures the entire path.

### **Blocks and propagation**

A **block interval** is the target time between blocks. A **block payload** is the transactions and other data inside a block. Increasing payload or reducing interval sends useful work more often, but gives nodes less time to download and verify it.

Nodes usually use a **gossip network**: each node forwards new data to several peers, which forward it again. Gossip avoids one central broadcaster and survives peer failure, but repeats network traffic. A late block can cause honest producers to build on different tips temporarily, increasing stale work or reorganization risk.

### **World state and state roots**

The **world state** is the current mapping from accounts or object identifiers to values. A full node stores that mapping in a database. The block header includes a compact state root, so another node can verify that execution produced exactly the committed result.

A **state witness** contains values and authentication paths needed for particular reads and writes. It is like giving a checker the few relevant pages of a huge ledger plus seals that connect them to the ledger's signed cover. Stateless validation reduces what the checker stores locally, but a builder or provider must still hold or reconstruct the pages.

### **Shards and cross-shard messages**

A **shard** processes one partition of work. If accounts A and B belong to different shards, their transfer cannot be one ordinary local database update. The source shard records a debit and emits an authenticated message; the destination verifies it before crediting.

This resembles transferring between two banks' ledgers. The receiving bank needs proof that the sending bank finalized the debit, a unique transfer identifier, and a rule preventing the same receipt from being deposited twice. The message is therefore asynchronous: finality and delivery take time.

### **Committees**

A sharded system may assign a subset of validators, called a **committee**, to each shard. Smaller committees process in parallel but give each transaction fewer independent checkers. Random assignment and periodic reshuffling make it harder for an attacker to concentrate validators in one shard.

Committee safety is probabilistic when members are sampled. Later calculations estimate the chance that an attacker controlling a fraction of the total population receives enough seats to control one committee. The formula is less important than the intuition: larger committees cost more communication but make extreme bad samples rarer.

### **How to read the formulas**

This chapter uses letters as labels for quantities. For example, `k` shards means the system has `k` parallel partitions; it does not mean exactly `k` times useful throughput. Cross-shard traffic, uneven demand, and committee communication reduce the ideal gain.

Units travel through every calculation. `MB/s` is data divided by time; gas per second is metered computation divided by time. If unlike units are added or a result drops its unit, the calculation is incomplete.

## **The Four Jobs of a Base Layer**

A general-purpose blockchain performs four related jobs:

1. **Execution** - applying transactions to the current state.
2. **Settlement** - deciding which state transition is canonical and resolving disputes.
3. **Consensus** - ordering blocks and finalizing them despite faulty participants.
4. **Data availability** - ensuring that the data needed to verify a block can be obtained.

A monolithic chain performs all four within one validator network. Every full validator repeats much of the same work. Scaling one job can expose another bottleneck: faster execution is of limited value if block propagation or consensus cannot keep up.

---

## **Vertical Scaling: Making One Chain Faster**

Vertical scaling improves the capacity of a single chain through:

- more efficient clients and databases;
- pipelined block production and execution;
- signature aggregation;
- faster peer-to-peer block propagation;
- a more efficient virtual machine;
- larger blocks or higher gas limits.

These changes matter, but are bounded by validator hardware and network capacity. Larger blocks take longer to propagate and verify. Higher state growth makes it harder for a new node to synchronize. Performance should therefore be reported with latency, hardware, state growth, and validator distribution, not TPS alone.

Gas per second is useful for EVM systems because it measures computational work rather than treating a simple transfer and a complex smart-contract call as identical. It still does not capture data availability or consensus capacity.

---

## **Horizontal Scaling Through Sharding**

<p align="center">
  <img src="../assets/course/ch04_sharding_receipt.svg" width="760" alt="Cross-shard transfer using an authenticated receipt">
  <br>
  <em>Figure 4.1: A source shard debits funds and emits a receipt; the destination verifies finality and inclusion, marks the nonce consumed, and credits once. Original figure for this book, based on the sharding workflow in SC6019 Lecture 02.</em>
</p>


Sharding divides the system into groups that process different portions of the workload. Rather than every node storing and executing every transaction, nodes are assigned to subsets called **shards**.

- **Network sharding** divides validators into committees.
- **Transaction sharding** assigns transactions to committees.
- **State sharding** divides the world state.
- **Execution sharding** processes independent transitions in parallel.

If there are *k* shards operating concurrently, aggregate throughput can grow with *k*. The benefit is horizontal: adding validators can create more processing capacity instead of more replicas of the same work.

### **Random Validator Assignment**

A shard committee is easier to attack than the full network because it is smaller. Random assignment makes it difficult for an adversary to choose the shard it controls. Periodic reshuffling limits long-lived capture.

The security question becomes probabilistic. More, smaller shards improve parallelism but reduce each committee's margin. Sharding changes the point at which the scalability trilemma is managed; it does not eliminate it.

### **Cross-Shard Transactions**

Transactions contained within one shard are simpler. A transaction that reads or writes state across shards requires coordination. A common design uses asynchronous messages:

1. the source shard executes the first part;
2. it emits a receipt;
3. the destination verifies and applies the receipt later.

This preserves parallelism but changes application semantics. Developers must account for delayed completion, partial failure, and asynchronous calls. Atomic composability is harder across shards.

### **State Validity and Data Availability**

Validators outside a shard need confidence that its transition is valid and that the underlying data exists. Techniques include fraud proofs, validity proofs, erasure coding, data availability sampling, and stateless validation with witnesses.

NEAR's Nightshade design represents shards as chunks within one logical chain. Cross-shard actions create receipts, while validators rotate responsibilities for chunk production and validation.[^1]

---

## **Interoperability as a Form of Sharding**

The course compares sharding with an ecosystem of independent chains. Cosmos zones process separate state and communicate through Inter-Blockchain Communication (IBC). IBC uses light-client verification and packet commitments to authenticate messages between chains.[^2]

Both models divide computation and state. Their security differs:

- protocol shards normally inherit one validator set;
- sovereign chains choose their own security and governance;
- shared-security systems sit between them.

Cross-chain communication introduces more assumptions. A bridge is only as safe as its verification mechanism, validator set, upgrade keys, and the chains on both sides.

---

## **Named Case Study: NEAR Receipts and the IBC Packet Lifecycle**

**Deployment labels: NEAR sharding and Inter-Blockchain Communication (IBC) are production.** Both turn a user action into asynchronous work, but at different boundaries. NEAR receipts move work between shards inside one protocol. IBC packets move authenticated application data between sovereign chains through light-client proofs and relayers. In neither system does "sent" mean the remote state has already changed.

### **NEAR: a transfer becomes receipts across shards**

NEAR divides state and execution across shards while blocks contain shard chunks. A signed transaction is routed to the shard holding the signer's account. Executing that transaction can create **receipts**, which are protocol objects carrying actions or data to another account and possibly another shard. NEAR's official transaction lifecycle explicitly separates the block where a transaction arrives, a later block where a receipt is processed, further function-call receipts, and a final refund receipt.[^5]

Trace Alice calling a contract on a different shard. Alice signs a transaction with her account, public-key context, nonce, receiver, actions, recent block hash, and fee-related fields. The transaction reaches the shard responsible for Alice. That shard validates authorization and nonce, charges the attached resources under the protocol rules, and converts the cross-shard action into an outgoing receipt addressed to the receiver. The source chunk commits to the outgoing work. The destination shard later receives the receipt through NEAR's routed receipt mechanism and executes the contract call against destination state.

The destination call may produce another receipt. For example, a marketplace contract on shard B can call a token contract on shard C and then receive a callback. Gas or deposit refunds are also receipts. The user's one transaction hash can therefore lead to a tree or chain of outcomes. NEAR documentation warns that transaction finality and receipt completion are not the same event: a transaction can be final while its generated receipts are still being processed.[^5] [^6]

Observable evidence should include the transaction outcome, receipt IDs, predecessor and receiver accounts, block/chunk locations, execution status for each receipt, logs, generated child receipts, and final refund. A wallet that shows only Alice's top-level transaction as successful can hide a failed remote function call. The safe status model is **transaction accepted**, **source execution complete**, **cross-shard receipt routed**, **destination execution complete**, **callbacks complete**, and **refund complete**.

Failure path: the destination contract panics. The source transaction and receipt creation can remain final while the destination execution records failure. The protocol does not roll back an already committed cross-shard history as if it were one database transaction. Application code must use callback results and idempotent state transitions. If a destination shard is temporarily congested, receipts queue and completion latency rises. If a resharding boundary moves accounts, routing and pending receipts must migrate together; otherwise a receipt can be lost or executed twice. If Alice resubmits because the interface still says pending, nonce and receipt identifiers must prevent accidental duplicate action.

The trust assumptions are those of one NEAR protocol: validator consensus, correct chunk validation and availability, deterministic runtime execution, routing, and shard-state handoff. Users do not choose an external relayer for an ordinary cross-shard receipt. This tighter integration improves uniformity, but a bug in the shared runtime, routing rules, or resharding logic can affect all applications using the mechanism.

### **IBC: send, relay, receive, acknowledge, or time out**

IBC connects chains through on-chain light clients, connections, channels, packet commitments, and permissionless relayers. The packet lifecycle documentation names four application-visible stages: send on the source, receive on the destination, acknowledgement on the source, and timeout on the source.[^7] [^8]

Trace a fungible-token transfer from Chain A to Chain B. The application on A escrows or burns the source representation under the token-transfer rules and calls the IBC channel to send a packet. The packet binds source and destination ports and channels, a sequence, payload, and a timeout height or timestamp. Chain A stores a commitment to the packet. This commitment is the fact a relayer later proves; no trusted courier signature is required.

A relayer observes the committed packet, waits for the source state needed by the destination's light client, and submits a receive message to Chain B with a proof. The IBC handler on B verifies that proof against its client of A, checks channel and sequence rules, prevents duplicate receipt, and invokes the destination application. The application writes an acknowledgement indicating success or an encoded error. Chain B commits that acknowledgement.

A relayer then submits the acknowledgement and proof back to Chain A. A verifies it through its light client of B, deletes or completes the packet commitment under the protocol rule, and calls the source application acknowledgement callback. The token application can finalize accounting and emit a user-visible result. Relayers may be paid or operated by third parties, but they do not gain authority to forge a packet that fails light-client, channel, sequence, and commitment checks.

If no valid receive occurs before the packet's timeout, a relayer or user submits a timeout proof to Chain A. The proof establishes that the destination passed the timeout condition without receiving the packet, under the channel rules. The source application runs its timeout callback and can unescrow or restore the user's asset. Receive and timeout race across two chains, so the proof rules and packet-receipt state ensure only one terminal outcome succeeds.

Observable evidence includes the source transaction, packet sequence and commitment, client heights, relayer transactions, destination receipt, acknowledgement bytes, source acknowledgement callback, and any timeout proof. "Relayed" is ambiguous: it must say whether a receive proof was submitted, verified, executed, acknowledged, and processed back at the source. Ordered and unordered channels also differ. An ordered channel enforces sequence and can close or block on timeout under its protocol rules; an unordered channel permits independent packet delivery while still preventing replay.

Failure path: every relayer goes offline. Funds are not automatically stolen, but progress stops until someone relays receive or timeout evidence. If Chain B halts before the timeout, Chain A may need a proof tied to a usable client state; client expiry or a frozen client can complicate recovery. If the destination application returns an error acknowledgement, the source callback must refund or unwind according to application rules rather than calling the packet a success. If a chain's consensus safety fails, its light-client security assumption fails too. IBC authenticates the state of the connected chains; it does not make a compromised source or destination chain honest.

### **What the comparison teaches**

| Boundary | NEAR cross-shard receipt | IBC packet |
|---|---|---|
| Security domain | One sharded protocol and validator system | Two sovereign chains plus on-chain light clients |
| Transport actor | Protocol routes receipts between shard chunks | Permissionless relayers carry proofs and messages |
| Unique work item | Receipt ID and receipt dependency graph | Port/channel pair and packet sequence |
| Completion | Destination receipt and all required callbacks/refunds execute | Receive plus acknowledgement processed, or valid timeout executes |
| Replay defense | Runtime receipt identity, nonce and execution state | Packet commitment, receipt/ack state, sequence and channel rules |
| Main liveness failure | Congested or unavailable shard/chunk path | No relayer, halted chain, expired/frozen client, unavailable proof |
| Application obligation | Handle asynchronous promise result and callback failure | Handle acknowledgement error and mutually exclusive timeout/refund |

The shared programming rule is to record intent before sending asynchronous work, make the remote handler idempotent, bind callbacks to the original request, and expose a terminal error or timeout path. The major difference is proof scope. NEAR consensus knows the source and destination shards. IBC's destination verifies a proof of source-chain state through a client, then the source verifies destination acknowledgement or timeout evidence in return.


## **Ethereum's Rollup-Centric Data Sharding**

Early Ethereum roadmaps emphasized execution shards. The rollup-centric roadmap shifted priority toward data capacity. Rollups execute outside Ethereum but publish data needed for reconstruction and verification. Increasing cheap data capacity can scale many rollups at once.

EIP-4844 introduced blob-carrying transactions, or proto-danksharding. Blob data is committed to by consensus but unavailable to EVM execution and retained only for a defined period. It provides a separate data market for rollups and groundwork for sampling.[^3]

Full danksharding aims to expand blob capacity while allowing nodes to verify availability without downloading every blob.[^4] This is Layer 1 scaling designed primarily to support Layer 2 execution.

---

## **Trade-Offs**

| Technique | Main Gain | Main Risk |
|---|---|---|
| Larger or faster blocks | More transactions per unit time | Higher node requirements and propagation pressure |
| Client or VM optimization | More work from the same hardware | Network or storage becomes the next bottleneck |
| Sharding | Parallel execution and storage | Smaller security domains and cross-shard complexity |
| Appchains | Isolation and sovereignty | Fragmented liquidity and separate security |
| Data sharding | More capacity for rollups | Sampling, coding, and networking complexity |

A production protocol must handle committee corruption, data withholding, partitions, validator churn, and state synchronization. The recovery path often determines real security.

## **Worked Example: A Cross-Shard Transfer**

Consider Alice on shard A paying Bob on shard B. Shard B must not credit Bob unless shard A has irrevocably debited Alice. A practical design uses an authenticated receipt. Shard A verifies Alice's signature and balance, debits ten tokens, and places a receipt in an outgoing queue. The receipt names the destination, Bob's account, the amount, a nonce, and proof that shard A finalized the debit. Shard B later verifies the proof and consumes the receipt exactly once. The nonce prevents replay.

The transfer is economically atomic but not simultaneous. Between debit and credit, the payment is in flight. Applications must expose that intermediate state. Congestion on shard B can delay delivery, and a contract on shard A cannot assume an immediate callback from shard B. Cross-shard calls therefore look more like reliable message passing than like calls inside one EVM transaction.

The protocol must price receipt queues, bound their growth, handle reorganizations, and define what happens when a destination rejects a message. Aggregate shard throughput alone hides these costs.

## **Committee Security by Calculation**

Suppose 1,000 validators include 250 controlled by an adversary. The protocol forms committees of 100 and fails if more than one-third of any committee is Byzantine. The expected adversarial count is 25, but an attack needs at least 34. Security depends on the tail probability of drawing that many attackers, not on the average.

Smaller committees create more parallel shards but widen this tail risk. Rotation limits persistent targeting, yet it costs bandwidth because validators need new shard state. Committee size, reshuffle frequency, validator stake distribution, and the fault threshold must be evaluated together.

## **Implementing a Sharded State Machine**

A sharding protocol needs more than a partition function. It must specify which shard owns each state item, how validators learn their assignment, how blocks commit to every shard, and how messages survive validator rotation.

A simple account partition might define `shard(account) = hash(account) mod k`. This balances random account addresses reasonably well, but it cannot balance activity. A popular contract can make one shard hot while others remain idle. More advanced designs move ranges or split state dynamically, but migration itself consumes capacity and changes which committee can authenticate a receipt.

A shard block normally commits to its input messages, transactions, resulting state, and outgoing messages. One conceptual header is:

```text
ShardHeader {
    shard_id
    height
    previous_shard_root
    input_receipts_root
    transactions_root
    new_state_root
    output_receipts_root
    committee_signature
}
```

The roots bind execution to the exact inputs and outputs. The committee signature certifies the header under the shard's fault rule. A beacon chain or common consensus layer can then order shard headers and make their receipts final.

### **Receipt Processing**

A destination shard should treat an incoming receipt like an authenticated, exactly-once message:

```text
process(receipt, proof):
    require verify_source_finality(receipt.source_header, proof)
    require receipt.destination_shard == this_shard
    require not consumed(receipt.id)
    require receipt.expiry >= current_height

    mark_consumed(receipt.id)
    result = execute(receipt.payload)
    emit acknowledgement(receipt.id, result)
```

The consumed marker prevents replay. Marking before external execution prevents reentrancy-like duplicate consumption. An expiry bounds queue lifetime, but requires a refund or cancellation rule on the source shard. If acknowledgements can themselves fail, the application needs an idempotent retry path.

### **Validator Rotation and State Handover**

Randomly rotating validators frustrates adaptive corruption, but a validator joining a shard needs its state. Downloading full state at every epoch can dominate bandwidth. Checkpoints, snapshots, state-sync proofs, and witnesses reduce this cost.

The handover boundary is security-sensitive. The old committee must not sign two final checkpoints, and the new committee must not process receipts against an unfinalized snapshot. Protocols often overlap committees or anchor the transition in a common beacon block.

## **Sharding Failure Modes**

**Single-shard capture.** An adversary gains enough committee seats to certify an invalid transition. Random assignment, adequate committee size, slashing, and cross-shard fraud or validity proofs reduce this risk.

**Data withholding.** A committee certifies a header but withholds the body. Other shards cannot verify receipts. Erasure coding and availability attestations make withholding detectable.

**Receipt flooding.** One shard creates more cross-shard messages than another can process. Per-destination queues, fees, rate limits, and backpressure prevent unbounded memory.

**Hot shard.** A popular application concentrates load. Dynamic resharding, application-level partitioning, and asynchronous subcomponents can redistribute work, but cannot make a single sequential state variable parallel.

**Correlated validators.** Random keys are not independent operators. If many validators share hosting, software, or control, committee probability computed from keys overstates resilience.

## **L1 Engineering Checklist**

Before claiming horizontal scale, a design should answer:

1. Which state and transactions belong to each shard?
2. What is the committee-selection distribution and corruption model?
3. How are cross-shard receipts authenticated, replay-protected, and expired?
4. What happens to an in-flight receipt across reorganization or resharding?
5. How does a new validator obtain state and prove its correctness?
6. How is unavailable shard data detected and recovered?
7. Which workloads create hot shards?
8. Does aggregate throughput include cross-shard communication and state sync?

## **State Sharding Design Choices**

A state-sharded chain must choose a partition key. Hash partitioning spreads addresses evenly but ignores application locality. Range partitioning keeps related keys together but can create hot ranges. Application-aware partitioning can reduce cross-shard calls but gives protocol designers or developers more responsibility.

Contracts complicate ownership. If a contract's code lives on one shard but its users' balances live elsewhere, calls become messages. If the complete contract state stays together, a popular application becomes a hot shard. If storage slots are split, one contract invocation may need several asynchronous reads.

There is no partition function that makes every workload local. A protocol can expose placement hints, support dynamic resharding, or encourage applications to model state as independent objects. Each choice moves complexity between the protocol and application.

### **Dynamic Resharding**

Dynamic resharding splits a busy shard or combines quiet shards. A safe split needs a finalized boundary:

1. choose a source checkpoint;
2. partition its state into child commitments;
3. assign new committees;
4. route new transactions by the new mapping;
5. forward or transform receipts created under the old mapping;
6. retain proofs linking child roots to the source root.

During transition, clients may hold stale routing information. Gateways can forward requests, but signatures and receipts should bind logical destination state rather than a transient network endpoint. Migrations also need backpressure; moving a large state database while processing peak load can worsen the congestion that triggered the split.

## **Stateless Validation and Witnesses**

A stateless validator receives the values and authentication paths needed for a block's reads. Starting from the prior state root, it verifies each witness, executes the block, applies writes, and obtains the new root.

If an account proof contains `O(log n)` hashes, a block touching many unrelated accounts carries many paths. Multiproofs share common branches. Verkle trees use vector commitments to reduce witness size for wide state. Smaller witnesses lower validator storage needs but increase builder duties and cryptographic verification.

Witness availability becomes part of block validity. A proposer that announces a header without witnesses can stall validators even when transaction data is available. Builders need full or distributed state access to construct witnesses, creating a risk that cheap validation centralizes production.

## **Cross-Shard Contract Pattern: Request and Callback**

Synchronous code might write:

```text
price = oracle.read(pair)
settle_trade(price)
```

Across shards, the caller sends a request and returns. The oracle later sends a callback:

```text
request_id = send oracle.read(pair)
store PendingTrade(request_id, user, limits, expiry)

on_oracle_reply(request_id, price):
    trade = load PendingTrade(request_id)
    require not trade.completed
    require now <= trade.expiry
    require price satisfies trade.limits
    mark trade.completed
    settle_trade(price)
```

The application must handle duplicate, late, missing, and reordered replies. It should not lock unrelated global state while waiting. This pattern resembles distributed services, with the added need for authenticated receipts and deterministic execution.

## **Sharding and Composability Economics**

Cross-shard calls consume source execution, consensus on the source receipt, network delivery, destination verification, and destination execution. Pricing only the source call subsidizes remote work and invites flooding. A fee can reserve destination capacity or let the receipt carry a budget refunded when unused.

Developers then face locality economics. Contracts interacting frequently have an incentive to share a shard; popular clusters become hot. Dynamic placement may improve throughput but changes latency and fees. Tooling should profile cross-shard call graphs before deployment and show developers which state edges dominate cost.

## **Stateless Validation: Witness Construction and Update**

Stateless validation replaces a validator's full local state lookup with a witness proving the values a block reads and changes. It reduces validation storage requirements, but moves witness production and bandwidth into the critical path.

Assume the prior state is committed by root `R0`. A transaction reads account `A`, checks its nonce and balance, debits it, and credits account `B`. The block builder supplies values plus authentication paths from each touched key to `R0`.

```text
StateWitness {
  pre_state_root,
  keys[],
  pre_values[],
  proof_nodes[],
  access_order,
  commitment_version
}
```

The validator verifies each pre-value under `R0`, executes the canonical transaction, replaces the changed leaves, and recomputes root `R1`. The block is valid only if `R1` equals its declared post-state root.

### Multiproofs

Independent Merkle proofs repeat nodes near the root. A multiproof shares common branches across many keys. Witness size depends on how accesses cluster: 1,000 adjacent keys can share more path material than 1,000 uniformly random keys.

Canonical multiproof encoding matters. The verifier needs an unambiguous rule for node order, omitted siblings, duplicate keys, empty values, and tree depth. Two encodings that prove the same leaves may be acceptable, but they must calculate one root and have bounded decoding work.

### Reads after writes

A block can read a value written by an earlier transaction in the same block. The witness authenticates the value at the block's pre-state; the executor's in-block state overlay supplies later reads. Builders should not provide a second contradictory "pre-state" proof for a value already changed in the block.

Access order and transaction order determine this overlay. Parallel execution may speculate, but final witness verification must reproduce canonical semantics.

### Missing and extra witness data

A missing proof node makes the block unverifiable and should reject it. Extra unused nodes consume bandwidth and parsing work; charge or cap them to prevent denial of service. Duplicate or cyclic references in a compressed witness must not cause unbounded memory or CPU.

The runtime can discover an undeclared key through a dynamic contract call. The block builder must include its witness. Access lists can help prefetching, but consensus validity follows actual execution, not a sender's incomplete prediction.

### State providers and builder concentration

Validators can be stateless while someone still stores state to build blocks and witnesses. If one state provider serves every builder, storage centralization moves rather than disappears. A production design supports multiple providers, snapshot reconstruction, authenticated queries, and a way for a new builder to acquire current state.

A provider cannot forge a value when proofs are checked, but it can censor or selectively delay keys. Builders need redundant queries and enough time to assemble witnesses before proposal deadlines.

### Witness bandwidth calculation

Suppose a block executes 2,000 transactions, touching 3 unique state keys each after deduplication. An average multiproof contribution of 180 bytes per unique key gives:

```text
2,000 × 3 × 180 B = 1.08 MB
```

If blocks arrive every 2 seconds, witness payload alone averages 540 kB/s before transaction data, signatures, networking overhead, and bursts. A hot workload may reduce unique keys and witness bytes while increasing execution contention; a random workload does the opposite.

Do not assume witness size scales linearly from one transaction. Measure deduplication, path sharing, code proofs, and the current tree shape. Report compressed and uncompressed size plus verification CPU.

### Witness generation pipeline

A builder:

1. selects ordered transactions;
2. simulates or executes to discover actual accesses;
3. fetches pre-state values and proof nodes;
4. deduplicates keys and builds a canonical multiproof;
5. re-executes against the witness as a validator would;
6. checks the resulting root;
7. publishes transactions and witness before the proposal deadline.

Late access discovery can force another state query and delay the block. Builders can prefetch from access lists or recent traces, but they must validate fetched proofs against the current root.

### Witness test matrix

Test:

- absent accounts versus zero-valued accounts;
- repeated read and write of one key;
- contract creation and deletion semantics;
- dynamic code and storage access;
- a read after an earlier in-block write;
- duplicate, reordered, extra, and missing proof nodes;
- maximum depth and largest code witness;
- prior-root mismatch after a reorganization;
- parallel execution followed by canonical root update;
- builder restart after state selection but before publication.

Differentially compare full-state execution with witness-only execution for generated blocks. Assert identical receipts, gas, logs, and post-state root. Then delete the full state from the validator environment and confirm that every required input is present in the published witness.

Statelessness succeeds when ordinary validators can verify and synchronize cheaply while block building and state service remain competitive, observable, and recoverable.

## **State Expiry and Revival Operations**

State expiry bounds the active state by removing data that has not been touched for a defined horizon. It is different from history expiry: history concerns old blocks and receipts, while state determines what the next transaction can read and change.

An expiry design needs four precise rules:

1. which objects expire: accounts, storage slots, contract code, or tree segments;
2. which event refreshes them: read, write, proof submission, or fee payment;
3. which commitment preserves expired values;
4. how a transaction revives data and who supplies the proof.

If these rules are vague, clients can disagree about whether a key is active and derive different state roots.

### Epoch transition

Consider 90-day expiry epochs. At the transition from epoch `e` to `e+1`, untouched leaves are removed from the active tree, but their values remain committed by an expiry accumulator root `E_e`. Active state root `A_e` and expiry roots jointly define the valid state universe.

```text
BlockState {
  active_root,
  expiry_roots[],
  expiry_policy_version,
  current_epoch
}
```

The number and retention of expiry roots must be bounded. Otherwise a client trades one ever-growing state structure for an ever-growing list of commitments.

### Revival transaction

Suppose Alice's account expired with nonce 17 and balance 4 ETH. A transaction that needs it carries:

- the historical value;
- a proof to the applicable expiry root;
- enough active-tree path data to insert the revived leaf;
- a transaction whose signature and nonce are checked against the revived value;
- any revival fee required by protocol rules.

The validator verifies the expiry proof, confirms the leaf has not already been revived or superseded, inserts it into active state, and then executes the transaction. An attacker must not be able to revive an older version of a key after a newer version exists.

### Worked revival cost

Assume a revival witness includes a 1,250-byte account proof, 600 bytes of code metadata, and 2,400 bytes for four storage slots. If calldata-equivalent accounting prices witness bytes at 8 gas each, the data component is:

```text
(1,250 + 600 + 2,400) B × 8 gas/B = 34,000 gas
```

Add 28,000 gas for proof verification and tree insertion:

```text
34,000 + 28,000 = 62,000 gas
```

At 20 gwei, that is `0.00124 ETH`, before the transaction's ordinary execution. This example is a cost model, not a recommendation: real pricing must track verification CPU, bandwidth, retained-state burden, and denial-of-service limits.

### Who retains expired data?

A commitment does not make values available. Users need archival nodes, wallets, applications, state-service markets, or their own backups to recover values and proofs. Protocol designers should state the recovery assumption explicitly.

A wallet that creates an account or contract can retain a compact recovery package: key identifiers, values, code, relevant expiry epoch, and proof-service hints. But proofs can become stale as commitment schemes migrate, so recovery tooling needs versioning and conversion paths.

Applications with many users cannot assume each user will preserve every storage value. They may sponsor state rent, refresh required keys, maintain proof services, or redesign storage so critical claims can be reconstructed from durable logs or user-held receipts.

### Incentives and abuse resistance

If touching a key refreshes its lifetime for free, an attacker can cheaply keep a large state set alive. Charge refresh according to the burden imposed, cap witness decoding, and decide whether a read refreshes state or only a write/payment does.

Revival also creates burst risk. A popular dormant application may revive thousands of keys after a news event. Benchmark epoch boundaries and revival storms, not just steady-state transactions.

State providers can extort users through availability rather than invalid data. Mitigations include redundant archives, standardized proof APIs, erasure-coded snapshots, periodic recovery drills, and application-level export tools.

### Reorganizations and epoch boundaries

A reorganization across an expiry boundary can change which keys expired and which root authenticates them. Clients must retain rollback information for the maximum reorganization window and avoid deleting values immediately at transition. Finalization should gate irreversible pruning.

A transaction prepared against one expiry root may become stale after a reorganization. Its failure should be explicit and safely retryable; a wallet should fetch a fresh proof rather than repeatedly rebroadcasting invalid data.

### Migration and release checklist

Before enabling expiry:

- publish object-level refresh and expiry semantics;
- prove that old values cannot overwrite newer ones;
- provide at least two independent archival/revival implementations;
- test recovery without the original full node;
- measure normal witnesses, revival storms, and epoch transitions;
- specify reorganization rollback and pruning delays;
- version commitment and proof formats;
- expose wallet warnings before state becomes costly to revive;
- document which data availability promises are protocol guarantees and which depend on services;
- rehearse commitment migration and archive-provider failure.

State expiry is operationally credible only when a user can return after the horizon, obtain the right data from more than one source, verify it against consensus commitments, and safely resume activity.

## **History Expiry, Archives, and Verifiable Queries**

Live consensus does not require every validator to retain every old block forever. **History expiry** lets ordinary nodes discard old bodies, receipts, or auxiliary indexes after a retention window while preserving commitments needed to authenticate the canonical past.

History expiry differs from state expiry. History explains how state arrived; state contains values execution may need next. A node can prune old receipts while retaining current balances, or expire inactive state while archives retain history.

### Data classes

Specify retention separately for:

- block headers and finality evidence;
- block bodies and transactions;
- receipts, logs, and events;
- state snapshots and diffs;
- consensus votes and slashing evidence;
- blobs or external DA payloads;
- indexes derived from canonical data;
- debugging traces that may not be consensus data.

Applications often depend on logs and indexes even when consensus does not. "The chain retains history" is incomplete without class and duration.

### Commitments and proofs

A retained header may commit to transaction and receipt roots. An archive can answer a query with the item plus a Merkle proof to the finalized header. The client also needs an authenticated header chain or checkpoint.

An indexer response such as "all transfers by Alice" is harder. A Merkle proof can authenticate returned events but does not prove no matching event was omitted unless the protocol commits to a suitable index. Completeness may require scanning every relevant block or using a verifiable indexed structure.

Distinguish:

- **membership:** this item is in committed history;
- **non-membership:** this key is absent from a committed set;
- **completeness:** these are all items matching a query;
- **canonicality:** the containing header is on finalized history.

### Archive providers

Archive service is operationally replaceable only when data formats, proofs, and request APIs are open and several providers retain the same history. A single public endpoint backed by one hidden database is a centralized dependency even if responses are authenticated.

Providers can omit or delay data without forging proofs. Clients use redundant sources, content-addressed snapshots, peer exchange, and local verification. Publish retention commitments and measure whether old random ranges remain retrievable.

### Portal and peer networks

A distributed history network can partition data across peers and retrieve by content key. Availability depends on replication, incentives, routing, and repair. Cryptographic hashes authenticate content but do not ensure a peer stores it.

Measure unique providers by failure domain, replica count by age, lookup latency, failed ranges, repair time, and survival after high-capacity peers leave.

### Pruning safety

A node should prune only after finality and the maximum reorganization window required by policy. Delete in resumable batches and preserve enough metadata to distinguish intentionally pruned data from corruption.

Snapshots used for sync need a verified successor path. Do not delete the only local state needed to reconstruct or roll back a snapshot activation still in progress.

Pruning can race RPC queries and indexers. Return an explicit "pruned before height H" response rather than null, which users may misread as proof that no event exists.

### Worked storage budget

Suppose canonical history grows by 3 MB/s. Raw annual growth is:

```text
3 MB/s × 31,536,000 s ≈ 94.6 TB/year
```

Ten independent full replicas require about 946 TB before encoding, indexes, backups, and overhead. If ordinary nodes retain 30 days:

```text
3 MB/s × 2,592,000 s ≈ 7.78 TB
```

That is still substantial. Compression, data-class separation, and lower-rate historical serving matter. Report measured rather than theoretical compression.

### Retrieval economics

Uploading data once does not fund indefinite serving. Archive models include protocol rewards, storage contracts, application payments, institutional archives, and voluntary replication.

Price retrieval separately from retention. A provider paid to store data may still throttle egress during mass exits. Recovery capacity must cover correlated demand, not ordinary query traffic.

If users need old data to withdraw, retention duration and retrieval throughput are part of asset safety. A proof window longer than data retention creates an impossible recovery path.

### Migration and format changes

Old history may use earlier transaction, receipt, commitment, or compression formats. Archive software needs versioned decoders and test vectors. Converting data into a new container must preserve the old canonical hash and proof relationship.

Retain original bytes when signatures or hashes cover exact encoding. Semantic reserialization can change hashes even if fields look equal.

### Privacy and legal operations

Public history may contain personal or unlawful content that cannot be removed from commitments. Service operators can limit indexing or serving under law, but should not claim the protocol erased what remains reconstructible elsewhere.

Avoid collecting unnecessary off-chain metadata in archive logs. Access patterns can reveal user interests even when chain data is public.

### Recovery drill

From a new machine and no privileged database:

1. authenticate a finalized old header;
2. retrieve a random block body, receipt, and blob from independent providers;
3. verify each commitment and canonicality;
4. reconstruct an application query across a range and test completeness;
5. remove the largest provider and repeat under burst load;
6. identify a deliberately unavailable range and exercise escalation or repair.

### Release assertions

Publish retention by data class, provider and region diversity, oldest retrievable height, random-range success rate, proof-verification tooling, pruning boundary, format migration policy, and recovery throughput.

History expiry is responsible when ordinary validation becomes cheaper while old evidence remains verifiably recoverable from a plural archive ecosystem for every protocol and user deadline that depends on it.

## **Mempool Admission and Denial-of-Service Control**

Before a transaction reaches a block, nodes receive, validate, store, and relay it in a **mempool**. Mempool capacity is not consensus capacity: attackers can consume CPU, memory, bandwidth, and database lookups with transactions that never become valid blocks.

### Admission pipeline

Apply checks from cheapest to most expensive:

1. bound message length and decode canonical fields;
2. check chain ID, version, and basic structure;
3. reject known duplicates and expired transactions;
4. verify fee floor and intrinsic resource bounds;
5. verify signature or authorization;
6. check nonce and obvious balance conditions against current state;
7. run bounded simulation when policy requires it;
8. store and relay under local limits.

Consensus validation still rechecks the transaction in a block. Mempool admission is local resource policy and must not become an undocumented consensus rule that prevents valid forced inclusion.

### Cheap-to-send, expensive-to-check

An attacker seeks **asymmetry**: a small request causing large work. Examples include malformed encodings that parse deeply, signatures using expensive paths, contract-account validation, state reads over cold keys, and simulations that allocate memory before reverting.

Cap nesting, lengths, decompression, signatures per envelope, validation gas, state accesses, and concurrent simulations. Cache valid and invalid results only with state/version keys that prevent stale decisions.

### Nonces and replacement

Account nonces normally impose order. If nonce 10 is missing, nonces 11-100 may wait. Attackers can create long gaps or repeatedly replace one transaction.

Limit queued future nonces per account and globally. A replacement must increase the relevant fee by a clear rule and preserve nonce and sender. Rate-limit replacement churn so tiny fee increments cannot force peers to repeatedly validate and gossip.

Structured nonce lanes need per-lane caps. Thousands of lanes can bypass a per-account sequential limit unless the account has an aggregate budget.

### Fee floors

A local fee floor filters transactions unlikely to pay for scarce resources. It should reflect encoded bytes, execution, state access, and validation cost. One gas scalar may underprice large signatures or complex account validation.

Dynamic floors respond to congestion, but peers can have different policies. Wallets need rejection reasons and current minimums. A low-fee valid transaction may remain eligible for direct block inclusion even if many mempools drop it.

### Eviction

When full, evict by an auditable policy using fee value, age, dependencies, and resource shape. Avoid one global fee-per-byte score that lets compute-heavy transactions crowd out bandwidth-efficient work or vice versa.

Evict dependent future-nonce transactions when their required predecessor disappears, or mark them parked with bounded storage. Do not gossip repeated evictions endlessly between peers with incompatible policy.

### Per-sender and per-peer limits

One sender can generate many keys, so identity-based limits alone do not stop Sybils. Combine sender, peer, IP/network, resource, and global limits cautiously. Network limits should not permanently exclude shared gateways or privacy networks.

Peers earn relay capacity through useful behavior, but reputation must decay and resist poisoning. A malicious peer should not cause an honest transaction to be globally blacklisted merely by sending it first.

### Gossip amplification

In a network of `N` nodes with average fanout `d`, naive forwarding can create many duplicate deliveries. Nodes advertise transaction hashes, request unknown bodies, deduplicate, and batch announcements.

Suppose 10,000 nodes each receive 2,000 new transactions per second and an average encoded transaction is 300 bytes. One full copy per node is already:

```text
10,000 × 2,000 × 300 B = 6 GB/s ecosystem ingress
```

Duplicates, inventory messages, and signatures add overhead. Measure per-node bandwidth and duplicate ratio under burst, not only average transaction rate.

### Reorganizations

Transactions from reverted blocks may return to the mempool if still valid. Recheck nonce, balance, fee, expiry, and conflicts against the new canonical state. Do not blindly restore a prior mempool snapshot.

Large reorganizations can cause a reinsertion storm while nodes also execute the new branch. Prioritize consensus catch-up and bound revalidation work.

### Privacy

Public mempools reveal sender, calls, amounts, and fee willingness before inclusion. Private endpoints reduce broadcast but give operators information and censorship power. Encrypted mempools change payload visibility while retaining size, timing, and ingress metadata.

Document retention and sharing. Mempool logs can contain sensitive pending actions that never appear on-chain.

### Observability

Track admitted, rejected, parked, replaced, evicted, expired, and included transactions by reason; validation CPU; state-read latency; memory/bytes; sender and peer concentration; duplicate gossip; oldest eligible age; and inclusion outcomes.

A growing mempool can mean demand exceeds capacity, a producer censors, fees are mispriced, or nonce dependencies are missing. Metrics need these dimensions.

### Adversarial tests

Flood malformed maximum-size envelopes, invalid signatures, cold-state checks, nonce gaps, replacement churn, many account-abstraction lanes, low-fee Sybils, conflicting transactions, peer reconnect loops, and reorganization reinsertion.

Assert bounded memory and validation work, continued admission for honest target traffic, no crash or unbounded queue, specific rejection reasons, and consensus catch-up priority.

The mempool is an untrusted network-facing scheduler. Scaling blocks without scaling and defending admission merely moves failure to the system's front door.

## **Node Synchronization and Snapshot Recovery**

A chain has not scaled sustainably if existing validators keep up but a replacement node cannot join, recover, or audit state within an acceptable window. Synchronization is part of the protocol's availability and decentralization budget.

A new node can obtain state in several ways:

- **genesis replay:** download and execute every block from genesis;
- **checkpoint sync:** start from a trusted or consensus-verified finalized checkpoint;
- **snapshot sync:** download a state snapshot committed by a finalized header, verify its chunks, then replay later blocks;
- **state sync:** request authenticated state ranges from peers while following headers;
- **witness sync:** verify new blocks from witnesses without first storing the entire state.

Genesis replay provides the strongest independent historical reconstruction but becomes slow as history and state grow. Snapshot sync reduces time to participation, but it must not turn a convenient file into an unexamined trusted database.

### Authenticated snapshot format

A snapshot manifest should bind:

```text
SnapshotManifest {
  chain_id,
  protocol_version,
  finalized_height,
  block_hash,
  state_root,
  chunk_count,
  chunk_hashes_root,
  state_encoding_version,
  compression,
  created_at
}
```

Each chunk has an index, uncompressed length, compressed length, content hash, and proof to `chunk_hashes_root`. After decoding all chunks, the client reconstructs the canonical state commitment and checks it against `state_root` from the finalized block.

Chunk hashes detect transfer corruption; the final state-root check detects a malicious but internally consistent snapshot. Both are needed. The decoder must reject duplicate keys, non-canonical encodings, decompression bombs, out-of-range lengths, overlapping ranges, and trailing data.

### Checkpoint trust

A hard-coded checkpoint is an explicit trust decision. A weak-subjectivity checkpoint may be needed when former validators can sign an alternative old history after exiting. Operators must know who distributes the checkpoint, its age limit, how it is authenticated, and how to obtain the same value through independent channels.

A BFT finality certificate can authenticate a checkpoint if the client already trusts the applicable validator set and verifies every set transition. A proof-of-work header chain needs its own accumulated-work and eclipse-resistance assumptions. "Fast sync" is not one security model.

### Worked catch-up budget

Suppose the active snapshot is 1.2 TB compressed and the node has 400 Mbps usable ingress. Ignoring overhead, transfer time is:

```text
1.2 TB × 8 / 400 Mb/s = 24,000 s ≈ 6.7 hours
```

If verification and insertion sustain only 25 MB/s, local processing takes:

```text
1,200,000 MB / 25 MB/s = 48,000 s ≈ 13.3 hours
```

Processing, not bandwidth, is the first bottleneck. Meanwhile the chain continues producing blocks. At 3 MB/s of new data, a 13.3-hour sync creates another roughly 144 GB of catch-up traffic. The node must process historical catch-up faster than the chain's live growth or it never converges.

Report time to header verification, snapshot acquisition, state-root verification, head catch-up, and validator readiness separately. "Synced" should mean the node can safely perform its intended role, not merely that it opened a peer connection.

### Peer and provider diversity

Downloading chunks from many addresses does not provide diversity if they share one cloud bucket or snapshot producer. Record snapshot producer, serving provider, region, autonomous system, and software implementation. Randomize requests so one peer cannot selectively shape all ranges.

A malicious peer can send valid but useless old chunks, stall the last range, or repeatedly trigger expensive decoding. Use per-peer deadlines, authenticated range selection, bounded concurrent work, resumable progress, and penalties that do not let an attacker evict honest peers cheaply.

### Crash consistency

Persist the verified manifest before chunks, record each completed chunk atomically, and make state installation idempotent. On restart, recheck stored chunk hashes and continue; do not silently mix chunks from different manifests or protocol versions.

Install the reconstructed database with an atomic directory or generation switch. If the process crashes during activation, it must restart from either the old database or the complete new one, never a partial mixture. Retain rollback state until the post-snapshot block replay and state-root checks succeed.

### Snapshot production

Producing a snapshot can contend with block execution for disk bandwidth and cache. Generate from a consistent finalized database view, not a live collection changing beneath the exporter. Bound memory, stream chunks, and verify the finished artifact using a separate importer before publishing it.

Multiple independent operators should produce snapshots for the same height. Byte-for-byte files may differ because of compression or chunking, but all must reconstruct the same canonical state root.

### Recovery drill

A release drill should:

1. remove the node's state database;
2. authenticate a finalized checkpoint through the documented rule;
3. download a snapshot with one corrupt, one delayed, and one unavailable serving peer;
4. crash during chunk verification and again during database activation;
5. resume without redownloading verified data;
6. reconstruct the exact committed state root;
7. replay blocks to the live head while load continues;
8. join validation without missing its operational readiness target.

Measure bytes, CPU, peak memory, disk amplification, random I/O, elapsed time, peer failures, and catch-up margin over live growth. Repeat from at least two geographic regions and on the minimum supported hardware.

Snapshot sync is credible when a skeptical operator can authenticate the checkpoint, reconstruct state from interchangeable providers, survive interruption, and converge faster than the chain grows without copying an incumbent's trust assumptions.

## **Worked Resharding Trace: Moving a Hot Account Range**

Static shards eventually become unbalanced. A popular application can saturate one shard while others remain idle. Dynamic resharding changes the partition map without losing, duplicating, or accepting transactions against two owners of the same state.

Assume shard `A` owns keys in range `[m, z]`. The protocol will move `[t, z]` to new shard `B` at epoch `E+1`. The transition needs an authenticated handoff point.

### Prepare

Before the boundary, consensus finalizes a resharding plan:

```text
ReshardPlan {
  plan_id,
  source_shard = A,
  destination_shard = B,
  key_range = [t, z],
  freeze_height,
  activation_epoch = E + 1,
  source_state_root,
  protocol_version
}
```

The plan is part of canonical state. Nodes reject a local operator command that changes ownership without this decision. Clients learn the future map early enough to route transactions and update proofs.

At `freeze_height`, shard `A` stops accepting new writes to the moving range under the old routing version. It finishes earlier transactions and outbound receipts, then commits a root for the frozen range. Reads may continue if the API labels the snapshot and prevents stale writes.

### Transfer

Shard `A` exports state leaves, contract code, storage, pending asynchronous messages, consumed-message nonces, and any rent or metadata required to interpret the range. A snapshot manifest binds chunks to the finalized range root:

```text
SnapshotManifest {
  plan_id,
  range_root,
  chunk_commitments[],
  pending_message_root,
  consumed_nonce_root,
  total_bytes
}
```

Shard `B` retrieves chunks from several peers, verifies every commitment, reconstructs the range, and replays or imports pending message state under a deterministic rule. Importing account balances without replay-protection state would let an old cross-shard receipt execute again after migration.

### Activate

At epoch `E+1`, validators agree on a partition map assigning `[t,z]` to `B` and an activation commitment produced by the import. Transactions carry or derive the routing version. Shard `A` rejects new-version writes to the range; shard `B` rejects old-version writes except explicitly authenticated forwarding messages.

There must be no interval where both shards can finalize ordinary writes to the same key. A forwarding period can improve availability, but forwarding is a message path, not dual ownership. It needs a nonce, expiry, destination binding, and idempotent handling.

### Failure cases

| Failure | Risk | Required behavior |
|---|---|---|
| Snapshot chunk missing | Activation with incomplete state | Delay activation or reconstruct from erasure/replica sources |
| Source reorganizes before freeze finality | Exported root no longer canonical | Discard snapshot and rebuild from canonical freeze point |
| Message arrives during freeze | Lost or double-applied callback | Include it before range root or queue under a bound handoff rule |
| Destination imports wrong code version | Divergent execution after activation | Bind protocol/code hashes and verify import vectors |
| Both shards accept a write | Conflicting ownership and asset creation | Routing-version and epoch checks reject one path |
| Validator set changes simultaneously | Handoff certificate ambiguity | Authenticate both set transition and range activation in one canonical boundary |
| Destination fails after source prunes | Unrecoverable state | Retain source snapshot until activation and recovery window finalizes |
| Client uses stale partition map | Submission delay or wrong-shard replay | Return authenticated redirect; never accept under ambiguous ownership |

### Capacity and state transfer

If the moving range contains 400 GB and must be copied within a 45-minute maintenance window, the minimum payload rate is:

```text
400 GB / 2,700 s ≈ 148 MB/s
```

This excludes encoding expansion, proofs, retransmission, concurrent state changes outside the frozen range, and peer overhead. At a 60 percent planning utilization, provision roughly `148 / 0.6 ≈ 247 MB/s` of usable transfer capacity. If that requirement is unrealistic, reduce range size, lengthen the window, pre-copy immutable data, or use incremental snapshots before the final freeze.

The freeze pauses writes, so migration planning must also bound user-visible downtime. A protocol can pre-copy most state while live, then transfer a final delta after freeze. The delta algorithm becomes safety-critical: it must prove that the base snapshot plus ordered delta equals the finalized handoff root.

### Resharding assertions

A test harness should generate transactions and cross-shard callbacks continuously while triggering the handoff. It should crash source and destination nodes at every manifest and activation boundary, delay random chunks, reorganize the pre-final freeze block, and restart with stale routing caches.

Assert conservation of balances, one owner per key and epoch, exact message-once semantics, identical imported roots across clients, bounded redirect loops, and the ability to recover before the source prunes. Resharding is complete only when state, pending work, replay protection, validator authentication, routing, and operational recovery move together.

## **Conclusion**

Layer 1 scaling does not mean only making blocks larger. It redesigns execution, storage, networking, data availability, and consensus so the system can grow without excluding independent validators. Sharding provides horizontal capacity; client and protocol optimization push vertical limits.

The emerging architecture is layered: the base layer supplies secure settlement and verifiable data while execution is parallelized across shards, rollups, and application-specific chains. The next chapter examines moving repeated interaction off the base chain.

## **References**

[^1]: Skidanov, Alex, Illia Polosukhin, and Bowen Wang. "Nightshade: NEAR Protocol Sharding Design." <https://near.org/papers/nightshade>.
[^2]: Cosmos. "IBC Protocol Overview." <https://docs.cosmos.network/ibc/latest/intro>.
[^3]: Buterin, Vitalik, et al. "EIP-4844: Shard Blob Transactions." <https://eips.ethereum.org/EIPS/eip-4844>.
[^4]: Ethereum.org. "Danksharding." <https://ethereum.org/roadmap/danksharding/>.

[^5]: NEAR Documentation. "Lifecycle of a Transaction." <https://docs.near.org/protocol/transactions/transaction-execution>.
[^6]: NEAR Documentation. "Token transfer flow." <https://docs.near.org/protocol/data-flow/token-transfer-flow>.
[^7]: Cosmos IBC Documentation. "IBC Lifecycle." <https://docs.cosmos.network/ibc/next/learn/ibc-lifecycle>.
[^8]: Cosmos IBC Specification. "Channel & Packet Semantics." <https://docs.cosmos.network/ibc/latest/spec/core/ics-004-channel-and-packet-semantics/README>.
