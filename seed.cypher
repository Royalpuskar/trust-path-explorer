// Synthetic graph. Use a fresh local Relate database. No external targets.
MERGE (a:Component {id:'application'})
MERGE (b:Component {id:'parser'})
MERGE (c:Component {id:'codec'})
MERGE (d:Component {id:'utility'})
MERGE (a)-[:DEPENDS_ON]->(b)
MERGE (b)-[:DEPENDS_ON]->(c)
MERGE (a)-[:DEPENDS_ON]->(d)
MERGE (e:Evidence {id:'test-parser',verdict:'pass'})
MERGE (f:Evidence {id:'test-codec',verdict:'pass'})
MERGE (g:Evidence {id:'review-codec',verdict:'fail'})
MERGE (b)-[:HAS_EVIDENCE]->(e)
MERGE (c)-[:HAS_EVIDENCE]->(f)
MERGE (c)-[:HAS_EVIDENCE]->(g);
