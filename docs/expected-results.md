# Synthetic acceptance fixture

The seed graph is deterministic. The bounded dependency path query should return these four rows (order by depth, component, evidence):

| component | depth | evidence | verdict |
|---|---:|---|---|
| parser | 1 | test-parser | pass |
| utility | 1 | null | null |
| codec | 2 | review-codec | fail |
| codec | 2 | test-codec | pass |

The codec is an indirect dependency with contradictory evidence. Utility has no evidence. A release reviewer should investigate both; a pass record must not erase a fail record. These expected rows were observed on Relate 1.1.0 in [CI run 45004926519](https://github.com/Royalpuskar/trust-path-explorer/actions/runs/45004926519/job/137154262805), for head `1cedf3a308b160e79d56a05ac8ee6718f98fe72f`. New revisions require fresh execution.

See https://relatedb.ai/ and https://neo4j.com/blog/graph-database/announcing-the-relate-by-neo4j-hackathon-2026-build-ai-agents-on-an-embedded-graph-database/ for official engine documentation.
