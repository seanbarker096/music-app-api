
import json

import flask

from api.typings.events import EventsGetFilter
from api.utils.rest_utils import auth, class_to_dict, process_api_set_request_param

blueprint = flask.Blueprint("events", __name__)

@blueprint.route("/events/", methods=["GET"])
@auth
def events_get():
    event_ids = process_api_set_request_param(
        parameter_name="ids[]", type=int, optional=False
    )

    events_get_filter = EventsGetFilter(
        ids=event_ids
    )
    events = flask.current_app.conns.midlayer.events_get(filter=events_get_filter).events
    response = {}

    response["events"] = [class_to_dict(event) for event in events]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
