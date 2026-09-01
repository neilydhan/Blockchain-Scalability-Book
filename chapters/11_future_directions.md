# **Chapter 11: Future Directions**

## **Introduction**

Blockchain scalability is moving from one-chain throughput contests toward specialized stacks. Execution, proving, sequencing, data availability, settlement, and interoperability are becoming separate services that can improve independently.

The next bottleneck is therefore not one number such as TPS. It is coordination: making many fast execution environments feel like one secure, usable system.

---

## **Real-Time Validity Proving**

Validity proofs once required long proving times and specialized circuits. Faster provers, hardware acceleration, recursive aggregation, and general-purpose zkVMs are reducing that delay.

Real-time proving would let a validity proof arrive within one block interval. This could shorten finality, simplify bridges, and allow even base-layer execution to be re-verified succinctly. The remaining constraints are prover cost, memory bandwidth, circuit correctness, and the centralization risk of specialized hardware.

A future proof market may separate block production from proving. Multiple provers compete to generate a proof, while the chain verifies only the winning result. This needs mechanisms for redundancy and censorship resistance so one prover outage does not stop the chain.

---

## **Shared Sequencing and Cross-Rollup Composability**

<p align="center">
  <img src="../assets/course/ch11_appchain_tradeoff.svg" width="760" alt="From a shared rollup to an application chain">
  <br>
  <em>Figure 11.1: The future appchain trade-off: dedicated execution and customization versus bridges and fragmented liquidity. Original figure for this book, based on SC6019 Lecture 06.</em>
</p>



Independent sequencers fragment ordering. A transaction cannot easily execute atomically across rollups, and cross-rollup messages wait for settlement.

Shared sequencers aim to order transactions for several rollups. If the same sequencer sees both sides, it can offer stronger inclusion guarantees and forms of atomic execution. Based rollups go further by deriving ordering from the base-layer proposer.

The benefit is interoperability and reduced sequencer trust. The risk is moving concentration into a shared service. A shared sequencer must define leader selection, failure recovery, fees, and what a rollup can do when the service censors it.

---

## **Proof Aggregation**

Instead of verifying every rollup proof separately, an aggregator can recursively prove that many proofs were valid. Layer 1 then verifies one proof.

Aggregation reduces settlement cost and lets small rollups share proving economies. It may also support canonical bridges between rollups that settle through the same proof system. The design must preserve data availability and identify which state roots were actually covered.

---

## **More Data Through Sampling**

EIP-4844 created blobspace for rollups. PeerDAS and full danksharding aim to increase capacity without requiring every node to download all blob data.[^1]

Dedicated data layers will also compete on throughput, sampling security, retention, and integration. The market may support different tiers: tightly integrated base-layer blobs for high-value settlement and cheaper external availability for applications willing to accept another consensus assumption.

---

## **Statelessness and State Expiry**

Data availability concerns recent block data, while state growth concerns the long-lived database of accounts and contracts. If state grows forever, running a validator becomes increasingly expensive.

Stateless validation moves toward blocks that include witnesses proving the state values they touch. Verkle trees were proposed to make these witnesses smaller. State expiry or rent would remove or charge for inactive state.

These ideas reduce validator storage but move responsibility elsewhere. Users or archival services may need to retain old state and provide proofs when it becomes active again.[^2]

---

## **Parallel and Specialized Virtual Machines**

Block-STM, object-centric execution, and declared access lists show how multi-core hardware can be used. Future VMs may make state dependencies explicit and provide programming tools that warn about hot-state bottlenecks.

Application-specific rollups will specialize further. An exchange may build native order-book primitives, a game may use an object model, and an AI-agent network may optimize frequent micropayments and verifiable computation. The trade-off is portability: specialized execution makes applications faster but less interchangeable.

---

## **Chain Abstraction**

Users should not need to know which chain holds gas, which bridge route is safe, or when a message changes finality domains. Chain abstraction combines smart accounts, intent systems, solvers, and cross-chain messaging to present one interface.

