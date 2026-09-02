# **Glossary**

This glossary defines terms as they are used in this book. Some projects use the same word differently; the surrounding security model always takes precedence over the label.

## **Start Here: Core Blockchain Terms**

**Address**

A public identifier used as a transaction sender, recipient, account, or contract location. An address is not a person's verified real-world identity.

**Block**

An ordered package of transactions and protocol data linked to prior history. A block can be proposed or included before it reaches the protocol's strongest finality.

**Block header**

The compact part of a block containing metadata and commitments such as the parent hash and state or transaction roots. The header binds a larger body without containing all of it.

**Canonical chain**

The history currently selected by the protocol's fork-choice and finality rules. Temporary competing branches may exist before convergence.

**Cryptographic hash**

A fixed-length fingerprint of data. A small input change produces a different fingerprint, and finding useful collisions should be infeasible under the assumed hash function.

**Digital signature**

Cryptographic evidence that the holder of a private key authorized specific bytes. It does not by itself prove sufficient funds, correct execution, inclusion, or finality.

**Finality**

The condition under which a block or transaction should not be reverted under stated protocol and fault assumptions. Finality may be probabilistic or based on an explicit protocol commit rule. A sequencer confirmation, proposal, or quorum certificate is not settlement or BFT finality unless that commit rule explicitly makes it so.

**Full node**

Software that independently checks blocks under protocol rules. Storage and historical-retention choices vary; "full" does not always mean retaining every old byte forever.

**Merkle proof**

A small set of neighboring hashes that proves one item is included under a Merkle root. It authenticates an item but does not guarantee that every committed item is available.

**Node**

A computer running blockchain protocol software and communicating with peers. Nodes may validate, produce blocks, serve data, or perform only a subset of roles.

**Private key and public key**

A private key is secret signing material. A corresponding public key lets others verify signatures. Control of a key establishes protocol authorization, not necessarily legal identity or rightful ownership after theft.

**Smart contract**

Program code executed under blockchain rules. A contract deterministically changes state from inputs; it does not infer intent beyond its code and authenticated messages.

**State**

The latest live values used by execution, such as balances, ownership, nonces, and contract storage. State differs from history, the record of how those values changed.

**Transaction**

A signed instruction submitted to the network. Its final outcome depends on admission, ordering, execution, fees, current state, consensus, and finality.

**Validator**

A participant that checks proposals and contributes votes, attestations, or other consensus evidence. The exact authority and penalty depend on the consensus protocol.

**Wallet**

Software that manages keys, constructs transactions, and displays observed status. A wallet usually relies on nodes or service providers for chain data unless it verifies through its own node or light client.

## **Architecture and State**

**Application chain (appchain)**

A blockchain or rollup dedicated to one application or a related group of applications. It can customize execution, fees, sequencing, and governance, but must supply or rent consensus, data availability, settlement, and bridging.

**Bridge**

A protocol that authenticates messages or assets between security domains. A canonical rollup bridge is enforced by its settlement contracts. A sidechain bridge normally depends on the sidechain's consensus, a light client, a committee, or a multisignature account.

**Commitment**

A short cryptographic value binding a party to larger data. A Merkle root and a polynomial commitment are examples. A commitment proves integrity when data is revealed; it does not by itself prove that data is available.

**Composability**

The ability of applications or contracts to interact. Synchronous composability allows several calls to complete atomically in one transaction. Asynchronous composability uses messages and requires explicit handling of delay and partial completion.

**Execution**

Applying ordered transactions to prior state to compute new state.

**Layer 1 (L1)**

The base blockchain whose consensus defines its canonical history and native state.

**Layer 2 (L2)**

A protocol that updates state outside an L1 while using that L1 for settlement, correctness enforcement, or exits. Merely connecting a separate chain with a bridge does not make it inherit L1 security.

**Monolithic blockchain**

A system whose validator network performs execution, settlement, consensus, and data availability.

**Modular blockchain**

An architecture that separates one or more of execution, settlement, consensus, and data availability into specialized systems.

**Settlement**

The function that accepts canonical state commitments and resolves disputes. Rollups commonly settle to an L1 smart contract.

**State root**

A cryptographic commitment to the full application or blockchain state at a point in history.

## **Layer 2 Systems**

**Canonical bridge**

The bridge enforced by a rollup's settlement contracts rather than an external liquidity provider.

**Challenge period**

The interval during which an optimistic state assertion can be disputed. Expiry without a successful challenge makes the assertion acceptable under the protocol's challenger, data, timing, and contract assumptions; it is not a validity proof of the transition.

**Channel**

A protocol in which a fixed or constrained set of participants exchange signed state updates and use the blockchain to open, close, or resolve disputes.

**Commit-chain**

An operator-based off-chain system that posts state commitments to a base chain and provides an exit or challenge mechanism. The exact term is used inconsistently, so data and validation assumptions must be stated.

**Fault proof or fraud proof**

Evidence that an asserted state transition is invalid. Interactive systems narrow a disagreement to a small computation that the settlement contract checks.

**Force inclusion**

A mechanism allowing a user to bypass a sequencer, usually by submitting a transaction through the settlement layer.

