import json

import flask

from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostCreateRequest,
    PostsGetFilter,
)
from api.utils import rest_utils

blueprint = flask.Blueprint("posts", __name__)

auth = rest_utils.auth


@blueprint.route("/posts/", methods=["POST"])
@auth
def post_create():
    data = flask.request.json

    post_create_request = PostCreateRequest(
        owner_id=data.get("owner_id", None),
        content=data.get("content", None),
    )

    post_result = flask.current_app.conns.midlayer.post_create(post_create_request)
    post = post_result.post

    attachment_file_ids = data.get("attachment_file_ids", None)
    attachment_file_ids = json.loads(attachment_file_ids) if attachment_file_ids else None
    attachment_dicts = []

    if attachment_file_ids and len(attachment_file_ids) > 0:
        attachment_create_request = PostAttachmentsCreateRequest(
            post_id=post.id, file_ids=attachment_file_ids
        )

        attachment_result = flask.current_app.conns.midlayer.post_attachments_create(
            attachment_create_request
        )

        for attachment in attachment_result.post_attachments:
            attachment_dicts.append(vars(attachment))

    response = {}
    response["post"] = vars(post_result.post)
    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/posts/<int:post_id>", methods=["GET"])
@auth
def post_get(post_id: int):
    data = flask.request.json

    if not post_id:
        raise Exception("Invalid request. Must provide a valid post_id")

    posts_get_filter = PostsGetFilter(post_ids=[post_id], is_deleted=False)

    posts_get_result = self.current_app.conns.midlayer.posts_get(posts_get_filter)
