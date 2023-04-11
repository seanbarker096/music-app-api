import json
from typing import Optional

from api.dao.performances_dao import PerformanceAttendancesDAO, PerformancesDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.performances import (
    PerformanceAttendanceCreateRequest,
    PerformanceAttendanceCreateResult,
    PerformanceCreateRequest,
    PerformanceCreateResult,
    PerformancesCountsGetFilter,
    PerformancesCountsGetResult,
    PerformancesGetFilter,
    PerformancesGetResult,
)
from api.utils.rest_utils import process_bool_request_param, process_int_request_param
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import PerformanceNotFoundException


class PerformancesMidlayerConnections:
    def __init__(self, config, performances_dao: Optional[PerformancesDAO] = None):
        self.performances_dao = performances_dao if performances_dao else PerformancesDAO(config)


class PerformancesMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[PerformancesMidlayerConnections] = None):
        self.performances_dao = conns.performances_dao if conns and conns.performances_dao else PerformancesDAO(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def performance_create(self, request: PerformanceCreateRequest):
        process_int_request_param(
            parameter_name="event_id", parameter=request.event_id, optional=True
        )
        process_int_request_param(
            parameter_name="performer_id", parameter=request.performer_id, optional=False
        )
        process_int_request_param(
            parameter_name="performance_date",
            parameter=request.performance_date,
            optional=False,
        )

        try:
            performance = self.performances_dao.performance_create(request)

            return PerformanceCreateResult(performance=performance)

        except Exception as e:
            raise Exception(
                f"Failed to create performance because {str(e)}. Request: {vars(request)}"
            )

    def performances_get(self, filter: PerformancesGetFilter):
        if filter.ids and len(filter.ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for filter field ids: {filter.ids}. At least one post_id must be provided",
                "filter.ids",
            )

        if filter.performer_ids and len(filter.performer_ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for filter field performer_ids: {filter.performer_ids}. At least one performer_id must be provided",
                "filter.performer_ids",
            )

        if filter.attendee_ids and len(filter.attendee_ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for filter field attendee_ids: {filter.attendee_ids}. At least one attendee_id must be provided",
                "filter.attendee_ids",
            )

        process_int_request_param("performance_date", filter.performance_date)

        if (
            not filter.ids
            and not filter.performer_ids
            and not filter.performance_date
            and not filter.attendee_ids
        ):
            raise InvalidArgumentException(
                f"At least one filter field must be provided. Filter: {json.dumps(vars(filter))}",
                "filter",
            )

        try:
            performances = self.performances_dao.performances_get(filter=filter)

            return PerformancesGetResult(performances=performances)

        except Exception as e:
            raise Exception(
                f"Failed to get performances because {str(e)}. Filter: {json.dumps(vars(filter))}"
            )

    def performance_counts_get(self, filter: PerformancesCountsGetFilter):
        if not filter.performance_ids or (
            filter.performance_ids and len(filter.performance_ids) == 0
        ):
            raise InvalidArgumentException(
                f"Invalid value provided for filter field performance_ids: {filter.performance_ids}. At least one performance_id must be provided",
                "filter.performance_ids",
            )

        process_bool_request_param(
            "include_attendee_count", filter.include_attendee_count, optional=True
        )
        process_bool_request_param("include_tag_count", filter.include_tag_count, optional=True)
        process_bool_request_param(
            "include_features_count", filter.include_features_count, optional=True
        )

        if (
            not filter.include_attendee_count
            and not filter.include_tag_count
            and not filter.include_featured_post_count
        ):
            raise InvalidArgumentException(
                f"At least one count filter field must be provided. Filter: {json.dumps(vars(filter))}",
                "filter",
            )

        try:
            return self.performances_dao.performances_counts_get(filter=filter)

        except Exception as e:
            raise Exception(
                f"Failed to get performance counts because {str(e)}. Filter: {json.dumps(vars(filter))}"
            )


class PerformanceAttendancesMidlayerConnections:
    def __init__(
        self, config, performance_attendances_dao: Optional[PerformanceAttendancesDAO] = None
    ):
        self.performance_attendances_dao = (
            performance_attendances_dao
            if performance_attendances_dao
            else PerformanceAttendancesDAO(config)
        )


class PerformanceAttendancesMidlayerMixin(BaseMidlayerMixin):
    def __init__(
        self,
        config,
        conns: Optional[PerformanceAttendancesMidlayerConnections] = None,
        performances_mid: Optional[PerformancesMidlayerMixin] = None,
    ):
        self.performances_mid = (
            performances_mid if performances_mid else PerformancesMidlayerMixin(config)
        )

        self.performance_attendances_dao = conns.performance_attendances_dao if conns and conns.performance_attendances_dao else PerformanceAttendancesDAO(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def performance_attendance_create(
        self, request: PerformanceAttendanceCreateRequest
    ) -> PerformanceAttendanceCreateResult:

        process_int_request_param(
            parameter_name="performance_id",
            parameter=request.performance_id,
            optional=False,
        )
        process_int_request_param(
            parameter_name="attendee_id", parameter=request.attendee_id, optional=False
        )

        try:
            # Check if the performance exists
            filter = PerformancesGetFilter(ids=[request.performance_id])

            performances = self.performances_mid.performances_get(filter=filter).performances

            if len(performances) == 0:
                raise PerformanceNotFoundException(
                    f"Failed to create performance attendance for performance with id {request.performance_id} and user {request.attendee_id} because the performance could not be found"
                )

            if len(performances) > 1:
                raise Exception(
                    f"Failed to create performance attendance for performance with id {request.performance_id} and user {request.attendee_id} because multiple performances were found"
                )

            if performances[0].id != request.performance_id:
                raise Exception(
                    f"Failed to create performance attendance for performance with id {request.performance_id} and user {request.attendee_id}. Failed when checking if performance exists because a different performance than the requested one was returned. "
                )

            performance_attendance = self.performance_attendances_dao.performance_attendance_create(
                request=request
            )

            return PerformanceAttendanceCreateResult(performance_attendance=performance_attendance)

        except Exception as e:
            raise Exception(
                f"Failed to create performance attendance because {str(e)}. Request: {vars(request)}"
            )
