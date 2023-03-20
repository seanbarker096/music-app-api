from typing import List

from api.events.event_observer import EventObserver
from api.events.event_subject import EventSubject
from api.events.tags.event_objects.tag_event import (
    TagCreatedEvent,
    TagEvent,
    TagEventType,
)
from api.events.tags.performance_tag_event_observer import PerformanceTagEventObserver
from api.events.tags.tag_event_observer import TagEventObserver
from api.typings.tags import Tag, TaggedEntityType, TaggedInEntityType
from exceptions.exceptions import InvalidArgumentException


class TagEventSubject:
    observers: List[TagEventObserver] = [
        PerformanceTagEventObserver,
    ]

    def __init__(self, config) -> None:
        self.observers = [observer(config) for observer in self.observers]

    def publish_event(self, state: Tag, event_type: TagEventType) -> None:
        event = self._build_event_object(state, event_type)

        for observer in self.observers:
            observer.process_event(event)

    def _build_event_object(self, tag: Tag, event_type: TagEventType) -> TagEvent:

        if event_type == TagEventType.CREATED:
            return TagCreatedEvent(tag)

        raise InvalidArgumentException(f"Invalid tag event type: {event_type}", "event_type")
