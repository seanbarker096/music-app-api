import json

import flask

from api.typings.performances import PerformanceCreateRequest
from api.utils.rest_utils import process_int_request_param

blueprint = flask.Blueprint("performances", __name__)


@blueprint.route("/performances/", method=["POST"])
def performance_create():
    data = flask.request.json

    venue_id = process_int_request_param(
        parameter_name="venue_id", parameter=data.get("venue_id", None), optional=False
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


@blueprint.route("/attendances/", method=["POST"])
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