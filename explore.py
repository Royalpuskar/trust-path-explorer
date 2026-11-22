"""Execute the synthetic fixture inside actual Relate; no external targets."""
import json
from pathlib import Path
from importlib.metadata import version

ROOT = Path(__file__).resolve().parent

def explore():
    import relate
    conn = relate.connect(":memory:")
    try:
        conn.execute((ROOT / "seed.cypher").read_text()).consume()
        rows = list(conn.execute((ROOT / "queries/dependency-paths.cypher").read_text()).data())
        edges = list(conn.execute((ROOT / "queries/dependency-edges.cypher").read_text()).data())
    finally:
        conn.close()
    by_component = {}
    for row in rows:
        component = by_component.setdefault(row["component"], {"depth": row["depth"], "evidence": []})
        component["depth"] = min(component["depth"], row["depth"])
        if row["evidence"] is not None:
            component["evidence"].append({"id": row["evidence"], "verdict": row["verdict"]})
    for component in by_component.values():
        verdicts = {e["verdict"] for e in component["evidence"]}
        component["status"] = ("conflicting" if {"pass","fail"} <= verdicts else
                               "failed" if "fail" in verdicts else
                               "pass recorded" if verdicts == {"pass"} else "missing or unknown")
    return {"engine": "relate-db", "version": version("relate-db"), "rows": rows,
            "root": "application", "components": by_component, "edges": edges, "scope": "Synthetic data; no authenticated evidence"}

if __name__ == "__main__":
    print(json.dumps(explore(), indent=2))
