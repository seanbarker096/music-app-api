class PerformanceAttendanceFixtureDTO:
    def __init__(
        self, 
        performance_id: int,
        attendee_id: int,
        create_time: int
    ):
        self.performance_id = performance_id
        self.attendee_id = attendee_id
        self.create_time =  create_time

    def get_performance_id(self):
        return self.performance_id

    def get_attendee_id(self):
        return self.attendee_id
    
    def get_create_time(self):
        return self.create_time