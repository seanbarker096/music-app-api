import json

import flask

from api.typings.performances import PerformanceCreateRequest, PerformancesGetFilter
from api.utils.rest_utils import (
    class_to_dict,
    process_api_set_request_param,
    process_bool_api_request_param,
    process_int_api_request_param,
    process_int_request_param,
    process_string_api_request_param,
)

blueprint = flask.Blueprint("performances", __name__)


@blueprint.route("/performances/", methods=["GET"])
def performances_get():
    performance_ids = process_api_set_request_param(parameter_name="ids[]", type=int, optional=True)

    performer_ids = process_api_set_request_param(
        parameter_name="performer_ids[]", type=int, optional=True
    )

    performance_date = process_int_api_request_param(
        parameter_name="performance_date", optional=True
    )

    performances = flask.current_app.conns.midlayer.performances_get(
        PerformancesGetFilter(
            ids=performance_ids, performer_ids=performer_ids, performance_date=performance_date
        )
    ).performances

    response = {}
    response["performances"] = [class_to_dict(performance) for performance in performances]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/performances/", methods=["POST"])
def performance_create():
    data = flask.request.json

    venue_id = process_int_request_param(
        parameter_name="venue_id", parameter=data.get("venue_id", None), optional=True
    )
    performer_id = process_int_request_param(
        parameter_name="performer_id", parameter=data.get("performer_id", None), optional=False
    )
    performance_date = process_int_request_param(
        parameter_name="performance_date",
        parameter=data.get("performance_date", None),
        optional=False,
    )

    performance_create_request = PerformanceCreateRequest(
        venue_id=venue_id,
        performer_id=performer_id,
        performance_date=performance_date,
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

@blueprint.route('attendees/<int:attendee_id>/performers', methods=['GET'])
def attendee_performers_get(attendee_id: int):
    """
    Get all performers whos performances the user has attended
    """
    
    get_counts = process_bool_api_request_param('count', optional=True)
    get_counts = get_counts if get_counts else False

    sort = process_string_api_request_param('sort', optional=True)


    if sort not in ['count']:
        raise Exception(f"Invalid sort parameter: {sort}. Valid values are: 'count'")
    

    filter = AttendeePerformersGetFilter(
        attendee_id=attendee_id,
        get_counts=get_counts,
        sort=sort
    )

    performers = flask.current_app.conns.midlayer.attendee_performers_get(filter=filter).performers

    response = {}
    response['performers'] = [class_to_dict(performer) for performer in performers]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype='application/json'
    )
