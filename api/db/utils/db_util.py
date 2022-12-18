import json
from typing import Dict, List, Optional


def assert_row_key_exists(
    row: Dict[str, any],
    key: str,
) -> None:
    if not key in row:
        raise Exception(f"Expected {key} to exist in {json.dumps(row)}")


def build_where_query_string(wheres: List[str], operator: Optional[str]) -> str:

    if len(wheres) == 0:
        raise Exception("wheres must have at least one item")

    if operator != "OR" and operator != "AND":
        raise Exception("Invalid operator provided. Operator shoulld be one of OR or AND")

    where_string = " WHERE "

    where_string = where_string + f" {operator} ".join(wheres)

    return where_string
