from unittest.mock import Mock

import flask

from api.typings.users import UserUpdateRequest, UserUpdateResult
from api.utils.rest_utils import auth

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/users/<int:user_id", METHODS=["PATCH"])
@auth
def user_update(self, user_id: int):

    ## TODO: Check if users exists in midlayer
    ...
