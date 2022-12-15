import json

import flask

from api.typings.posts import PostAttachmentsCreateRequest, PostCreateRequest
from api.utils import rest_utils

blueprint = flask.Blueprint("posts", __name__)

auth = rest_utils.auth


@auth
@blueprint.route("/posts/", methods=["POST"])
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
