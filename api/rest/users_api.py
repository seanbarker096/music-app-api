import json
from unittest.mock import Mock

import flask

from api.typings.users import UsersGetFilter, UsersGetProjection, UserUpdateRequest
from api.utils.rest_utils import (
    auth,
    class_to_dict,
    process_api_set_request_param,
    process_bool_api_request_param,
    process_int_api_request_param,
    process_string_api_post_request_param,
    process_string_api_request_param,
    process_string_request_param,
)

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/users/<int:user_id>", methods=["PATCH"])
@auth
def user_update(user_id: int):
    ## TODO: Add update time for user object and update this value in DAO
    request = flask.request.json

    print(request)

    avatar_file_uuid = process_string_request_param(
        "avatar_file_uuid", request.get("avatar_file_uuid", None)
    )
    bio = process_string_request_param("bio", request.get("bio", None))
    first_name = process_string_request_param("first_name", request.get("first_name", None))
    second_name = process_string_request_param("second_name", request.get("second_name", None))

    user_update_request = UserUpdateRequest(
        user_id=user_id,
        avatar_file_uuid=avatar_file_uuid,
        bio=bio,
        first_name=first_name,
        second_name=second_name,
    )

    updated_user = flask.current_app.conns.midlayer.user_update(request=user_update_request).user

    response = {}
    response["user"] = vars(updated_user)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/users", methods=["GET"])
@auth
def users_get():
    user_ids = process_api_set_request_param(parameter_name="user_ids[]", type=int)
    include_profile_image = process_bool_api_request_param(
        parameter_name="include_profile_image", optional=True
    )

    filter = UsersGetFilter(user_ids=user_ids)
    projection = UsersGetProjection(include_profile_image=include_profile_image)
    result = flask.current_app.conns.midlayer.users_get(filter, projection)

    response = {}

    user_dicts = []
    for user in result.users:
        user.avatar_file = class_to_dict(user.avatar_file) if user.avatar_file else None
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


@blueprint.route("/search", methods=["GET"])
@auth
def user_search():

    request = flask.request.values

    search_query = process_string_api_request_param(
        parameter_name="search_query",
        parameter=request.get("search_query", None),
        optional=False,
        allow_empty_string=True,
    )

    include_profile_image = process_bool_api_request_param(
        parameter_name="include_profile_image", optional=True
    )

    limit = process_int_api_request_param(parameter_name="limit", optional=True)

    filter = UsersGetFilter(search_query=search_query, limit=limit)
    projection = UsersGetProjection(include_profile_image=include_profile_image)
    result = flask.current_app.conns.midlayer.users_get(filter, projection)

    response = {}

    user_dicts = []
    for user in result.users:
        user.avatar_file = class_to_dict(user.avatar_file) if user.avatar_file else None
        user_dicts.append(class_to_dict(user))

    response["users"] = user_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
