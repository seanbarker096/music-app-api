from typing import Optional


class Performance:
    id: int = ...
    venue_id: Optional[int] = ...
    performer_id: int = ...
    performance_date: int = ...
    create_time: int = ...
    update_time: int = ...

    def __init__(
        self,
        id: int,
        performer_id: int,
        performance_date: int,
        create_time: int,
        update_time: int,
        venue_id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.venue_id = venue_id
        self.performer_id = performer_id
        self.performance_date = performance_date
        self.create_time = create_time
        self.update_time = update_time


class PerformanceCreateRequest:
    venue_id: Optional[int] = ...
    performer_id: int = ...
    performance_date: int = ...

    def __init__(
        self,
        performer_id: int,
        performance_date: int,
        venue_id: Optional[int] = None,
    ) -> None:
        self.venue_id = venue_id
        self.performer_id = performer_id
        self.performance_date = performance_date
