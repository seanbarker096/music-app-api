import functools
import json
from enum import Enum
from typing import Dict, List

import flask

from api.authentication_service.typings import AuthUser, TokenType
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import (
    InvalidAuthTokenException,
    ResponseBaseException,
)


def process_string_api_request_param(parameter_name: str, optional=True) -> str:
    """Validates and returns a flask request string parameter"""
    parameter = flask.request.values.get(parameter_name, None)

    return process_string_request_param(parameter_name, parameter, optional)


def process_string_api_post_request_param(request_body: Dict[str, any], parameter_name: str) -> str:
    """Validates and returns a flask json request body string parameter"""
    parameter = request_body.get(parameter_name, None)

    return process_string_request_param(parameter_name, parameter, optional=False)


def process_string_request_param(parameter_name: str, parameter: any, optional=True) -> str:
    """Validates and returns a flask request body string parameter"""

    if parameter is None and optional:
        return None

    if parameter is None and not optional:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if not isinstance(parameter, str) or len(parameter) == 0:
        raise Exception(
            f"Invalid value {parameter} for parameter '{parameter_name}'. {parameter_name} must be a valid string"
        )

    return parameter


def process_int_api_request_param(parameter_name: str, optional=True) -> int:
    """Validates and returns a flask request body integer parameter"""
    parameter = flask.request.values.get(parameter_name, None)

    return process_int_request_param(parameter_name, parameter, optional)


def process_int_request_param(parameter_name: str, parameter: any, optional=True) -> int:
    if parameter is None and optional:
        return None

    if parameter is None and not optional:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    parameter = int(parameter)

    if not isinstance(parameter, int):
        raise Exception(
            f"Invalid value {parameter} for parameter '{parameter_name}'. {parameter_name} must be a valid integer"
        )

    return parameter


def process_enum_request_param(parameter_name: str, enum: Enum, optional=True) -> str | int:

    parameter = flask.request.values.get(parameter_name, None)

    if parameter is None and optional:
        return None

    if not parameter:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if parameter not in set(item.value for item in enum):
        raise Exception(
            f"Invalid value {parameter} for parameter '{parameter_name}'. {parameter} does not exist in enum {enum.__class__.__name__}"
        )

    return parameter


def process_enum_set_api_request_param(
    parameter_name: str, enum: Enum, type: str | int = str, optional=True
) -> str | int:
    if not optional and parameter_name not in flask.request.values:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if optional and not parameter_name in flask.request.values:
        return None

    list = flask.request.values.getlist(parameter_name, type)

    return process_enum_set_param(parameter_name, list, enum)


def process_enum_set_param(
    parameter_name: str, list_param: List[str | int], enum: Enum
) -> List[str | int]:

    enum_set = set(item.value for item in enum)

    for parameter in list_param:
        if parameter not in enum_set:
            raise InvalidArgumentException(
                f"Invalid value {parameter} in parameter '{parameter_name}'. {parameter} does not exist in enum {enum.__class__.__name__}",
                parameter_name,
            )

    return list_param


def process_bool_api_request_param(parameter_name: str, optional=True) -> bool:
    """Validates and returns a flask request body boolean parameter"""
    parameter = flask.request.values.get(parameter_name, None)

    if isinstance(parameter, str):
        if parameter.lower() not in ["true", "false"]:
            raise Exception(
                f"Invalid value {parameter} for parameter '{parameter_name}'. {parameter_name} must be a valid boolean"
            )
        else:
            parameter = parameter.lower() == "true"

    return process_bool_request_param(parameter_name, parameter, optional)


def process_bool_request_param(parameter_name: str, parameter: any, optional=True) -> bool:
    """Validates and returns a flask request body boolean parameter"""
    if parameter is None and optional:
        return None

    if parameter is None and not optional:
        raise Exception(f"Missing required request parameter '{parameter_name}'")

    if parameter not in [True, False]:
        raise Exception(
            f"Invalid value {parameter} for parameter '{parameter_name}'. {parameter_name} must be a valid boolean"
        )

    return parameter


