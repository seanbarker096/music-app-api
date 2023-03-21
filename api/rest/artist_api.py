import json

import flask

from api.typings.artists import ArtistsGetFilter
from api.utils import rest_utils
from api.utils.rest_utils import auth, process_api_set_request_param
from exceptions.exceptions import InvalidArgumentException

blueprint = flask.Blueprint("artists", __name__)


@blueprint.route("/artists/", methods=["GET"])
@auth
def artists_get():
    uuids = process_api_set_request_param(parameter_name="uuids[]", type=str)
    ids = process_api_set_request_param(parameter_name="ids[]", type=int)

    artists_get_filter = ArtistsGetFilter(uuids=uuids, ids=ids)

    artists = flask.current_app.conns.midlayer.artists_get(artists_get_filter).artists

    response = {}
    artist_dicts = [rest_utils.class_to_dict(artist) for artist in artists]

    response["artists"] = artist_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/artist/<string:uuid>", methods=["GET"])
@auth
def artist_get_or_create(uuid: str):
    artist = flask.current_app.conns.midlayer.artist_get_or_create(uuid=uuid).artists[0]
    artist_dict = rest_utils.class_to_dict(artist)

    return flask.current_app.response_class(
        response=json.dumps(artist_dict), status=200, mimetype="application/json"
    )


@blueprint.route("/artists/search/", methods=["POST"])
@auth
def artists_search():
    data = flask.request.json

    search_query = data.get("search_query", None)

    if not search_query or not isinstance(search_query, str):
        raise InvalidArgumentException("Must provide a search query", search_query)

    result = flask.current_app.conns.midlayer.artist_search(search_query)

    artists = result.artists
    artist_dicts = [rest_utils.class_to_dict(artist) for artist in artists]

    response = {}
    response["artists"] = artist_dicts
    response["total"] = result.total
    response["offset"] = result.offset
    response["limit"] = result.limit
    response["next"] = result.next
    response["previous"] = result.previous

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
