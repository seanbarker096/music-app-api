import json
from typing import Optional

from api.dao.events_dao import EventsDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.events import (
    EventCreateRequest,
    EventCreateResult,
    EventsGetFilter,
    EventsGetResult,
    EventType,
)
from api.utils.rest_utils import (
    process_enum_request_param,
    process_int_request_param,
    process_string_request_param,
)
from exceptions.exceptions import InvalidArgumentException


class EventsMidlayerConnections:
    def __init__(self, config, events_dao: Optional[EventsDAO] = None):
        self.events_dao = events_dao if events_dao else EventsDAO(config)

class EventsMidlayerMixin(BaseMidlayerMixin):
    
    def __init__(self, config, conns: Optional[EventsMidlayerConnections] = None):
        self.events_dao = conns.events_dao if conns and conns.events_dao else EventsDAO(config)
        super().__init__(config)

    def event_create(self, request: EventCreateRequest) -> EventCreateResult:
        process_int_request_param(
            parameter_name="start_date", parameter=request.start_date, optional=False
        )
        process_int_request_param(
            parameter_name="end_date", parameter=request.end_date, optional=False
        )
        process_enum_request_param(
            parameter_name="event_type", parameter=request.event_type, enum=EventType, optional=False
        )
        process_string_request_param(
            parameter_name="venue_name", parameter=request.venue_name, optional=False
        )
        process_string_request_param(
            parameter_name="name", parameter=request.name, optional=True
        )

        ## If event name isn't set, then use venue name. This could be the case for things like festivals, or just when the event is simply a performance at a given venue
        if request.name is None:
            request.name = request.venue_name
        
        if request.start_date > request.end_date:
            raise InvalidArgumentException(
                f"Start date must be before end date. Request: {json.dumps(vars(request))}",
                "start_date",
            )

        try:
            event = self.events_dao.event_create(request)

            return EventCreateResult(event=event)

        except Exception as e:
            raise Exception(
                f"Failed to create event because {str(e)}. Request: {json.dumps(vars(request))}"
            )        

    def events_get(self, filter: EventsGetFilter):
        process_string_request_param("venue_name", filter.venue_name)
        process_int_request_param("start_date", filter.start_date)
        process_int_request_param("end_date", filter.end_date)

        if (
            not filter.start_date
            and not filter.end_date
            and not filter.venue_name
        ):
            raise InvalidArgumentException(
                f"At least one filter field must be provided. Filter: {json.dumps(vars(filter))}",
                "filter",
            )

        try:
            events = self.events_dao.events_get(filter=filter)

            return EventsGetResult(events=events)

        except Exception as e:
            raise Exception(
                f"Failed to get events because {str(e)}. Filter: {json.dumps(vars(filter))}"
            )
