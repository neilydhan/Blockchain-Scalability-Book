# **Chapter 3: Layer 1 vs Layer 2 — Comparing Different Approaches to Blockchain Scaling**

## **Introduction**

As demand for blockchain applications grows, the need for scalable infrastructure has become paramount. Whether it's the congestion seen during the 2017 CryptoKitties craze, the gas wars of DeFi summer, or the rise of on-chain AI agents, blockchains must process increasing transaction loads without compromising decentralization or security. Scalability is no longer a theoretical challenge—it’s a practical necessity for blockchain adoption.

Two dominant paradigms have emerged in tackling scalability: **Layer 1 scaling** (modifying the base blockchain itself) and **Layer 2 scaling** (building auxiliary protocols atop existing blockchains). This chapter provides a clear comparison between these approaches—highlighting their benefits, trade-offs, and how they shape the future of decentralized systems.

---

## **What Is Layer 1 Scaling?**

Layer 1 refers to the **base blockchain protocol**, such as Ethereum, Bitcoin, or Solana. Scaling Layer 1 involves changing the underlying consensus mechanism, data structure, or execution environment to boost performance.

Sharding, for instance, divides the blockchain into smaller, parallel chains (shards) that process transactions independently. This not only increases throughput but also reduces the storage and computational burden on individual nodes, making it easier for more participants to run full nodes and maintain decentralization.

### **Common Layer 1 Scaling Techniques**

- **Increasing Block Size or Block Frequency**  
  More transactions per block or faster blocks can increase throughput. However, this increases the resource requirements for running full nodes, possibly reducing decentralization.

- **Optimizing Execution Environments**  
  Ethereum’s move toward the **Ethereum Virtual Machine (EVM)** and other chains adopting alternative VMs (MoveVM, WASM) aim to reduce computation cost and improve parallelizability.

- **Consensus Optimization**  
  Switching from energy-intensive PoW (Proof of Work) to more efficient PoS (Proof of Stake) improves finality and throughput. Further optimizations like pipelining and signature aggregation reduce consensus latency.

- **Sharding**  
  Dividing the blockchain into smaller parts (shards) so different transactions can be processed in parallel. This increases throughput while keeping node requirements manageable.

---

## **What Is Layer 2 Scaling?**

<p align="center">
  <img src="../assets/course/ch03_l1_l2_architecture.svg" width="760" alt="Layer 1 and Layer 2 architecture comparison">
  <br>
  <em>Figure 3.1: Channels and rollups use Layer 1 for enforcement or settlement, while a sidechain connects through a bridge but runs separate consensus. Original figure for this book.</em>
</p>


Layer 2 (L2) solutions **operate on top of Layer 1**, offloading computation and storage while anchoring security back to the base layer. L2s are increasingly favored for their **modularity**, **faster innovation cycles**, and **lighter trust assumptions** (by leveraging Layer 1 security).

While Optimistic Rollups offer lower computational costs and are easier to implement, they introduce a protocol-defined challenge period during which transactions can be disputed. This delay can be a bottleneck for applications requiring instant finality. In contrast, zkRollups provide near-instant finality through cryptographic proofs but require more complex infrastructure and higher upfront costs.

### **Common Layer 2 Techniques**

- **State Channels**  
  Two parties lock funds on L1 and interact off-chain, only submitting the final state to L1. Great for recurring transactions between fixed participants.

- **Plasma**  
  A hierarchical chain structure where child chains handle transactions and periodically commit results to L1.

- **Optimistic Rollups**  
  Transactions are executed off-chain and posted to L1 with a challenge period. Assumes correctness unless proven otherwise. Lower cost, but slower finality due to dispute windows.

- **Zero-Knowledge Rollups (zkRollups)**  
  Batch transactions are executed off-chain and verified on-chain using succinct cryptographic proofs. Offers fast finality and lower gas, but comes with higher complexity.

---

## **Comparing Layer 1 vs Layer 2**

---

## **Real-World Trade-Offs**

Both approaches present trade-offs that reflect deeper engineering and governance decisions.

- **Layer 1 Scaling** is critical for **long-term systemic performance** and for enabling L2s to thrive (e.g., Ethereum’s proto-danksharding for rollup data). However, it requires **broad consensus**, rigorous testing, and risks centralization if node requirements rise.

- **Layer 2 Scaling** allows **rapid experimentation** and composability. Projects like **Starknet** and **Optimism** push forward zk and fraud-proof technologies, while enabling users and devs to benefit from Ethereum’s trust guarantees.

Ethereum’s transition to Proof of Stake (PoS) with the Merge is a prime example of Layer 1 scaling. By reducing energy consumption and improving finality, PoS has laid the groundwork for future scalability improvements like sharding. Meanwhile, rollups amortize publication and verification costs across batches, often making application transactions cheaper than equivalent L1 execution.

While Layer 2 solutions offer significant scalability improvements, they are not without risks. For example, Optimistic Rollups rely on fraud proofs, which require users to monitor the chain for malicious activity. If users fail to do so, they risk losing funds. Similarly, zkRollups, while secure, require complex cryptographic infrastructure that can be challenging to implement and maintain.

---

## **Why Both Layers Matter**

Rather than being in conflict, **Layer 1 and Layer 2 solutions are complementary**. Layer 1 provides a **secure and decentralized foundation**, while Layer 2 enables **scalable and application-specific environments**.

