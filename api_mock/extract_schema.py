import json
import os
import random

FILE_PATH = "football_api_sports.json"


def load_random_json():
    """Load the file and return a single random JSON object."""
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError("data.json not found")

    with open(FILE_PATH, "r") as f:
        data = json.load(f)

    if not data:
        raise ValueError("data.json is empty")

    return random.choice(data)


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
        # assume list items are same type: use schema of the first item
        return [extract_schema(value[0])]

    # primitive (int, float, str, bool, None)
    return type(value).__name__


def main():
    random_json = load_random_json()
    schema = extract_schema(random_json)

    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
