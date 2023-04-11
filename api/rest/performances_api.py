import json

import flask

from api.typings.performances import (
    PerformanceCreateRequest,
    PerformancesCountsGetFilter,
    PerformancesGetFilter,
)
from api.utils.rest_utils import (
    auth,
    class_to_dict,
    process_api_set_request_param,
    process_bool_api_request_param,
    process_int_api_request_param,
    process_int_request_param,
    process_string_api_request_param,
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

    filter = PerformancesGetFilter(
        attendee_ids=attendee_ids,
        ids=performance_ids,
        performer_ids=performer_ids,
        performance_date=performance_date,
    )
    performances = flask.current_app.conns.midlayer.performances_get(filter).performances

    response = {}
    response["performances"] = [class_to_dict(performance) for performance in performances]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/performances/", methods=["POST"])
@auth
def performance_create():
    data = flask.request.json

    event_id = process_int_request_param(
        parameter_name="event_id", parameter=data.get("event_id", None), optional=True
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
        event_id=event_id,
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


@blueprint.route("/performances/counts/", methods=["GET"])
@auth
def performance_counts_get():
    performance_ids = process_api_set_request_param(parameter_name="performance_ids[]", type=int, optional=False)

    include_attendee_count = process_bool_api_request_param(
        parameter_name="include_attendee_count", optional=True
    )

    include_tag_count = process_bool_api_request_param(
        parameter_name="include_tag_count", optional=True
    )

    include_features_count = process_bool_api_request_param(
        parameter_name="include_features_count", optional=True
    )

    filter = PerformancesCountsGetFilter(
        performance_ids=performance_ids,
        include_attendee_count=include_attendee_count,
        include_tag_count=include_tag_count,
        include_features_count=include_features_count,
    )

    result = flask.current_app.conns.midlayer.performance_counts_get(filter)

    performances = result.performances
    counts = result.counts

    response = {}
    response["performances"] = [class_to_dict(performance) for performance in performances]
    response["counts"] = [class_to_dict(count) for count in counts]

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
