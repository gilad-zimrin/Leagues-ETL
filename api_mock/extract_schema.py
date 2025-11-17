import json
import os
from deepdiff import DeepDiff
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = 'api_football_teams.json'

def extract_schema(value):
    """
    Recursively extract schema from ANY JSON value:
    - dict -> keys with nested schema
    - list -> schema of the first element (or "empty_list")
    - primitives -> type name
    """

    if isinstance(value, dict):
        return {k: extract_schema(v) for k, v in value.items()}

    if isinstance(value, list):
        if not value:
            return "empty_list"
        return [extract_schema(value[0])]

    return type(value).__name__


def load_all_json():
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError("data.json not found")

    with open(FILE_PATH, "r") as f:
        data = json.load(f)

    if not data:
        raise ValueError("data.json is empty")

    return data


def compare_schemas():
    data = load_all_json()

    schemas = []
    for item in data:
        schemas.append(extract_schema(item))

    # the first schema is our baseline
    base_schema = schemas[0]

    differences = []
    for i, s in enumerate(schemas[1:], start=1):
        diff = DeepDiff(base_schema, s, ignore_order=True)
        if diff:
            differences.append((i, diff))

    if not differences:
        print("All JSON objects share the SAME schema.\nSchema:\n")
        print(json.dumps(base_schema, indent=2))
        return

    print("⚠ Schema differences detected:\n")
    for index, diff in differences:
        print(f"--- Difference at JSON index {index} ---")
        print(diff.pretty())
        print()


if __name__ == "__main__":
    compare_schemas()