The security challenge is making hidden routing legible. A solver can improve price and speed but introduces execution and censorship questions. Interfaces should show which chain settles a transaction, when it is final, and which recovery path exists.

---

## **Decentralizing the Full Stack**

Many scaling systems launch with centralized sequencers, provers, upgrade keys, or data committees. This can be a practical deployment stage, but decentralization should be measured rather than promised.

Useful milestones include:

- permissionless proof or fault-proof participation;
- force inclusion and forced withdrawal;
- multiple independent sequencers;
- delayed and transparent upgrades;
- distributed data custody;
- open-source clients from more than one team.

Decentralizing one component can expose another. A decentralized sequencer does not fix a multisig-controlled bridge, and a permissionless prover does not fix unavailable data.

---

## **MEV and Proposer-Builder Separation**

Scaling creates more blockspace but does not remove maximum extractable value. Faster sequencing and cross-domain transactions create new opportunities for reordering and latency advantages.

Proposer-builder separation divides block construction from consensus proposal. Specialized builders compete to assemble valuable blocks while validators choose among bids. Protocol designs must prevent builder concentration, censorship, and timing games. Encrypted mempools and inclusion lists are possible counterweights.

---

## **How to Judge Future Claims**

New systems should be evaluated across the entire stack:

1. What workload produced the throughput result?
2. What hardware and validator count were used?
3. Where are execution and data stored?
4. How is invalid state rejected?
5. Can users force inclusion and exit?
6. Which keys can upgrade the system?
7. What finality does the quoted latency represent?
8. What happens during sequencer, prover, bridge, or DA failure?

A scalability result is meaningful only when its security and operating assumptions are stated beside it.

## **A Plausible End-State Architecture**

A future wallet may accept an intent - "swap this asset and pay that merchant" - without asking which chain should execute it. Solvers compete to route the action. A shared sequencer reserves positions across two rollups. Each rollup executes in a parallel VM. Its prover produces a recursive proof. Blob data is dispersed through PeerDAS, and an aggregate proof settles on Ethereum. The wallet shows one confirmation while tracking several finality stages.

Every component exists in an early form. Composition is the hard part. If one rollup reverts, atomic settlement must unwind the other. If a solver disappears, the user needs a refund. If the shared sequencer censors the intent, each rollup needs independent inclusion. If data is available but proving stalls, another prover must take over.

Scalability comes from dividing work, but division creates interfaces. Future systems will be judged by whether those interfaces remain verifiable during failure.

## **Research Problems Still Open**

Cross-rollup atomicity is difficult without a shared trust or timing domain. Decentralized sequencing must resist censorship without recreating global consensus latency. Proof systems need lower hardware barriers and stronger circuit assurance. Data sampling needs resilient peer-to-peer networking at larger scale. State expiry needs a usable way to revive old state. MEV mitigation must operate across several domains, not one mempool.

The field also has a measurement problem. Theoretical capacity, testnet bursts, and sustained mainnet throughput are routinely presented as equivalent. Reproducible workloads, hardware disclosure, adversarial tests, and measurements of recovery and decentralization are needed alongside speed.

## **Based and Shared Sequencing Protocols**

A based rollup lets the L1 proposer order rollup transactions. Users submit through L1-aware builders or inclusion mechanisms, and rollup execution follows the L1 order. This inherits L1 liveness and censorship properties more directly but ties latency and throughput to L1 proposal timing.

A shared sequencer runs a separate ordering protocol for several rollups. It can promise atomic bundles such as "execute on rollup A only if the corresponding action is ordered on rollup B." The promise is meaningful only if both rollups verify the same ordering certificate and define compatible failure behavior.

A shared-sequencing message may bind:

```text
AtomicBundle {
    bundle_id
    participating_rollups[]
    transactions[]
    common_ordering_height
    expiry
}
```

Each rollup must decide what happens if another rollup rejects its transaction during execution. True atomicity may require preconditions, escrow, or a later settlement protocol; common ordering alone does not make arbitrary state transitions atomic.