def process_api_set_request_param(
    parameter_name: str, type: any, optional=True
) -> List[str | int] | None:
    """Validates and returns a flask request body array parameter"""

    if optional and not parameter_name in flask.request.values:
        return None

    if parameter_name in flask.request.values:
        processed_list = flask.request.values.getlist(parameter_name, type)

        # werkzeug.datastructures.MultiDict will remove values from the list if they can't be converted to the type
        if len(processed_list) != len(flask.request.values.getlist(parameter_name)):
            raise InvalidArgumentException(
                f"Invalid value found in set parameter {parameter_name}", parameter_name
            )

        return processed_list

    raise Exception(f"Missing required request parameter '{parameter_name}'")


def class_to_dict(class_instance: object):

    if not isinstance(class_instance, object):
        raise InvalidArgumentException(
            "Must provide an object instance to convert it to a dictionary", "class_instance"
        )

    return vars(class_instance)


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


def remove_bearer_from_token(token: str):
    ## Handle tokens in Authorization header format ("Bearer the_actual_token")
    strings = token.split("Bearer ")

    if len(strings) == 2 and strings[0] == "":
        token = strings[1]

    return token


def after_request_setup(response: flask.Response):
    """Common after request setup to be used here and in unit tests"""
    add_token_headers(response)

    return response


## TODO: Consider if this should jsut return AuthState set to Unauthenticated
def auth(func):
    @functools.wraps(func)
    def wrapped_f(*args, **kwargs):
        auth_token = flask.request.headers.get("Authorization")
        auth_token = remove_bearer_from_token(auth_token) if auth_token else None

        flask.g.new_auth_token = None

        if auth_token:
            try:
                decoded_token = flask.current_app.conns.auth_service.validate_token(auth_token)
                auth_user = build_auth_user_from_token_payload(decoded_token)
                flask.g.auth_user = auth_user
                ## If auth token valid return
                return func(*args, **kwargs)

            except InvalidAuthTokenException:
                ## If auth service throws try to validate refresh token
                pass

        refresh_token = flask.request.headers.get("Refresh-Token")
        refresh_token = remove_bearer_from_token(refresh_token) if refresh_token else None

        if not refresh_token:
            print("exception 1")
            raise Exception(
                "Authorization of the request failed. Please try logging out and in again to revalidate your session"
            )
        try:
            decoded_token = flask.current_app.conns.auth_service.validate_token(refresh_token)

            auth_user = build_auth_user_from_token_payload(decoded_token)
            flask.g.auth_user = auth_user

            new_auth_token = flask.current_app.conns.auth_service.create_token(
                auth_user=auth_user,
                token_type=TokenType.ACCESS.value,
                refresh_token=refresh_token,
            )

            ## Updated auth tokens for all routes other than /logout. This is a authed route but we want to invalidate auth tokens here
            if func.__name__ != "logout":
                ## If generation of new auth_token succeeds then set it as a global so we can add to the response header later
                flask.g.new_auth_token = new_auth_token

        except Exception:
            print("exception 2")
            raise Exception(
                "Authorization of the request failed. Please try logging out and in again to revalidate your session"
            )

        return func(*args, **kwargs)

    return wrapped_f


def build_auth_user_from_token_payload(payload: Dict[str, str | int]) -> AuthUser:
    """
    :param dict: Token payload
    """
    user_id = payload.get("user_id", None)
    role = payload.get("role", None)

    if not user_id or not role:
        raise Exception("Error when extracting requesting user information from token")

    return AuthUser(user_id=user_id, role=role)


def add_token_headers(response):
    """If a new auth token was generated during any given request (e.g. if it expired and refresh token used to generate new one), add it to the response header"""
    if flask.g.get("new_auth_token", None):
        response.headers["Authorization"] = f"Bearer {flask.g.new_auth_token}"
    return response
