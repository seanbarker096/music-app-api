import json

import flask

from api.typings.features import FeatureCreateRequest, FeaturesGetFilter
from api.utils.rest_utils import auth, class_to_dict, get_set_request_param
from exceptions.exceptions import InvalidArgumentException

blueprint = flask.Blueprint("features", __name__)


@blueprint.route("/features/", methods=["GET"])
@auth
def features_get():
    data = flask.request.values
    print(data)

    owner_type = data.get("owner_type", None, str)

    owner_id = data.get("owner_id", None, int)

    if not owner_id and not owner_type:
        raise InvalidArgumentException("Must provide at least one filter field", json.dumps(data))

    if owner_type and (not isinstance(owner_type, str) or owner_type == ""):
        raise InvalidArgumentException(
            "Invalid request. owner_type must be a valid string", owner_type
        )

    if owner_id and not isinstance(owner_id, int):
        raise InvalidArgumentException(
            "Invalid request. owner_id must be a valid integer", owner_id
        )

    features_get_filter = FeaturesGetFilter(owner_type=owner_type, owner_id=owner_id)

    features = flask.current_app.conns.midlayer.features_get(features_get_filter).features

    response = {}
    feature_dicts = [class_to_dict(feature) for feature in features]

    response["features"] = feature_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/features/", methods=["POST"])
def feature_create():

    data = flask.request.get_json()

    context_type = data.get("context_type", None, str)
    context_id = data.get("context_id", None, int)
    owner_type = data.get("owner_type", None, str)
    owner_id = data.get("owner_id", None, int)

    if not context_type or not context_id or not owner_type or not owner_id:
        raise InvalidArgumentException("Missing required field in request", json.dumps(data))

    feature_create_request = FeatureCreateRequest(
        context_type=context_type,
        context_id=context_id,
        owner_type=owner_type,
        owner_id=owner_id,
    )

    feature = flask.current_app.conns.midlayer.feature_create(feature_create_request).feature

    response = {}
    response["feature"] = class_to_dict(feature)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