## **Proof Markets and Aggregation Trees**

A proof market separates execution from the right to prove. Executors publish traces or commitments, and provers bid to generate proofs before a deadline. Redundant provers reduce liveness dependence on one operator.

Aggregation combines proofs in a tree. Leaf proofs cover rollup blocks; intermediate proofs verify groups; a root proof covers many rollups. The settlement layer verifies one root and records the list or commitment of included state roots.

The market needs data access, deterministic witness formats, payment rules, and a fallback when no bid arrives. Aggregation also creates latency: waiting for more leaves lowers verification cost per block but delays settlement. Operators choose an aggregation window much like batchers choose a transaction window.

## **Intents and Solver Safety**

An intent expresses an outcome rather than exact transactions. A user might authorize receiving at least 100 units of asset B before a deadline in exchange for at most 1 unit of asset A. Solvers choose routes across exchanges and chains.

The signed intent must bound solver authority:

- input asset and maximum amount;
- minimum output and recipient;
- permitted chains or settlement contracts;
- expiry and nonce;
- fee limit;
- whether partial fill is allowed;
- cancellation rule.

Settlement should be atomic from the user's perspective: either the output condition is proven and payment releases, or the input remains recoverable. Off-chain solver reputation is not a substitute for enforceable bounds.

Chain abstraction can make routing invisible while keeping the signed conditions visible. Wallets should still report which domains hold funds and when the result reaches finality.

## **Stateless Validation Pipeline**

A stateless block includes or makes available witnesses for every state access. Validators begin with the prior state root, verify each witness, execute transactions, update touched commitments, and compute the new root without storing the entire state.

Block builders now carry more responsibility: they need state to generate witnesses. If only a few builders maintain complete state, validation becomes cheap while block production centralizes. Distributed state providers, witness markets, and state expiry rules aim to balance this.

A state-expiry design must answer how dormant state returns. A user may present the old value plus a proof against an archived root, pay to reactivate it, and place it in current state. The archive can be untrusted for correctness if proofs verify, but it must remain available.

## **Research Evaluation Milestones**

A future technology should move through increasingly strong evidence:

1. **Correct model.** Security and liveness are proved under explicit assumptions.
2. **Reference implementation.** The protocol runs and interoperates against test vectors.
3. **Adversarial testnet.** Faults, withholding, reorganization, and overload are injected.
4. **Independent implementations.** More than one team reproduces the protocol.
5. **Measured production.** Sustained workloads and recovery paths are published.
6. **Reduced control.** Sequencing, proving, DA, and upgrades gain independent operators.

Roadmap language often mixes these stages. Readers should distinguish a research proposal from deployed, permissionless, failure-tested infrastructure.

## **Decentralized Prover Networks**

A prover network accepts jobs containing a program version, public inputs, witness commitment, deadline, and reward. Provers may submit proofs directly or commit before revealing to prevent copying.

The network must avoid several failure modes. One prover can underbid and fail near the deadline. A coordinator can censor jobs. Witness data can leak private application inputs. Different hardware may produce proofs at unequal cost, concentrating supply.

Redundancy policies assign important jobs to several provers or maintain a fallback prover. Proof verification makes incorrect output harmless to safety, but repeated missed deadlines harm liveness. Reputation, bonds, and slashing can price that behavior if failure is objectively attributable.

## **Preconfirmations**

A preconfirmation is a signed promise by a proposer or sequencer about future inclusion or order. It can give users sub-block latency before consensus finality.

A useful promise states transaction, target slot or height, maximum position or ordering relation, fee, expiry, and penalty. The signer needs collateral or future revenue at risk. Otherwise a conflicting promise is merely evidence of bad behavior without compensation.

Preconfirmations create a market for near-term blockspace and can improve user experience. They can also favor sophisticated builders and private order flow. Protocols must define whether promises are transferable, how conflicts are resolved, and what happens during reorganization.

## **Encrypted Mempools and Threshold Decryption**

