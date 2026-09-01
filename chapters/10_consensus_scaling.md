# **Chapter 10: Consensus Scaling**

## **Introduction**

Consensus allows independent nodes to agree on one ordered history despite failures and malicious behavior. It is also a scalability bottleneck. More validators improve fault tolerance and decentralization, but create more messages, signatures, and network delay.

Consensus scaling therefore seeks lower communication cost and faster finality without hiding the network and adversary assumptions that make those results possible.

---

## **Safety, Liveness, and Finality**

A consensus protocol must separate three properties:

- **Safety** – honest nodes do not finalize conflicting blocks.
- **Liveness** – the protocol continues to finalize blocks.
- **Finality** – once finalized, a block cannot be reverted without violating the fault assumption.

Network timing matters. A synchronous model assumes a known message-delay bound. A partially synchronous model assumes the bound eventually holds but its starting time is unknown. An asynchronous model makes no timing bound.

These assumptions determine both fault tolerance and latency. Performance claims that omit them are incomplete.

---

## **Nakamoto and BFT-Style Consensus**

Nakamoto consensus selects a chain through accumulated proof of work. It scales to an open validator set and tolerates temporary forks, but finality is probabilistic. Larger or faster blocks increase stale-block pressure and may favor well-connected miners.

Classical Byzantine fault tolerant protocols use voting rounds. Under partial synchrony, a committee of *3f + 1* replicas can make progress and remain safe with up to *f* Byzantine replicas. Once a quorum certificate is formed, finality can be deterministic.

The challenge is communication. A naive all-to-all vote exchange requires quadratic messages as the validator set grows.

---

## **HotStuff**

<p align="center">
  <img src="../assets/course/ch10_hotstuff_flow.svg" width="760" alt="Leader-based BFT consensus flow">
  <br>
  <em>Figure 10.1: A leader proposes, replicas vote, votes form a quorum certificate, and chained certificates drive commitment. A timeout moves the protocol to a new view. Original figure for this book, based on the HotStuff paper.</em>
</p>


HotStuff is a leader-based BFT protocol designed for linear communication in the normal case. Replicas vote on a leader's proposal, and the leader aggregates votes into a quorum certificate. A sequence of certified proposals creates the locking conditions needed for safety.[^1]

Its key contributions include:

- linear communication with threshold signatures or aggregated votes;
- optimistic responsiveness after the network becomes timely;
- a pacemaker abstraction for leader changes;
- pipelining in chained HotStuff.

A bad leader can still delay a view, but the protocol rotates leaders. The pacemaker and timeout rules are therefore as important to liveness as the happy path.

---

## **Sync HotStuff**


The course examines Sync HotStuff, a synchronous state-machine replication protocol. In the steady state, a leader broadcasts a proposal, replicas echo it, and a replica can commit after waiting for the maximum round-trip delay unless it observes equivocation.[^2]

The stronger synchrony assumption permits tolerance of up to one-half Byzantine replicas, compared with the familiar one-third bound under partial synchrony. The paper reports steady-state latency near `2Δ`, where `Δ` is the known delay bound, and optimistic responsiveness when fewer than one-quarter of replicas fail to respond.

The trade-off is explicit: stronger fault tolerance and a simple fast path depend on a meaningful bound on network delay. A wide-area public blockchain may find that assumption harder to defend than a consortium network or data-center service.

---

## **Reducing Communication**

Consensus protocols use several techniques to scale:

### **Leader Aggregation**

Validators send votes to a leader instead of broadcasting every vote to everyone. The leader distributes one certificate.

### **Threshold and Aggregate Signatures**

Many signatures are compressed into a smaller proof of quorum. This saves bandwidth and verification work, although distributed key generation and signer accountability introduce complexity.

### **Committees**

A smaller rotating committee reaches agreement on behalf of a larger set. Random selection reduces targeted capture, but committee size determines the probability of a Byzantine majority.

### **Pipelining**

Different consensus stages for consecutive blocks overlap. Throughput rises even if the latency of one block is unchanged.

### **DAG-Based Mempools**

Protocols can separate transaction dissemination from ordering. Validators first certify batches in a directed acyclic graph, then consensus orders references to those batches. This reduces duplicated data transmission and keeps the ordering layer small.[^3]

---

## **Block Propagation Is Part of Consensus**

A theoretically efficient vote protocol can still be bottlenecked by distributing block data. Compact blocks, erasure-coded broadcast, relay networks, and separating headers from transaction bodies reduce this pressure.

There is also a censorship and centralization risk. Specialized relays and powerful block builders improve propagation but can become privileged infrastructure. Consensus performance must be measured with the network topology and block payload, not votes alone.

---

## **Consensus and Execution Separation**

Consensus orders transactions; execution computes their effects. Separating them allows consensus to agree on compact batch references while execution and data dissemination proceed in parallel. Modular systems take this further by assigning consensus and data availability to one layer and execution to another.

The layers still interact. Consensus cannot finalize unavailable data safely, and execution cannot finalize state without a canonical order.

---

## **Comparison**

