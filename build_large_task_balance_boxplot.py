#!/usr/bin/env python3
"""Build a 30-plus-per-group boxplot from broader O*NET occupation data.

This script:
1. Uses the full O*NET occupation and work-activity tables
2. Computes a task-balance score for each detailed occupation
3. Selects the highest and lowest task-balance occupations
4. Fetches projected growth from O*NET Local Trends
5. Creates a boxplot with 40 occupations per group
"""

from __future__ import annotations

import argparse
import io
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BG = "#F6F0E7"
INK = "#1F2933"
JUDGMENT_COLOR = "#C7A663"
PROCESS_COLOR = "#4B5563"
GRID = "#D8C3A5"

DEFAULT_REPO_ROOT = Path("/Users/stephenye/stephen/coding/project/datajam")
DEFAULT_ZIP = DEFAULT_REPO_ROOT / "data" / "raw" / "onet_30_2_excel.zip"

PROCESS_ELEMENTS = [
    "Processing Information",
    "Documenting/Recording Information",
    "Updating and Using Relevant Knowledge",
]
ADVICE_ELEMENTS = [
    "Analyzing Data or Information",
    "Interpreting the Meaning of Information for Others",
    "Providing Consultation and Advice to Others",
]
GROWTH_PATTERN = re.compile(
    r"Projected growth <small class=\"d-sm-block\">\(2024-2034\)</small></dt>\s*<dd[^>]*>.*?([-\d]+)%",
    re.S,
)


@dataclass
class GrowthResult:
    soc_code: str
    projected_growth_pct: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a large task-balance boxplot with 30+ occupations per group."
    )
    parser.add_argument(
        "--onet-zip",
        type=Path,
        default=DEFAULT_ZIP,
        help="Path to onet_30_2_excel.zip",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repo root where figures/reports/data/processed outputs will be saved.",
    )
    parser.add_argument(
        "--target-per-group",
        type=int,
        default=40,
        help="How many occupations to include in each group.",
    )
    parser.add_argument(
        "--candidate-buffer",
        type=int,
        default=20,
        help="Extra candidates fetched per group in case some local-trends pages fail.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for point jitter in the plot.",
    )
    return parser.parse_args()


def read_onet_excel_from_zip(zip_path: Path, file_name: str) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(f"db_30_2_excel/{file_name}") as handle:
            return pd.read_excel(io.BytesIO(handle.read()))


def aggregate_scale_average(
    table: pd.DataFrame,
    element_names: Iterable[str],
    scale_id: str,
    column_name: str,
) -> pd.Series:
    filtered = table[
        table["Element Name"].isin(element_names) & (table["Scale ID"] == scale_id)
    ].copy()
    return filtered.groupby("O*NET-SOC Code")["Data Value"].mean().rename(column_name)


def build_task_balance_table(zip_path: Path) -> pd.DataFrame:
    occupation_data = read_onet_excel_from_zip(zip_path, "Occupation Data.xlsx")
    work_activities = read_onet_excel_from_zip(zip_path, "Work Activities.xlsx")

    occupations = (
        occupation_data[["O*NET-SOC Code", "Title"]]
        .drop_duplicates("O*NET-SOC Code")
        .rename(
            columns={
                "O*NET-SOC Code": "soc_code",
                "Title": "occupation_title",
            }
        )
        .reset_index(drop=True)
    )

    process_activities = aggregate_scale_average(
        work_activities,
        PROCESS_ELEMENTS,
        "LV",
        "process_activities",
    )
    advice_analysis = aggregate_scale_average(
        work_activities,
        ADVICE_ELEMENTS,
        "LV",
        "advice_analysis",
    )

    merged = occupations.merge(
        process_activities, left_on="soc_code", right_index=True, how="inner"
    )
    merged = merged.merge(
        advice_analysis, left_on="soc_code", right_index=True, how="inner"
    )
    merged["task_balance"] = merged["advice_analysis"] - merged["process_activities"]
    return merged.sort_values("task_balance", ascending=False).reset_index(drop=True)


def fetch_growth_for_code(soc_code: str) -> GrowthResult:
    url = f"https://www.onetonline.org/link/localtrends/{soc_code}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        text = urlopen(req, timeout=20).read().decode("utf-8", errors="ignore")
    except Exception:
        return GrowthResult(soc_code=soc_code, projected_growth_pct=None)

    match = GROWTH_PATTERN.search(text)
    if not match:
        return GrowthResult(soc_code=soc_code, projected_growth_pct=None)
    return GrowthResult(soc_code=soc_code, projected_growth_pct=int(match.group(1)))


