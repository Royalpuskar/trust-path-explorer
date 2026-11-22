import unittest
from xml.etree import ElementTree as ET
from explore import explore
from report_html import render, render_graph

class GraphFixture(unittest.TestCase):
    def test_dependency_graph_and_conflicting_evidence(self):
        report = explore()
        self.assertEqual(report["version"], "1.1.0")
        self.assertEqual([(r["component"],r["depth"],r["evidence"],r["verdict"]) for r in report["rows"]],
            [("parser",1,"test-parser","pass"),("utility",1,None,None),
             ("codec",2,"review-codec","fail"),("codec",2,"test-codec","pass")])
        self.assertEqual(report["components"]["codec"]["status"], "conflicting")
        self.assertEqual(report["components"]["utility"]["status"], "missing or unknown")
        self.assertEqual(report["components"]["parser"]["status"], "pass recorded")

    def test_queried_edges_and_html_report(self):
        report = explore()
        self.assertEqual(report["edges"], [
            {"source":"application","target":"parser"},
            {"source":"application","target":"utility"},
            {"source":"parser","target":"codec"}])
        html = render(report)
        for value in ("relate-db 1.1.0", "review-codec", "test-codec", "conflicting",
                      "missing or unknown", "Raw query results"):
            self.assertIn(value, html)
        self.assertIn("<code>parser</code> → <code>codec</code>", html)
        self.assertIn("No evidence recorded.", html)
        self.assertNotIn("<script", html)
        report["scope"] = '<script>alert("test")</script>'
        self.assertIn("&lt;script&gt;", render(report))

    def test_svg_map_matches_queried_edges_and_statuses(self):
        report = explore()
        svg = ET.fromstring(render_graph(report))
        ns = {"s":"http://www.w3.org/2000/svg"}
        arrows = [(p.attrib["data-source"], p.attrib["data-target"])
                  for p in svg.findall(".//s:path[@data-source]", ns)]
        self.assertEqual(arrows, [(edge["source"],edge["target"]) for edge in report["edges"]])
        nodes = {g.attrib["data-component"]:g.find("s:title",ns).text
                 for g in svg.findall("s:g", ns)}
        self.assertEqual(set(nodes), {"application","parser","codec","utility"})
        self.assertEqual(nodes["codec"], "codec: conflicting")
        self.assertEqual(nodes["utility"], "utility: missing or unknown")
        self.assertEqual(nodes["application"], "application: Root (not assessed)")
        self.assertEqual(svg.attrib["role"], "img")
        self.assertIn(render_graph(report), render(report))
        injected = 'x"><script>alert(1)</script>'
        report["edges"].append({"source":"application","target":injected})
        parsed = ET.fromstring(render_graph(report))
        self.assertIn(injected, [g.attrib["data-component"] for g in parsed.findall("s:g",ns)])
        self.assertFalse(parsed.findall(".//s:script",ns))

if __name__ == "__main__":
    unittest.main()
