"""Command-line entry point: analyze a sales CSV and produce charts + a report.

Example:
    python main.py -i data/sales.csv -o output --top 8
"""
from __future__ import annotations

import argparse
from pathlib import Path

from sales_insight import analysis, charts
from sales_insight.loader import load_sales


def build_report(summary: dict, by_category, by_region, top) -> str:
    lines = [
        "# Sales Report",
        "",
        f"- Period: {summary['first_date']} to {summary['last_date']}",
        f"- Total orders: {summary['total_orders']:,}",
        f"- Total units sold: {summary['total_units']:,}",
        f"- Total revenue: ${summary['total_revenue']:,.2f}",
        f"- Average order value: ${summary['avg_order_value']:,.2f}",
        "",
        "## Revenue by Category",
        "```",
        by_category.to_string(),
        "```",
        "",
        "## Revenue by Region",
        "```",
        by_region.to_string(),
        "```",
        "",
        "## Top Products",
        "```",
        top.to_string(),
        "```",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Analyze sales data from a CSV and generate charts and a report."
    )
    parser.add_argument("-i", "--input", default="data/sales.csv", help="Path to the sales CSV")
    parser.add_argument("-o", "--output", default="output", help="Directory for charts and report")
    parser.add_argument("--top", type=int, default=8, help="Number of top products to chart")
    args = parser.parse_args(argv)

    df = load_sales(args.input)
    summary = analysis.summarize(df)
    monthly = analysis.revenue_by_month(df)
    by_category = analysis.revenue_by_category(df)
    by_region = analysis.revenue_by_region(df)
    top = analysis.top_products(df, args.top)

    out = Path(args.output)
    charts.plot_monthly_revenue(monthly, out)
    charts.plot_category_revenue(by_category, out)
    charts.plot_region_share(by_region, out)
    charts.plot_top_products(top, out)

    report = build_report(summary, by_category, by_region, top)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(report, encoding="utf-8")

    print(report)
    print(f"Charts and report saved to: {out.resolve()}")


if __name__ == "__main__":
    main()