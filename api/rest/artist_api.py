import json

import flask

from api.typings.artists import ArtistsGetFilter
from api.utils import rest_utils
from api.utils.rest_utils import get_set_request_param

blueprint = flask.Blueprint("artists", __name__)


@blueprint.route("/artists/", methods=["GET"])
def artists_get():

    uuids = get_set_request_param(parameter_name="user_ids[]", type=int)

    artists_get_filter = ArtistsGetFilter(uuids=uuids)

    artists = flask.current_app.conns.midlayer.artists_get(artists_get_filter).artists

    response = {}
    artist_dicts = [rest_utils.class_to_dict(artist) for artist in artists]

    response["artists"] = artist_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