Encrypting transaction content until order is fixed can reduce front-running. Users encrypt under a committee key; consensus orders ciphertexts; a threshold of members releases decryption shares afterward.

The committee can withhold shares and halt execution. If members decrypt early, they regain ordering advantage. Distributed key generation, verifiable shares, penalties, and fallback timeouts address these risks.

Encryption hides content but not all metadata. Sender, ciphertext size, timing, and fee may still reveal strategy. It also complicates simulation and fee estimation because builders cannot inspect execution before ordering.

## **Cross-Domain MEV**

A transaction on one rollup can change an asset price used on another. Whoever observes or controls message timing may arbitrage the difference. Shared sequencing can coordinate order, but settlement delays and independent reorganization rules remain.

Cross-domain MEV analysis follows information: when does each actor learn an order, price, proof, or bridge message? It also follows control: who can delay publication, proof, or relay? A modular stack may move MEV from one block producer to sequencers, solvers, relayers, or proof markets.

## **Hardware Acceleration and Decentralization**

GPUs, FPGAs, ASICs, fast networking, and high-bandwidth memory increase execution and proving. Specialized hardware can lower unit cost while raising the capital required to compete.

Open hardware designs, commodity-compatible algorithms, proof markets, and cheap verification can preserve access. Measure market concentration and switching cost, not only benchmark speed. A protocol tied to one vendor's hardware inherits supply-chain and censorship risk.

## **Post-Quantum Considerations**

Large-scale quantum computers would threaten common signature and commitment schemes. Migration is difficult because old accounts and bridge keys may remain vulnerable even after the protocol supports new signatures.

A roadmap needs quantum-resistant account authorization, validator signatures, proof commitments, and a process for inactive users to migrate. Post-quantum signatures are larger, affecting data availability and bandwidth. Hash-based proof systems have different assumptions but still use signatures and commitments elsewhere in the stack.

This is long-term research, but scalability and cryptographic agility interact: larger keys and proofs consume the capacity future protocols are trying to create.

## **What "Finished" Means for a Scaling System**

A system is not finished when its fast path reaches mainnet. It approaches maturity when independent clients interoperate, users can force inclusion and exit, proof and DA systems survive operator failure, upgrades are delayed and visible, bridges have bounded risk, benchmarks are reproducible, and incident history demonstrates recovery.

Roadmaps should track removal of trust assumptions alongside throughput. The final product is not maximum speed; it is sustained, verifiable service under realistic faults.

## **Research-to-Production Gate**

Future techniques are easiest to misread when a paper result, benchmark, testnet, and production service are described with the same tense. A deployment gate should require evidence at each level.

### 1. Security statement

Write the exact property and assumptions. For a preconfirmation, define what is promised, who signs, how conflicts are proven, and which collateral can be penalized. For an encrypted mempool, define confidentiality before ordering, the decryption threshold, withholding behavior, and metadata leakage. For a prover market, define correctness, deadline, witness privacy, and fallback.

A proof in one model does not cover implementation bugs, economic griefing, key compromise, or dependencies omitted from the model. List those separately.

### 2. Interoperable specification

The specification needs canonical encodings, domains, state machines, error behavior, version negotiation, test vectors, and upgrade rules. Two teams should implement it without sharing code and agree on every accepted and rejected vector.

Specifications should make unsafe ambiguity impossible. "Recent block," "sufficient collateral," or "available data" needs a parameter or verification rule. Unknown versions should fail closed while preserving a recovery path for in-flight work.

### 3. Reference and independent implementations

A reference client demonstrates one interpretation; an independent client tests whether the specification is complete. Differential tests compare outputs across generated and adversarial inputs. Reproducible builds, pinned dependencies, and public issue histories help reviewers distinguish protocol properties from one implementation.

### 4. Adversarial network

A testnet should inject withholding, equivocation, censorship, partitions, clock skew, key rotation, malformed proofs, worker loss, and overload. Rewards for breaking assumptions are useful only when the target and disclosure process are clear.