| Family | Finality | Typical Fault Bound | Communication Idea | Main Trade-Off |
|---|---|---|---|---|
| Nakamoto | Probabilistic | Resource majority | Gossip and longest/heaviest chain | Slow certainty and fork risk |
| PBFT-style | Deterministic | `< 1/3` Byzantine | Multi-phase voting | Quadratic communication in basic form |
| HotStuff | Deterministic | `< 1/3` Byzantine | Leader aggregation and certificates | Leader/pacemaker complexity |
| Sync HotStuff | Deterministic | `< 1/2` Byzantine | Synchronous echo and wait | Relies on known delay bound |
| DAG + BFT | Deterministic | Usually `< 1/3` Byzantine | Separate dissemination and order | More protocol components |

## **Worked Example: Why a Quorum Certificate Matters**

Take four replicas, A through D, with at most one Byzantine replica. A quorum contains three votes. A leader proposes block X and gathers votes from A, B, and C. The certificate proves that at least two honest replicas voted for X.

Could conflicting block Y also obtain three votes at the same height? Any two sets of three among four overlap in at least two replicas. At least one overlapping replica is honest, so locking and voting rules prevent both certificates under the safety assumptions.

A certificate compresses quorum evidence, but it does not alone define commitment. HotStuff uses a chain of certified proposals so replicas can distinguish a safe extension from a conflict. That structure permits safe leader replacement.

## **The Liveness Path**

If leader A is offline, replicas time out, move to a new view, and send their highest certificates to leader B. B extends the safest certificate. Once messages arrive within the eventual network bound, it gathers a quorum and progress resumes.

Timeouts that are too short cause needless view changes during latency spikes. Timeouts that are too long make a faulty leader expensive. Pacemakers often back off after failures and reset after stable progress. Two implementations of the same paper can therefore show very different latency.

## **Throughput Is Not Finality Latency**

Pipelining can commit one block per round after the pipeline fills even if each block needs several rounds to become final. Throughput measures spacing between committed blocks; latency measures one transaction's journey. Benchmarks should report both, plus validator count, geography, payload size, signature scheme, and failure conditions.

## **HotStuff State and Voting Rules**

A HotStuff replica tracks more than the latest block. It stores the current view, the highest quorum certificate it knows, and a lock that prevents votes creating conflicting commits.

A proposal contains a block extending a parent and a justify QC. A replica votes only when the proposal is safe according to the locking rule. A simplified check is:

```text
safe_to_vote(proposal):
    return proposal.extends(locked_block)
        or proposal.justify_qc.view > locked_qc.view
```

The first condition follows the current lock. The second permits progress when the proposal carries newer quorum evidence. Exact protocol variants differ, but the invariant is the same: honest replicas do not vote in a way that lets two conflicting chains both satisfy the commit rule.

In chained HotStuff, each proposal can serve as a phase for an earlier block. Consecutive QCs pipeline prepare, pre-commit, and commit evidence. Once the required certified chain exists, an ancestor commits. The pipeline raises throughput because a new proposal advances several blocks' phases at once.

## **Pacemaker and View Synchronization**

Safety can hold in a fully asynchronous period, but liveness requires honest replicas to spend enough time in the same view with an honest leader. The pacemaker creates this overlap.

When a timer expires, a replica broadcasts a timeout containing its highest QC. A timeout certificate or threshold of timeout messages justifies moving to the next view. The new leader collects the highest safety evidence and proposes an extension.

Timeout selection is adaptive. A fixed timeout small enough for normal operation may cause endless view changes during an outage. An exponential backoff eventually exceeds actual delay after the network stabilizes. Implementations reset or reduce timeouts carefully after progress so latency returns to normal without synchronizing replicas into another failure cycle.

## **Threshold Signatures and Accountability**

A threshold signature compresses `2f + 1` votes into one constant-size certificate. Validators first participate in distributed key generation or receive shares under another trusted process. No coalition below the threshold can sign.

Aggregation saves bandwidth, but a single threshold signature can hide individual signers. Systems needing slashing evidence may carry signer bitmaps or use aggregate signatures that preserve attribution. Key rotation, lost shares, and membership changes also add operational cost.

A consensus design should say whether a QC proves only quorum weight or also identifies every signer. This affects forensic analysis and punishment after equivocation.

## **DAG Mempools**

Consensus proposals often carry large transaction batches. If every leader retransmits those bytes, bandwidth and leader performance dominate. A DAG mempool separates dissemination:

1. each validator broadcasts a transaction batch;
2. peers sign availability acknowledgements;
3. a certificate proves enough peers received the batch;
4. later consensus proposals order compact certificates rather than raw transactions.

The DAG records causal references among certificates. Ordering can continue with small messages after data dissemination has completed. Safety still depends on the ordering consensus, while availability depends on the certificate threshold and retrieval protocol.

This architecture adds queues and garbage collection. Nodes must retain certified batches until committed, recover missing parents, and prevent an attacker from flooding unreferenced data.

## **Consensus Implementation Checklist**

