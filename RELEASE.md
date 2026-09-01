# Edition Candidate 0.9.0

**Title:** *Blockchain Scalability Book*  
**Author:** Neil Han  
**Status:** Technical edition candidate  
**Canonical source:** `main` in https://github.com/neilydhan/Blockchain-Scalability-Book

This candidate covers the scalability problem from measurement and decentralization constraints through Layer 1 execution, payment channels, rollups, modular architecture, data availability, parallel execution, consensus, and research-to-production evaluation. It includes worked calculations, protocol traces, implementation checklists, exercises, instructor solutions, a glossary, and a practitioner handbook.

## Release Evidence

A distributable release must identify:

- semantic version and UTC build time;
- exact Git commit;
- manuscript word count;
- mdBook and browser versions;
- SHA-256 checksums for the HTML archive and PDF;
- the result of integrity, link, and visual checks;
- the date on which time-sensitive protocol claims were rechecked.

Run `scripts/package-release.sh` from a clean checkout of the intended commit. The script builds HTML and PDF, writes a machine-readable manifest, creates the HTML archive, and writes checksums. It refuses to package a dirty tree so the commit remains a sufficient source identifier.

## Candidate Limitations

Version 0.9.0 is suitable for technical review, course use, and publisher evaluation. Before a 1.0 release, complete a final copyedit and citation audit, inspect every PDF page at publication zoom, confirm rights and credits, and recheck claims about live protocol status and parameters against dated primary sources.

The repository's HTML output is canonical. The PDF is a reproducible print candidate; a printer or publisher may still require changes to trim size, font embedding, color profile, accessibility metadata, and cover production.
