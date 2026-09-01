# **Chapter 1: Understanding Blockchain Scalability Challenges**

## **Introduction**  

Blockchain technology promises a decentralized, secure, and transparent approach to handling digital transactions and computation. However, as its adoption grows, scalability remains a significant barrier preventing blockchain networks from achieving mass adoption. Unlike traditional centralized systems like VISA or PayPal, which process thousands of transactions per second (TPS), major blockchain networks like Ethereum and Bitcoin struggle to achieve even a fraction of that throughput.

Scalability is critical not just for financial transactions but also for broader applications like gaming, AI-driven agents, and supply chain tracking. This chapter introduces blockchain scalability issues, examining real-world bottlenecks, past challenges, and industry efforts to redefine what scalability means in a decentralized system.

---
## **Why Naive Comparisons Fail**

A payment network, an exchange database, and a public blockchain perform different work under different trust assumptions. A card network may authorize a payment quickly while settlement, fraud handling, and bank reconciliation occur later. A public blockchain validates signatures, executes shared state, propagates data, and reaches Byzantine consensus before offering its strongest finality.

This does not make performance comparison useless. It means the comparison must hold the workload and completion boundary constant. A transfer-only TPS figure cannot be compared with arbitrary smart-contract execution. A sequencer acknowledgement cannot be compared with L1 finality. A laboratory cluster cannot be compared with a geographically distributed validator network without reporting the difference.

The immediate symptoms of insufficient capacity are familiar: transactions wait, fee markets rise, users retry, and applications become unreliable. Historic events such as the CryptoKitties congestion episode made those symptoms visible. Their precise fees and shares of network traffic are less important than the mechanism: demand exceeded scarce blockspace, so inclusion latency and price rose together.

## **Gas and the Price of Shared Computation**

Ethereum meters execution in **gas**. Every operation consumes a defined gas amount, and a transaction supplies a gas limit that bounds its work. This prevents a Turing-complete program from consuming validator resources forever.

Since EIP-1559, an Ethereum transaction pays a protocol-determined **base fee** that is burned and may add a **priority fee** to reward inclusion. The base fee changes with block utilization. The transaction's execution payment is approximately:

> `gas used × (base fee + priority fee)`

Blob-carrying transactions use a separate blob fee market. This separation matters for scaling: rollup data demand can change without pricing every EVM operation identically.

Gas is both metering and congestion pricing. It approximates execution and state cost well enough for the protocol to ration resources, but it is not a perfect hardware benchmark. An opcode's gas schedule is a governance and security parameter, while actual client performance changes with software and hardware.

## **Case Study: Congestion and Application Design**

When one popular application fills blocks, every application sharing the fee market competes for the same capacity. Users who need immediate inclusion bid more; users with low-value actions wait or leave. This is the practical consequence of synchronous composability: applications share one state and can interact atomically, but they also share congestion.

Scaling designs respond differently. A larger L1 block admits more shared activity but raises validator load. An application-specific chain isolates congestion but fragments state and security. A rollup batches application execution and shares the cost of data publication. A state channel avoids publishing repeated interactions but works only for a constrained participant set.

The right design depends on whether the application needs global synchronous state, how valuable its assets are, what latency users need, and how they recover from operator failure.

## **What Does “Scalability” Really Mean?**  

The term **scalability** is frequently used in blockchain discussions, but defining it precisely is challenging. Does it mean:  

- Higher **transactions per second**?  
- Faster **block finalization**?  
- More efficient use of **hardware resources**?  
- Achieving greater throughput **without centralization**?  

### **Lack of a Formal Definition**  

In multiprocessor computing, **scalability** is commonly discussed, but a widely accepted technical definition is lacking. In a seminal research paper, **Mark D. Hill** notes:  

> "Scalability is a frequently claimed attribute of multiprocessor systems. While the basic concept is intuitive, there is no generally accepted definition of scalability." [^1]

