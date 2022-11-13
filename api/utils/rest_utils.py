from typing import Dict


def process_string_request_param(request_body: Dict[str, any], parameter_name: str) -> str:
    """Validates and returns a flask request body string parameter"""
    parameter = request_body.get(parameter_name, None)

    if not parameter:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if not isinstance(parameter, str) or len(parameter) == 0:
        raise Exception(f"Invalid value {parameter} for parameter '{parameter_name}'")

    return parameter
