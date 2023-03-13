from typing import Optional

from api.dao.performances_dao import PerformancesDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.performances import PerformanceCreateRequest
from api.utils.rest_utils import process_int_request_param


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
