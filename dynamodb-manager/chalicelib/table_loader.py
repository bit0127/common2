import os
import json

def load_table_configs():
    """Load all JSON files from the 'chalicelib/tables' directory."""
    tables = []
    tables_dir = os.path.join(os.path.dirname(__file__), "tables")

    for filename in os.listdir(tables_dir):
        if filename.endswith(".json"):
            with open(os.path.join(tables_dir, filename), "r") as f:
                tables.append(json.load(f))

    return tables
