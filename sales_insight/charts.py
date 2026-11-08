"""Render charts from the analysis results and save them as PNG files."""
from __future__ import annotations

from pathlib import Path

import matplotlib

# Use a non-interactive backend so charts render to files even on a
# machine with no display (servers, CI, containers).
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#f7f7f7",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    }
)

ACCENT = "#2563eb"


def _save(fig, out_dir: str | Path, name: str) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_monthly_revenue(monthly, out_dir) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly.values, marker="o", color=ACCENT, linewidth=2)
    ax.set_title("Monthly Revenue", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.tick_params(axis="x", rotation=45)
    return _save(fig, out_dir, "monthly_revenue.png")


def plot_category_revenue(by_category, out_dir) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(by_category.index, by_category.values, color=ACCENT)
    ax.set_title("Revenue by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue ($)")
    return _save(fig, out_dir, "category_revenue.png")


def plot_region_share(by_region, out_dir) -> Path:
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        by_region.values,
        labels=by_region.index,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.4, "edgecolor": "white"},
    )
    ax.set_title("Revenue Share by Region", fontsize=14, fontweight="bold")
    return _save(fig, out_dir, "region_share.png")


def plot_top_products(top, out_dir) -> Path:
    fig, ax = plt.subplots(figsize=(9, 6))
    top = top.sort_values()  # biggest on top for a horizontal bar chart
    ax.barh(top.index, top.values, color=ACCENT)
    ax.set_title(f"Top {len(top)} Products by Revenue", fontsize=14, fontweight="bold")
    ax.set_xlabel("Revenue ($)")
    return _save(fig, out_dir, "top_products.png")