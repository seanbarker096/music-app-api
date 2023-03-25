import json

import flask

from api.typings.performers import PerformersGetFilter
from api.utils import rest_utils
from api.utils.rest_utils import auth, process_api_set_request_param
from exceptions.exceptions import InvalidArgumentException

blueprint = flask.Blueprint("performers", __name__)


@blueprint.route("/performers/", methods=["GET"])
@auth
def performers_get():
    uuids = process_api_set_request_param(parameter_name="uuids[]", type=str)
    ids = process_api_set_request_param(parameter_name="ids[]", type=int)

    performers_get_filter = PerformersGetFilter(uuids=uuids, ids=ids)

    performers = flask.current_app.conns.midlayer.performers_get(performers_get_filter).performers

    response = {}
    performer_dicts = [rest_utils.class_to_dict(performer) for performer in performers]

    response["performers"] = performer_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/performer/<string:uuid>", methods=["GET"])
@auth
def performer_get_or_create(uuid: str):
    performer = flask.current_app.conns.midlayer.performer_get_or_create(uuid=uuid).performers[0]
    performer_dict = rest_utils.class_to_dict(performer)

    return flask.current_app.response_class(
        response=json.dumps(performer_dict), status=200, mimetype="application/json"
    )


@blueprint.route("/performers/search/", methods=["POST"])
@auth
def performers_search():
    data = flask.request.json

    search_query = data.get("search_query", None)

    if not search_query or not isinstance(search_query, str):
        raise InvalidArgumentException("Must provide a search query", search_query)

    result = flask.current_app.conns.midlayer.performer_search(search_query)

    performers = result.performers
    performer_dicts = [rest_utils.class_to_dict(performer) for performer in performers]

    response = {}
    response["performers"] = performer_dicts
    response["total"] = result.total
    response["offset"] = result.offset
    response["limit"] = result.limit
    response["next"] = result.next
    response["previous"] = result.previous

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )

# @blueprint.route('attendees/<int:attendee_id>', methods=['GET'])
# def attendee_performers_get(attendee_id: int):
#     """
#     Get all performers whos performances the user has attended
#     """
    
#     get_counts = process_bool_api_request_param('count', optional=True)
#     get_counts = get_counts if get_counts else False


#     if sort not in ['count']:
#         raise Exception(f"Invalid sort parameter: {sort}. Valid values are: 'count'")
    

#     filter = AttendeePerformersGetFilter(
#         attendee_id=attendee_id,
#         get_counts=get_counts,
#         sort=sort
#     )

#     performers = flask.current_app.conns.midlayer.attendee_performers_get(filter=filter).performers

#     response = {}
#     response['performers'] = [class_to_dict(performer) for performer in performers]

#     return flask.current_app.response_class(
#         response=json.dumps(response), status=200, mimetype='application/json'
#     )