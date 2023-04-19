import datetime
import json

import flask

from api.typings.events import EventCreateRequest, EventsGetFilter, EventType
from api.typings.performances import (
    PerformanceCreateRequest,
    PerformancesGetFilter,
    PerformancesGetProjection,
)
from api.utils.rest_utils import (
    auth,
    class_to_dict,
    process_api_set_request_param,
    process_bool_api_request_param,
    process_enum_request_param,
    process_int_api_request_param,
    process_int_request_param,
    process_string_request_param,
)

blueprint = flask.Blueprint("performances", __name__)


@blueprint.route("/performances/", methods=["GET"])
@auth
def performances_get():
    performance_ids = process_api_set_request_param(parameter_name="ids[]", type=int, optional=True)

    performer_ids = process_api_set_request_param(
        parameter_name="performer_ids[]", type=int, optional=True
    )

    performance_date = process_int_api_request_param(
        parameter_name="performance_date", optional=True
    )

    attendee_ids = process_api_set_request_param(
        parameter_name="attendee_ids[]", type=int, optional=True
    )

    include_attendance_count = process_bool_api_request_param(
        parameter_name="include_attendance_count", optional=True
    )

    filter = PerformancesGetFilter(
        attendee_ids=attendee_ids,
        ids=performance_ids,
        performer_ids=performer_ids,
        performance_date=performance_date,
    )

    projection = PerformancesGetProjection(
        include_attendance_count=include_attendance_count
    )

    performances = flask.current_app.conns.midlayer.performances_get(filter, projection).performances

    response = {}
    response["performances"] = [class_to_dict(performance) for performance in performances]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/performances/", methods=["POST"])
@auth
def performance_create():
    data = flask.request.json

    performer_id = process_int_request_param(
        parameter_name="performer_id", parameter=data.get("performer_id", None), optional=False
    )
    performance_date_unix_timestamp = process_int_request_param(
        parameter_name="performance_date",
        parameter=data.get("performance_date", None),
        optional=False,
    )

    venue_name = process_string_request_param(
        parameter_name="venue_name", parameter=data.get("venue_name", None), optional=False
    )

    event_start_date_unix_timestamp = process_int_request_param(
        parameter_name="event_start_date",
        parameter=data.get("event_start_date", None),
        optional=False,
    )

    event_end_date_unix_timestamp = process_int_request_param(
        parameter_name="event_end_date", parameter=data.get("event_end_date", None), optional=False
    )

    event_type = process_enum_request_param(
        parameter_name="event_type",
        enum=EventType,
        parameter=data.get("event_type", None),
        optional=False,
    )

    performance_date = datetime.datetime.fromtimestamp(performance_date_unix_timestamp)
    # Extract date part from datetime object
    performance_date = performance_date.date()

    event_start_date = datetime.datetime.fromtimestamp(event_start_date_unix_timestamp)
    event_start_date = event_start_date.date()

    event_end_date = datetime.datetime.fromtimestamp(event_end_date_unix_timestamp)
    event_end_date = event_end_date.date()

    if performance_date > event_end_date or performance_date < event_start_date:
        raise Exception("Performance date must fall within event dates")

    ## check if event exists. If it doesn't then create it
    event_filter = EventsGetFilter(
        start_date=event_start_date_unix_timestamp,
        end_date=event_end_date_unix_timestamp,
        venue_name=venue_name,
    )

    events = flask.current_app.conns.midlayer.events_get(event_filter).events

    if len(events) == 0:
        event_create_request = EventCreateRequest(
            start_date=event_start_date_unix_timestamp,
            end_date=event_end_date_unix_timestamp,
            venue_name=venue_name,
            event_type=event_type,
        )

        event = flask.current_app.conns.midlayer.event_create(event_create_request).event

    else:
        event = events[0]

    event_id = event.id

    performance_create_request = PerformanceCreateRequest(
        event_id=event_id,
        performer_id=performer_id,
        performance_date=performance_date_unix_timestamp,
    )

    performance = flask.current_app.conns.midlayer.performance_create(
        performance_create_request
    ).performance

    response = {}
    response["performance"] = vars(performance)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/attendances/", methods=["POST"])
@auth
def attendance_create():
    request = flask.request.json

    performance_id = process_int_request_param(
        parameter_name="performance_id",
        parameter=request.get("performance_id", None),
        optional=False,
    )

    attendee_id = process_int_request_param(
        parameter_name="attendee_id",
        parameter=request.get("attendee_id", None),
        optional=False,
    )

    attendance = flask.current_app.conns.midlayer.attendance_create(
        performance_id=performance_id, attendee_id=attendee_id
    ).attendance

    response = {}
    response["attendance"] = vars(attendance)

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
