MATCH p=(root:Component {id:'application'})-[:DEPENDS_ON*1..5]->(component:Component)
OPTIONAL MATCH (component)-[:HAS_EVIDENCE]->(e:Evidence)
RETURN component.id AS component, length(p) AS depth, e.id AS evidence, e.verdict AS verdict
ORDER BY depth, component, evidence;