Measure recovery, not only whether the network restarted. Did users retain assets? Could independent operators reconstruct state? Did queued work converge without duplicates? Which privileged action was required?

### 5. Bounded production launch

Limit value, throughput, upgrade delay, and dependency scope while incident response is still being learned. Publish the exact controls. A rate limit can bound loss but may also block honest exit. An emergency pause can protect funds but creates a governance key that belongs in the security model.

Increase limits only after observing realistic workload, failures, and independent operation. Time in production is not evidence when one team still runs every critical role.

### 6. Control reduction

Maturity should remove powers and single dependencies: permissionless challengers and provers, multiple sequencers or a tested forced path, independent DA retrieval, client diversity, delayed upgrades, key separation, and user exit under old rules.

A roadmap item is complete when its trust assumption is removed or bounded and the replacement path has survived failure tests, not when a governance vote changes a label.

## **Worked Decision: Should an Exchange Use Preconfirmations?**

Assume an exchange rollup wants 200-millisecond order acknowledgements while settlement finality takes minutes. A sequencer can sign a promise that a valid order will appear before slot `s` with a maximum position and fee.

The promise improves user feedback but introduces questions:

- Can the sequencer issue conflicting positions to two traders?
- What evidence proves a missed inclusion deadline?
- Is the penalty larger than the profit from breaking the promise?
- Does a base-layer reorganization excuse performance?
- Can users submit without accepting a preconfirmation?
- Is the promise valid after an upgrade or sequencer-set change?

A useful envelope is:

```text
Preconfirmation {
  chain_id,
  rollup_id,
  transaction_hash,
  promised_slot,
  ordering_constraint,
  max_fee,
  sequencer_set_version,
  expiry,
  signer
}
```

The exchange can display "preconfirmed" as a separate state, never as settled. Risk limits may allow small reversible actions after preconfirmation while withdrawals and cross-domain releases wait for stronger finality.

Suppose a conflicting promise can earn the sequencer at most $50,000 during a stressed market. A $10,000 slash does not create credible deterrence. Collateral must cover plausible extractable value, and enforcement must be timely and objective. If a coalition controls both ordering and the evidence path, nominal collateral may not be reachable.

The launch test should have the sequencer intentionally miss and conflict promises, rotate keys with outstanding promises, and operate through an L1 reorganization. Users should see the state change, claim process, and final outcome without relying on a private support decision.

## **Technology Watch Template**

Track developing mechanisms with a dated table:

| Field | Question |
|---|---|
| Claim | What measurable improvement is promised? |
| Stage | Paper, prototype, testnet, limited production, or permissionless production? |
| Assumptions | Network, cryptography, honest parties, hardware, governance? |
| Implementation | Which code and commit implement the claim? |
| Evidence | Proof, benchmark, test vectors, audits, incidents? |
| Dependencies | Sequencer, prover, DA, settlement, relayer, keys? |
| Recovery | What happens when each dependency fails? |
| Control | Who can upgrade, pause, censor, or change membership? |
| User status | What can a wallet truthfully display at each boundary? |
| Next gate | Which falsifiable test must pass before wider use? |

Update the table when evidence changes. Do not silently convert a future roadmap into a present property. That discipline keeps a future-directions chapter useful after individual project timelines change.

## **Conclusion**

The future is likely to combine rollups, real-time proofs, sampled data, parallel VMs, shared sequencing, and abstracted cross-chain interfaces. This stack can support far more activity than a single replicated machine.

Its central challenge is preserving verifiability while complexity moves between layers. The successful systems will not be those with the largest TPS claim. They will make their assumptions visible, provide credible recovery paths, and let ordinary users benefit from scale without becoming experts in every layer beneath them.

## **References**

[^1]: Feist, Dankrad, et al. "EIP-7594: PeerDAS." <https://eips.ethereum.org/EIPS/eip-7594>.
[^2]: Ethereum.org. "The Verge." <https://ethereum.org/roadmap/verkle-trees/>.
