# **Chapter 7: Modular vs Monolithic Blockchains**

## **Introduction**

A monolithic blockchain asks one protocol and validator network to provide execution, settlement, consensus, and data availability. A modular blockchain separates some of these functions so that specialized systems can perform them independently.

Modularity is not automatically more decentralized or more secure. It creates explicit interfaces and lets each layer scale differently, but the end-to-end system inherits the assumptions and failure modes of every layer it uses.

---

## **The Monolithic Model**

In a monolithic chain, validators:

1. receive and order transactions;
2. execute them;
3. agree on a block;
4. store and distribute the block data;
5. maintain the resulting state.

The strength of this model is integrated security and synchronous composability. A transaction can call several contracts against one state and either complete atomically or revert. Developers and users reason about one fee market, one finality rule, and one validator set.

The weakness is replicated work. Increasing capacity raises the requirements of the same nodes that secure the network. Congestion in one popular application can affect every other application.

---

## **The Modular Stack**

<p align="center">
  <img src="../assets/course/ch11_appchain_tradeoff.svg" width="760" alt="Shared rollup and appchain trade-off">
  <br>
  <em>Figure 7.1: Moving from shared blockspace to an appchain buys control and dedicated capacity but creates another interoperability boundary. Original figure for this book, based on SC6019 Lecture 06.</em>
</p>



A modular system separates the four jobs:

- **Execution layers** run transactions and compute state transitions.
- **Settlement layers** verify proofs, resolve disputes, and define canonical state.
- **Consensus layers** order data and finalize blocks.
- **Data availability layers** publish enough data for verification and reconstruction.

An Ethereum rollup is a practical example. The rollup provides execution, while Ethereum supplies settlement, consensus, and data availability. A sovereign rollup may instead use a data availability layer for ordering and publication while its own nodes define the canonical state and fork-choice rules.

---

## **Why Specialization Helps**

Modularity allows different scaling techniques for different bottlenecks:

- execution can use parallel VMs or application-specific logic;
- validity proofs can compress verification;
- data layers can use erasure coding and sampling;
- settlement can remain deliberately conservative;
- many execution layers can share one security base.

It also gives applications sovereignty. A game may prioritize low latency, an exchange may optimize parallel order processing, and a privacy application may use a custom proof system without asking an entire Layer 1 community to change its execution environment.

---

## **The Hidden Costs of Modularity**

### **Fragmented Liquidity and State**

Assets and applications spread across execution layers. Moving between them requires bridges and asynchronous messages. The integrated composability of one chain becomes a distributed-systems problem.

### **More Trust Boundaries**

A modular transaction can depend on a sequencer, a proof system, a settlement contract, a data layer, and a bridge. A failure in any one can delay finality or block exits.

### **Different Meanings of Finality**

A user may see sequencer confirmation in seconds, data publication later, and settlement finality later still. Applications must decide which stage is sufficient for deposits, withdrawals, and cross-chain messages.

### **Operational Complexity**

Developers need indexers, relayers, proof infrastructure, bridge monitoring, and policies for upgrades across several layers. The stack is easier to customize but harder to observe as a whole.

---

## **Celestia and Data Availability Specialization**

Celestia focuses on ordering transactions and making their data available rather than executing application state. Light nodes sample small portions of erasure-coded blocks. With enough random samples, they gain high confidence that the complete block can be reconstructed by the network.[^1]

This allows many rollups to publish data without requiring Celestia validators to execute each rollup. The rollup chooses whether its state is validated by a settlement layer, validity proofs, fraud proofs, or its own full nodes.

The security statement must be precise: the data layer can show that data was published, but it does not necessarily prove that a particular rollup's state transition was valid.

---

## **Sovereign and Settled Rollups**

A **settled rollup** submits state roots to a settlement contract that enforces its validity or dispute rules. Its canonical bridge depends on that contract.

A **sovereign rollup** uses a data layer for ordering and availability, while rollup nodes interpret the data and choose the canonical fork. Upgrades may occur through social consensus among those nodes rather than through a settlement contract.

This is a governance difference as much as a technical one. Settled rollups gain shared enforcement and canonical bridges. Sovereign rollups gain freedom over their state machine and upgrade process.

---

## **Monolithic vs Modular**

| Dimension | Monolithic | Modular |
|---|---|---|
| Execution and security | Integrated | Split across layers |
| Composability | Synchronous within one state | Often asynchronous across layers |
| Scaling | Bounded by shared validator resources | Specialized and horizontally expandable |
| Application control | Constrained by base protocol | Custom VMs, fees, and governance |
| Failure analysis | Fewer interfaces | More dependencies and bridge risk |
| User experience | One account and fee market | Bridging and varied finality |

