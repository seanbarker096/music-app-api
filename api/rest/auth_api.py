import json
import os

import flask

from api.authentication_service.typings import (
    AuthStateCreateRequest,
    AuthStateDeleteRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenType,
)
from api.typings.auth import LoginResult
from api.typings.users import (
    User,
    UserCreateRequest,
    UsersGetFilter,
    UsersGetProjection,
)
from api.utils.rest_utils import (
    api_error_response,
    auth,
    build_auth_user_from_token_payload,
    error_handler,
    process_string_api_post_request_param,
    process_string_api_request_param,
    process_string_request_param,
    remove_bearer_from_token,
)
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import (
    BadRequestException,
    InvalidTokenException,
    ResponseBaseException,
    UnknownException,
    UserAlreadyExistsException,
)

blueprint = flask.Blueprint("auth", __name__)


@blueprint.route("/login/", methods=["POST"])
@error_handler
def login():
    request = flask.request.json

    password = request.get("password", None)
    email = request.get("email", None)
    username = request.get("username", None)

    process_string_api_request_param("username", username, optional=True)
    process_string_api_request_param("email", username, optional=True)
    process_string_api_request_param("password", password, optional=False)

    if not username and not email:
        raise BadRequestException(
            "Must provide at least one of username or email", "username, email"
        )

    user = flask.current_app.conns.midlayer.get_user_by_username_or_email_and_password(
        password=password, username=username, email=email, projection=UsersGetProjection()
    )

    auth_state_request = AuthStateCreateRequest(
        auth_user=AuthUser(user_id=user.id, role=AuthUserRole.USER.value)
    )

    result = flask.current_app.conns.auth_service.create_auth_state(request=auth_state_request)

    auth_state = result.auth_state

    ## This shouldn't really happen. If auth failed an error should be thrown
    if auth_state.status != AuthStatus.AUTHENTICATED.value:
        raise Exception(f"Failed to authenticate user with id {user.id}")

    response = {
        "user_id": auth_state.auth_user.user_id,
        "auth_status": auth_state.status,
        "role": auth_state.auth_user.role,
        "access_token": auth_state.access_token,
        "refresh_token": auth_state.refresh_token,
    }

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    response.headers["Authorization"] = f"Bearer {auth_state.access_token}"

    key = flask.current_app.config["config_file"]["app-api-key"].get("key")
    response.headers["x-appifr"] = key

    return response


@blueprint.route("/signup/", methods=["POST"])
def signup():
    request = flask.request.json

    password = process_string_api_post_request_param(
        request_body=request, parameter_name="password"
    )
    username = process_string_api_post_request_param(
        request_body=request, parameter_name="username"
    )

    email = process_string_api_post_request_param(request_body=request, parameter_name="email")

    user_create_request = UserCreateRequest(
        username=username,
        password=password,
        email=email,
    )

    try:
        user = flask.current_app.conns.midlayer.user_create(request=user_create_request).user
    except UserAlreadyExistsException as e:
        return api_error_response(e)

    ## now authenticate the new user
    auth_state_request = AuthStateCreateRequest(
        auth_user=AuthUser(user_id=user.id, role=AuthUserRole.USER.value)
    )

    result = flask.current_app.conns.auth_service.create_auth_state(request=auth_state_request)

    auth_state = result.auth_state

    ## This shouldn't really happen. If auth failed an error should be thrown
    if auth_state.status != AuthStatus.AUTHENTICATED.value:
        raise Exception(f"Failed to authenticate user with id {user.id}")

    response = {
        "user_id": auth_state.auth_user.user_id,
        "auth_status": auth_state.status,
        "role": auth_state.auth_user.role,
        "access_token": auth_state.access_token,
        "refresh_token": auth_state.refresh_token,
    }

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    response.headers["Authorization"] = f"Bearer {auth_state.access_token}"

    key = flask.current_app.config["config_file"]["app-api-key"].get("key")
    response.headers["x-appifr"] = key

    return response


