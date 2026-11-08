"""Compute summary metrics and aggregations from the sales data.

Every function takes the cleaned DataFrame from ``loader.load_sales`` and
returns either a plain dict (for the headline numbers) or a pandas Series
(for grouped results that are easy to chart).
"""
from __future__ import annotations

import pandas as pd


def summarize(df: pd.DataFrame) -> dict:
    """Headline numbers for the whole dataset."""
    return {
        "total_orders": int(len(df)),
        "total_units": int(df["quantity"].sum()),
        "total_revenue": float(df["revenue"].sum()),
        "avg_order_value": float(df["revenue"].mean()),
        "first_date": df["date"].min().date().isoformat(),
        "last_date": df["date"].max().date().isoformat(),
    }


def revenue_by_month(df: pd.DataFrame) -> pd.Series:
    """Total revenue per calendar month, indexed by ``YYYY-MM``."""
    monthly = df.set_index("date").resample("ME")["revenue"].sum()
    monthly.index = monthly.index.strftime("%Y-%m")
    return monthly


def revenue_by_category(df: pd.DataFrame) -> pd.Series:
    return df.groupby("category")["revenue"].sum().sort_values(ascending=False)


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    return df.groupby("region")["revenue"].sum().sort_values(ascending=False)


def top_products(df: pd.DataFrame, n: int = 8) -> pd.Series:
    return (
        df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(n)
    )