The choice is not binary. A monolithic chain can host modular rollups, and a modular data layer still has a monolithic consensus protocol. Real systems sit on a spectrum.

---

## **A Framework for Evaluating an Architecture**

Ask the following questions:

1. Where is execution performed?
2. Who orders transactions, and can users bypass that party?
3. Where is data published, and for how long?
4. Who verifies state transitions?
5. Which layer defines finality?
6. How can users exit during a failure?
7. Who can upgrade each layer?
8. Which messages or bridges connect fragmented state?

These questions reveal more than labels such as L2, appchain, validium, or modular chain.

## **End-to-End Transaction Walkthrough**

Imagine a game rollup that executes on a custom VM, posts data to Celestia, and settles validity proofs on Ethereum. A player signs a move. The sequencer orders it and gives a soft confirmation. The VM updates the player's objects. Encoded data is included by Celestia consensus. A prover generates a transition proof, and Ethereum records the new state root after verification.

The move crosses several finality boundaries. The sequencer can promise an order but fail to publish. Celestia can finalize the data while knowing nothing about the game rules. Ethereum verifies the state only after the commitment and proof arrive. A bridge or marketplace must decide which boundary is sufficient before releasing an asset.

This architecture scales because no validator set performs every job. It is harder to debug: a delayed withdrawal may be stuck at sequencing, DA submission, proving, Ethereum inclusion, or relaying. User interfaces need to name the stalled layer rather than report a generic "pending" status.

## **Security Composition**

End-to-end safety is bounded by the weakest assumption on the path. Correct execution with unavailable data prevents users from constructing new state. Available data with a broken bridge allows theft. Sound proofs with an immediate upgrade key leave governance in control.

A useful engineering artifact is a dependency graph. For each edge, document what is trusted, how failure is detected, what finality is assumed, and whether users can recover without cooperation from the failed component.

## **Designing the Interfaces Between Modules**

A modular architecture succeeds or fails at its interfaces. Each interface should carry enough authenticated information for the receiving layer to verify its responsibility without silently assuming another layer did the work.

### **Execution to Settlement**

An execution layer sends a state assertion containing the prior root, new root, input range, data commitment, and proof metadata. The settlement contract verifies a fault or validity proof and records the accepted root. It should not accept a root without binding it to an exact data range, because otherwise a proof about one batch may be replayed or interpreted against another.

### **Execution to Data Availability**

The rollup publishes a namespaced blob or batch and receives a commitment plus inclusion proof. Rollup nodes need a deterministic rule that maps a settlement assertion to the DA commitment. If the DA chain reorganizes after settlement accepts the assertion, recovery depends on the finality assumptions embedded in the bridge or oracle connecting them.

### **Settlement to Bridge**

A bridge verifies that a withdrawal message belongs to an accepted state root and has not already been consumed. The message needs source chain, destination chain, sender, recipient, asset, amount, nonce, and version. Domain separation is what keeps a proof from one rollup or deployment from being valid in another.

### **Sequencer to User**

A sequencer receipt is a promise, not necessarily final state. It should identify the ordered transaction, L2 block, sequencer signature, and expiry or reorganization policy. Wallets can then label it accurately as pending publication or pending settlement.

## **Sovereign Rollup Fork Choice**

A sovereign rollup does not ask a settlement contract to choose its canonical state. Full nodes read ordered data from the DA layer and apply the rollup's fork-choice and execution rules locally. An upgrade may be a social fork: users choose software interpreting the same data differently.

This gives the community sovereignty but complicates light clients and bridges. A light client needs a way to identify the accepted rollup rules and validator or proof system. A bridge needs its own decision about which fork is canonical. A settled rollup outsources that decision to the settlement contract; a sovereign rollup cannot avoid defining it somewhere.

## **Modular Liveness Matrix**

| Failed component | Immediate effect | Safety impact | Recovery path |
|---|---|---|---|
| Sequencer | No fast ordering | Usually none if force inclusion works | Submit through fallback or L1 inbox |
| Batch submitter | New state lacks published data | Unposted confirmations can disappear | Another submitter posts the batch |
| DA network | New batches cannot be proven available | Accepting unavailable data can break recovery | Halt settlement, switch only through governed upgrade |
| Prover | Validity finality stalls | Normally none | Another prover reconstructs witness |
| Settlement chain | Withdrawals and finality stall | Depends on reorganization/finality failure | Wait or invoke documented social recovery |
| Bridge relayer | Messages delayed | None if anyone can relay | Permissionless relay |
| Upgrade multisig | Routine upgrades delayed | None | Governance replacement under existing rules |

