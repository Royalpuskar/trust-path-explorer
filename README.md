# Trust Path Explorer

Trace software trust claims across dependency, evidence and reviewer relationships. Reveal missing evidence and conflicting paths rather than relying on a flat checklist.

## Competition and scope
Independent new project for [Relate by Neo4j](https://relate.devpost.com/rules). Started November 21, 2026. Proposed architecture: Relate-backed graph, deterministic multi-hop traversal and an interactive provenance map. The synthetic data will contain artifacts, components, attestations and evidence records; no real credentials, personal data or publisher-authentication claims.

## First graph fixture

`seed.cypher` defines a synthetic dependency graph; `queries/dependency-paths.cypher` traces bounded dependency paths and the attached evidence. `docs/expected-results.md` specifies the four expected rows. These are prepared queries, not yet executed against Relate.

## Run the database-backed candidate

Use Python 3.9+ and a virtual environment. Install `python -m pip install -r requirements.txt`, then run `python -m unittest -v test_explore` and `python explore.py`. This executes the actual Relate 1.1.0 embedded engine, not a mock. It compares the query output against the four-row acceptance fixture. The package version is pinned to the [published PyPI release](https://pypi.org/project/relate-db/1.1.0/). Fresh CI must confirm compatibility. No external services or credentials are used.

## Implementation milestones
- [x] Confirm official Relate installation/API and pin its version.
- [ ] Implement actual Relate graph ingestion and queries, with reproducible seed dataset.
- [ ] Compare graph findings against a flat baseline on a fixed fixture.
- [ ] Build a distinct graph exploration interface with accessible text alternatives.
- [ ] Validate disconnected paths, cycles, conflicting assertions and missing evidence.
- [ ] Add setup, tests, license, demo and AI-use statement.
- [ ] Add required GitHub topic `relate` through repository settings.

Status: database-backed runner and integration test prepared; actual execution and deployment remain pending. AI-assisted planning; significant AI use must be disclosed in submission. No contest registration or submission claimed.

Copyright 2026 Royalpuskar.
