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

    attendee_ids = process_api_set_request_param(
        parameter_name="attendee_ids[]", type=int, optional=True
    )

    filter =  PerformancesGetFilter(
            attendee_ids=attendee_ids,
            ids=performance_ids,
            performer_ids=performer_ids,
            performance_date=performance_date
        )
    performances = flask.current_app.conns.midlayer.performances_get(filter).performances

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

# I need a new endpoint which accepts a list of performance ids, and fetches the number of attendees, the number of tagged posts (tags) and the number of posts that have been featured by the performance. Not all counts need to be returned. The counts the endpoint should return are determine by the following parameters:

# - include_attendee_count: bool
# - include_tag_count: bool
# - include_featured_post_count: bool

# Please write the code for this below:

@blueprint.route("/performances/counts/", methods=["GET"])
def performance_counts_get():
    performance_ids = process_api_set_request_param(parameter_name="ids[]", type=int, optional=True)

    include_attendee_count = process_bool_api_request_param(
        parameter_name="include_attendee_count", optional=True
    )

    include_tag_count = process_bool_api_request_param(
        parameter_name="include_tag_count", optional=True
    )

    include_featured_post_count = process_bool_api_request_param(
        parameter_name="include_featured_post_count", optional=True
    )

    filter =  PerformanceCountsGetFilter(
        performance_ids=performance_ids,
        include_attendee_count=include_attendee_count,
        include_tag_count=include_tag_count,
        include_featured_post_count=include_featured_post_count
    )

    result = flask.current_app.conns.midlayer.performance_counts_get(filter)

    performances = result.performances
    counts = result.counts

    response = {}
    response["performances"] = [class_to_dict(performance) for performance in performances]
    response["counts"] = []

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )