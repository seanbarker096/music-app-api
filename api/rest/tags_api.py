import json

import flask

from api.typings.tags import TagCreateRequest, TaggedEntityType, TagsGetFilter
from api.utils.rest_utils import (
    auth,
    class_to_dict,
    process_enum_request_param,
    process_int_api_request_param,
)
from exceptions.exceptions import InvalidArgumentException

blueprint = flask.Blueprint("tags", __name__)


@blueprint.route("/tags/", methods=["POST"])
@auth
def tag_create():
    data = flask.request.get_json()

    tagged_in_entity_type = data.get("tagged_in_entity_type", None)
    tagged_in_entity_id = data.get("tagged_in_entity_id", None)
    tagged_entity_type = data.get("tagged_entity_type", None)
    tagged_entity_id = data.get("tagged_entity_id", None)
    creator_id = data.get("creator_id", None)

    if (
        not tagged_in_entity_type
        or not tagged_in_entity_id
        or not tagged_entity_type
        or not tagged_entity_id
        or not creator_id
    ):
        raise InvalidArgumentException("Missing required field in request", json.dumps(data))

    tag_create_request = TagCreateRequest(
        tagged_in_entity_type=tagged_in_entity_type,
        tagged_in_entity_id=tagged_in_entity_id,
        tagged_entity_type=tagged_entity_type,
        tagged_entity_id=tagged_entity_id,
        creator_id=creator_id,
    )

    tag = flask.current_app.conns.midlayer.tag_create(tag_create_request).tag

    response = {}
    response["tag"] = class_to_dict(tag)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/tags/", methods=["GET"])
@auth
def tags_get():
    tagged_entiy_id = process_int_api_request_param("tagged_entity_id")
    tagged_entity_type = process_enum_request_param("tagged_entity_type", TaggedEntityType)

    request = TagsGetFilter(tagged_entity_id=tagged_entiy_id, tagged_entity_type=tagged_entity_type)

    tags = flask.current_app.conns.midlayer.tags_get(request).tags

    response = {}
    response["tags"] = [class_to_dict(tag) for tag in tags]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
