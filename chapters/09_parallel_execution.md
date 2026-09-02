# **Chapter 9: Parallel Execution**

## **Introduction**

Most blockchain virtual machines execute transactions in a block one after another. This makes verification deterministic and simple, but it leaves modern multi-core processors underused. Parallel execution asks which transactions can run at the same time without changing the final state.

The problem is not merely starting several threads. Transactions can read and write shared accounts and contracts. A parallel engine must detect conflicts and produce exactly the result required by the chain's canonical transaction order.

---

## **Intuition: Which Transactions Can Run Together?**

A block defines an ordered list of transactions. The simplest executor processes transaction 1, updates state, then processes transaction 2 against that new state. This **sequential execution** is easy to reason about but uses only one execution path at a time.

Parallel execution asks whether independent transactions can run simultaneously on several CPU cores while producing exactly the result the canonical order requires.

Imagine two cashiers. Alice transfers funds between accounts A and B while Chen transfers funds between C and D. The account sets do not overlap, so both updates can be calculated together. If Chen instead spends from B, his result depends on Alice's earlier update and the two operations conflict.

### **Reads, writes, and conflicts**

A transaction's **read set** is the state it inspects. Its **write set** is the state it changes. Two transactions conflict when canonical order can affect the result:

- both write the same value;
- one writes a value the other reads;
- a dynamic call discovers another overlapping key.

Two reads of the same value do not conflict because neither changes it.

A **conflict graph** represents transactions as points and conflicts as connecting lines. Transactions with no line between them can be candidates for the same parallel wave. This is a planning model; actual virtual-machine behavior may discover more accesses.

### **Declared and optimistic execution**

A **declared-access** system requires a transaction to identify accounts or objects it may touch before execution. The scheduler can separate non-overlapping declarations. Over-declaring reduces parallelism; under-declaring must fail or follow a protocol rule.

An **optimistic executor** starts transactions in parallel without knowing every access. It records what each attempt read and wrote. At commit time, it checks whether an earlier canonical transaction changed something the attempt read. If so, the attempt is **aborted** and retried against newer state.

"Optimistic" here means doing speculative work first and validating conflicts later. It does not change the canonical transaction order or permit different nodes to keep different outcomes.

### **Multi-version state**

A **multi-version database** keeps several versions of a value tagged by transaction position. A speculative transaction reads the newest version that should precede it. If an earlier transaction later creates a newer relevant version, validation detects that the speculative read was stale.

Think of draft pages numbered by order. A worker assigned page 8 may read the latest accepted edit before 8. If page 5 later changes that paragraph, page 8's work must be checked again.

### **Determinism and commitment**

CPU thread timing differs between machines. One worker may finish first on one validator and last on another. Consensus remains safe only if every valid schedule commits the same ordered result.

The executor may schedule freely internally, but state roots, receipts, logs, gas, return values, and failure outcomes must match the reference sequential semantics. Parallelism is an implementation method, not a new meaning for the block.

### **The hot-state limit**

A popular counter, liquidity pool, or market price can become **hot state** touched by many transactions. More CPU cores do not help when every update must follow one another. This is like adding checkout lanes when every cashier still needs the same single stamp.

Applications improve concurrency by splitting independent balances or markets, using append-only claims, aggregating later, and avoiding unnecessary global counters. The protocol can schedule better only when the workload contains real independence.

### **Reading speedup**

If a fraction of work must remain serial, it limits total speedup. Eight cores cannot make a program eight times faster when half its work uses one ordered path. Retries, validation, database locking, and final root construction add more overhead.

Worked examples later show attempts and milliseconds explicitly. Count all speculative attempts, including discarded ones; reporting only successfully committed transactions hides wasted resources.

## **Why the EVM Is Commonly Sequential**

<p align="center">
  <img src="../assets/course/ch09_parallel_scheduler.svg" width="760" alt="Parallel execution scheduler, conflicts, and deterministic commit">
  <br>
  <em>Figure 9.1: Independent transactions can run on different workers, while conflicting reads wait or retry and commitment preserves the canonical result. Original figure for this book, based on Block-STM and SC6019 Lecture 05.</em>
