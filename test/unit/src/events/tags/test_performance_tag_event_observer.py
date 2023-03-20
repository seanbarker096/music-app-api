import time
from test.unit import TestCase
from unittest.mock import Mock

from api.events.tags.event_objects.tag_event import (
    TagCreatedEvent,
    TagEvent,
    TagEventType,
)
from api.events.tags.performance_tag_event_observer import PerformanceTagEventObserver
from api.events.tags.tag_event_subject import TagEventSubject
from api.typings.performances import (
    PerformanceAttendance,
    PerformanceAttendanceCreateRequest,
    PerformanceAttendanceCreateResult,
)
from api.typings.posts import Post, PostOwnerType, PostsGetFilter, PostsGetResult
from api.typings.tags import Tag, TaggedEntityType, TaggedInEntityType


class PerformanceTagEventObserverTest(TestCase):
    def test_process_tag_created_event(self):
        post_id = 5
        post_creator_id = 2

        mock_posts_midlayer = Mock()
        mock_performances_attendance_midlayer = Mock()

        post = Post(
            id=post_id,
            owner_id=post_creator_id,
            owner_type=PostOwnerType.USER.value,
            content="A video from an artist performance",
            create_time=time.time(),
            creator_id=post_creator_id,
        )

        mock_posts_midlayer.posts_get = Mock(return_value=PostsGetResult(posts=[post]))

        expected_performance_attendance = PerformanceAttendance(
            id=1,
            performance_id=10,
            attendee_id=post_creator_id,
            create_time=time.time(),
        )

        mock_performances_attendance_midlayer.performance_attendance_create = Mock(
            return_value=PerformanceAttendanceCreateResult(
                performance_attendance=expected_performance_attendance
            )
        )

        tag = Tag(
            id=1,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            tagged_in_entity_id=post_id,
            tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
            tagged_entity_id=5,
            creator_id=post_creator_id,
        )

        observer = PerformanceTagEventObserver(
            config={},
            performance_attendances_midlayer=mock_performances_attendance_midlayer,
            posts_midlayer=mock_posts_midlayer,
        )

        performance_attendance = observer.process_event(event=TagCreatedEvent(tag=tag))

        self.assertEqual(
            performance_attendance.id,
            expected_performance_attendance.id,
            "Should create a new performance attendance",
        )
        self.assertEqual(
            performance_attendance.attendee_id,
            expected_performance_attendance.attendee_id,
            "Should return the created performance attedance with the correct attendee_id",
        )
        self.assertEqual(
            performance_attendance.performance_id,
            expected_performance_attendance.performance_id,
            "Should return the created performance attedance with the correct performance_id",
        )

        mock_posts_midlayer.posts_get.assert_called_once()

        mock_performances_attendance_midlayer.performance_attendance_create.assert_called_once()