**Optimistic rollup**

A rollup that accepts state assertions unless they are successfully challenged with a fault proof.

**Plasma**

A family of child-chain designs that commit roots to a parent chain while users retain proofs and use exit games. Data withholding and mass exits are central design problems.

**Rollup**

A system that executes transactions outside its settlement layer, publishes the data needed to reconstruct its state, and uses fraud or validity proofs to enforce correctness.

**Sequencer**

The party or protocol that orders L2 transactions and produces L2 blocks. It can provide low-latency confirmation but may introduce censorship, liveness, and ordering risks.

**Sidechain**

A separate blockchain connected by a bridge. It normally has independent consensus and does not automatically inherit the base chain's security.

**State channel**

A channel for arbitrary application state rather than payments alone.

**Validity rollup**

A rollup whose state commitments must be accompanied by a cryptographic proof of correct execution. Often called a ZK rollup, even when the proof is not used for privacy.

**Validium**

A validity-proof system that stores transaction data outside the settlement layer. Correctness can remain proven while data withholding prevents users from reconstructing state.

**Volition**

A system that lets users or applications choose between on-chain and off-chain data availability.

**Watchtower**

A service that monitors the chain and responds to dishonest or stale channel closures for an offline user.

## **Data Availability and Proofs**

**Blob**

In Ethereum, a temporary data object introduced by EIP-4844 for rollup publication. Consensus commits to blobs, while EVM execution cannot directly read their contents.

**Data availability (DA)**

The property that data required to verify or reconstruct a state was disseminated and obtainable during the protocol's required window.

**Data availability committee (DAC)**

A set of parties attesting that off-chain data is available. It reduces publication cost but introduces a threshold trust assumption.

**Data availability sampling (DAS)**

A method by which light nodes request random pieces of erasure-coded data to gain confidence that the full block can be reconstructed.

**PeerDAS**

Ethereum's peer data availability sampling protocol, activated in the Fusaka upgrade on December 3, 2025. Nodes custody and sample subsets of erasure-coded blob columns rather than every node downloading every blob.

**Erasure coding**

Encoding that expands data into redundant shares so the original can be reconstructed from a threshold subset.

**KZG commitment**

A polynomial commitment scheme used by Ethereum blob transactions. It binds a proposer to blob data and supports compact evaluation proofs.

**SNARK**

A succinct non-interactive argument of knowledge. Different SNARKs make different setup, cryptographic, proof-size, and prover-cost trade-offs.

**STARK**

A scalable transparent argument of knowledge. STARKs avoid a trusted setup and use hash-based assumptions, generally with larger proofs than many SNARK systems.

**Validity proof**

A cryptographic proof that a computation or state transition followed specified rules. Validity does not by itself prove data availability.

**Witness**

Auxiliary data proving that a computation used particular state values. Stateless validation gives validators witnesses instead of requiring all state locally.

**Zero knowledge**

A property allowing a proof to reveal that a statement is true without revealing its private witness. Succinct validity proofs do not have to be zero knowledge.

## **Messaging, Operations, and Governance**

**Censorship resistance**

The ability of a valid transaction to reach execution despite one or more actors trying to exclude it. A force-inclusion path is useful only if its delay and cost are bounded in practice.

**Domain separation**

Binding a signature, hash, or message to a chain, protocol version, epoch, and message type so valid data from one context cannot be replayed in another.

**Escape hatch**

A mechanism allowing users to withdraw or advance state without the normal operator. Escape hatches depend on available data, executable contracts, and affordable base-layer capacity.

**Forced inclusion**

A path by which a user submits a transaction through a more trusted layer when the normal sequencer censors it. Forced inclusion guarantees should state delay, fee, ordering, and failure behavior.

**Light client**

A client that verifies headers, committees, or succinct proofs rather than downloading and executing every transaction. Its security depends on how it authenticates consensus and validator-set changes.

**Preconfirmation**

A signed promise about future transaction inclusion or ordering made before consensus finality. A credible promise specifies expiry and an enforceable consequence for violation.

**Reorganization (reorg)**

Replacement of a previously preferred but not final chain segment. Cross-chain systems need explicit rules for messages observed before their source chain is final.

**Relayer**

An actor that transports a message or proof between systems. A well-designed bridge does not trust a relayer for correctness and allows any party to replace a failed relayer.

**Remote procedure call (RPC)**

An application interface through which a client asks a node or gateway to submit transactions or read chain data. An RPC response reports what that endpoint observed or accepted; it is not consensus evidence unless the client independently verifies the corresponding proof, certificate, or finalized chain state.

**Social recovery**

Recovery that requires human coordination, governance, or a trusted checkpoint rather than following the ordinary protocol automatically. It may restore service but changes the trust model.

**Timelock**

A mandatory delay between scheduling and executing an upgrade or privileged action. A timelock is protective only if users and monitors can detect the action and respond before execution.

**Weak subjectivity**

The requirement for a proof-of-stake client to begin from a sufficiently recent trusted checkpoint, limiting long-range histories signed by validators whose stake is no longer slashable.

## **Performance and Reliability**

**Admission control**