</p>



An Ethereum transaction may call arbitrary contracts, which may call other contracts and touch storage addresses not obvious from the transaction envelope. The effect of transaction B can depend on the state produced by transaction A. Executing B early may therefore return a different value.

Sequential execution solves this by applying transactions in order. It is deterministic but limits execution throughput to a single ordered pipeline. Faster CPUs help, but adding cores does not automatically increase gas per second.

---

## **Conflict Graphs**

Two transactions can run concurrently when their state accesses do not conflict. A conflict exists when:

- both write the same state location; or
- one writes a location the other reads.

Two read-only accesses are compatible. If the access sets are known, an engine can build a dependency graph and schedule independent transactions together.

The main challenge is discovering those access sets. Smart contracts generate addresses dynamically, and calls may depend on prior reads.

---

## **Declared Access Lists**

Some systems ask transactions to declare the accounts or objects they will access. The scheduler can group non-overlapping transactions before execution.

Solana transactions specify accounts and whether they are read-only or writable. The Sealevel runtime can execute transactions that do not contend for writable accounts in parallel.[^1]

Sui uses an object-centric model. Transactions involving owned objects can often follow a fast path because their dependencies are explicit, while shared-object transactions require consensus ordering.[^2]

The benefit is predictable scheduling. The cost is a programming model that exposes concurrency to developers and users. Popular shared contracts can still become hot spots.

---

## **Optimistic Parallel Execution**

Optimistic execution starts transactions speculatively, detects conflicts afterward, and re-executes work when necessary. It is similar to software transactional memory in databases.

Block-STM, used by Aptos, executes an ordered block with multiple worker threads. Transactions record reads and writes in multi-version data structures. If a read is invalidated by an earlier transaction, the affected transaction is aborted and retried. Despite speculative execution, the committed result respects the original block order.[^3]

This approach preserves a familiar transaction model and discovers dependencies at runtime. Its performance depends on workload contention. Independent transfers scale well; thousands of transactions updating one shared counter do not.

---

## **Determinism and Consensus**

Validators must agree on the same state root. Parallel scheduling itself may be nondeterministic, but the committed semantics cannot be.

A safe engine defines:

1. a canonical transaction order;
2. rules for which version of state each read observes;
3. conflict detection and validation;
4. deterministic abort and retry behavior;
5. a final write order equivalent to sequential execution.

A performance bug can become a consensus bug if different validators commit different results. Parallel runtimes therefore need testing that combines database concurrency control with adversarial smart-contract behavior.

---

## **The Hot-State Problem**

Parallel execution does not help when a workload concentrates on one piece of state. An automated market maker pool, popular NFT mint, or global counter can serialize the block.

Applications can reduce contention through:

- partitioned order books or liquidity pools;
- per-user nonces and balances;
- commutative updates;
- batching and aggregation;
- actor or object models;
- delayed reconciliation.

This is co-design: the VM exposes concurrency, and applications organize state so the concurrency can be used.

---

## **Parallel Execution vs Sharding**

Parallel execution uses multiple cores within a validator. Sharding divides work across validator groups.

| Dimension | Parallel Execution | Sharding |
|---|---|---|
| Main scale unit | CPU cores in one validator | Validators and committees |
| State view | Often shared | Partitioned |
| Composability | Can remain synchronous | Cross-shard calls often asynchronous |
| Main limit | Contention and hardware | Committee security and communication |

The techniques complement each other. Each shard can execute transactions in parallel, and a rollup can use a parallel VM while relying on another layer for data and settlement.

---

## **Named Transaction Traces: Solana, Sui, and Aptos**

**Deployment label: all three are production networks.** They expose concurrency differently. Solana transactions declare account access before execution. Sui makes object identity and ownership central to its transaction model. Aptos orders transactions and uses Block-STM to discover conflicts during speculative execution. The useful comparison is not a peak transactions-per-second number. It is what information the scheduler has, what happens when two transactions collide, and which result becomes canonical.

### **Solana: declared accounts become runtime locks**

