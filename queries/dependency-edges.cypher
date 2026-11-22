MATCH (source:Component)-[:DEPENDS_ON]->(target:Component)
RETURN source.id AS source, target.id AS target
ORDER BY source, target;
