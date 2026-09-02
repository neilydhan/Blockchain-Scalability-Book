# Preface

Blockchain scalability is often presented as a list of projects or a race for the largest throughput number. This book takes a different approach. It follows the work a system must perform, the assumptions that make the result trustworthy, and the recovery path when the fast path fails.

## Purpose of This Book

The goal is to connect research mechanisms with implementation and evaluation. Readers should finish able to trace a transaction from submission through execution, data publication, consensus, settlement, and finality; identify the first saturated resource; and explain what a user can do when an operator, prover, relayer, or validator set fails.

The book covers Layer 1 optimization and sharding, channels and Plasma, optimistic and validity rollups, modular architectures, data availability, parallel execution, and consensus scaling. It treats bridges, upgrades, observability, state growth, and mass recovery as part of scalability rather than operational details outside the design.

## Who This Book Is For

The primary readers are:

- developers implementing blockchain protocols, rollups, bridges, wallets, and applications;
- architects comparing monolithic, modular, sharded, and layered systems;
- researchers and students connecting papers to deployed mechanisms;
- operators and reviewers testing performance, safety, liveness, and recovery claims.

A reader should be comfortable with hashes, signatures, transactions, smart contracts, and basic distributed-systems vocabulary. The glossary defines the specialized terms used throughout the book.

## Origin

I developed this material from blockchain courses taught at Nanyang Technological University in Singapore, including CZ4153/CE4153 Blockchain Technology and SC6019 Blockchain Privacy & Scalability. The lectures covered data sharding, rollups, zero-knowledge proofs, modular systems, parallel execution, and consensus.

The book grew from a teaching need: students could find papers, documentation, and product descriptions, but few resources connected the full scaling stack and its failure modes. The figures and examples retain that classroom objective while adding implementation checklists, calculations, test plans, and primary references.

## How to Read the Worked Examples

The book uses worked examples to make protocol limits concrete. They are models with stated assumptions, not live fee quotes or performance promises.

Each calculation should be read in four steps:

1. **Name the quantity.** Throughput is work per second; latency is time per action; bandwidth is bytes or bits per second; probability is dimensionless.
2. **Write the assumptions.** Transaction mix, hardware, finality rule, compression, and failure conditions determine the result.
3. **Carry the units.** Dividing bytes by bytes per second produces seconds. Multiplying gas by price per gas produces a fee. Units expose many mistakes.
4. **Interpret the boundary.** The smallest resource ceiling is the current bottleneck; it is not a universal maximum after the workload changes.

### Common notation

Letters are local labels, defined near each example:

- `n` commonly means a total count, such as validators or encoded shares;
- `k` commonly means a required subset or number of shards;
- `f` commonly means faulty participants or a fraction;
- `λ` (lambda) means an arrival rate;
- `μ` (mu) means a service or processing rate;
- `p50`, `p95`, and `p99` are percentiles: 50, 95, or 99 percent of observations complete at or below that value;
- `R0` and `R1` label a prior and next state root;
- `T1`, `T2`, and so on label transactions in one trace.

A percentile describes a distribution, not an average. If p99 latency is ten seconds, 99 percent of measured actions finished within ten seconds and one percent took longer. The test duration and sample count still matter.

### Decimal and binary units

- `kB`, `MB`, and `GB` use powers of 1,000 in this book unless a source says otherwise.
- `KiB`, `MiB`, and `GiB` use powers of 1,024.
- Network rates written `Mbps` are megabits per second; divide by eight to obtain ideal megabytes per second before overhead.
- `ms` means milliseconds; 1,000 ms equals one second.
- Ethereum fees may use `gwei`, where one gwei is one billionth of an ETH.

### Probability language

A model probability is conditional on its assumptions. Independent samples must truly be hard for an attacker to predict or correlate. A one-in-a-million result per event may still occur often when a system runs billions of events. Always pair a probability with the event rate, exposure time, and consequence.

### Pseudocode and data structures

Code blocks such as `Packet { ... }` are often pseudocode. They expose fields that must be bound or checked but are not a copy-paste implementation. A production encoding must additionally define byte order, field lengths, canonical forms, versioning, bounds, and error behavior.