Trace two users buying different items from one marketplace program. Each Solana transaction contains signatures, a message, recent blockhash or durable-nonce context, instructions, and an account-key list. Each instruction identifies the program and the accounts it will read or write. The message marks accounts as writable or read-only. This declaration is part of the signed transaction, not a scheduler guess.[^1][^4]

The processing pipeline receives and deserializes the transaction, verifies signatures, sanitizes structure, checks compute budget and age, validates nonce and fee payer, loads accounts, executes instructions, then commits or rolls back.[^4] Before execution, the runtime can see that transaction A writes inventory account `item_A` while transaction B writes `item_B`. If their other writable sets do not overlap, workers can execute them in parallel even though both call the same marketplace program. Program identity alone does not force serialization; writable state overlap does.

Now add one global writable counter recording all sales. Both transactions name it. The runtime cannot safely execute both writes concurrently, so the counter becomes a lock conflict and a throughput bottleneck. If a client forgets to provide an account an instruction needs, the program cannot reach out to arbitrary undeclared state; execution fails. If a transaction declares an account writable when it only reads it, correctness survives but concurrency falls. If it understates access, the transaction fails rather than quietly bypassing locks.

Observable evidence includes the signed account list, writable flags, instruction list, compute-unit use, execution logs, status, and commit slot. A benchmark should report writable-account overlap and account-lock failures. Ten programs touching one hot token or market account may serialize more than ten calls to one program over disjoint accounts.

### **Sui: owned and shared objects choose different paths**

Sui represents state as objects with identifiers, versions, ownership, and digests. A transaction names the objects it consumes or mutates. This makes dependencies explicit at an application level: two transfers over unrelated owned objects are independent, while two calls mutating one shared object contend on that object's order.[^5][^6]

Trace a coffee-shop payment using address-owned coin objects. The wallet constructs a transaction naming the gas object, payment coin, recipient, commands, and current object versions. The user signs it and submits it. Validators verify authorization and object references, sequence the transaction under the applicable Sui path, execute Move commands, and produce signed transaction effects naming created, mutated, wrapped, or deleted objects. The effects become final under Sui's transaction rules and are later included in a checkpoint.[^5]

For an owned-object transaction, ownership gives a direct authorization and dependency structure. Separate customers spending separate coin objects do not contend on one account balance row. A shared-object transaction, such as updating one public auction, needs consensus ordering because independent users may race to mutate the same object. Sui's consensus documentation and transaction lifecycle connect this path to Mysticeti and checkpointing. The object model narrows conflict domains; it does not remove the need to order genuinely shared state.

Failure follows object versions. If two signed transactions try to consume the same owned coin version, both cannot succeed. Once one effect is final, replay or the conflicting spend is rejected by the version and ownership rules. If a wallet builds against a stale shared-object or owned-object reference, it must refresh and reconstruct rather than retry opaque bytes indefinitely. A globally shared object can become the same hot-state bottleneck seen in other systems, even when unrelated objects execute in parallel.

Observable evidence includes transaction digest, input object IDs and versions, signatures, effects certificate or final effects, and checkpoint inclusion. "Final effects" and "included in checkpoint" answer different operational questions. Indexers and bridges may wait for checkpoint evidence even when a user interface already shows transaction finality.

### **Aptos: Block-STM discovers conflicts speculatively**

Aptos transactions do not need to declare a complete read/write set in advance. Consensus establishes a block order. The execution engine then applies Block-STM, a software transactional memory design that speculates on multiple ordered transactions, records versioned reads and writes, validates those reads, and re-executes work whose assumptions were invalidated by an earlier transaction.[^7][^8]

Trace an ordered block containing `T0`, `T1`, and `T2`. `T0` updates Alice's balance. `T1` touches an unrelated resource. `T2` reads Alice's balance and sends funds. Workers may start all three. `T1` can finish independently. `T2` may first read an older multi-version value while `T0` is still running. Validation later sees that canonical earlier transaction `T0` changed the resource. Block-STM aborts and re-executes `T2` against the right version. The final state must match sequential execution in consensus order even though the work overlapped.

