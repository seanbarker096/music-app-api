import functools
import json
from typing import Dict

import flask

from api.authentication_service.typings import AuthUser, TokenType
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


def auth(func):
    @functools.wraps(func)
    def wrapped_f():
        auth_token = flask.request.headers.get("Authorization")
        flask.g.new_auth_token = None

        if auth_token:
            try:
                flask.current_app.conns.auth_service.validate_token(auth_token)
                ## If auth token valid return
                return
            except:
                ## Otherwise try generating a new one using refresh token
                pass

        refresh_token = flask.request.headers.get("RefreshToken")

        if not refresh_token:
            raise Exception(
                "Authorization of the request failed. Please try logging out and in again to revalidate your session"
            )
        try:
            payload = flask.current_app.conns.auth_service.validate_token(refresh_token)

            auth_user = AuthUser(user_id=payload["user_id"], role=payload["role"])

            new_auth_token = flask.current_app.conns.auth_service.create_token(
                auth_user=auth_user,
                token_type=TokenType.ACCESS.value,
                refresh_token=refresh_token,
            )
            ## If generation of new auth_token succeeds then set it as a global so we can add to the response header later
            flask.g.new_auth_token = new_auth_token

        except Exception:
            raise Exception(
                "Authorization of the request failed. Please try logging out and in again to revalidate your session"
            )

        return func

    return wrapped_f
