
from test.integration import IntegrationTestCase
from test.integration.src.fixtures.DTO.performance_attendance_fixture_dto import (
    PerformanceAttendanceFixtureDTO,
)
from test.integration.src.fixtures.DTO.performance_fixture_dto import (
    PerformanceFixtureDTO,
)
from test.integration.src.fixtures.DTO.performer_fixture_dto import PerformerFixtureDTO

from api.dao.performers_dao import PerformersDAO
from api.typings.performers import AttendeePerformersGetFilter


class PerformersDAOIntegrrationTest(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.performers_dao = PerformersDAO(self.config,self.db)

    def test_attendee_performers_get(self):
        attendee_id = 5555

        # Seed performers
        performer_one_dto = PerformerFixtureDTO(
            name="Performer One",
            uuid="performer-one",
            biography="Performer One Biography",
            create_time=self.current_time,
        )

        performer_one_id = self.fixture_factory.performer_fixture_create(performer_one_dto)

        performer_two_dto = PerformerFixtureDTO(
            name="Performer Two",
            uuid="performer-two",
            biography="Performer Two Biography",
            create_time=self.current_time,
        )

        performer_two_id = self.fixture_factory.performer_fixture_create(performer_two_dto)


        # Seed performances
        performance_one_dto = PerformanceFixtureDTO(
            performer_id=performer_one_id,
            performance_date=self.current_time,
            create_time=self.current_time,
            update_time=None,
            venue_id=111,
        )

        performance_one_id = self.fixture_factory.performance_fixture_create(
            performance_one_dto
        )

        performance_two_dto = PerformanceFixtureDTO(
            performer_id=performer_one_id,
            performance_date=self.current_time - 200000, # roughly a day earlier,
            create_time=self.current_time,
            update_time=None,
            venue_id=222,
        )


        performance_two_id = self.fixture_factory.performance_fixture_create(
            performance_two_dto
        )

        performance_three_dto = PerformanceFixtureDTO(
            performer_id=performer_two_id,
            performance_date=self.current_time - 200000,
            create_time=self.current_time,
            update_time=None,
            venue_id=111,
        )

        performance_three_id = self.fixture_factory.performance_fixture_create(
            performance_three_dto
        )

        # Seed performance attendance

        performance_attendance_one_dto = PerformanceAttendanceFixtureDTO(
            performance_id=performance_one_id,
            attendee_id=attendee_id,
            create_time=self.current_time,
        )

        self.fixture_factory.performance_attendance_fixture_create(
            performance_attendance_one_dto
        )

        performance_attendance_two_dto = PerformanceAttendanceFixtureDTO(
            performance_id=performance_two_id,
            attendee_id=attendee_id,
            create_time=self.current_time,
        )

        self.fixture_factory.performance_attendance_fixture_create(
            performance_attendance_two_dto
        )

        # Test

        filter = AttendeePerformersGetFilter(
            attendee_id=attendee_id,
            get_counts=True,
            limit=10
        )

        result = self.performers_dao.attendee_performers_get(filter)

        performers = result.performers
        counts = result.counts

        self.assertEqual(
            len(performers),
            1,
            "Should only return performers whos shows the user has attended"
        )

        performer = performers[0]
        self.assertEqual(
            performer.id,
            performer_one_id,
            'Should return the correct performer'
        )

        self.assertEqual(
            len(counts),
            1,
            "Should only return counts for performers whos shows the user has attended"
        )

        count_result = counts[0]

        self.assertEqual(
            count_result.count,
            2,
            "Should return a count equal to the number of the performers shows attended by the user"
        )
        self.assertEqual(
            count_result.performer_id,
            performer_one_id,
            "Should return a count for the correct performer"
        )
        self.assertEqual(
            count_result.attendee_id,
            attendee_id,
            "Should return a count for the correct attendee"
        )