This optimistic design extracts parallelism without requiring programmers to predict all accesses. Its failure cost is wasted work. An adversarial or badly designed workload can let many transactions run almost to completion and then conflict on one late-read resource. Re-execution increases CPU, cache and memory pressure while committed throughput falls. Correctness requires aborted attempts to leave no durable events, writes, gas result, or external effect. The final receipts and state root must be independent of worker count and thread timing.

Aptos's end-to-end transaction path is broader than Block-STM. A client submits to a fullnode; transactions propagate toward validators, enter the consensus and Quorum Store pipeline, are ordered, executed, and committed to storage.[^8] A fast speculative attempt is not client finality. The user observes submission, pending state, block order, execution result, and commit.

### **Fixed workload comparison**

| Workload | Solana | Sui | Aptos |
|---|---|---|---|
| Two payments over disjoint state | Parallel when declared writable account sets do not conflict | Independent owned objects expose separate dependencies | Block-STM speculates in parallel and validates successfully |
| Two updates to one hot market | Shared writable account creates lock contention | Shared object requires one consensus order and remains hot | Speculation conflicts; later ordered transaction may re-execute |
| Dependency information | Signed account list and writable flags before execution | Object IDs, versions, ownership and shared-object status | Read/write dependencies discovered during speculative execution |
| Safe collision behavior | Conflicting locks prevent unsafe concurrent writes | Object version/order prevents two incompatible effects | Validation aborts stale speculation and retries in canonical order |
| Performance trap | Overbroad writable lists and global accounts | One popular shared object | Late conflicts and repeated speculative work |
| Audit evidence | Accounts, instructions, logs, compute, slot/status | Inputs and versions, effects, checkpoint | Ordered block index, attempts/conflicts, receipt, committed state |

All three preserve a deterministic canonical result. They differ in when dependency information appears and who bears mistakes. Solana makes the client and program expose accounts. Sui makes object topology part of application design. Aptos lets the runtime discover dependencies but may spend extra work on wrong speculation. A credible comparison replays the same contention distribution and reports committed results, retries or lock conflicts, latency percentiles, and state-commit cost.


## **Benchmarking Parallel Engines**

Peak TPS is especially misleading here. A benchmark should report:

- transaction mix and conflict rate;
- number and type of CPU cores;
- state size and storage medium;
- block size and latency;
- abort/re-execution rate;
- throughput under hot-state contention;
- time to compute and verify the state root.

The correct question is not how many ideal transfers fit in a second, but how performance degrades as real contracts share state.

## **Worked Example: Three Transactions, Two Cores**

Start with Alice holding ten tokens and Bob holding none. T1 transfers four from Alice to Bob. T2 reads Bob's balance and sends half to Carol. T3 updates an unrelated game object.

T1 and T3 can run concurrently because their read/write sets do not overlap. T2 cannot safely commit before T1 because it must observe Bob's balance of four. If T2 speculatively reads zero, validation detects that T1 wrote the same location earlier in canonical order. T2 aborts, reads version four, and retries. The result matches sequential execution while useful work from T3 ran in parallel.

Replace T3 with 10,000 swaps against one liquidity pool and the workload serializes because every swap touches the same reserves. More cores do not remove a contract-level dependency. Transfer-only benchmarks hide this behavior.

## **Designing Contracts for Concurrency**

An exchange can partition markets so ETH/USDC trades do not conflict with BTC/USDC. A game can store inventories as owned objects and batch global rankings. A rewards contract can accumulate per-user claims rather than increment one global counter.

These designs trade immediate global consistency for parallel work and need explicit reconciliation rules. The VM cannot invent independence that the application's state model does not contain.

## **Multi-Version State and Validation**

Optimistic parallel execution needs a versioned view of state. When transaction `T_i` writes key `k`, the executor records version `(i, value)`. A later transaction reads the highest version with index less than its own canonical index.

Workers may execute out of order, so a read can initially observe a speculative value. Validation checks whether the read version is still the correct predecessor after earlier transactions finish. If not, the transaction and dependent work are scheduled again.

