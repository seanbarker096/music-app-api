from typing import List, Optional


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


class PerformancesGetFilter:
    ids: Optional[list[int]] = ...
    performer_ids: Optional[list[int]] = ...
    performance_date: Optional[int] = ...

    def __init__(
        self,
        ids: Optional[list[int]] = None,
        performer_ids: Optional[list[int]] = None,
        performance_date: Optional[int] = None,
    ) -> None:
        self.ids = ids
        self.performer_ids = performer_ids
        self.performance_date = performance_date


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


class PerformanceCreateResult:
    performance: Performance = ...

    def __init__(
        self,
        performance: Performance,
    ) -> None:
        self.performance = performance


class PerformanceAttendance:
    id: int = ...
    performance_id: int = ...
    attendee_id: int = ...
    create_time: int = ...

    def __init__(
        self,
        id: int,
        performance_id: int,
        attendee_id: int,
        create_time: int,
    ) -> None:
        self.id = id
        self.performance_id = performance_id
        self.attendee_id = attendee_id
        self.create_time = create_time


class PerformanceAttendanceCreateRequest:
    performance_id: int = ...
    attendee_id: int = ...

    def __init__(
        self,
        performance_id: int,
        attendee_id: int,
    ) -> None:
        self.performance_id = performance_id
        self.attendee_id = attendee_id


class PerformanceAttendanceCreateResult:
    performance_attendance: PerformanceAttendance = ...

    def __init__(
        self,
        performance_attendance: PerformanceAttendance,
    ) -> None:
        self.performance_attendance = performance_attendance