[^1]: Mark D. Hill, *What is Scalability？*. [Available here](https://minds.wisconsin.edu/bitstream/handle/1793/9676/file_1.pdf?sequence=1&isAllowed=y).

This ambiguity extends to blockchain. Without a standard metric, projects often define scalability in ways that serve their marketing rather than technical clarity.  

---
## **Defining Scalability: Lessons from Databases**  

Scalability is a concept that transcends blockchain technology. To clearly define blockchain scalability, it’s helpful to first explore how scalability is defined and measured in traditional databases—systems that have been optimizing for performance and growth for decades. By understanding the principles of database scalability, we can better appreciate the unique challenges and opportunities in blockchain systems.  

### **What Is Database Scalability?**  

In the context of databases, scalability refers to the system’s ability to handle increasing workloads—such as more users, transactions, or data—without degrading performance. A scalable database can grow to meet demand, whether by adding more resources to a single machine (**vertical scaling**) or distributing the workload across multiple machines (**horizontal scaling**).  

### **How Is Database Scalability Measured?**  

Database scalability is typically quantified using the following metrics:  

- **Throughput**: The number of transactions or queries the system can process per second (**TPS** or **QPS**).  
- **Latency**: The time it takes to complete a single transaction or query.  
- **Resource Utilization**: How efficiently the system uses hardware resources (e.g., CPU, memory, storage).  
- **Elasticity**: The ability to scale up or down dynamically in response to changing workloads.  

These metrics provide a clear framework for evaluating scalability, whether in centralized databases or decentralized blockchains.  

---

## **Fundamental Problems in Blockchain Scalability**  

While traditional databases have largely solved scalability through centralized or semi-centralized approaches, blockchains face unique challenges due to their **decentralized nature**. The core problems in blockchain scalability stem from three fundamental requirements:  

1. **Replicated Computation** → Every node in the network processes all transactions, leading to redundant computation.  
2. **Replicated Storage** → Every node stores all historical data, resulting in significant storage overhead.  
3. **Consensus Overhead** → Nodes must agree on the total ordering of transactions, which introduces communication and coordination costs.  

These requirements create a **scalability trilemma**: achieving **high throughput, low latency, and decentralization** simultaneously is extremely difficult.  

For example:  

- **In Bitcoin and Ethereum**, every node processes all transactions and stores the entire blockchain, limiting throughput and increasing latency.  
- **Consensus protocols like Proof of Work (PoW) or Proof of Stake (PoS)** add significant overhead, further reducing scalability.  

---

## **Fundamental Challenges for Scalable Blockchain Systems**  

To address these problems, the blockchain community is exploring whether it’s possible to achieve:  

- **Partial Transaction Processing** → Can nodes process only a subset of transactions, rather than all of them?  
- **Partial Data Storage** → Can nodes store only a portion of the blockchain data, rather than the entire history?  
- **Efficient Consensus** → Can consensus protocols be optimized to reduce communication overhead while maintaining security?  

These challenges are often framed in terms of three key properties:  

- **State Validity** → Ensuring that the state of the blockchain (e.g., account balances, smart contract states) is correct and consistent across nodes.  
- **Data Availability** → Ensuring that all necessary data is available for validation, even if nodes only store partial data.  
- **Byzantine Adversary Resistance** → Ensuring that the system remains secure and consistent even in the presence of malicious actors.  

---

## **Defining Blockchain Scalability**  

Given these challenges, we can define **blockchain scalability** as the ability of a blockchain system to:  

- **Increase throughput** (transactions per second) without significantly increasing latency.  
- **Reduce resource usage** (computation, storage, and communication) while maintaining decentralization and security.  
- **Scale dynamically** to handle growing workloads, such as more users, transactions, or smart contract interactions.  

Unlike traditional databases, **blockchain scalability must be achieved without compromising the core principles of decentralization, security, and immutability**. This makes scalability one of the most pressing challenges in blockchain technology today.  

---
## **Learning from Traditional Systems: Benchmarking Scalability**  

Now that we have defined blockchain scalability and examined its fundamental challenges, a natural question arises: **how do we measure scalability effectively?** The blockchain industry still lacks a universal standard for benchmarking scalability, making it difficult to compare different systems objectively.  

To better understand the importance of benchmarking, we can turn to **database systems**, which have been optimizing for performance and scalability for decades. **The benchmarking methodologies used in databases provide valuable insights into how structured performance evaluation can drive improvements and innovation.**  

---

## **Benchmarking Databases: A Systematic Approach**  

In the database industry, benchmarking plays a crucial role in evaluating **performance, scalability, and efficiency**. Over decades, database systems have developed structured benchmarking methodologies that help compare different architectures under standardized conditions. These benchmarks are essential because they provide a **consistent, repeatable** way to measure how systems handle increasing workloads, allowing developers and researchers to optimize performance.  

---

### **How Are Databases Benchmarked?**  

Databases are benchmarked using **standardized testing frameworks** that assess performance across various workloads. Some of the most widely used database benchmarks include:  

- **TPC-C** – Measures online transaction processing (**OLTP**) performance, simulating real-world e-commerce workloads.  
- **TPC-H** – Evaluates **decision-support systems** and complex queries.  
- **YCSB (Yahoo! Cloud Serving Benchmark)** – Designed for benchmarking **NoSQL databases** and key-value stores.  
- **OLTPBench** – A framework that supports multiple **transactional workloads** for relational databases.  

Each benchmark focuses on key performance indicators such as:  

- **Throughput (Transactions Per Second, TPS)** – Measures how many transactions the system can process within a given time.  
- **Latency** – Assesses the delay between submitting a query and receiving a response.  
- **Scalability** – Evaluates how well the system adapts as the number of users, queries, or nodes increases.  
- **Concurrency Handling** – Determines the system’s ability to process multiple operations simultaneously.  
- **Resource Utilization** – Examines how efficiently the system uses **CPU, memory, and storage**.  

These benchmarks follow **rigorous methodologies**, ensuring **fair comparisons** across different database architectures, whether **relational (SQL) or NoSQL systems**.

---

### **Why Is Benchmarking Important?**  

1. **Standardization** – It allows for **objective comparisons** between different database implementations.  
2. **Optimization** – Helps engineers identify **bottlenecks** and optimize performance.  
3. **Scalability Insights** – Demonstrates how a database performs under **real-world, high-load conditions**.  
4. **Industry Adoption** – A well-established benchmark can influence **technology adoption** by enterprises.  

Without proper benchmarking, database performance claims would be **inconsistent, misleading, or difficult to verify**. The structured benchmarking frameworks provide **scientific rigor** to ensure that improvements in performance are **measurable and reproducible**.  

---

### **Challenges in Benchmarking Databases**  

While database benchmarking has been widely adopted, it is **not without challenges**:  

- **Diverse Workloads** → Different databases are optimized for different use cases (**OLTP vs. OLAP**), making direct comparisons difficult.  
- **Hardware Variability** → Performance can be heavily influenced by **underlying infrastructure**, requiring careful test standardization.  
- **Tuning & Optimization** → Some databases require extensive **manual tuning** to perform well in benchmarks, which may not reflect real-world conditions.  
- **Scalability Metrics** → Traditional benchmarks measure **centralized scalability**, but distributed systems introduce new variables like **consistency models, replication lag, and fault tolerance**.  

Despite these challenges, **database benchmarking remains one of the most reliable ways to evaluate system performance**, providing valuable insights for system architects and engineers.

---

## **Relevance to Blockchain Benchmarking**  

Understanding how databases are benchmarked helps us appreciate **why benchmarking blockchains is even more complex**. Unlike traditional databases, **blockchains introduce decentralization, consensus mechanisms, and cryptographic constraints**, making performance evaluation far more challenging.  

In the next section, we’ll explore how the blockchain industry is attempting to **develop standardized benchmarking frameworks**, such as **BLOCKBENCH**, to measure blockchain scalability systematically.  

---
## **Benchmarking Blockchain Scalability: BlockBench & Gas Per Second**  

As blockchain adoption grows, the need for **scalability benchmarking** becomes increasingly important. Unlike traditional databases, where performance can be measured using well-established benchmarks like TPC-C and YCSB, blockchain lacks a universal standard for measuring scalability. This makes it difficult to compare different blockchain implementations objectively.  

Two emerging approaches—**BlockBench** and **Gas Per Second (GPS)**—offer early attempts to standardize blockchain performance metrics.  

---

### **BlockBench: A First Step Toward Blockchain Benchmarking**  

BlockBench [^2] is one of the earliest frameworks developed to benchmark **private (permissioned) blockchains**. It introduces a structured methodology for evaluating blockchain scalability, focusing on three key layers:  

1. **Consensus Layer** – Measures how different consensus algorithms (e.g., PBFT, PoW, PoA) affect performance.  
2. **Data Layer** – Analyzes blockchain storage models and how they impact read/write speeds.  
3. **Execution Layer** – Benchmarks smart contract execution speed and efficiency, particularly for EVM-based chains.  

BlockBench evaluates **throughput, latency, and fault tolerance** using real-world workloads, such as key-value storage benchmarks (YCSB) and OLTP-style transactions.  

However, while BlockBench provides a useful starting point, its focus is primarily on **private blockchains**, making it **less relevant for public, high-throughput blockchains like Ethereum**.  

[^2]: Tien Tuan Anh Dinh, *BLOCKBENCH: A Framework for Analyzing Private Blockchains*. [Available here](https://www.comp.nus.edu.sg/~ooibc/blockbench.pdf).

---

### **Gas Per Second: A More Accurate Measure for EVM Chains**  

While **Transactions Per Second (TPS)** is commonly used to measure blockchain performance, it has limitations—**not all transactions consume the same computational resources**. A more precise metric, **Gas Per Second (GPS)** [^3], offers a better way to benchmark Ethereum and EVM-compatible blockchains.  

#### **Why GPS Matters**
- **Gas measures computational effort, not just transaction count.**  
- **GPS accounts for both execution and storage costs**, making it a better performance indicator than TPS.  
- **Helps prevent DoS attacks** by ensuring that performance evaluations account for resource usage, not just raw transaction count.  

GPS is calculated as:  
> **Gas Per Second = (Target Gas Usage Per Block) / (Block Time)**  

This metric allows researchers and developers to compare execution performance across different Ethereum-based Layer 1 and Layer 2 chains, offering a **standardized way to assess scalability**.  

[^3]: Georgios Konstantopoulos, *Reth’s path to 1 gigagas per second, and beyond*. [Available here](https://www.paradigm.xyz/2024/04/reth-perf).

---

### **The Road Ahead for Blockchain Benchmarking**  

While **BlockBench** and **GPS** are steps in the right direction, blockchain benchmarking is still in its infancy. A **comprehensive performance benchmark** should account for:  

1. **Execution scalability** – How efficiently smart contracts are processed.  
2. **State growth impact** – The cost of managing increasing blockchain state sizes.  
3. **Hardware utilization** – How well different clients optimize CPU and storage usage.  
4. **Cross-chain interoperability** – Performance across modular execution layers.  

Standardizing blockchain benchmarks will require ongoing collaboration between **developers, researchers, and infrastructure providers**. As blockchains move beyond experimental scaling models, rigorous benchmarking will be essential to ensuring that new architectures **deliver real performance gains** without compromising decentralization or security.  

---

## **Why This Matters**  

Understanding **database scalability** provides a useful benchmark for evaluating **blockchain scalability**. However, the **decentralized nature** of blockchains introduces unique constraints that require **innovative solutions**. By addressing the fundamental problems of **replicated computation, replicated storage, and consensus overhead**, and tackling the fundamental challenges of **state validity, data availability, and Byzantine adversary resistance**, the blockchain community can pave the way for **scalable, high-performance systems**.  

In the next section, we’ll explore how these challenges are being addressed through **Layer 1 and Layer 2 solutions**, as well as technologies like **sharding** and **rollups**.

---

## **A Scalability Model for This Book**

The word *scalability* is often used when a team really means peak throughput. This book uses a stricter definition:

> A blockchain scales when it can support increasing useful demand while keeping verification, participation, and failure recovery within acceptable cost and latency bounds.

This definition has four consequences. First, the workload must be specified. Ten thousand independent transfers are not equivalent to ten thousand swaps that all modify one liquidity pool. Second, resources must be specified: CPU model, core count, memory, storage, network bandwidth, validator count, and geographic distribution. Third, security must remain comparable. A system that replaces 1,000 independent validators with one database has increased capacity but has not demonstrated blockchain scalability. Fourth, the result must survive failure. Normal-path TPS says little about a sequencer outage, leader change, data withholding attack, or mass exit.

### **Throughput, Latency, and Capacity**

*Throughput* is completed work per unit time. *Latency* is the time one request takes. *Capacity* is the maximum sustainable load before latency or failure rate becomes unacceptable. They interact but are not interchangeable.

A batching system illustrates the distinction. Waiting to collect 1,000 transactions may increase throughput and reduce cost per transaction, but the first user in the batch waits longer. A pipelined consensus protocol may commit one block per round after warming up even though each block needs several rounds to reach finality. Always ask which quantity improved.

### **Vertical and Horizontal Scaling**

Vertical scaling extracts more work from one machine by using faster hardware or better software. Horizontal scaling divides work among machines. Blockchains need both, but horizontal scaling is harder because machines may be faulty or adversarial and must agree on shared state.

A useful mental model is a replicated state machine. If every validator executes every transaction, adding validators increases redundancy and security but does not add execution capacity. Sharding, rollups, and parallel execution change which work is repeated, where it is performed, or how independent work is scheduled.

## **A Transaction as a Resource Vector**

TPS treats every transaction as one unit. In reality, a transaction consumes several resources:

- signature verification and EVM computation;
- state reads and writes;
- bytes propagated across the network;
- bytes retained temporarily or permanently;
- consensus votes and block space;
- proof generation or verification in a validity system.

Represent a workload as a vector rather than a count. A calldata-heavy rollup batch stresses data bandwidth. A zero-knowledge application may stress proving. A hot DeFi contract stresses sequential state access. The sustainable transaction rate is bounded by the first exhausted resource.

Ethereum gas captures part of computation and storage cost, which makes gas per second more informative than transfer TPS. It is still not a universal metric because gas schedules approximate resource usage and exclude consensus and off-chain proving.

## **Worked Example: Benchmarking Two Chains**

Chain A reports 20,000 TPS using simple transfers on eight validator machines in one data center. Chain B reports 4,000 TPS using contract calls across 200 geographically distributed validators. Chain A is faster for the measured workload, but the headline does not establish that its architecture is more scalable.

A fair experiment fixes or reports the transaction mix, validator hardware, network topology, state size, block size, duration, client version, and tolerated failure rate. It measures p50 and p99 latency, not only the average. It runs long enough to expose state growth and database compaction. It introduces a faulty leader or network delay and records recovery.

The output should be a curve. At low load, latency is stable. As offered load approaches capacity, queues form and tail latency rises. Beyond the knee, throughput may flatten while failures increase. The knee of that curve under a realistic workload is more useful than one peak number.

## **The Four-Layer Evaluation Framework**

<p align="center">
  <img src="../assets/course/ch01_scalability_stack.svg" width="760" alt="Execution, settlement, consensus, and data availability">
  <br>
  <em>Figure 1.4: A blockchain transaction depends on execution, settlement, consensus, and data availability. Monolithic chains combine them; modular systems separate some roles. Original figure for this book.</em>
</p>


The chapters ahead repeatedly separate four functions:

1. **Execution** computes state transitions.
2. **Settlement** decides which transition is accepted and resolves disputes.
3. **Consensus** orders data and finalizes a history.
4. **Data availability** ensures that the information needed for verification can be obtained.

A monolithic chain performs all four together. A rollup may execute elsewhere while Ethereum supplies settlement, consensus, and data. A modular DA layer may order and publish data without knowing an application's execution rules. Keeping these functions separate prevents category errors, such as assuming a validity proof also proves data availability or assuming a bridge gives a sidechain Layer 1 security.

## **Security and Decentralization Measurements**

Decentralization is not a raw node count. Nodes operated by one company, hosted in one cloud, or controlled by one key do not provide independent failure domains. Relevant measures include stake or hash-power concentration, client diversity, hosting and geographic distribution, hardware requirements, governance power, and the ability of an ordinary user to verify and exit.

Security should be expressed as an adversary model. What fraction of validators can be Byzantine? Can the attacker delay the network, corrupt participants adaptively, or withhold data? Which guarantees fail first: liveness, safety, censorship resistance, or data retrieval? A protocol is secure only relative to those assumptions.

## **How to Read Performance Claims**

When a project claims a large scalability gain, ask:

- What transactions were executed?
- Was the number measured, simulated, or projected?
- Which hardware and network were used?
- How many independent validators participated?
- Which finality boundary ended the timer?
- Was data publication included?
- Did the test include proof generation, state storage, and failures?
- Can users recover if the normal operator disappears?

These questions do not dismiss performance work. They make results reproducible and comparable.

## **From Transaction Submission to Finality**

A blockchain performance measurement needs a precise start and finish. A transaction passes through construction and signing, RPC admission, peer-to-peer propagation, block inclusion, execution and fork choice, then finality. "Transaction latency" may stop at any one of these boundaries.

A wallet often shows block inclusion because it is fast and useful. A bridge waits for stronger finality because releasing assets against a reverted source transaction can create an unbacked claim. A rollup adds further milestones: sequencer acknowledgement, L2 inclusion, data publication, proof acceptance, and settlement finality.

This path explains why VM throughput is not chain throughput. The result still has to be encoded, propagated, agreed upon, committed to state, indexed, and served back to users.

## **Queueing and the Capacity Knee**

When transactions arrive more slowly than the system processes them, queues remain short. Near capacity, ordinary variance produces bursts faster than blocks or batches can absorb. Waiting time rises even before average demand exceeds average service.

Let work arrive at rate `λ` and be processed at sustainable rate `μ`. A basic queue becomes unstable when `λ ≥ μ`. Blockchains add batches, heterogeneous transactions, and fee priority, but the lesson holds: running continuously at advertised peak throughput creates poor tail latency.

A sound capacity plan reserves headroom for larger witnesses, failed leaders, prover retries, database compaction, and recovery traffic. Fee markets act as admission control. When demand exceeds scarce blockspace, users bid for priority while low-value work waits. The fee spike is the mechanism allocating congestion, not an unrelated symptom.

## **State, History, and Working Sets**

**History** is the ordered record of blocks and transactions. **State** is the latest value of live accounts, contracts, or objects. The **working set** is the portion current execution touches. Pruning history does not shrink live state. Stateless validation reduces a validator's need to store state by supplying witnesses, but a builder or state provider still needs data to produce those witnesses.

Benchmark duration matters because caches hide storage cost. A short test may keep its working set in memory. A long-running chain reads cold state, compacts databases, creates snapshots, and serves synchronization. Sustainable performance includes these tasks.

## **A Reproducible Benchmark Procedure**

1. Define completion: execution, inclusion, optimistic confirmation, proof acceptance, or consensus finality.
2. Publish transaction templates, state size, locality, and conflict rate.
3. Record client commits, protocol parameters, validator count, hardware, geography, and network shaping.
4. Warm representative state under a published rule.
5. Sweep offered load while measuring queue depth, failures, resource usage, fees, and p50/p95/p99 latency.
6. Inject a faulty leader, sequencer outage, delayed region, data withholding event, and prover crash.
7. Report the highest load meeting the latency and error objective, not the largest transient burst.

### **Worked Benchmark: A Rollup Exchange**

Suppose an exchange sees 60% limit-order placements, 30% cancellations, and 10% market orders. Placements write an order and one price level. Market orders can touch many levels and accounts. A transfer benchmark misses this shared state.

A realistic generator samples prices and sizes, creates bursts around market moves, and records sequencer acknowledgement, L2 inclusion, publication, proof completion, and settlement. The first limit may be a hot price level. After partitioning markets, blob publication may dominate. After compression, proof generation may queue. Each optimization requires another end-to-end test.

## **Scalability Claims as Falsifiable Statements**

A useful claim states workload, duration, validator topology, hardware, latency, finality, and failure behavior. "This system sustains the published mixed workload for one hour across 100 distributed validators while p99 finality stays below ten seconds and one leader failure recovers within thirty seconds" can be tested. "Up to 100,000 TPS" cannot.

## **Chapter Summary**

Blockchain scalability is sustained useful capacity under explicit workload, resource, security, and recovery assumptions. TPS alone omits transaction complexity, latency, hardware, decentralization, and data. The central difficulty comes from globally replicated execution and storage plus the communication required for Byzantine consensus.

The rest of the book studies ways to divide or compress that work: sharding at Layer 1, channels and rollups at Layer 2, modular data availability, parallel execution, and more efficient consensus.
