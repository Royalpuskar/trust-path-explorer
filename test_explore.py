import unittest
from explore import explore
from report_html import render

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

if __name__ == "__main__":
    unittest.main()
