import json
from typing import Dict

import flask

from exceptions.response.exceptions import ResponseBaseException


def process_string_request_param(request_body: Dict[str, any], parameter_name: str) -> str:
    """Validates and returns a flask request body string parameter"""
    parameter = request_body.get(parameter_name, None)

    if not parameter:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if not isinstance(parameter, str) or len(parameter) == 0:
        raise Exception(f"Invalid value {parameter} for parameter '{parameter_name}'")

    return parameter


def build_api_error_repsonse(e: ResponseBaseException, http_status_code: int):
    response = {
        "status": "error",
        "message": e.get_message(),
        "error_code": e.get_code(),
        "detail": e.get_detail(),
    }
    return flask.current_app.response_class(
        response=json.dumps(response), status=http_status_code, mimetype="application/json"
    )
