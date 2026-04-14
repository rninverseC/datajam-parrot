#!/usr/bin/env python3
"""Redo the finance-growth boxplot with more datapoints.

This version uses all business/financial occupations in the processed dataset
and creates two groups with a median split on task_balance:

- more judgment-heavy
- more process-heavy

The plot keeps the boxplot for summary but overlays every point so the user can
see the full sample size directly.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DEFAULT_CSV = Path("/tmp/datajam26-parrot/data/processed/business_financial_ml_dataset.csv")

BG = "#F6F0E7"
INK = "#1F2933"
JUDGMENT_COLOR = "#C7A663"
PROCESS_COLOR = "#4B5563"
GRID = "#D8C3A5"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a larger boxplot for projected growth.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to business_financial_ml_dataset.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where the plot and summary files should be written.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used for point jitter in the plot.",
    )
    return parser.parse_args()


def build_groups(data: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    median_task_balance = float(data["task_balance"].median())
    grouped = data.copy()
    grouped["boxplot_group"] = np.where(
        grouped["task_balance"] >= median_task_balance,
        "more judgment-heavy",
        "more process-heavy",
    )
    return grouped, median_task_balance


def make_plot(data: pd.DataFrame, output_path: Path, seed: int) -> None:
    rng = np.random.default_rng(seed)
    order = ["more judgment-heavy", "more process-heavy"]
    colors = [JUDGMENT_COLOR, PROCESS_COLOR]

    fig, ax = plt.subplots(figsize=(10, 6.3), facecolor=BG)
    ax.set_facecolor(BG)

    groups = [
        data.loc[data["boxplot_group"] == label, "projected_growth_pct"].to_numpy(dtype=float)
        for label in order
    ]
    box = ax.boxplot(groups, tick_labels=order, patch_artist=True, widths=0.5)

    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
        patch.set_edgecolor(INK)

    for median in box["medians"]:
        median.set_color(INK)
        median.set_linewidth(2)

    for i, (label, color) in enumerate(zip(order, colors), start=1):
        subset = data.loc[data["boxplot_group"] == label]
        x = i + rng.uniform(-0.11, 0.11, size=len(subset))
        y = subset["projected_growth_pct"].to_numpy(dtype=float)
        ax.scatter(
            x,
            y,
            color=color,
            edgecolor=INK,
            linewidth=0.7,
            s=54,
            alpha=0.9,
            zorder=3,
        )

    ax.set_title(
        "Projected Growth Across Business/Financial Occupations\n"
        "Grouped by Task Balance (All 35 Occupations)",
        color=INK,
        weight="bold",
    )
    ax.set_ylabel("Projected Growth % (2024-2034)", color=INK)
    ax.grid(axis="y", color=GRID, alpha=0.65)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(INK)

    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_summary(data: pd.DataFrame, output_path: Path, median_task_balance: float) -> None:
    summary = (
        data.groupby("boxplot_group")["projected_growth_pct"]
        .agg(["count", "mean", "median", "min", "max"])
        .reindex(["more judgment-heavy", "more process-heavy"])
    )

    lines = [
        "Larger Boxplot Summary",
        f"Source CSV: {args.csv}",
        "Grouping rule: median split on task_balance",
        f"Median task_balance threshold: {median_task_balance:.3f}",
        "",
    ]

    for label, row in summary.iterrows():
        lines.extend(
            [
                f"{label}:",
                f"  count = {int(row['count'])}",
                f"  mean projected growth = {row['mean']:.3f}",
                f"  median projected growth = {row['median']:.3f}",
                f"  min = {row['min']:.3f}",
                f"  max = {row['max']:.3f}",
                "",
            ]
        )

    output_path.write_text("\n".join(lines))


if __name__ == "__main__":
    args = parse_args()
    if not args.csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {args.csv}")

    data = pd.read_csv(args.csv)
    required = {"projected_growth_pct", "task_balance", "occupation_title"}
    missing = required.difference(data.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CSV is missing required columns: {missing_text}")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    grouped, threshold = build_groups(data)
    plot_path = output_dir / "business_finance_boxplot_35.png"
    summary_path = output_dir / "business_finance_boxplot_35_summary.txt"
    grouped_csv_path = output_dir / "business_finance_boxplot_35_groups.csv"

    make_plot(grouped, plot_path, args.seed)
    write_summary(grouped, summary_path, threshold)
    grouped.to_csv(grouped_csv_path, index=False)

    print(f"Saved plot: {plot_path}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved grouped data: {grouped_csv_path}")
