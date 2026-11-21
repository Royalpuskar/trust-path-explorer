# Trust Path Explorer

Trace software trust claims across dependency, evidence and reviewer relationships. Reveal missing evidence and conflicting paths rather than relying on a flat checklist.

## Competition and scope
Independent new project for [Relate by Neo4j](https://relate.devpost.com/rules). Started November 21, 2026. Proposed architecture: Relate-backed graph, deterministic multi-hop traversal and an interactive provenance map. The synthetic data will contain artifacts, components, attestations and evidence records; no real credentials, personal data or publisher-authentication claims.

## First graph fixture

`seed.cypher` defines a synthetic dependency graph; `queries/dependency-paths.cypher` traces bounded dependency paths and the attached evidence. `docs/expected-results.md` specifies the four expected rows. These are prepared queries, not yet executed against Relate.

## Implementation milestones
- [ ] Confirm official Relate installation/API and pin its version.
- [ ] Implement actual Relate graph ingestion and queries, with reproducible seed dataset.
- [ ] Compare graph findings against a flat baseline on a fixed fixture.
- [ ] Build a distinct graph exploration interface with accessible text alternatives.
- [ ] Validate disconnected paths, cycles, conflicting assertions and missing evidence.
- [ ] Add setup, tests, license, demo and AI-use statement.
- [ ] Add required GitHub topic `relate` through repository settings.

Status: graph fixture and Cypher query uploaded; Relate integration and deployment are not yet implemented. AI-assisted planning; significant AI use must be disclosed in submission. No contest registration or submission claimed.

Copyright 2026 Royalpuskar.
