import time
from test.unit import TestCase
from unittest.mock import Mock

from api.events.tags.event_objects.tag_event import TagEventType
from api.events.tags.performance_tag_event_observer import PerformanceTagEventObserver
from api.events.tags.tag_event_subject import TagEventSubject
from api.typings.performances import (
    PerformanceAttendance,
    PerformanceAttendanceCreateRequest,
    PerformanceAttendanceCreateResult,
)
from api.typings.posts import Post, PostOwnerType, PostsGetFilter, PostsGetResult
from api.typings.tags import Tag, TaggedEntityType, TaggedInEntityType


class TagEventSubjectTest(TestCase):
    def test_publish_event(self):
        post_id = 5
        post_creator_id = 2

        observer = Mock()
        observer.process_event = Mock()

        subject = TagEventSubject(self.config, observers=[])

        # mock_posts_midlayer = Mock()
        # mock_performances_attendance_midlayer = Mock()

        subject.attach(observer)

        # post = Post(
        #     id=post_id,
        #     owner_id=post_creator_id,
        #     owner_type=PostOwnerType.USER.value,
        #     content="A video from an artist performance",
        #     create_time=time.time(),
        #     creator_id=post_creator_id,
        # )

        # mock_posts_midlayer.posts_get = Mock(return_value=PostsGetResult(posts=[post]))

        # performance_attendance = PerformanceAttendance(
        #     id=1,
        #     performance_id=10,
        #     attendee_id=post_creator_id,
        # )

        # mock_performances_attendance_midlayer.performance_attendance_create = Mock(
        #     return_value=PerformanceAttendanceCreateResult(attendance=performance_attendance)
        # )

        tag = Tag(
            id=1,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            tagged_in_entity_id=post_id,
            tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
            tagged_entity_id=5,
            creator_id=post_creator_id,
        )

        published_event = subject.publish_event(tag, TagEventType.CREATED.value)

        self.assertEqual(published_event.tag, tag)
        self.assertEqual(published_event.type, TagEventType.CREATED.value)
        observer.process_event.assert_called_once_with(published_event)

        # mock_posts_midlayer.posts_get.assert_called_once_with(PostsGetFilter(ids=[post_id]))

        # mock_performances_attendance_midlayer.performance_attendance_create.assert_called_once_with(
        #     PerformanceAttendanceCreateRequest(
        #         performance_id=5,
        #         attendee_id=post_creator_id,
        #     )
        # )
