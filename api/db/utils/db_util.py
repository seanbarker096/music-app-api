import json
from typing import Dict


def assert_row_key_exists(key: str, row: Dict[str, any]) -> None:
    if not key in row:
        raise Exception(f"Expected {key} to exist in {json.dumps(row)}")
