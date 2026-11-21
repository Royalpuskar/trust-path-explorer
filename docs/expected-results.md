# Synthetic acceptance fixture

The seed graph is deterministic. The bounded dependency path query should return these four rows (order by depth, component, evidence):

| component | depth | evidence | verdict |
|---|---:|---|---|
| parser | 1 | test-parser | pass |
| utility | 1 | null | null |
| codec | 2 | review-codec | fail |
| codec | 2 | test-codec | pass |

The codec is an indirect dependency with contradictory evidence. Utility has no evidence. A release reviewer should investigate both; a pass record must not erase a fail record. This is an expected fixture, not observed output. The query has not yet been run on Relate; its CLI compatibility and exact result need verification.

See https://relatedb.ai/ and https://neo4j.com/blog/graph-database/announcing-the-relate-by-neo4j-hackathon-2026-build-ai-agents-on-an-embedded-graph-database/ for official engine documentation.
