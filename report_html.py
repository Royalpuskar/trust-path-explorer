"""Generate an offline, self-contained HTML report from actual Relate output."""
from html import escape
from explore import explore

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
code{overflow-wrap:anywhere}li{margin:8px 0}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse}
td,th{border-bottom:1px solid #dbe3dc;text-align:left;padding:10px}th{background:#e5ede6}
:focus-visible{outline:3px solid #246d73;outline-offset:3px}footer{margin-top:28px;color:#405c56}
</style></head><body><main><p class="eyebrow">LOCAL GRAPH INVESTIGATION / SYNTHETIC FIXTURE</p><h1>Follow the trust path.</h1>
<p>Inspect dependencies and the evidence attached to them, including conflicting claims and gaps.</p>""" + f"""
<p class="note">{e(report["scope"])}. A recorded pass is not publisher authentication or release approval.</p>
<p>Engine: <strong>{e(report["engine"])} {e(report["version"])}</strong> · {len(components)} dependencies · {len(report["rows"])} evidence rows</p>
<div class="grid"><section><h2>Dependency links</h2><ul>{edges}</ul></section>
<section><h2>Evidence by component</h2>{''.join(cards)}</section></div>
<section><h2>Raw query results</h2><div class="table-wrap"><table><thead><tr><th>Component</th><th>Depth</th><th>Evidence</th><th>Verdict</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<footer>Generated from local Relate queries. No external assets, requests or scripts. Expand or collapse evidence records with the keyboard or pointer.</footer>
</main></body></html>"""

if __name__ == "__main__":
    print(render(explore()))
