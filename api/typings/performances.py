from typing import List, Optional


class Performance:
    id: int = ...
    event_id: Optional[int] = ...
    performer_id: int = ...
    performance_date: int = ...
    create_time: int = ...
    update_time: int = ...
    attendance_count: Optional[int] = ...

    def __init__(
        self,
        id: int,
        performer_id: int,
        performance_date: int,
        create_time: int,
        update_time: int,
        event_id: Optional[int] = None,
        attendance_count: Optional[int] = None,
    ) -> None:
        self.id = id
        self.event_id = event_id
        self.performer_id = performer_id
        self.performance_date = performance_date
        self.create_time = create_time
        self.update_time = update_time
        self.attendance_count = attendance_count


class PerformancesGetFilter:
    attendee_ids: Optional[list[int]] = ...
    ids: Optional[list[int]] = ...
    performer_ids: Optional[list[int]] = ...
    performance_date: Optional[int] = ...

    def __init__(
        self,
        attendee_ids: Optional[list[int]] = None,
        ids: Optional[list[int]] = None,
        performer_ids: Optional[list[int]] = None,
        performance_date: Optional[int] = None,
    ) -> None:
        self.attendee_ids = attendee_ids
        self.ids = ids
        self.performer_ids = performer_ids
        self.performance_date = performance_date


class PerformancesGetProjection:
    include_attendance_count: Optional[bool] = ...

    def __init__(
        self,
        include_attendance_count: Optional[bool] = False,
    ) -> None:
        self.include_attendance_count = include_attendance_count


class PerformancesGetResult:
    performances: List[Performance] = ...

    def __init__(
        self,
        performances: List[Performance],
    ) -> None:
        self.performances = performances


class PerformanceCreateRequest:
    event_id: int = ...
    performer_id: int = ...
    performance_date: int = ...

    def __init__(
        self,
        performer_id: int,
        performance_date: int,
        event_id: int,
    ) -> None:
        self.event_id = event_id
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


class PerformanceCounts:
    performance_id: int = ...
    attendee_count: Optional[int] = ...
    tag_count: Optional[int] = ...
    features_count: Optional[int] = ...

    def __init__(
        self,
        performance_id: int,
        attendee_count: Optional[int] = None,
        tag_count: Optional[int] = None,
        features_count: Optional[int] = None,
    ) -> None:
        self.performance_id = performance_id
        self.attendee_count = attendee_count
        self.tag_count = tag_count
        self.features_count = features_count


class PerformancesCountsGetResult:
    performances: List[Performance] = ...
    counts: List[PerformanceCounts] = ...

    def __init__(
        self,
        performances: List[Performance],
        counts: List[PerformanceCounts],
    ) -> None:
        self.performances = performances
        self.counts = counts
