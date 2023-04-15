from enum import Enum
from typing import Optional


class EventType(Enum):
    MUSIC_FESTIVAL = 'music_festival'
    MUSIC_CONCERT = 'music_concert'

class Event:
    start_date: int = ...
    end_date: int = ...
    event_type: EventType = ...
    venue_name: str = ...
    name: str = ...
    create_time: int = ...
    update_time: int = ...

    def __init__(
        self,
        start_date: int,
        end_date: int,
        event_type: EventType,
        venue_name: str,
        name: str,
        create_time: int,
        update_time: int,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.event_type = event_type
        self.venue_name = venue_name
        self.name = name
        self.create_time = create_time
        self.update_time = update_time


class EventCreateRequest:
    start_date: int = ...
    end_date: int = ...
    event_type: EventType = ...
    venue_name: str = ...
    name: str = ...

    def __init__(
        self,
        start_date: int,
        end_date: int,
        event_type: EventType,
        venue_name: str,
        name: str,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.event_type = event_type
        self.venue_name = venue_name
        self.name = name


class EventCreateResult:
    event: Event = ...

    def __init__(self, event: Event):
        self.event = event


class EventsGetFilter:
    start_date: Optional[int] = ...
    end_date: Optional[int] = ...
    venue_name: Optional[str] = ...

    def __init__(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        venue_name: Optional[str] = None,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.venue_name = venue_name


class EventsGetResult:
    events: list[Event] = ...

    def __init__(self, events: list[Event]):
        self.events = events