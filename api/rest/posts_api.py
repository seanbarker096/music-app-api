import json

import flask
from api.typings.posts import PostCreateRequest

blueprint = flask.Blueprint("posts", __name__)


@blueprint.route("/posts/", methods=["POST"])
def post_create(self):
    data = flask.request.data

    post_create_request = PostCreateRequest(
        owner_id="TEMP", content=data.content, attachment_id=flask.data.attachment_id
    )

    result = self.conns.midlayer.post_create(post_create_request)

    response = {}
    response["post"] = vars(result.post)

    response = flask.current_app.response_class(
        response=json.dumps(result), status=200, mimetype="application/json"
    )
