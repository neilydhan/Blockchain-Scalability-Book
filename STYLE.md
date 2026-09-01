# Editorial and Technical Style

This style sheet keeps terminology, calculations, and claims consistent across editions.

## Audience and Voice

Write for engineers, researchers, architects, and advanced students. Define a mechanism before using its acronym. Prefer a concrete protocol trace or calculation to promotional adjectives. State what is guaranteed, under which assumptions, and what happens when an assumption fails.

Use present tense for protocol mechanics. Date claims about deployments, roadmaps, prices, participation, and performance. Distinguish a paper, prototype, testnet, limited production system, and permissionless production system.

## Canonical Terms

- **Layer 1 (L1)** and **Layer 2 (L2):** spell out at first use in a chapter, then use the abbreviation. Use a hyphen only as an adjective, as in "Layer-2 protocol".
- **rollup:** one word. Use **optimistic rollup** and **validity rollup** for the security mechanism. Use **ZK rollup** only when discussing the established product category; zero knowledge is not required for every validity proof.
- **data availability (DA):** the ability to obtain block data needed to verify or reconstruct state. Do not use it to mean permanent archival storage.
- **finality:** qualify it as probabilistic, economic, BFT, settlement, or application finality. A sequencer confirmation is not settlement finality.
- **state root:** a commitment to state. Do not call it the state itself.
- **light client:** software that verifies a reduced proof of consensus or state without executing and storing everything. A trusted API consumer is not automatically a light client.
- **bridge:** name the verification model: multisignature, optimistic, light-client, validity-proof, or canonical rollup bridge. Avoid "trustless."
- **throughput:** report the unit and workload. Prefer transactions per second only when transaction composition is specified; otherwise report gas, bytes, or resource units per second.
- **latency:** identify start and end events and percentile. Distinguish inclusion, confirmation, finality, proof, and withdrawal latency.
- **node, validator, block producer, sequencer, prover, relayer:** use the role that actually performs the action. They are not interchangeable.
- **Merkle proof / Merkle tree:** capitalize the proper name. Use **multiproof** as one word.
- **zero-knowledge proof:** hyphenate as an adjective. Use **zero knowledge** as a noun phrase.
- **on-chain / off-chain / cross-chain:** hyphenate as adjectives and adverbs for consistency.

## Numbers and Units

Use SI decimal units for network rates and payloads unless a source explicitly reports binary units. Write `MB`, `kB/s`, `ms`, `gwei`, and `gas` consistently. Show formulas with units so dimensional mistakes are visible. State whether a fee is an assumed example or a live parameter.

Separate capacity, observed demand, and benchmark throughput. For benchmarks, report hardware, software version, dataset or workload, duration, warm-up, concurrency, latency percentiles, failures, finality rule, and security configuration.

## Security Claims

Replace "secure" with the property meant: safety, liveness, censorship resistance, data availability, soundness, or accountable safety. Name the adversary threshold and network assumption. Avoid "trustless"; enumerate trusted code, committees, governance, timing assumptions, and data sources.

A mitigation is not a proof. Rate limits and pause keys bound loss but add governance assumptions. State the safe failure mode and recovery authority.

## Code, Messages, and Figures

Pseudocode should expose types, ordering, domain separation, bounds, and error behavior when those details affect safety. Use fenced `text` blocks for data structures that are illustrative rather than executable.

Every figure needs a numbered caption, meaningful alternative text, and an editable source. Every table needs headers that make sense without relying on the surrounding paragraph.

## Citations

Prefer specifications, standards, protocol repositories, peer-reviewed papers, and official postmortems. A reference supports the sentence immediately before it; do not attach one citation to a paragraph containing several unrelated claims. Include access or status dates for mutable web documentation at release time.

## Editorial Review

Search every chapter for undefined acronyms, absolute claims, unqualified finality, throughput without workload, and words such as "simply," "obviously," or "just" that hide complexity. Read calculations independently, verify units, and reproduce a sample from source data. Run the repository checks, then inspect the rendered output rather than treating a clean build as visual proof.
