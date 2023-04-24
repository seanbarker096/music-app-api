import json

import flask

from api.typings.features import (
    FeatureCreateRequest,
    FeaturedEntityType,
    FeaturerType,
    FeaturesDeleteRequest,
    FeaturesGetFilter,
)
from api.utils.rest_utils import (
    auth,
    class_to_dict,
    process_api_set_request_param,
    process_enum_api_request_param,
    process_int_api_request_param,
)
from exceptions.exceptions import InvalidArgumentException

blueprint = flask.Blueprint("features", __name__)


@blueprint.route("/features/", methods=["GET"])
@auth
def features_get():
    featurer_type = process_enum_api_request_param("featurer_type", FeaturerType)
    featurer_id = process_int_api_request_param("featurer_id")
    featured_entity_type = process_enum_api_request_param("featured_entity_type", FeaturedEntityType)
    featured_entity_id = process_int_api_request_param("featured_entity_id")

    if (
        not featurer_id
        and not featurer_type
        and not featured_entity_id
        and not featured_entity_type
    ):
        raise InvalidArgumentException(
            "Must provide at least one filter field", json.dumps(flask.request.values)
        )

    features_get_filter = FeaturesGetFilter(
        featurer_type=featurer_type,
        featurer_id=featurer_id,
        featured_entity_type=featured_entity_type,
        featured_entity_id=featured_entity_id,
    )

    features = flask.current_app.conns.midlayer.features_get(features_get_filter).features

    response = {}
    feature_dicts = [class_to_dict(feature) for feature in features]

    response["features"] = feature_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


#TODO: Delete this api endpoint as dont think its used anymore
@blueprint.route('/posts/', methods=['GET'])
@auth
def get_users_posts_features():
    """
    Get all features for all posts owned by a user
    """
    post_owner_id = process_int_api_request_param(parameter_name='post_owner_id', optional=False)
    featurer_type = process_enum_api_request_param(parameter_name='featurer_type', enum=FeaturerType, optional=False)

    features = flask.current_app.conns.midlayer.get_users_posts_features(post_owner_id=post_owner_id, featurer_type=featurer_type).features


    # Sort all features by their post id
    features_by_post_id = {}
    for feature in features:
        if feature.featured_entity_id not in features_by_post_id:
            features_by_post_id[feature.featured_entity_id] = []
        features_by_post_id[feature.featured_entity_id].append(class_to_dict(feature))

    features_by_post_id_arr = []
    for key, val in features_by_post_id.items():
        features_by_post_id_arr.append(
            {
                key: val
            }
        )
        
    response = {}
    response["features_by_post_id"] = features_by_post_id_arr

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/features/", methods=["POST"])
@auth
def feature_create():

    data = flask.request.get_json()

    featured_entity_type = data.get("featured_entity_type", None)
    featured_entity_id = data.get("featured_entity_id", None)
    featurer_type = data.get("featurer_type", None)
    featurer_id = data.get("featurer_id", None)

    if not featured_entity_type or not featured_entity_id or not featurer_type or not featurer_id:
        raise InvalidArgumentException("Missing required field in request", json.dumps(data))

    creator_id = int(flask.g.auth_user.user_id)

    feature_create_request = FeatureCreateRequest(
        featured_entity_type=featured_entity_type,
        featured_entity_id=featured_entity_id,
        featurer_type=featurer_type,
        featurer_id=featurer_id,
        creator_id=creator_id,
    )

    feature = flask.current_app.conns.midlayer.feature_create(feature_create_request).feature

    response = {}
    response["feature"] = class_to_dict(feature)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

@blueprint.route("/features/", methods=["DELETE"])
@auth
def feature_delete():
    feature_ids = process_api_set_request_param(parameter_name="ids[]", type=int, optional=False)

    tag_delete_request = FeaturesDeleteRequest(ids=feature_ids) 
    flask.current_app.conns.midlayer.features_delete(request=tag_delete_request)

    return flask.current_app.response_class(status=204, mimetype="application/json")
