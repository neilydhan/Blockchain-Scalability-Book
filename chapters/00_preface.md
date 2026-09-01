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
