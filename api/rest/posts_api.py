import json

import flask

from api.typings.posts import PostCreateRequest
from api.utils import rest_utils

blueprint = flask.Blueprint("posts", __name__)

auth = rest_utils.auth


@auth
@blueprint.route("/posts/", methods=["POST"])
def post_create():
    data = flask.request.json

    post_create_request = PostCreateRequest(
        owner_id=123, content=data["content"], attachment_id=data.get("attachment_id", None)
    )

    result = flask.current_app.conns.midlayer.post_create(post_create_request)

    response = {}
    response["post"] = vars(result.post)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
