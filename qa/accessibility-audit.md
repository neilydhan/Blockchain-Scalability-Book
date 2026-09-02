# Basic-Reader Accessibility Audit

This audit checks whether a reader who understands only that a blockchain records signed transactions can enter each chapter without an external glossary.

## Reading Standard

Each major concept should provide, before detailed formalism:

1. the problem it solves;
2. a plain definition;
3. the normal sequence of events;
4. the evidence or trust boundary;
5. a failure example;
6. notation and units used by calculations.

An analogy is useful when it preserves the security boundary. It should be followed by the exact mechanism so readers do not mistake the analogy for the protocol.

## Coverage Added

- Chapter 1: complete transaction, block, state, node, validator, contract, VM, hash, Merkle proof, consensus, finality, safety, and liveness foundation.
- Chapter 3: L1 versus L2 as changing the base versus moving work while retaining enforcement.
- Chapter 4: resource pipeline, gossip, world state, witnesses, sharding, committees, formulas, and units.
- Chapter 5: signed channel states, disputes, timelocks, HTLC routing, directional liquidity, sidechains, Plasma, and rollups.
- Chapter 6: rollup roles, optimistic and validity proof intuition, data, blobs, bridges, forced inclusion, and status boundaries.
- Chapter 7: monolithic and modular jobs, sovereign versus settled rollups, relayers, domain separation, and composed security.
- Chapter 8: validity versus availability, withholding, erasure coding, sampling probability, commitments, and namespaces.
- Chapter 9: read/write conflicts, scheduling, speculation, multi-version state, determinism, and hot state.
- Chapter 10: Byzantine and network models, Sybil resistance, Nakamoto and BFT consensus, quorum overlap, QCs, views, fork choice, and DAGs.
- Chapter 11: future-mechanism vocabulary and maturity labels.

## Acronym and Notation Review

High-frequency technical abbreviations are expanded or defined before deep use: L1, L2, DA, DAS, EVM, VM, HTLC, BFT, QC, DAG, PBS, MEV, SNARK, STARK, RPO, RTO, SLO, and DAC. Symbolic examples state what letters and units mean near the calculation. Transaction labels such as `T1` and roots such as `R0` are local identifiers rather than unexplained standards.

## Remaining Reader Supports

The glossary remains a reference, not a prerequisite. Review questions test mechanisms and assumptions rather than acronym recall. Deep implementation sections intentionally retain precise structures, threat models, and calculations after their introductory ramps.
