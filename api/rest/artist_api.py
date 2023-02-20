import json

import flask

from api.typings.artists import ArtistsGetFilter
from api.utils import rest_utils
from api.utils.rest_utils import auth, get_set_request_param

blueprint = flask.Blueprint("artists", __name__)


@blueprint.route("/artists/", methods=["GET"])
@auth
def artists_get():
    print(flask.request.values)
    uuids = get_set_request_param(parameter_name="uuid[]", type=str)

    print("uuids: ", uuids)

    artists_get_filter = ArtistsGetFilter(uuids=uuids)

    artists = flask.current_app.conns.midlayer.artists_get(artists_get_filter).artists

    response = {}
    artist_dicts = [rest_utils.class_to_dict(artist) for artist in artists]

    response["artists"] = artist_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
