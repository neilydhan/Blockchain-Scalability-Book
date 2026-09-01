# Blockchain Scalability Book

The Blockchain Scalability Book explains how blockchains increase capacity while preserving verifiability, security, and credible recovery. It connects Layer 1 changes, channels, rollups, modular data availability, parallel execution, and consensus through end-to-end transaction and failure paths.

Start with our [Preface](chapters/00_preface.md) to learn more about the book's purpose and structure.

## Why This Book?
Scaling is a resource and systems problem, not a contest for the largest transactions-per-second number. This book gives readers the mechanisms, calculations, threat models, and evaluation methods needed to compare designs on equal terms.

## Chapters
The book is divided into chapters, each focusing on a specific aspect of scalability. The chapters form a complete first edition and remain open to corrections, new evidence, and technical improvements.

Status: Complete

1. **[Introduction to Blockchain Scalability](chapters/01_introduction.md)**: Foundation concepts and overview of blockchain scalability challenges.
2. **[The Blockchain Trilemma](chapters/02_blockchain_trilemma.md)**: Understanding the fundamental trade-offs in blockchain design.
3. **[Layer 1 vs Layer 2](chapters/03_layer_1_vs_layer_2.md)**: Comparing different approaches to blockchain scaling.
4. **[Layer 1 On-Chain Scalability](chapters/04_layer_1_on_chain_scalability.md)**: Exploring base layer scaling solutions.
5. **[Layer 2 Off-Chain Scalability](chapters/05_layer_2_off_chain_scalability.md)**: Understanding off-chain scaling approaches.
6. **[Rollups](chapters/06_rollups.md)**: Deep dive into rollup technology and implementations.
7. **[Modular vs Monolithic](chapters/07_modular_vs_monolithic.md)**: Exploring different blockchain architecture approaches.
8. **[Data Availability Scaling](chapters/08_data_availability_scaling.md)**: Solutions for blockchain data scaling.
9. **[Parallel Execution](chapters/09_parallel_execution.md)**: Understanding concurrent transaction processing.
10. **[Consensus Scaling](chapters/10_consensus_scaling.md)**: Scaling blockchain consensus mechanisms.
11. **[Future Directions](chapters/11_future_directions.md)**: Emerging trends and future scalability solutions.

The additional material includes a glossary, review questions with solution sketches, a practitioner evaluation handbook, figure credits, and reusable threat-model worksheets.

> Note: This is a living technical book. Protocols and roadmaps change, so contributions that correct, update, or deepen the material are welcome.


## How to Contribute
Corrections, reproducible measurements, primary-source updates, original diagrams, and implementation experience are welcome.

### Getting Started
1. **Read the Contribution Guidelines**: Check out our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on how to contribute.
2. **Choose a Chapter**: Look at the [Summary](SUMMARY.md) to find a chapter you're interested in.
3. **Fork the Repository**: Make your changes and submit a pull request.

## How to Run the Book
To read and develop this book locally, you'll need to install [mdBook](https://rust-lang.github.io/mdBook/), a command-line tool for creating books with Markdown.

### Installation
```bash
cargo install mdbook
```
### Clone this repository
```bash
git clone https://github.com/neilydhan/Blockchain-Scalability-Book.git
cd Blockchain-Scalability-Book
```
### Build and serve the book
```bash
./scripts/build-book.sh
mdbook serve --open
```
The first command creates a clean HTML build. The second starts a local server, opens the book, and watches for changes. To create a PDF candidate with Chrome or Chromium, run `./scripts/build-pdf.sh`. See the [publishing guide](PUBLISHING.md) for release and visual-review steps.

## Donations

Donations support maintenance and continued technical review of the book.

We use [GitHub Sponsors](https://github.com/sponsors/neilydhan), or you can send USDT or USDC to the following address directly:

- **USDT/USDC Address**: 0x8B12f280f997308B98c2a820279Faf61Aa54345c
- **Network**: Ethereum (ERC-20)



## License
This work is licensed under the [MIT License](LICENSE.md). By contributing to this book, you agree to abide by its terms.

## Stay Connected
Use repository issues and discussions for corrections, technical questions, and proposed improvements.