Conceptually:

```text
execute(i):
    for each read(k):
        v = latest_version_before(k, i)
        record read_dependency(k, v.version)
    buffer writes as version i

validate(i):
    for each recorded dependency (k, j):
        require j == latest_committed_version_before(k, i)
    if any requirement fails:
        abort i and dependent transactions
```

A real implementation must coordinate incarnation numbers, speculative writes, memory reclamation, and dependency wake-ups without turning the scheduler itself into a bottleneck.

## **Static Scheduling With Access Lists**

Declared-access systems know conflicts before execution. Build a graph whose vertices are transactions and whose edges connect conflicting read/write sets. Transactions without edges between them can share a parallel wave.

The declaration needs enforcement. If a transaction touches an undeclared writable account, execution must fail rather than silently access it. Over-declaration is safe but reduces parallelism. Users or builders therefore have an incentive to provide narrow access lists.

Block construction can become concurrency-aware. A builder may choose a set of lower-fee independent transactions that uses all cores instead of a slightly higher-fee set contending on one account. This creates a new fee-market question: how should blockspace price scarce sequential state access versus abundant parallel capacity?

## **Deterministic State Commitment**

Even after execution, validators must compute one state root. If parallel workers update a shared Merkle tree with locks, root construction can serialize. Alternatives batch writes, sort them by key, and update independent subtrees concurrently before combining roots.

The state-commitment scheme affects witness generation and stateless validation. Verkle or sparse Merkle structures have different update, proof, and storage costs. VM throughput measured without root computation can overstate full-block performance.

## **Parallel Execution Failure Modes**

**Abort storms.** Many speculative transactions read values repeatedly invalidated by earlier writes. Adaptive scheduling can serialize hot keys after conflicts are detected.

**False conflicts.** Coarse account-level locks serialize transactions touching independent storage slots in one contract. Finer keys improve concurrency at the cost of tracking overhead.

**Nondeterministic host behavior.** Time, random numbers, floating-point differences, or iteration over unordered structures can produce different results. The VM must define deterministic inputs and arithmetic.

**Denial of service.** An attacker constructs transactions that trigger expensive speculative work and repeated aborts. Fees must cover wasted execution or the scheduler must bound speculation.

**State-root bottleneck.** Execution scales across cores but commitment remains sequential. End-to-end benchmarks reveal this gap.

## **Benchmark Matrix**

A useful benchmark varies both transaction complexity and conflict rate:

| Workload | Conflict pattern | What it measures |
|---|---|---|
| Independent transfers | Distinct accounts | Best-case scheduler scaling |
| Hot counter | One shared write | Worst-case serialization |
| DEX pairs | Partitioned markets | Application-level parallelism |
| NFT mint | Shared supply plus user writes | Burst contention |
| Mixed contracts | Read/write distribution from production | Realistic abort behavior |
| Adversarial conflicts | Deliberate invalidations | DoS resilience |

Report execution, validation, aborts, root computation, memory, and speedup against the same engine running one worker.

## **Scheduling Algorithms**

A scheduler can use several strategies.

**Greedy waves** place a transaction in the earliest wave whose writes do not conflict with earlier reads or writes. This works well when access lists are known and graph construction is cheap.

**Work stealing** gives each worker a queue and lets idle workers take ready transactions from others. It balances irregular execution times, but dependency bookkeeping must prevent a transaction from running before required predecessors.

**Speculative windowing** executes only a bounded range ahead of the validated frontier. A large window exposes more parallelism but wastes more work when early transactions invalidate later reads.

**Hot-key serialization** detects repeatedly conflicting keys and routes their transactions to an ordered lane while leaving unrelated work parallel.

The best scheduler depends on conflict distribution, transaction duration, and cost of abort. Benchmarks should include short and long transactions; counting transactions alone hides load imbalance.

## **Parallel Execution Memory, I/O, and NUMA Effects**

Adding execution workers can move the bottleneck from CPU instructions to memory bandwidth, cache coherence, or state-database I/O. A scheduler benchmark that reports core count without memory and storage behavior can mistake hardware saturation for protocol contention.

