import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PortfolioEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads(
            (ROOT / "data" / "derived" / "reported_evidence.json").read_text(encoding="utf-8")
        )

    def test_reported_scope(self):
        self.assertEqual(self.evidence["scope"]["posts"], 7255)
        self.assertEqual(self.evidence["scope"]["survey_total_respondents"], 75)

    def test_stress_distribution_reconciles(self):
        distribution = self.evidence["survey_stress_distribution_pct"]
        self.assertAlmostEqual(sum(distribution.values()), 100.0, places=1)
        self.assertAlmostEqual(sum(distribution[key] for key in ("3", "4", "5")), 85.4, places=1)

    def test_program_participation_reconciles(self):
        self.assertAlmostEqual(sum(self.evidence["program_participation_pct"].values()), 100.0, places=1)

    def test_final_topic_count(self):
        self.assertEqual(len(self.evidence["final_lda_topics"]), 4)

    def test_public_artifacts_exist(self):
        expected = [
            "reports/구해줘_잡스.pdf",
            "reports/원페이지_보고서.pdf",
            "reports/부정_토픽_모델링_시각화.html",
            "notebooks/portfolio_summary.ipynb",
            "visualizations/key_evidence.png",
        ]
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_private_source_text_is_not_committed(self):
        for folder_name in ("raw", "processed"):
            folder = ROOT / "data" / folder_name
            if folder.exists():
                files = [path for path in folder.iterdir() if path.is_file() and path.name != ".gitkeep"]
                self.assertFalse(files, files)


if __name__ == "__main__":
    unittest.main()
