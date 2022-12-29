import json
from unittest.mock import Mock

import flask

from api.typings.users import UserUpdateRequest, UserUpdateResult
from api.utils.rest_utils import auth, process_string_request_param

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/users/<int:user_id>", methods=["PATCH"])
@auth
def user_update(user_id: int):
    print("running")
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
