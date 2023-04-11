from typing import Optional


class PerformanceFixtureDTO:

    def __init__(
        self,
        performer_id: int,
        performance_date: int,
        create_time: int,
        update_time: Optional[int] = None,
        event_id: Optional[int] = None
        ):
        self.performer_id = performer_id
        self.performance_date = performance_date
        self.create_time = create_time
        self.update_time = update_time
        self.event_id = event_id

    def get_performer_id(self) -> int:
        return self.performer_id
    
    def get_performance_date(self) -> int:
        return self.performance_date
    
    def get_create_time(self) -> int:
        return self.create_time
    
    def get_update_time(self) -> int:
        return self.update_time
    
    def get_event_id(self) -> Optional[int]:
        return self.event_id