- Ethereum’s roadmap exemplifies this layered vision—L1 focuses on decentralization and data availability, while L2s handle execution at scale.
- In the long run, we may see **multi-layer ecosystems** where L3s handle app-specific logic, anchored to L2s, which in turn rely on a robust L1.

---

## **A Transaction's Path Through Layer 1 and Layer 2**

The difference between L1 and L2 becomes clearer by following the same token transfer through each system.

On Layer 1, a user signs a transaction and sends it to the peer-to-peer network. A block producer chooses its position, every validating node executes it, consensus selects the canonical block, and the resulting state becomes final under the chain's rules. Execution, data publication, and consensus all happen in the same security domain.

On a rollup, the user normally sends the transaction to an L2 sequencer. The sequencer orders and executes it and may return a soft confirmation immediately. Later, the rollup publishes transaction data and a state commitment. Ethereum consensus finalizes that publication. The rollup contract then accepts the state after either a fraud-proof window or verification of a validity proof. One user action therefore has several milestones: receipt by the sequencer, inclusion in an L2 block, publication to L1, proof acceptance, and L1 finality.

A sidechain follows a different path. Its own validators execute and finalize the transaction. Ethereum sees nothing unless a bridge message is later submitted. The sidechain may be fast, but its correctness comes from its validator set and bridge, not from Ethereum merely because assets can move between them.

These paths explain why the label "Layer 2" should describe a security relationship rather than a position in a diagram. A system is meaningfully layered when the base chain can enforce state correctness or user exits under stated assumptions.

## **The Scaling Bottleneck Moves**

A system rarely has one permanent bottleneck. Raising an L1 gas limit can move the limit from execution to block propagation. A parallel VM can move it from CPU to state-database access. A rollup can make execution cheap enough that data publication dominates fees. Cheap blobspace can make proving or sequencing the next constraint.

This is why capacity planning must be end to end. Let:

- `E` be sustainable execution capacity in gas per second;
- `D` be data capacity in bytes per second;
- `C` be consensus capacity in blocks or votes per second;
- `P` be proof generation capacity for a validity system.

Application throughput is bounded by the first saturated resource. Adding capacity to `E` has little effect when each transaction consumes enough published bytes to saturate `D`. An optimization should identify which resource is limiting under the target workload and show that the next resource can absorb the displaced demand.

## **A Better Comparison Framework**

The earlier table gives a useful overview, but a production choice needs more detail.

### **Security and Recovery**

Ask who can make invalid state final, who can withhold data, and what a user can do when the normal operator disappears. An L2 with a centralized sequencer may still preserve fund safety if users can force inclusion and exit. A sidechain with many validators may still be exposed if its bridge is controlled by a small multisig.

### **Finality**

Separate user-perceived confirmation from economic and cryptographic finality. L2 confirmations are often fast because a sequencer promises an order. A bridge receiving a large deposit may wait for L1 settlement and proof acceptance instead.

### **Cost**

Layer 1 users pay for globally replicated execution and data. Rollup users share publication and verification across a batch. Sidechain users pay that chain's validators. Channel users pay to open and close while bearing the opportunity cost of locked liquidity. Fee comparisons should include the cost of withdrawal and failure recovery, not only the normal transaction.

### **Composability**

Contracts on one synchronous state machine can call each other atomically. Moving execution across rollups or shards turns those calls into messages. The result may scale better, but developers must handle delay, replay protection, and partial completion.

### **Decentralization of Operations**

Validator count is only one dimension. Sequencers, provers, relayers, bridge administrators, RPC providers, and upgrade signers can each become a control point. A complete architecture diagram names these roles.

## **Worked Design Choice: An On-Chain Game**

Suppose a game generates 500 player actions per second, needs sub-second feedback, and has occasional high-value asset withdrawals.

Putting every action on Ethereum L1 gives strong settlement but poor cost and latency. A payment channel is insufficient because players interact with shared game state. A high-throughput sidechain can meet latency, but the game's valuable assets inherit the sidechain bridge's trust model. A rollup can execute frequent actions cheaply and settle asset ownership to Ethereum, while a centralized sequencer initially provides fast feedback.

The rollup is not automatically the answer. If the game state is too large to publish economically, a validium or external DA layer may be considered. That lowers cost but adds a withholding assumption. If the game requires every player action to synchronously interact with DeFi on Ethereum, asynchronous messaging may make the experience unacceptable. The design decision follows the workload and recovery requirements, not a universal ranking of technologies.

## **Chapter Summary**

Layer 1 scales the base protocol; Layer 2 reduces the work the base layer performs per user action while retaining a settlement or enforcement relationship. Sidechains add independent capacity but carry independent consensus and bridge risk. Channels specialize in repeated interactions; rollups specialize in batched general-purpose execution.

The right comparison follows a transaction from submission through finality and failure recovery. It identifies the bottleneck, the trust domain at every stage, and the user's escape path.

## **Conclusion**

Scaling blockchain is not a single-track journey. While Layer 1 changes lay the groundwork for a performant base, Layer 2 innovations accelerate real-world usability. Understanding their strengths, limitations, and interplay is crucial for builders, researchers, and users shaping the decentralized future.

In the next chapter, we’ll dive deeper into Layer 1 scaling—exploring the techniques used to scale consensus, execution, and data availability within the core protocol. As we’ll see, scaling the base layer is not just about increasing throughput—it’s about balancing performance, security, and decentralization in a way that supports the entire blockchain ecosystem.
