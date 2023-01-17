import json
from unittest.mock import Mock

import flask

from api.typings.users import UsersGetFilter, UserUpdateRequest
from api.utils.rest_utils import (
    auth,
    get_set_request_param,
    process_string_request_param,
)

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/users/<int:user_id>", methods=["PATCH"])
@auth
def user_update(user_id: int):
    ## TODO: Add update time for user object and update this value in DAO
    request = flask.request.json

    avatar_file_uuid = process_string_request_param(
        request_body=request, parameter_name="avatar_file_uuid"
    )

    user_update_request = UserUpdateRequest(user_id=user_id, avatar_file_uuid=avatar_file_uuid)

    updated_user = flask.current_app.conns.midlayer.user_update(request=user_update_request).user

    # except:
    #     ## TODO: Create custom app exceptions here and handle correct using build_api_error_response.

    response = {}
    response["user"] = vars(updated_user)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/users", methods=["GET"])
@auth
def users_get():
    user_ids = get_set_request_param(parameter_name="user_ids[]", type=int)

    filter = UsersGetFilter(user_ids=user_ids)
    result = flask.current_app.conns.midlayer.users_get(filter)

    response = {}

    user_dicts = []
    for user in result.users:
        user_dicts.append(vars(user))

    response["users"] = user_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/users/<int:user_id>", methods=["GET"])
@auth
def user_get_by_id(user_id: int):
    user = flask.current_app.conns.midlayer.get_user_by_id(user_id)

    response = {}
    response["user"] = vars(user)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
