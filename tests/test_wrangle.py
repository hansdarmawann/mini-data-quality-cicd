"""Tiny, deterministic tests suitable for a fast CI demo."""

import csv
from pathlib import Path
import tempfile
import unittest

from wrangle import clean_orders


class CleanOrdersTests(unittest.TestCase):
    def test_sample_data_yields_three_valid_orders(self):
        with tempfile.TemporaryDirectory() as tempdir:
            destination = Path(tempdir) / "cleaned.csv"
            count = clean_orders(Path("data/orders_raw.csv"), destination)

            with destination.open(newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(count, 3)
            self.assertEqual([row["order_id"] for row in rows], ["O001", "O002", "O006"])
            self.assertEqual([row["customer"] for row in rows], ["Alice", "Bob", "Eka"])
            self.assertEqual([row["amount"] for row in rows], ["120", "350", "80"])

    def test_missing_required_column_is_rejected(self):
        with tempfile.TemporaryDirectory() as tempdir:
            source = Path(tempdir) / "invalid.csv"
            destination = Path(tempdir) / "cleaned.csv"
            source.write_text("order_id,customer\nO001,Alice\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Missing required CSV columns"):
                clean_orders(source, destination)


if __name__ == "__main__":
    unittest.main()
