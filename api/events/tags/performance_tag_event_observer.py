import json
import logging
from typing import Optional

from api.events.tags.event_objects.tag_event import (
    TagCreatedEvent,
    TagEvent,
    TagEventType,
)
from api.events.tags.tag_event_observer import TagEventObserver
from api.midlayer.performances_mid import PerformanceAttendancesMidlayerMixin
from api.midlayer.posts_mid import PostsMidlayerMixin
from api.typings.performances import (
    PerformanceAttendance,
    PerformanceAttendanceCreateRequest,
)
from api.typings.posts import PostsGetFilter
from api.typings.tags import TaggedEntityType, TaggedInEntityType
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import PostNotFoundException


class PerformanceTagEventObserver(TagEventObserver):
    def __init__(
        self,
        config,
        performance_attendances_midlayer: Optional[PerformanceAttendancesMidlayerMixin] = None,
        posts_midlayer: Optional[PostsMidlayerMixin] = None,
    ) -> None:
        super().__init__(config)

        self.performance_attendances_midlayer = (
            performance_attendances_midlayer
            if performance_attendances_midlayer
            else PerformanceAttendancesMidlayerMixin(config)
        )
        self.posts_midlayer = posts_midlayer if posts_midlayer else PostsMidlayerMixin(config)

    def process_event(self, event: TagEvent) -> any:
        try:
            if event.type == TagEventType.CREATED.value:
                return self._handle_tag_created_event(event)

        except Exception as e:
            return self.handle_exception(e, event)

    def _handle_tag_created_event(self, event: TagCreatedEvent) -> PerformanceAttendance | None:
        """
        Marks the post owner as having attended a performance, whenever a performance is tagged in a post.

        :param event: The tag created event
        :type event: TagCreatedEvent

        :return: The performance attendance that was created
        """
        tag = event.tag

        if (
            tag.tagged_entity_type != TaggedEntityType.PERFORMANCE.value
            or tag.tagged_in_entity_type != TaggedInEntityType.POST.value
        ):
            # raise InvalidArgumentException(
            #     f"Invalid tag event. Currently only tagging perforamnces in posts is supported. Please extend these checks if you want to support other tag events. Tag event: {json.dumps(vars(event))}",
            #     "event",
            # )
            return None

        post_id = tag.tagged_in_entity_id
        posts_get_filter = PostsGetFilter(ids=[post_id])

        posts = self.posts_midlayer.posts_get(filter=posts_get_filter).posts

        if len(posts) == 0:
            raise PostNotFoundException(
                f"Failed to process tag created event because the tagged in post with id {post_id} could not be found."
            )

        post = posts[0]

        request = PerformanceAttendanceCreateRequest(
            performance_id=tag.tagged_entity_id, attendee_id=post.owner_id
        )

        return self.performance_attendances_midlayer.performance_attendance_create(
            request=request
        ).performance_attendance
