"""Unit tests for the analysis and loading logic.

Run with:  pytest
"""
from __future__ import annotations

import pandas as pd
import pytest

from sales_insight import analysis
from sales_insight.loader import load_sales


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "date": pd.to_datetime(["2025-01-15", "2025-01-20", "2025-02-10"]),
            "product": ["Laptop", "Novel", "Laptop"],
            "category": ["Electronics", "Books", "Electronics"],
            "region": ["North", "South", "North"],
            "quantity": [1, 3, 2],
            "unit_price": [1000.0, 10.0, 1000.0],
            "revenue": [1000.0, 30.0, 2000.0],
        }
    )


def test_summarize(sample_df):
    s = analysis.summarize(sample_df)
    assert s["total_orders"] == 3
    assert s["total_units"] == 6
    assert s["total_revenue"] == pytest.approx(3030.0)
    assert s["avg_order_value"] == pytest.approx(1010.0)
    assert s["first_date"] == "2025-01-15"
    assert s["last_date"] == "2025-02-10"


def test_revenue_by_category(sample_df):
    result = analysis.revenue_by_category(sample_df)
    assert result["Electronics"] == pytest.approx(3000.0)
    assert result["Books"] == pytest.approx(30.0)
    assert result.index[0] == "Electronics"  # sorted descending


def test_revenue_by_region(sample_df):
    result = analysis.revenue_by_region(sample_df)
    assert result["North"] == pytest.approx(3000.0)
    assert result["South"] == pytest.approx(30.0)


def test_top_products(sample_df):
    result = analysis.top_products(sample_df, n=1)
    assert len(result) == 1
    assert result.index[0] == "Laptop"
    assert result.iloc[0] == pytest.approx(3000.0)


def test_revenue_by_month(sample_df):
    result = analysis.revenue_by_month(sample_df)
    assert result["2025-01"] == pytest.approx(1030.0)
    assert result["2025-02"] == pytest.approx(2000.0)


def test_load_sales_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_sales(tmp_path / "does_not_exist.csv")


def test_load_sales_missing_columns(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_sales(bad)


def test_load_sales_adds_revenue(tmp_path):
    good = tmp_path / "good.csv"
    good.write_text(
        "order_id,date,product,category,region,quantity,unit_price\n"
        "1,2025-01-01,Laptop,Electronics,North,2,500\n",
        encoding="utf-8",
    )
    df = load_sales(good)
    assert df["revenue"].iloc[0] == pytest.approx(1000.0)