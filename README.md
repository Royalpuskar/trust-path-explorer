# Trust Path Explorer

Trace software trust claims across dependency, evidence and reviewer relationships. Reveal missing evidence and conflicting paths rather than relying on a flat checklist.

## Competition and scope
Independent new project for [Relate by Neo4j](https://relate.devpost.com/rules). Started November 21, 2026. Proposed architecture: Relate-backed graph, deterministic multi-hop traversal and an interactive provenance map. The synthetic data will contain artifacts, components, attestations and evidence records; no real credentials, personal data or publisher-authentication claims.

## First graph fixture

`seed.cypher` defines a synthetic dependency graph; `queries/dependency-paths.cypher` traces bounded dependency paths and the attached evidence. `docs/expected-results.md` specifies the four expected rows. The four-row fixture was verified on the real Relate 1.1.0 engine in [CI run 45004926519](https://github.com/Royalpuskar/trust-path-explorer/actions/runs/45004926519/job/137154262805) at revision `1cedf3a308b160e79d56a05ac8ee6718f98fe72f`. Later revisions require fresh tests.

## Run the database-backed candidate

Use Python 3.9+ and a virtual environment. Install `python -m pip install -r requirements.txt`, then run `python -m unittest -v test_explore` and `python explore.py`. This executes the actual Relate 1.1.0 embedded engine, not a mock. It compares the query output against the four-row acceptance fixture. The package version is pinned to the [published PyPI release](https://pypi.org/project/relate-db/1.1.0/). Fresh CI must confirm compatibility. No external services or credentials are used.

## Generate the local demonstration

After installing the pinned requirements, run `python report_html.py > trust-report.html` and open the generated file in a browser. The report is generated on demand from two real queries: evidence traversal and dependency edges. A script-free layered SVG renders the queried dependency edges and minimum depths with explicit status labels. Its adjacent textual edge list and keyboard-accessible evidence panels expose the same information without requiring visual interpretation. A raw result table preserves all evidence rows. No remote resources, JavaScript or live target data. The preceding report revision passed both integration tests ([CI logs](https://github.com/Royalpuskar/trust-path-explorer/actions/runs/45005350966/job/137155631628)). A new SVG regression test checks edge parity, status labels and XML escaping. The new revision requires fresh CI and visual validation.

## Why graph traversal matters

A direct-only inventory derived from the queried root edges contains parser and utility. The bounded traversal additionally finds codec, whose pass and fail evidence conflicts. The HTML report now makes this difference explicit. This is a synthetic fixture comparison, not a claim of exhaustive real-world detection. The additional baseline test requires fresh CI.

## Alternate graph fixture

The second synthetic graph (`fixtures/alternate.cypher`) adds a cycle, two distinct paths to codec and a disconnected component pair. It preserves every raw query row but deduplicates identical evidence ID/verdict pairs in summaries, so repeated paths do not multiply the same evidence. Conflicting verdicts stay visible. Run `python -c "from explore import explore; from report_html import render; print(render(explore('alternate')))" > alternate-report.html` to generate its report. The new integration test verifies minimum depth, repeated-path evidence, conflicts and unreachable components against the installed Relate engine; fresh CI is required.

## Implementation milestones
- [x] Confirm official Relate installation/API and pin its version.
- [x] Implement actual Relate graph ingestion and queries, with reproducible seed dataset.
- [x] Compare graph findings against a flat baseline on a fixed fixture (CI at 7285f5f).
- [ ] Build a distinct graph exploration interface with accessible text alternatives.
- [ ] Validate disconnected paths, cycles, conflicting assertions and missing evidence.
- [ ] Add setup, tests, license, demo and AI-use statement.
- [ ] Add required GitHub topic `relate` through repository settings.

Status: four integration tests passed at revision `7285f5f` ([CI](https://github.com/Royalpuskar/trust-path-explorer/actions/runs/45022899521)); alternate fixture and a fifth integration test added. Fresh CI, browser visual validation and deployment remain pending. AI-assisted planning; significant AI use must be disclosed in submission. No contest registration or submission claimed.

Copyright 2026 Royalpuskar.
