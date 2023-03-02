import json

import flask

from api.typings.features import FeaturesGetFilter
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
