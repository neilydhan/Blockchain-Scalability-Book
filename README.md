# Mastering Blockchain Scalability

**A mechanism-first guide to blockchain capacity, security, trust, and recovery.**

Blockchain scalability is a resource and systems problem, not a contest for the largest transactions-per-second number. This book follows transactions and failures end to end across Layer 1, Layer 2, rollups, modular data availability, parallel execution, and consensus. It gives master's students and practitioners worked calculations, explicit security assumptions, threat-model worksheets, benchmark methods, graduate-level exercises, and solution sketches.

[**Read online**](https://neilydhan.github.io/Blockchain-Scalability-Book/) · [**Download PDF**](https://github.com/neilydhan/Blockchain-Scalability-Book/releases/latest) · [**Cite**](CITATION.cff) · [**Teach this book**](ACADEMIC.md) · [**Contribute**](CONTRIBUTING.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22257267.svg)](https://doi.org/10.5281/zenodo.22257267)

## Who This Book Is For

This is a technical systems book for:

- master's students in blockchain, distributed systems, security, and computer architecture;
- lecturers building a graduate blockchain or distributed-systems course;
- protocol engineers working on execution, rollups, data availability, bridges, and consensus;
- founders, architects, researchers, analysts, and developers who need to evaluate scalability claims.

It is not a beginner's introduction to cryptocurrency trading or Web3 applications. Readers should be comfortable with basic data structures, networks, and the idea that a blockchain records signed transactions. Chapter 1 supplies the blockchain foundations needed by readers arriving from adjacent engineering fields.

## Choose a Reading Path

- **Understand the field:** start with the [Preface](chapters/00_preface.md), then Chapters 1-3.
- **Evaluate rollups and modular systems:** read Chapters 5-8, then use the [Threat-Model Worksheets](chapters/16_threat_model_worksheets.md).
- **Study execution and consensus:** read Chapters 9-10 and the worked calculations in each chapter.
- **Compare a protocol or vendor:** use the [Practitioner Evaluation Handbook](chapters/14_evaluation_handbook.md) and [Benchmark Reporting Template](chapters/17_benchmark_reporting_template.md).
- **Build a course:** use the [Instructor and Course Adoption Guide](ACADEMIC.md) with the exercises and solution sketches.

## Current Edition

The current public edition is **v1.1.1**. Its release contains a 420-page PDF, browsable HTML archive, build manifest, and SHA-256 checksums.

- [Latest release and downloads](https://github.com/neilydhan/Blockchain-Scalability-Book/releases/latest)
- [Version history](https://github.com/neilydhan/Blockchain-Scalability-Book/releases)
- [Source for v1.1.1](https://github.com/neilydhan/Blockchain-Scalability-Book/tree/v1.1.1)
- [Preface and Chapter 1 sample](SAMPLE.md)

Use the latest-release link when you want the newest edition. Use a version-specific release when citing or reproducing a result.

## What the Book Covers

1. [Introduction to Blockchain Scalability](chapters/01_introduction.md)
2. [The Blockchain Trilemma](chapters/02_blockchain_trilemma.md)
3. [Layer 1 vs Layer 2](chapters/03_layer_1_vs_layer_2.md)
4. [Layer 1 On-Chain Scalability](chapters/04_layer_1_on_chain_scalability.md)
5. [Layer 2 Off-Chain Scalability](chapters/05_layer_2_off_chain_scalability.md)
6. [Rollups](chapters/06_rollups.md)
7. [Modular vs Monolithic](chapters/07_modular_vs_monolithic.md)
8. [Data Availability Scaling](chapters/08_data_availability_scaling.md)
9. [Parallel Execution](chapters/09_parallel_execution.md)
10. [Consensus Scaling](chapters/10_consensus_scaling.md)
11. [Future Directions](chapters/11_future_directions.md)

The additional material includes a glossary, review questions with solution sketches, a practitioner evaluation handbook, figure credits, reusable threat-model worksheets, and a benchmark-reporting template.

## Cite the Book

Until a DOI is assigned, cite the versioned GitHub release:

> Han, Neil. *Mastering Blockchain Scalability*. Version 1.1.1, 2026. GitHub. https://github.com/neilydhan/Blockchain-Scalability-Book/releases/tag/v1.1.1

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff). Cite a version-specific release when exact page numbers or claims matter.

## Build the Book

Install [mdBook](https://rust-lang.github.io/mdBook/) 0.4.52 or a tested compatible release, then run:

```bash
./scripts/build-book.sh
```

The command checks the source, builds the HTML edition into `book/`, and adds book metadata, canonical links, a sitemap, and `robots.txt`. To build the PDF candidate or EPUB:

```bash
./scripts/build-pdf.sh
./scripts/build-epub.sh
```

See the [Publishing Guide](PUBLISHING.md) for the release and visual-review gates.

## Contribute

Corrections, reproducible measurements, primary-source updates, original diagrams, and implementation experience are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md), choose a chapter from [`SUMMARY.md`](SUMMARY.md), and submit a pull request. Use [GitHub Issues](https://github.com/neilydhan/Blockchain-Scalability-Book/issues) for a specific correction or proposal.

This is a living technical book. Protocols and roadmaps change, so every claim about a deployed system should carry a source and a date.

## Support Maintenance

GitHub Sponsors and the donation details below support technical review and continued maintenance.

- [Sponsor Neil Han on GitHub](https://github.com/sponsors/neilydhan)
- USDT/USDC: `0x8B12f280f997308B98c2a820279Faf61Aa54345c` on Ethereum (ERC-20)

## License

Book prose, exercises, tables, and original figures are licensed under [CC BY-SA 4.0](LICENSE.md). Build software under `scripts/`, `theme/`, and `.github/` is licensed under the [MIT License](LICENSE.md). Third-party quotations, trademarks, and credited materials retain their respective rights.
