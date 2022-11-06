import json

import flask

from api.authentication_service.typings import (
    AuthStateCreateRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
)
from api.typings.auth import LoginResult
from api.typings.users import User, UsersGetFilter

blueprint = flask.blueprint("auth", __name__)


@blueprint.route("/login/", methods=["POST"])
def login(self):
    request = flask.request.json

    password = request.get("password", None)
    username = request.get("username", None)

    if not password or not username:
        raise Exception("Must provide username and password")

    if not isinstance(password, str) or len(password) == 0:
        raise Exception("Invalid argument password. Password must be a valid string")

    if not isinstance(username, str) or len(username) == 0:
        raise Exception("Invalid argument username. Username must be a valid string")

    filter = UsersGetFilter(password=request["password"], username=request["username"])
    user = flask.current_app.conns.midlayer.get_user_by_username_and_password(filter)

    auth_state_request = AuthStateCreateRequest(
        auth_user=AuthUser(user_id=user.id, role=AuthUserRole.USER)
    )

    result = flask.current_app.conns.auth_service.create_auth_state(request=auth_state_request)

    auth_state = result.auth_state

    ## This shouldn't really happen. If auth failed an error should be thrown
    if auth_state.status != AuthStatus.AUTHENTICATED.value:
        raise Exception(f"Failed to authenticate user with id {user.id}")

    response = {
        "user_id": auth_state.auth_user.user_id,
        "token": auth_state.access_token,
        "r_token": auth_state.refresh_token,
    }

    response = flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

    response.headers["Authorization"] = f"Bearer {auth_state.access_token}"

    return response
