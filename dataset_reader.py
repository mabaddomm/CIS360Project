"""
dataset_reader.py
────────────────────────────────────────────────────────────────
Simple reader — one function per MongoDB collection.

Usage:
    from dataset_reader import DatasetReader

    r = DatasetReader()
    r.read_papers()
    r.read_fusion_methods()
    r.read_datasets()

CLI:
    python dataset_reader.py
"""

import json
from pymongo import MongoClient


def _print_rows(rows: list[dict], label: str) -> None:
    """Print each row on its own numbered line."""
    print(f"\n── {label} ({len(rows)} rows) ──")
    for i, row in enumerate(rows, start=1):
        print(f"  [{i}] {json.dumps(row, default=str)}")
    if not rows:
        print("  (no rows found)")


class DatasetReader:

    def __init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name:   str = "data_fusion_ontology",
    ):
        db = MongoClient(mongo_uri)[db_name]
        self.papers   = db["papers"]
        self.methods  = db["fusion_methods"]
        self.datasets = db["datasets"]

    # ── One function per collection ────────────────────────────────────────

    def read_papers(self) -> list[dict]:
        """Read all rows from the papers collection (DOI sheet)."""
        rows = list(self.papers.find({}))
        _print_rows(rows, "Papers")
        return rows

    def read_fusion_methods(self) -> list[dict]:
        """Read all rows from the fusion_methods collection (Fusion Method sheet)."""
        rows = list(self.methods.find({}))
        _print_rows(rows, "Fusion Methods")
        return rows

    def read_datasets(self) -> list[dict]:
        """Read all rows from the datasets collection (Data sheet)."""
        rows = list(self.datasets.find({}))
        _print_rows(rows, "Datasets")
        return rows


# ── Run all three when executed directly ───────────────────────────────────

if __name__ == "__main__":
    r = DatasetReader()
    r.read_papers()
    r.read_fusion_methods()
    r.read_datasets()