### Shared memory pressure

Workers read account metadata, contract code, storage values, version tables, and execution results. If their working sets exceed cache, they fetch from main memory. More workers then compete for finite memory bandwidth.

Suppose one worker executes 8,000 transactions per second and reads 40 kB of memory per transaction. Its read demand is:

```text
8,000 × 40 kB = 320 MB/s
```

Sixteen ideal workers would request 5.12 GB/s before writes, proofs, database overhead, and cache misses. On a machine sustaining 4 GB/s for this access pattern, speedup saturates before sixteen workers even without logical conflicts.

Measure cache misses, memory bandwidth, allocation, garbage collection, and lock wait. CPU utilization below 100 percent can coexist with a memory bottleneck.

### Non-uniform memory access

Multi-socket servers often have **non-uniform memory access (NUMA)**: a core reaches memory attached to its own socket faster than memory attached to another. A shared version table allocated on one socket can make remote workers slower.

Pin worker threads, place memory by access locality, partition state caches, and report socket topology. A result from one large NUMA server does not automatically predict performance on many smaller machines.

Scheduler correctness must not depend on thread pinning. NUMA tuning changes performance only; state roots and receipts remain identical.

### Database I/O

Cold state misses memory and reaches storage. Random reads can dominate latency even when nominal SSD bandwidth is high. Report IOPS, queue depth, read/write amplification, compaction, cache size, and state locality.

An optimistic executor may read state during speculative attempts that later abort. If 30 percent of attempts abort after cold reads, storage traffic can rise without committed throughput. Cache pollution can also slow the successful path.

Use an execution cache keyed by state version and invalidate it deterministically. A stale cache result must be detected before commit; cache correctness is consensus-critical even when cache policy is not.

### False sharing and locks

Two workers can update independent logical values stored on the same cache line. Hardware repeatedly transfers ownership of that line, causing **false sharing** even though the transactions do not conflict at protocol level.

Separate frequently written worker counters, use per-worker buffers, and merge them deterministically. Instrument lock hold time and contention by data structure. A global metrics lock can destroy scalability while the VM itself is parallel.

### State commitment bottleneck

Execution may run in parallel while Merkle-tree or other state commitment updates serialize near shared ancestors. Batch and deduplicate leaf updates, calculate independent subtrees concurrently, then combine roots in canonical order.

Do not report execution completion before commitment when validators need the new root to accept the block. Measure execution, validation, writeback, root calculation, and database flush separately.

### Oversubscription

More software workers than hardware threads can hide I/O latency, but excessive workers increase context switching and memory use. GPU or prover tasks on the same host may also compete for CPU, memory, and I/O.

Sweep worker counts rather than choosing the maximum. Record where throughput plateaus and tail latency or abort rate worsens. The best count can change with workload locality and state size.

### Persistence and crash recovery

Parallel workers produce intermediate results that must become durable atomically with the committed block boundary. A crash after some database writes but before root persistence must roll back or replay idempotently.

Use write batches, journals, generations, or copy-on-write structures. Recovery rechecks the last durable state root and must not expose partial receipts or logs to indexers.

### Hardware-aware benchmark matrix

Vary:

- cores, sockets, and simultaneous multithreading;
- memory channels, capacity, and NUMA placement;
- hot versus cold working set;
- storage medium, IOPS, queue depth, and compaction;
- worker count and scheduler policy;
- conflict distribution and abort depth;
- commitment scheme and flush policy;
- background snapshot, proof, and indexing load.

Report throughput and p99 block completion with hardware counters. A 10x VM microbenchmark speedup may become 2x end-to-end when state commitment and storage dominate.

### Operational assertions

Assert identical outputs across worker counts and placements, bounded memory under adversarial conflicts, recovery from crashes at every persistence boundary, no starvation under cold-state load, and stable catch-up while snapshots or compaction run.

Parallel blockchain execution scales when independent work survives both logical conflicts and physical resource limits. The scheduler, memory hierarchy, database, commitment tree, and persistence path form one executor.

## **Fee Markets for Contention**

