"""Generate a realistic sample sales dataset for demonstration.

Run this once to create ``data/sales.csv``. The data is synthetic but
mimics a small retail store: products grouped into categories, sold across
regions over a full year, with mild holiday seasonality. A fixed random
seed makes the output reproducible.
"""
from __future__ import annotations

import csv
import random
from datetime import date
from pathlib import Path

# product -> (category, base unit price in dollars)
CATALOG = {
    "Laptop": ("Electronics", 1200.0),
    "Smartphone": ("Electronics", 800.0),
    "Tablet": ("Electronics", 450.0),
    "Headphones": ("Electronics", 150.0),
    "Smartwatch": ("Electronics", 250.0),
    "Coffee Maker": ("Home & Kitchen", 120.0),
    "Blender": ("Home & Kitchen", 90.0),
    "Vacuum Cleaner": ("Home & Kitchen", 200.0),
    "Microwave": ("Home & Kitchen", 180.0),
    "T-Shirt": ("Clothing", 25.0),
    "Jeans": ("Clothing", 60.0),
    "Jacket": ("Clothing", 110.0),
    "Sneakers": ("Clothing", 95.0),
    "Novel": ("Books", 15.0),
    "Textbook": ("Books", 75.0),
    "Yoga Mat": ("Sports", 30.0),
    "Dumbbells": ("Sports", 55.0),
    "Bicycle": ("Sports", 400.0),
}

REGIONS = ["North", "South", "East", "West", "Central"]

# Higher weight = more sales that month (Nov/Dec holiday bump).
MONTH_WEIGHTS = [0.7, 0.7, 0.8, 0.9, 1.0, 1.0, 0.9, 0.9, 1.0, 1.1, 1.4, 1.6]


def random_date(rng: random.Random) -> date:
    month = rng.choices(range(1, 13), weights=MONTH_WEIGHTS, k=1)[0]
    day = rng.randint(1, 28)  # 1..28 is valid for every month
    return date(2025, month, day)


def generate_rows(n_orders: int, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    products = list(CATALOG)
    rows = []
    for order_id in range(1, n_orders + 1):
        product = rng.choice(products)
        category, base_price = CATALOG[product]
        quantity = rng.randint(1, 5)
        unit_price = round(base_price * rng.uniform(0.9, 1.1), 2)
        rows.append(
            {
                "order_id": order_id,
                "date": random_date(rng).isoformat(),
                "product": product,
                "category": category,
                "region": rng.choice(REGIONS),
                "quantity": quantity,
                "unit_price": unit_price,
            }
        )
    rows.sort(key=lambda r: r["date"])
    return rows


def main() -> None:
    out_path = Path(__file__).parent / "data" / "sales.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_rows(2000)
    fieldnames = [
        "order_id", "date", "product", "category",
        "region", "quantity", "unit_price",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} orders to {out_path}")


if __name__ == "__main__":
    main()