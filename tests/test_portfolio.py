import json
import unittest
from pathlib import Path

from scripts.evaluate_sentiment import evaluate_predictions


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
            "visualizations/sentiment_validation.png",
        ]
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_private_source_text_is_not_committed(self):
        self.assertFalse((ROOT / "reports" / "구해줘_잡스_참가보고서.hwp").exists())
        for folder_name in ("raw", "processed"):
            folder = ROOT / "data" / folder_name
            if folder.exists():
                files = [path for path in folder.iterdir() if path.is_file() and path.name != ".gitkeep"]
                self.assertFalse(files, files)

    def test_sentiment_evaluation_metrics(self):
        metrics = evaluate_predictions(
            ["negative", "neutral", "positive", "negative"],
            ["negative", "positive", "positive", "negative"],
        )
        self.assertEqual(metrics["n"], 4)
        self.assertEqual(metrics["accuracy"], 0.75)
        self.assertEqual(metrics["confusion_matrix"], [[2, 0, 0], [0, 0, 1], [0, 0, 1]])


if __name__ == "__main__":
    unittest.main()
