"""Clean a tiny CSV dataset using only the Python standard library."""

import csv
from pathlib import Path

INPUT_PATH = Path("data/orders_raw.csv")
OUTPUT_PATH = Path("data/orders_clean.csv")


def clean_orders(source: Path, destination: Path) -> int:
    """Strip names, reject invalid/non-positive amounts, remove duplicate IDs."""
    cleaned = []
    seen_ids = set()

    with source.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        expected_columns = {"order_id", "customer", "amount"}
        if not expected_columns.issubset(reader.fieldnames or []):
            raise ValueError("Missing required CSV columns")

        for row in reader:
            order_id = (row["order_id"] or "").strip()
            customer = (row["customer"] or "").strip().title()

            try:
                amount = int((row["amount"] or "").strip())
            except ValueError:
                continue

            if not order_id or not customer or amount < 0 or order_id in seen_ids:
                continue

            cleaned.append({"order_id": order_id, "customer": customer, "amount": amount})
            seen_ids.add(order_id)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["order_id", "customer", "amount"])
        writer.writeheader()
        writer.writerows(cleaned)

    return len(cleaned)


if __name__ == "__main__":
    count = clean_orders(INPUT_PATH, OUTPUT_PATH)
    print(f"Data cleaning complete: {count} valid orders saved to {OUTPUT_PATH}")
