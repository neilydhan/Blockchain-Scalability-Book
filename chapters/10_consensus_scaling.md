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

## **Conclusion**

Consensus scaling is the engineering of messages, signatures, leaders, committees, and timing assumptions. HotStuff makes the normal path linear and pipeline-friendly. Sync HotStuff shows what becomes possible under synchrony. DAG-based systems separate data dissemination from ordering.

No protocol is simply "faster consensus." Each result depends on its network model, fault threshold, committee construction, block payload, and recovery behavior. The final chapter looks at how these techniques may converge in future blockchain architecture.

## **References**

[^1]: Yin, Maofan, et al. "HotStuff: BFT Consensus in the Lens of Blockchain." <https://arxiv.org/abs/1803.05069>.
[^2]: Abraham, Ittai, et al. "Sync HotStuff: Simple and Practical Synchronous State Machine Replication." <https://arxiv.org/abs/2005.13432>.
[^3]: Danezis, George, Lefteris Kokoris-Kogias, Alberto Sonnino, and Alexander Spiegelman. "Narwhal and Tusk." <https://arxiv.org/abs/2105.11827>.
