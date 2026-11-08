"""Load and validate the sales CSV."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "order_id", "date", "product", "category",
    "region", "quantity", "unit_price",
]


def load_sales(path: str | Path) -> pd.DataFrame:
    """Read a sales CSV, validate it, and add a ``revenue`` column.

    Clear errors are raised for a missing file or missing columns so the
    caller gets a helpful message instead of a cryptic crash downstream.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["date", "quantity", "unit_price"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df