A transaction can consume little CPU yet block many others by writing a popular key. Traditional gas meters its direct execution but not the opportunity cost of serializing a block.

A concurrency-aware market could charge for declared writable accounts, price hot keys dynamically, reserve parallel lanes, or let builders optimize total fee under a conflict graph. Each proposal affects predictability and manipulation. A user might over-declare reads to exclude competitors, while a builder might prefer independent low-fee transactions that fill idle cores.

The protocol must keep consensus deterministic. If scheduling affects inclusion, validators still verify one canonical ordered block; local thread decisions cannot change fees or results.

## **Parallel Smart-Contract Patterns**

### **Sharded Counters**

Replace one global counter with `k` buckets selected by account hash. Updates spread across buckets; reads sum them. This improves writes but makes reads more expensive and may provide only eventual snapshots.

### **Escrowed Objects**

Move an asset into an order-specific object before matching. Independent orders then touch independent state. Settlement combines only matched objects.

### **Commutative Accumulators**

Some updates can be combined regardless of order, such as adding independent reward deltas. The VM or contract batches deltas and applies a deterministic reduction.

### **Epoch Batching**

Collect actions during an epoch and compute one aggregate update. This reduces shared writes but adds latency and requires rules for ordering within the batch.

Patterns should preserve invariants under retries and partial execution. A parallel-friendly design that weakens accounting correctness is not an optimization.

## **Testing Determinism**

Run the same block many times with different worker counts, queue seeds, thread timing, and storage latency. Every run must produce identical receipts, logs, gas, and state root.

Differential tests compare the parallel engine with a simple sequential reference. Fuzzers generate transactions with nested calls, reverts, dynamic storage, and conflict patterns. Crash tests stop a worker after speculative writes and verify that recovery discards uncommitted versions.

Race detectors help implementation safety, but protocol determinism is a higher-level property. Two race-free executions can still disagree if iteration order or error precedence is unspecified.

## **End-to-End Speedup Limits**

Amdahl's law bounds speedup when part of execution remains serial. If fraction `p` is parallel and fraction `1-p` is serial, speedup on `N` workers is at most:

> `1 / ((1 - p) + p/N)`

If 20% of block processing is serial, infinite workers cannot exceed 5× speedup. Signature checks may parallelize while ordering, hot state, receipt assembly, and root commitment remain serial.

Measure the entire validation pipeline before projecting core scaling. Optimizing the parallel fraction can make the unchanged serial section the dominant cost.

## **Worked Scheduler Trace: Speculate, Validate, Commit**

Consider four transactions in canonical block order:

```text
T1: read A; write B = A + 1
T2: read C; write D = C + 1
T3: read B; write C = B + 1
T4: read E; write F = E + 1
```

`T1`, `T2`, and `T4` can begin from the same snapshot because their initial access sets do not conflict. `T3` reads `B`, which `T1` writes, and writes `C`, which `T2` read. If `T3` speculates before those dependencies are resolved, validation must abort and retry it against the state that includes earlier canonical transactions.

One possible trace is:

```text
worker 1: execute T1 at version 0 -> tentative write B
worker 2: execute T2 at version 0 -> tentative write D
worker 3: execute T3 at version 0 -> reads old B, tentative write C
worker 4: execute T4 at version 0 -> tentative write F

validate T1 -> success; commit version 1
validate T2 -> success; commit version 2
validate T3 -> stale read of B; abort tentative C
validate T4 -> success; commit when canonical prefix permits
retry T3 after T1/T2 -> read committed B; write C; commit version 3
commit T4 as version 4
```

Workers can finish out of order, but the visible result must match sequential execution of `T1,T2,T3,T4`. An engine may buffer `T4` even after successful validation until every earlier transaction has a committed result or deterministic abort.

### Multi-version state

Optimistic engines commonly tag values with transaction versions. A speculative read records both key and version observed. Validation asks whether an earlier canonical transaction wrote that key after the read's snapshot. If so, the read is stale.

```text
ReadRecord  = (transaction, key, observed_version)
WriteRecord = (transaction, key, new_value)
```

