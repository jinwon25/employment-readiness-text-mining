"""Evaluate saved sentiment predictions with portfolio reporting metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score


DEFAULT_LABELS = ("negative", "neutral", "positive")


def evaluate_predictions(
    truth: Sequence[str], predictions: Sequence[str], labels: Sequence[str] = DEFAULT_LABELS
) -> dict:
    """Return deterministic classification metrics for a fixed label order."""
    truth = list(truth)
    predictions = list(predictions)
    labels = list(labels)
    if not truth:
        raise ValueError("Evaluation data is empty")
    if len(truth) != len(predictions):
        raise ValueError("Actual and predicted labels must have the same length")

    unexpected = (set(truth) | set(predictions)) - set(labels)
    if unexpected:
        raise ValueError(f"Unexpected labels: {sorted(unexpected)}")

    report = classification_report(
        truth,
        predictions,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )
    return {
        "n": len(truth),
        "labels": labels,
        "accuracy": round(float(accuracy_score(truth, predictions)), 6),
        "macro_f1": round(float(f1_score(truth, predictions, labels=labels, average="macro", zero_division=0)), 6),
        "per_class": {
            label: {metric: round(float(report[label][metric]), 6) for metric in ("precision", "recall", "f1-score", "support")}
            for label in labels
        },
        "confusion_matrix": confusion_matrix(truth, predictions, labels=labels).tolist(),
    }


def save_confusion_matrix(metrics: dict, output: Path) -> None:
    labels = metrics["labels"]
    matrix = metrics["confusion_matrix"]
    figure, axis = plt.subplots(figsize=(6.5, 5.5))
    image = axis.imshow(matrix, cmap="Blues")
    figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    axis.set(
        title=f"Sentiment confusion matrix\nAccuracy {metrics['accuracy']:.3f} · Macro-F1 {metrics['macro_f1']:.3f}",
        xlabel="Predicted label",
        ylabel="Actual label",
        xticks=range(len(labels)),
        yticks=range(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
    )
    threshold = max(max(row) for row in matrix) / 2
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            axis.text(
                column_index,
                row_index,
                value,
                ha="center",
                va="center",
                color="white" if value > threshold else "#0F172A",
            )
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate Accuracy, Macro-F1, class metrics and a confusion matrix from saved predictions."
    )
    parser.add_argument("input", type=Path, help="CSV containing actual and predicted labels")
    parser.add_argument("--actual-column", default="label")
    parser.add_argument("--prediction-column", default="predicted_label")
    parser.add_argument("--labels", default=",".join(DEFAULT_LABELS), help="Comma-separated label order")
    parser.add_argument("--output-json", type=Path, default=Path("reports/sentiment_metrics.json"))
    parser.add_argument("--output-figure", type=Path, default=Path("visualizations/sentiment_confusion_matrix.png"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = pd.read_csv(args.input)
    required = {args.actual_column, args.prediction_column}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    metrics = evaluate_predictions(frame[args.actual_column], frame[args.prediction_column], labels)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_confusion_matrix(metrics, args.output_figure)
    print(json.dumps({"metrics": str(args.output_json), "figure": str(args.output_figure)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
