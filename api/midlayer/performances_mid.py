from typing import Optional

from api.dao.performances_dao import PerformanceAttendancesDAO, PerformancesDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.performances import (
    PerformanceAttendanceCreateRequest,
    PerformanceAttendanceCreateResult,
    PerformanceCreateRequest,
    PerformanceCreateResult,
    PerformancesGetFilter,
)
from api.utils.rest_utils import process_int_request_param
from exceptions.response.exceptions import PerformanceNotFoundException


class PerformancesMidlayerConnections:
    def __init__(self, config, performances_dao: Optional[PerformancesDAO] = None):
        self.performances_dao = performances_dao if performances_dao else PerformancesDAO(config)


class PerformancesMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None):
        connections = (
            conns.performances_mid_conns
            if conns and conns.performances_mid_conns
            else PerformancesMidlayerConnections(config)
        )

        self.performances_dao = connections.performances_dao

        ## Call the next mixins constructor
        super().__init__(config, conns)

    def performance_create(self, request: PerformanceCreateRequest):
        venue_id = process_int_request_param(
            parameter_name="venue_id", parameter=request.venue_id, optional=False
        )
        performer_id = process_int_request_param(
            parameter_name="performer_id", parameter=request.performer_id, optional=False
        )
        performance_date = process_int_request_param(
            parameter_name="performance_date",
            parameter=request.performance_date,
            optional=False,
        )

        try:
            performance = self.performances_dao.performance_create(
                venue_id=venue_id,
                performer_id=performer_id,
                performance_date=performance_date,
            )

            return PerformanceCreateResult(performance=performance)

        except Exception as e:
            raise Exception(
                f"Failed to create performance because {str(e)}. Request: {vars(request)}"
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
        connections: Optional["MidlayerConnections"] = None,
        performances_mid: Optional[PerformancesMidlayerMixin] = None,
    ):
        connections = (
            connections.performance_attendances_mid_conns
            if connections and connections.performance_attendances_mid_conns
            else PerformanceAttendancesMidlayerConnections(config)
        )

        self.performance_attendances_dao = connections.performance_attendances_dao

        self.performances_mid = (
            performances_mid if performances_mid else PerformancesMidlayerMixin(config, connections)
        )

        super().__init__(config, connections)

    def performance_attendance_create(
        self, request: PerformanceAttendanceCreateRequest
    ) -> PerformanceAttendanceCreateResult:

        performance_id = process_int_request_param(
            parameter_name="performance_id",
            parameter=request.performance_id,
            optional=False,
        )
        user_id = process_int_request_param(
            parameter_name="user_id", parameter=request.user_id, optional=False
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
                performance_id=performance_id, user_id=user_id
            )

            return PerformanceAttendanceCreateResult(performance_attendance=performance_attendance)

        except Exception as e:
            raise Exception(
                f"Failed to create performance attendance because {str(e)}. Request: {vars(request)}"
            )