When a section becomes difficult, return to five questions: who acts, what data they use, what evidence the next party checks, when the result becomes final, and how failure is recovered.

## Reader Pathways

The book supports three routes.

### Basic blockchain background

Read the Preface, then Chapters 1-3 in order. Chapter 1 supplies the mental model and Chapter 2 teaches how to reason about trade-offs. In later chapters, read the opening intuition section before the detailed protocol traces. Use the core glossary and basic-knowledge warm-up whenever a term is unfamiliar.

A first reading can skip implementation data structures and return to them after answering:

- What problem does the mechanism solve?
- Who performs the work?
- What evidence does another party check?
- When is the result final?
- What happens when the normal service fails?

### Builder or operator

Read Chapters 1 and 3, then follow the mechanism you operate: Chapter 4 for L1/state, Chapters 5-6 for L2, Chapters 7-8 for modular/DA, Chapters 9-10 for execution/consensus, and Chapter 11 for emerging designs. Use the evaluation handbook, threat-model worksheets, and benchmark template alongside the chapter.

### Course or research study

Read Chapters 1-11 in sequence, complete the warm-up and chapter questions, then run the quantitative and fault-injection laboratories. Treat references as starting points for source verification, not substitutes for reproducing an argument.

### Signals in the text

- **Intuition sections** explain the mental model and vocabulary.
- **Worked examples** calculate a bounded scenario and state assumptions.
- **Protocol traces** show message and state order.
- **Failure matrices** separate safe behavior from recovery.
- **Production assertions** turn explanations into tests.
- **References** identify primary specifications and papers.

No route removes the need to state assumptions. The book becomes more formal gradually, but each deep section should remain connected to an actor, message, evidence check, deadline, and recovery path.

## How to Use This Book

Chapters 1-3 establish the measurement model and architecture vocabulary. Chapters 4-10 examine the main mechanisms. Chapter 11 looks at developing directions without treating research proposals as deployed facts.

The glossary supports reference use. Review questions test reasoning rather than recall. The practitioner handbook turns the book's methods into an evaluation procedure. Readers designing a system should work through the capstone and failure-injection exercises, not only the descriptive chapters.

Each chapter can be consulted independently, but later chapters assume the distinction among execution, settlement, consensus, and data availability introduced in Chapter 1.

## What This Book Measures

A performance claim is incomplete unless it names:

- the workload and state distribution;
- offered load, sustained throughput, and tail latency;
- the start and completion boundary;
- hardware, client version, network topology, and duration;
- validator, sequencer, prover, and data assumptions;
- behavior during faults and the cost of recovery.

The unit of analysis is the end-to-end user action. Faster execution does not help when data publication is saturated. A cheap normal transaction does not prove that mass exit is affordable. A validity proof establishes only the statement encoded by its program and public inputs.

## Conventions

**Layer 1 (L1)** is the base chain whose consensus defines canonical history. **Layer 2 (L2)** performs work outside the base chain while using it for settlement or enforcement. **Data availability (DA)** means the information needed to verify or reconstruct state was published and obtainable. **Finality** is always relative to a stated protocol and fault model.

Example numbers are illustrative unless a source and measurement context are given. Protocol rules and roadmaps change. Current claims should be checked against the linked specification or primary paper before they drive a production decision.

Code-like examples emphasize invariants and interfaces rather than one programming language. Terms such as *must* describe requirements for the design under discussion, not standards-language obligations unless a specification is cited.

## Contributions and Corrections

This is a living technical book. Corrections, reproducible measurements, protocol updates, implementation lessons, and original figures are welcome through the repository's [contribution process](../CONTRIBUTING.md).

A useful contribution states its source and scope. Performance updates should include workload and hardware. Security corrections should name the violated assumption or invariant. Figures should have editable source and clear rights. Time-sensitive product claims should be replaced with protocol mechanisms or pinned to a dated primary source.

## Acknowledgments

This book builds on the work of protocol researchers, client engineers, auditors, operators, educators, and students. Classroom questions and implementation failures are especially valuable: they reveal where a paper-level description is not enough for someone who must build, operate, or rely on the system.
