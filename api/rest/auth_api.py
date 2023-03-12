import json

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
    auth,
    build_api_error_repsonse,
    build_auth_user_from_token_payload,
    process_string_request_param,
    remove_bearer_from_token,
)
from exceptions.response.exceptions import UserAlreadyExistsException

blueprint = flask.Blueprint("auth", __name__)


@blueprint.route("/login/", methods=["POST"])
def login():
    request = flask.request.json

    password = request.get("password", None)
    username = request.get("username", None)

    if not password or not username:
        raise Exception("Must provide username and password")

    if not isinstance(password, str) or len(password) == 0:
        raise Exception("Invalid argument password. Password must be a valid string")

    if not isinstance(username, str) or len(username) == 0:
        raise Exception("Invalid argument username. Username must be a valid string")

    user = flask.current_app.conns.midlayer.get_user_by_username_and_password(
        username=request["username"], password=request["password"], projection=UsersGetProjection()
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

    return response


@blueprint.route("/signup/", methods=["POST"])
def signup():
    request = flask.request.json

    password = process_string_request_param(request_body=request, parameter_name="password")
    username = process_string_request_param(request_body=request, parameter_name="username")
    first_name = process_string_request_param(request_body=request, parameter_name="first_name")
    second_name = process_string_request_param(request_body=request, parameter_name="second_name")
    email = process_string_request_param(request_body=request, parameter_name="email")

    user_create_request = UserCreateRequest(
        username=username,
        password=password,
        first_name=first_name,
        second_name=second_name,
        email=email,
    )

    try:
        user = flask.current_app.conns.midlayer.user_create(request=user_create_request).user
    except UserAlreadyExistsException as e:
        return build_api_error_repsonse(e, 400)

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
    request = flask.request.json

    token_type = process_string_request_param(request_body=request, parameter_name="token_type")

    if token_type == "access":
        refresh_token = flask.request.headers.get("Refresh-Token")
        refresh_token = remove_bearer_from_token(refresh_token) if refresh_token else None

        if not refresh_token:
            raise Exception(
                "Request failed as invalid refresh token provided. A valid refresh token is required to obtain an acess token"
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

            response = {"token": new_auth_token}

            return flask.current_app.response_class(
                response=json.dumps(response), status=200, mimetype="application/json"
            )

        except Exception:
            raise Exception("Failed to create a new auth token")