def collect_growth(codes: list[str], max_workers: int = 12) -> pd.DataFrame:
    results: list[GrowthResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {pool.submit(fetch_growth_for_code, code): code for code in codes}
        for future in as_completed(future_map):
            results.append(future.result())

    return pd.DataFrame(
        {
            "soc_code": [result.soc_code for result in results],
            "projected_growth_pct": [
                result.projected_growth_pct for result in results
            ],
        }
    )


def select_groups(
    ranked: pd.DataFrame,
    target_per_group: int,
    candidate_buffer: int,
) -> pd.DataFrame:
    candidate_size = target_per_group + candidate_buffer
    judgment_candidates = ranked.head(candidate_size).copy()
    process_candidates = ranked.tail(candidate_size).copy()

    codes_to_fetch = list(
        dict.fromkeys(
            judgment_candidates["soc_code"].tolist()
            + process_candidates["soc_code"].tolist()
        )
    )
    growth = collect_growth(codes_to_fetch)

    judgment = judgment_candidates.merge(growth, on="soc_code", how="left")
    process = process_candidates.merge(growth, on="soc_code", how="left")

    judgment = judgment[judgment["projected_growth_pct"].notna()].head(target_per_group)
    process = (
        process[process["projected_growth_pct"].notna()]
        .sort_values("task_balance", ascending=True)
        .head(target_per_group)
    )

    if len(judgment) < 30 or len(process) < 30:
        raise RuntimeError(
            "Could not build groups with at least 30 occupations each. "
            f"Got {len(judgment)} and {len(process)}."
        )

    judgment["boxplot_group"] = "more judgment-heavy"
    process["boxplot_group"] = "more process-heavy"
    return pd.concat([judgment, process], ignore_index=True)


def make_plot(data: pd.DataFrame, plot_path: Path, seed: int) -> None:
    rng = np.random.default_rng(seed)
    order = ["more judgment-heavy", "more process-heavy"]
    colors = [JUDGMENT_COLOR, PROCESS_COLOR]

    fig, ax = plt.subplots(figsize=(10.2, 6.5), facecolor=BG)
    ax.set_facecolor(BG)

    groups = [
        data.loc[data["boxplot_group"] == label, "projected_growth_pct"].to_numpy(dtype=float)
        for label in order
    ]
    box = ax.boxplot(groups, tick_labels=order, patch_artist=True, widths=0.52)

    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
        patch.set_edgecolor(INK)

    for median in box["medians"]:
        median.set_color(INK)
        median.set_linewidth(2)

    for i, (label, color) in enumerate(zip(order, colors), start=1):
        subset = data.loc[data["boxplot_group"] == label]
        x = i + rng.uniform(-0.12, 0.12, size=len(subset))
        y = subset["projected_growth_pct"].to_numpy(dtype=float)
        ax.scatter(
            x,
            y,
            s=40,
            color=color,
            edgecolor=INK,
            linewidth=0.6,
            alpha=0.9,
            zorder=3,
        )

    ax.set_title("Projected Growth by Occupation Task Balance", color=INK, weight="bold")
    ax.set_ylabel("Projected Growth %", color=INK)
    ax.grid(axis="y", color=GRID, alpha=0.65)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(INK)

    fig.tight_layout()
    fig.savefig(plot_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_summary(data: pd.DataFrame, summary_path: Path) -> None:
    summary = (
        data.groupby("boxplot_group")["projected_growth_pct"]
        .agg(["count", "mean", "median", "min", "max"])
        .reindex(["more judgment-heavy", "more process-heavy"])
    )

    lines = [
        "Large Task-Balance Boxplot Summary",
        "Source: O*NET occupation/work-activity tables plus O*NET Local Trends",
        "Selection rule: top 40 and bottom 40 occupations by task_balance",
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

    summary_path.write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    if not args.onet_zip.exists():
        raise FileNotFoundError(f"O*NET zip not found: {args.onet_zip}")

    repo_root = args.output_dir
    figures_dir = repo_root / "figures"
    reports_dir = repo_root / "reports"
    processed_dir = repo_root / "data" / "processed"
    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    ranked = build_task_balance_table(args.onet_zip)
    selected = select_groups(ranked, args.target_per_group, args.candidate_buffer)

    plot_path = figures_dir / "large_task_balance_boxplot_80.png"
    summary_path = reports_dir / "large_task_balance_boxplot_80_summary.txt"
    csv_path = processed_dir / "large_task_balance_boxplot_80_groups.csv"

    make_plot(selected, plot_path, args.seed)
    write_summary(selected, summary_path)
    selected.to_csv(csv_path, index=False)

    print(f"Saved plot: {plot_path}")
    print(f"Saved summary: {summary_path}")
    print(f"Saved grouped data: {csv_path}")
    print()
    counts = selected["boxplot_group"].value_counts()
    for label in ["more judgment-heavy", "more process-heavy"]:
        print(f"{label}: {int(counts.get(label, 0))}")


if __name__ == "__main__":
    main()