A retry must clear or supersede every tentative write and derived event from the aborted execution. Leaving one log, gas refund, message, or cache entry visible can create a state root that no sequential execution produces.

### Dynamic access

The scheduler may not know `T3` touches `C` until execution. Contract calls can compute keys from prior reads and invoke other contracts. Declared access lists improve planning, but the runtime must define behavior when a transaction touches an undeclared key: reject it, expand its lock set and retry, or execute it on a conservative path. Silently continuing breaks the scheduler's conflict assumptions.

### Deterministic failure

Transactions that revert still consume protocol-defined resources and may emit no durable writes. Parallel execution must reproduce the same success/revert decision and gas accounting as sequential execution. Sources of nondeterminism include host clocks, thread order, unordered map iteration, floating-point behavior, random number generators, external I/O, and races in native precompiles.

Consensus inputs such as block time or randomness must enter through canonical block fields. The VM should expose no process-local value that differs among validators.

### Scheduler invariants

For each committed block, test:

1. parallel and reference sequential execution produce identical state roots;
2. receipts, events, gas totals, and return data also match;
3. every committed read observes the newest earlier canonical write;
4. aborted attempts leave no durable state or externally visible event;
5. retries terminate or hit a deterministic block limit;
6. worker crashes and restarts do not change the committed prefix;
7. transaction outcome does not depend on worker count or thread interleaving.

Differential testing should run the same generated block with one worker, several worker counts, randomized scheduling seeds, and the sequential reference. Persist the seed and access trace on failure so the race can be reproduced.

## **Contention and Admission Control**

Retries consume real CPU, memory bandwidth, and cache capacity without increasing committed throughput. An attacker can construct transactions that appear independent early, then converge on one key late in execution. Even reverted attempts may exhaust the executor.

A production scheduler needs limits and pricing for speculative work. Options include capping attempts per transaction, charging for repeated execution under protocol rules, routing known-hot contracts to a serial lane, and using recent access history to avoid speculation likely to conflict. Any heuristic may affect performance but must not affect the canonical outcome.

Suppose 1,000 transactions each take 1 millisecond on the first attempt. With 16 workers and no conflicts, ideal execution time is about 62.5 milliseconds before serial overhead. If 40 percent abort once after completing their work, the executor performs 1,400 transaction-attempts, increasing ideal worker time to 87.5 milliseconds. If retries serialize on one hot key, the critical path can approach 400 milliseconds plus parallel work. Reporting only successful transactions hides this amplification.

Expose attempt count, aborted work, conflict keys, serial-lane depth, validation time, commit time, and state-database stalls. Capacity is the rate of committed canonical work under the target contention distribution, not the rate of speculative starts.

## **Conclusion**

Parallel execution turns transaction independence into throughput. Declared-access systems expose dependencies before execution; optimistic systems discover them during execution and retry conflicts. Both must preserve deterministic, sequentially valid results.

The limit is contention. A parallel VM is most effective when its application model avoids global hot state. The next chapter examines a different bottleneck: agreement among many validators.

## **References**

[^1]: Solana. "Transactions and Instructions." <https://solana.com/docs/core/transactions>.
[^2]: Sui. "The Sui Smart Contracts Platform." <https://docs.sui.io/paper/sui.pdf>.
[^3]: Gelashvili, Rati, et al. "Block-STM: Scaling Blockchain Execution by Turning Ordering Curse to a Performance Blessing." <https://arxiv.org/abs/2203.06871>.

[^4]: Solana Documentation. "Transaction processing pipeline." <https://solana.com/docs/core/transactions/transaction-pipeline>.
[^5]: Sui Documentation. "Life of a Transaction." <https://docs.sui.io/develop/transactions/transaction-lifecycle>.
[^6]: Sui Documentation. "Types of Object Ownership." <https://docs.sui.io/develop/objects/object-ownership/>.
[^7]: Aptos Documentation. "Execution." <https://aptos.dev/network/blockchain/execution>.
[^8]: Aptos Documentation. "Life of a Transaction." <https://aptos.dev/network/blockchain/blockchain-deep-dive>.