The matrix distinguishes safety from liveness. A component can be operationally centralized without being able to steal assets, yet its outage can still make the application unusable.

## **Implementation Checklist for a Modular Stack**

1. Pin protocol and verifier versions in every cross-layer message.
2. Use chain and rollup domain identifiers in signatures and proofs.
3. Define finality delays for each source chain before consuming messages.
4. Make relaying permissionless where possible.
5. Expose each pipeline stage in user receipts and monitoring.
6. Reconstruct state from DA using an independent node before launch.
7. Test sequencer, prover, submitter, DA, and settlement outages separately.
8. Document coordinated upgrades when one interface changes.

## **Cross-Layer Message Envelopes**

A modular stack should standardize the envelope carried across layers. One conceptual format is:

```text
MessageEnvelope {
    protocol_version
    source_domain
    destination_domain
    source_height
    nonce
    sender
    target
    payload_hash
    expiry
}
```

The source-domain state commits to the envelope. A relay supplies the envelope plus proof to the destination. The destination verifies source finality, domain and version, expiry, and replay status before dispatching the payload.

Versioning belongs in the signed or committed message. Otherwise an upgrade can cause two layers to decode the same bytes differently. `payload_hash` avoids ambiguous variable-length encodings; the full payload follows a canonical serialization. Nonces can be global, per sender, or per channel, but the destination must enforce exactly one model.

### **Ordered and Unordered Channels**

An ordered channel processes nonce `n` only after `n-1`. This is easy for applications needing sequence, but one missing message blocks all later work. An unordered channel accepts any unused nonce and requires the application to manage dependencies.

IBC makes this distinction explicit. Modular rollup systems need the same clarity. A token bridge may use unordered transfers, while a replicated state machine may require order.

## **Relayers Are Replaceable, Not Trusted**

A relayer observes a source event and submits its proof to a destination. If the proof is complete and verification is on-chain, a dishonest relayer cannot forge a message; it can only delay or censor its own delivery.

This liveness property depends on permissionless replacement. Message data and proofs must be publicly retrievable, and another relayer must be allowed to submit them. Exclusive relayers turn a replaceable service into a trust boundary.

Fee design pays relayers without letting them alter recipients or amounts. The source message can name a maximum fee, or the destination can reimburse the submitter under protocol rules. Applications should handle duplicate relay attempts safely.

## **Cross-Layer Reorganizations**

A destination consuming a message before source finality risks accepting an event that later disappears. Waiting longer reduces this risk but increases latency. Different source chains provide deterministic finality, probabilistic confirmations, or optimistic assertions.

A bridge policy maps source evidence to destination acceptance. For probabilistic chains, it may require a confirmation depth. For BFT chains, it verifies a finality certificate. For rollups, it waits for challenge or validity-proof completion. This policy should be explicit and upgradeable only with a delay because changing it alters the security budget of every pending message.

## **Operating a Modular Stack**

Observability should correlate one transaction across every layer. Assign a stable journey identifier and record:

- sequencer receipt and L2 block;
- DA transaction and commitment;
- proof job, version, and completion;
- settlement transaction and accepted root;
- outbound message nonce;
- relay submission and destination execution.

Alerts should name which service owns the delay. Service-level objectives can then distinguish fast confirmation, publication deadline, proof deadline, settlement deadline, and message-delivery deadline.

Runbooks need safe halt conditions. If DA finality is uncertain, settlement should stop accepting new assertions rather than guess. If the prover is down, sequencing may continue only within a bounded unpublished or unproven window. If a bridge verifier has a bug, a pause key may limit loss, but its scope and recovery governance must be documented.

## **Modular Cost Accounting**

The application pays several providers: sequencer, execution nodes, DA layer, prover, settlement chain, and relayers. Some costs are variable per transaction; others are fixed infrastructure or security subsidies.

Unit economics should allocate batch and proof cost by the resource each transaction consumes, not divide equally. A large data-heavy transaction should pay more DA cost; a computation-heavy transaction should pay more proving cost. Mispricing invites denial of service against the subsidized resource.

## **Conclusion**

Monolithic blockchains offer integrated security and composability but require validators to repeat all major work. Modular architectures separate execution, settlement, consensus, and data availability so each can specialize and many execution layers can share a base.

The gain is flexibility and scale. The cost is fragmentation and a larger set of dependencies. The next chapter examines the least intuitive of these services – proving that block data is actually available without requiring every node to download all of it.

## **References**

[^1]: Celestia Docs. "Data Availability." <https://docs.celestia.org/learn/celestia-101/data-availability/>.
