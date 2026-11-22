"""Generate an offline, self-contained HTML report from actual Relate output."""
from html import escape
from explore import explore

def render_graph(report):
    """Draw a layered, script-free map of the queried fixture, not inferred edges."""
    root = report["root"]
    components = report["components"]
    edges = report["edges"]
    nodes = {root, *components}
    for edge in edges:
        nodes.update((edge["source"], edge["target"]))
    # Unknown depths remain separate rather than implying a reachable path.
    layers = {}
    for name in sorted(nodes):
        depth = 0 if name == root else components.get(name, {}).get("depth")
        layers.setdefault(depth, []).append(name)
    order = sorted(layers, key=lambda depth: (depth is None, depth or 0))
    width = max(640, max(map(len, layers.values())) * 190 + 110)
    height = len(order) * 116 + 28
    positions = {}
    for row, depth in enumerate(order):
        for column, name in enumerate(layers[depth]):
            positions[name] = (round(100 + (width - 100) * (column + .5) / len(layers[depth])), 30 + row * 116)
    def e(value):
        return escape(str(value), quote=True)
    colors = {"conflicting":"#fbe2df", "failed":"#fbe2df",
              "missing or unknown":"#fff0c5", "pass recorded":"#dcefe4"}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="graph-title graph-desc" '
             f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
             '<title id="graph-title">Queried dependency map</title>',
             '<desc id="graph-desc">Arrows point from a component to its declared dependency. Each node states its evidence status. The list below provides all edges as text.</desc>',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#49675f"/></marker></defs>']
    for row, depth in enumerate(order):
        label = "Unreached" if depth is None else f"Depth {depth}"
        parts.append(f'<text x="12" y="{row*116+60}" fill="#435d57" font-size="12">{label}</text>')
    for edge in edges:
        source, target = edge["source"], edge["target"]
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        if source == target:
            d = f"M{x1+80} {y1+27} C{x1+105} {y1-35} {x1-105} {y1-35} {x1-80} {y1+27}"
        elif y2 > y1:
            d = f"M{x1} {y1+56} C{x1} {y1+80} {x2} {y2-24} {x2} {y2}"
        elif y2 < y1:
            d = f"M{x1} {y1} C{x1} {y1-24} {x2} {y2+80} {x2} {y2+56}"
        else:
            direction = 1 if x2 > x1 else -1
            d = f"M{x1+80*direction} {y1+28} L{x2-80*direction} {y2+28}"
        parts.append(f'<path data-source="{e(source)}" data-target="{e(target)}" d="{d}" fill="none" stroke="#49675f" stroke-width="2" marker-end="url(#arrow)"/>')
    for name, (x, y) in positions.items():
        status = "Root (not assessed)" if name == root else components.get(name, {}).get("status", "not assessed")
        label = name if len(name) <= 19 else name[:18] + "…"
        parts.append(f'<g data-component="{e(name)}"><title>{e(name)}: {e(status)}</title>'
                     f'<rect x="{x-80}" y="{y}" width="160" height="56" rx="8" fill="{colors.get(status, "#e5ede6")}" stroke="#49675f"/>'
                     f'<text x="{x}" y="{y+23}" text-anchor="middle" font-size="14" font-weight="700" fill="#182c29">{e(label)}</text>'
                     f'<text x="{x}" y="{y+42}" text-anchor="middle" font-size="11" fill="#182c29">{e(status)}</text></g>')
    return "".join(parts) + "</svg>"


def render(report):
    def e(value):
        return escape(str(value), quote=True)
    components = report["components"]
    badges = {"conflicting":"conflict", "failed":"conflict",
              "missing or unknown":"missing", "pass recorded":"pass"}
    cards = []
    for name, component in sorted(components.items(), key=lambda item: (item[1]["depth"], item[0])):
        status = component["status"]
        evidence = "".join(
            f'<li><code>{e(item["id"])}</code> — {e(item["verdict"])}</li>'
            for item in component["evidence"]
        ) or "<li>No evidence recorded.</li>"
        cards.append(f'<details open><summary><strong>{e(name)}</strong> '
                     f'<span class="{badges.get(status, "missing")}">{e(status)}</span>'
                     f'<small>Depth {e(component["depth"])}</small></summary><ul>{evidence}</ul></details>')
    edges = "".join(f'<li><code>{e(edge["source"])}</code> → <code>{e(edge["target"])}</code></li>'
                    for edge in report["edges"])
    rows = "".join('<tr>' + "".join(f'<td>{e(row[key]) if row[key] is not None else "—"}</td>'
                                    for key in ("component", "depth", "evidence", "verdict")) + '</tr>'
                   for row in report["rows"])
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Trust Path Explorer | Local evidence report</title><style>
*{box-sizing:border-box}body{margin:0;background:#f0f4ee;color:#182c29;font:16px/1.55 system-ui,sans-serif}
main{max-width:1040px;margin:auto;padding:clamp(18px,5vw,64px)}
.eyebrow{font:700 12px monospace;letter-spacing:.15em;color:#315c53}h1{font-size:clamp(2.3rem,6vw,4.3rem);line-height:1.05;margin:.4em 0}
.note{border-left:5px solid #9e7026;padding:12px 18px;background:#fff9e9}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:16px}
section,details{background:white;border:1px solid #cbd8d0;padding:20px;border-radius:10px}
details{margin:12px 0}summary{cursor:pointer}summary small{display:block;color:#435d57}
summary span{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.85rem;margin-left:8px}
.conflict{background:#fbe2df;color:#87231a}.missing{background:#fff0c5;color:#765207}.pass{background:#dcefe4;color:#205e41}
 .graph-wrap{overflow:auto;max-width:100%;background:#f5f8f3;border:1px solid #dbe3dc;border-radius:8px;margin-bottom:18px}.graph-wrap svg{display:block;max-width:none}code{overflow-wrap:anywhere}li{margin:8px 0}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse}
td,th{border-bottom:1px solid #dbe3dc;text-align:left;padding:10px}th{background:#e5ede6}
:focus-visible{outline:3px solid #246d73;outline-offset:3px}footer{margin-top:28px;color:#405c56}
</style></head><body><main><p class="eyebrow">LOCAL GRAPH INVESTIGATION / SYNTHETIC FIXTURE</p><h1>Follow the trust path.</h1>
<p>Inspect dependencies and the evidence attached to them, including conflicting claims and gaps.</p>""" + f"""
<p class="note">{e(report["scope"])}. A recorded pass is not publisher authentication or release approval.</p>
<p>Engine: <strong>{e(report["engine"])} {e(report["version"])}</strong> · {len(components)} dependencies · {len(report["rows"])} evidence rows</p>
<section><h2>Dependency map</h2><p>Arrows indicate declared dependencies; nodes are grouped by minimum queried depth. Scroll the map horizontally if needed.</p><div class="graph-wrap" tabindex="0" aria-label="Scrollable dependency map">{render_graph(report)}</div><h3>Dependency links (text alternative)</h3><ul>{edges}</ul></section><div class="grid">
<section><h2>Evidence by component</h2>{''.join(cards)}</section></div>
<section><h2>Raw query results</h2><div class="table-wrap"><table><thead><tr><th>Component</th><th>Depth</th><th>Evidence</th><th>Verdict</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<footer>Generated from local Relate queries. No external assets, requests or scripts. Expand or collapse evidence records with the keyboard or pointer.</footer>
</main></body></html>"""

if __name__ == "__main__":
    print(render(explore()))
