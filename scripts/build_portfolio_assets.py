"""Build privacy-safe portfolio charts from reported aggregate evidence."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data" / "derived" / "reported_evidence.json"
OUTPUT = ROOT / "visualizations" / "key_evidence.png"


def build() -> Path:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    stress = evidence["survey_stress_distribution_pct"]
    participation = evidence["program_participation_pct"]
    popularity = evidence["popular_post_comparison"]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.patch.set_facecolor("#F8FAFC")

    stress_values = list(stress.values())
    axes[0].bar(list(stress.keys()), stress_values, color=["#CBD5E1", "#94A3B8", "#60A5FA", "#2563EB", "#1E3A8A"])
    axes[0].set(title="Job-search stress", xlabel="Level (1=low, 5=high)", ylabel="Share (%)")
    axes[0].text(0.98, 0.95, "85.4% at level 3+", transform=axes[0].transAxes, ha="right", va="top", color="#1D4ED8", weight="bold")

    participation_values = [participation["participated"], participation["not_participated"]]
    axes[1].bar(["Participated", "Not participated"], participation_values, color=["#93C5FD", "#F59E0B"])
    axes[1].set(title="Campus career programs", ylabel="Share (%)")
    axes[1].tick_params(axis="x", rotation=12)
    axes[1].text(1, participation_values[1] + 2, f"{participation_values[1]:.1f}%", ha="center", color="#B45309", weight="bold")

    negative_values = [popularity["general_mean_negative_intensity"], popularity["popular_top_10_pct_mean_negative_intensity"]]
    axes[2].bar(["General posts", "Popular top 10%"], negative_values, color=["#94A3B8", "#EF4444"])
    axes[2].set(title="Mean negative intensity", ylabel="Model score", ylim=(0, 0.58))
    axes[2].tick_params(axis="x", rotation=12)
    axes[2].text(0.5, 0.95, "t=2.202, p=.031\nassociation, not causation", transform=axes[2].transAxes, ha="center", va="top", fontsize=9)

    for axis in axes:
        axis.set_facecolor("#F8FAFC")
        axis.grid(axis="y", alpha=0.18)
    fig.suptitle("Reported evidence: survey access gap and community sentiment", fontsize=15, weight="bold", y=1.04)
    fig.text(0.5, -0.02, "Source: 2025 CAU Business & Economics academic festival presentation", ha="center", color="#475569", fontsize=9)
    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return OUTPUT


if __name__ == "__main__":
    print(build())