A mechanism that limits or prices incoming work so queues and resources remain within an operating objective. Fee markets are one form of admission control.

**Backpressure**

A signal from a saturated downstream component that slows upstream production. Without backpressure, a sequencer can create batches faster than a prover or DA layer can process them.

**Capacity**

The maximum sustainable offered load that meets a stated latency and error objective. Capacity is measured for a workload, hardware configuration, network, duration, and completion boundary.

**Capacity knee**

The region where increasing offered load causes tail latency and queue depth to rise rapidly while completed throughput grows slowly or stops growing.

**Critical path**

The longest dependency chain determining completion time. Parallel work outside the critical path may improve resource use without reducing user latency.

**Headroom**

Unused capacity reserved for demand variance, component loss, retries, compaction, view change, or recovery traffic. Headroom should be chosen separately for each resource.

**Idempotence**

The property that repeating an operation has the same durable effect as applying it once. Message consumption, deposits, withdrawals, and retried jobs need idempotent identifiers.

**Offered load**

The rate at which clients submit work, whether or not the system accepts or completes it. Reporting completed throughput without offered load hides overload behavior.

**Operating envelope**

The workloads and fault conditions under which a system meets its throughput, latency, safety, liveness, cost, and recovery objectives.

**p50, p95, p99 latency**

Percentile latencies. p99 is the value at or below which 99 percent of measured operations complete. Percentiles require a defined population, window, and completion boundary.

**Queue stability**

A condition in which backlog remains bounded over time. A temporary high throughput result is not sustainable when queued data, proofs, or transactions continually grow.

**Recovery point objective (RPO)**

The maximum accepted loss of durable work or state after failure. A blockchain safety design often targets no loss of finalized state, while auxiliary indexes may permit replay from an earlier point.

**Recovery time objective (RTO)**

The target time to restore a specified service after failure. State which service and finality boundary the timer covers.

**Saturation**

A state where one resource is fully utilized and limits completed work. CPU, storage I/O, network bandwidth, DA publication, proving, or consensus can each saturate independently.

**Service-level objective (SLO)**

A measurable target such as p99 settlement within ten minutes for 99.9 percent of withdrawals. An alert should map to user impact or exhaustion of the SLO's error budget.

**Tail latency**

Latency of slower requests, commonly represented by high percentiles. Tail behavior reveals queues, pauses, retries, and skew hidden by averages.

**Throughput**

Completed work per unit time under a defined completion rule. Submitted, sequenced, executed, proved, and finalized throughput are different metrics.

**Utilization**

The fraction of a resource's capacity in use. Running near 100 percent average utilization usually produces unstable queues when service time or arrivals vary.

**Workload mix**

The distribution of transaction or request types, state-access patterns, sizes, and bursts used in a test. A throughput result applies to that mix, not to an abstract average transaction.

## **Execution and Consensus**

**Block-STM**

An optimistic parallel execution engine that speculates on transactions, detects invalidated reads, and retries conflicts while preserving a canonical order.

**Byzantine fault**

Arbitrary faulty behavior, including conflicting messages, collusion, and malicious deviation from protocol.

**Committee**

A subset of validators assigned to vote on or process part of the system.

**Consensus**

Agreement on an ordered canonical history among independent nodes despite faults.

**Fast path**

A protocol route that reaches an outcome with fewer phases or less ordering work under favorable conditions. The term is system specific. In current Sui terminology, address-owned objects can use Mysticeti fast-path certification without waiting for total-order consensus, while shared and party objects use consensus sequencing.

**Hot state**

State accessed by many concurrent transactions. Hot state creates conflicts and limits parallel execution.

**Liveness**

The guarantee that the protocol eventually continues to process and finalize valid work under stated conditions.

**MEV**

Maximum extractable value: value captured by controlling transaction inclusion, exclusion, or ordering.

**Nakamoto consensus**

Longest- or heaviest-chain consensus introduced by Bitcoin, with probabilistic finality and Sybil resistance based on proof of work.

**Pacemaker**

The component of a leader-based BFT protocol that manages timeouts and view changes.

**Parallel execution**

Executing independent transactions concurrently while producing a deterministic result equivalent to the protocol's canonical semantics.

**Quorum certificate (QC)**

Aggregated evidence that a quorum of replicas voted for a proposal in one protocol phase. A QC does not by itself imply finality unless the protocol's commit rule explicitly says it does; chained protocols commonly require later certificates.

**Quorum intersection**

The property that two threshold quorums overlap in enough participants or weight to include an honest voter under the stated fault bound.

**Prover market**

A system that assigns proof-generation jobs among independent providers. Correctness follows from verification, while deadlines, witness privacy, job availability, and concentration remain operational concerns.

**Safety**

The guarantee that honest participants do not finalize conflicting states.

**Sharding**

Partitioning validators, transactions, execution, or state so different groups process different work concurrently.

**Synchronous, partially synchronous, asynchronous**

Network models. A synchronous protocol assumes a known message-delay bound. Partial synchrony assumes a bound eventually holds. An asynchronous model assumes no timing bound.

**View change**

The process that replaces a stalled or faulty consensus leader and carries forward the certificates or locks needed for safety.
