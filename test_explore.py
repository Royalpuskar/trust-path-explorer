import unittest
from explore import explore

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

if __name__ == "__main__":
    unittest.main()