- Define the exact block, vote, QC, timeout, and view-change messages.
- Domain-separate every signature by chain, epoch, message type, and view.
- Persist locks and safety state before sending votes.
- Test crash recovery between persistence and network send.
- Bound proposal and certificate sizes.
- Measure leader change under packet loss and skew.
- Include real block dissemination in benchmarks.
- Specify validator-set transitions and old-key retirement.
- Expose highest QC, lock, current view, and timeout metrics.
- Run conflicting-message and malformed-certificate tests across all clients.

The most dangerous consensus bugs live in rare transitions: restart, epoch change, delayed old messages, and view changes during partial network recovery.

## **Epoch and Validator-Set Changes**

Consensus safety proofs often assume a fixed validator set, while proof-of-stake systems change membership. An epoch transition must bind the new set to a finalized decision by the old set.

A transition block can commit to validator public keys, weights, activation height, and protocol version. New validators begin voting only after the transition is final. Old signatures remain valid for old views but cannot authorize new-epoch blocks.

Light clients need a chain of authenticated set changes. Skipping directly from an old checkpoint to a current header without verifying intermediate transitions lets an attacker invent a validator set. Sync committees or succinct proofs compress this chain under additional assumptions.

Long-range attacks occur when old validators, whose stake is no longer slashable, sign an alternative history. Weak subjectivity addresses this by requiring clients to obtain a recent trusted checkpoint within a defined period. This is a social/bootstrap assumption distinct from short-range BFT safety.

## **Slashing and Equivocation Evidence**

A validator equivocates by signing conflicting messages that protocol rules prohibit, such as two blocks at one height or incompatible votes in one view. Slashing evidence contains both signatures and enough context to verify conflict.

Evidence must be objective and compact. A timeout is not proof of malice because networks fail. Conflicting signed votes are. Penalties can remove stake, remove future rewards, or eject validators. Excessive correlated slashing can threaten network recovery, so protocols distinguish accidental downtime from safety violations.

Accountability requires retaining signer identity. A threshold signature without attribution proves quorum but may not reveal which members equivocated. Systems may keep individual votes off-chain, publish signer bitmaps, or use aggregatable signatures preserving evidence.

## **Fork Choice and Finality Gadgets**

Some systems separate a fork-choice rule from finality. Fork choice selects the head validators should build on now; a finality gadget periodically certifies checkpoints that should never revert under the fault bound.

During temporary disagreement, honest validators can see different heads while agreeing on the latest finalized checkpoint. Applications choose confirmation policy based on risk. A low-value payment may accept head inclusion; a bridge waits for checkpoint finality.

The interaction matters. Votes used for finality may also influence fork choice, and network delay can cause validators to build on stale heads. Specifications must define tie-breaking, latest-message handling, justified checkpoints, and behavior when finality stalls.

## **Consensus Safety Testing**

A model checker explores small validator sets and message schedules, looking for two conflicting commits. Property-based tests generate delays, duplicates, reorderings, restarts, and Byzantine messages. Network simulations scale to realistic committees and geography.

Critical scenarios include:

- leader equivocates across network partitions;
- replicas restart after voting but before persisting state;
- old votes arrive after a view change;
- epoch transition overlaps a timeout;
- validator weight changes near a quorum boundary;
- clock skew triggers premature timeout;
- malformed aggregate signatures stress verification;
- a minority floods valid but useless certificates.

Testing cannot replace proof, and proof cannot replace implementation testing. The model, specification, and code must encode the same protocol.

## **Consensus Operations**

Operators monitor view duration, proposal delay, vote arrival distribution, missed leaders, QC formation time, finality lag, peer diversity, and clock offset. A rise in view changes may indicate a faulty leader, regional network problem, overloaded verification, or timeout too close to normal p99 delay.

Incident response should preserve signed messages and timing evidence. Restarting every validator simultaneously can destroy liveness or forensic context. Staged recovery keeps enough replicas online and avoids violating lock persistence.

Capacity planning includes signature verification, block execution, data propagation, and state commitment. Increasing committee size without network and verification headroom can lower security in practice by causing honest validators to miss deadlines.

## **Conclusion**

Consensus scaling is the engineering of messages, signatures, leaders, committees, and timing assumptions. HotStuff makes the normal path linear and pipeline-friendly. Sync HotStuff shows what becomes possible under synchrony. DAG-based systems separate data dissemination from ordering.

No protocol is simply "faster consensus." Each result depends on its network model, fault threshold, committee construction, block payload, and recovery behavior. The final chapter looks at how these techniques may converge in future blockchain architecture.

## **References**

[^1]: Yin, Maofan, et al. "HotStuff: BFT Consensus in the Lens of Blockchain." <https://arxiv.org/abs/1803.05069>.
[^2]: Abraham, Ittai, et al. "Sync HotStuff: Simple and Practical Synchronous State Machine Replication." <https://arxiv.org/abs/2005.13432>.
[^3]: Danezis, George, Lefteris Kokoris-Kogias, Alberto Sonnino, and Alexander Spiegelman. "Narwhal and Tusk." <https://arxiv.org/abs/2105.11827>.