@blueprint.route("/logout/", methods=["POST"])
@auth
def logout():
    refresh_token = flask.request.headers.get("Refresh-Token", None)
    refresh_token = remove_bearer_from_token(refresh_token)

    request = AuthStateDeleteRequest(refresh_token=refresh_token)

    flask.current_app.conns.auth_service.delete_auth_state(request)

    return flask.current_app.response_class(status=200, mimetype="application/json")


@blueprint.route("/validate/", methods=["GET"])
@auth
def validate_auth_session():
    """Use to validate auth tokens. Throws if @auth check fails"""
    return flask.current_app.response_class(status=200, mimetype="application/json")


@blueprint.route("/token/", methods=["POST"])
def get_token():
    """
    Use to create a new access token from a refresh token
    """
    request = flask.request.json

    token_type = process_string_api_post_request_param(
        request_body=request, parameter_name="token_type"
    )

    try:
        if token_type == "access":
            refresh_token = flask.request.headers.get("Refresh-Token")
            refresh_token = remove_bearer_from_token(refresh_token) if refresh_token else None

            if not refresh_token:
                raise InvalidTokenException(
                    "Request failed as invalid refresh token provided. A valid refresh token is required to obtain an acess token"
                )

            decoded_token = flask.current_app.conns.auth_service.validate_token(refresh_token)

            auth_user = build_auth_user_from_token_payload(decoded_token)
            flask.g.auth_user = auth_user

            new_auth_token = flask.current_app.conns.auth_service.create_token(
                auth_user=auth_user,
                token_type=TokenType.ACCESS.value,
                refresh_token=refresh_token,
            )

            response = {"token": new_auth_token}

            return flask.current_app.response_class(
                response=json.dumps(response), status=200, mimetype="application/json"
            )

        else:
            raise InvalidTokenException(
                message="Invalid token type provided. Token must of type 'access'"
            )

    except ResponseBaseException as err:
        return api_error_response(err)

    except Exception:
        err = UnknownException("Unknown error occurred")
        return api_error_response(err)


# @blueprint.route("/refresh-token/", methods=["POST"])
# def get_refresh_token():
#     """
#     Used by applications to get a new refresh token on behalf of a user to prevent their session expiring. We also send them a new access token
#     """
#     try:
#         # Only allow authorized apps to request a refrehs token directly. Users can only get one by logging in
#         request = flask.request.json
#         api_key = flask.request.headers.get("x-appifr")

#         key = flask.current_app.config["config_file"]["app-api-key"].get("key")

#         # Verify the API key is valid
#         if api_key != key:
#             # If unauthorised app makes request we dont want to tell them why the request failed
#             raise UnknownException("Unauthorized application made request to /refresh-token/")

#         user_id = process_int_request_param("user_id", request.get("user_id", None))

#         # Check if user exists. Will throw if not found
#         flask.current_app.conns.midlayer.get_user_by_id(user_id=user_id)

#         auth_state_request = AuthStateCreateRequest(
#             auth_user=AuthUser(user_id=user_id, role=AuthUserRole.USER.value)
#         )

#         result = flask.current_app.conns.auth_service.create_auth_state(request=auth_state_request)

#         auth_state = result.auth_state

#         ## This shouldn't really happen. If auth failed an error should be thrown
#         if auth_state.status != AuthStatus.AUTHENTICATED.value:
#             raise Exception(f"Failed to authenticate user with id {user_id}")

#         response = {
#             "user_id": auth_state.auth_user.user_id,
#             "auth_status": auth_state.status,
#             "role": auth_state.auth_user.role,
#             "access_token": auth_state.access_token,
#             "refresh_token": auth_state.refresh_token,
#         }

#         response = flask.current_app.response_class(
#             response=json.dumps(response), status=200, mimetype="application/json"
#         )

#         response.headers["Authorization"] = f"Bearer {auth_state.access_token}"

#         return response

#     except Exception as err:
#         return api_error_response(err)
