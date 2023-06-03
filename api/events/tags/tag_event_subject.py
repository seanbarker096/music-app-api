from typing import List, Optional

from api.events.tags.event_objects.tag_event import (
    TagCreatedEvent,
    TagDeletedEvent,
    TagEvent,
    TagEventType,
)
from api.events.tags.performance_tag_event_observer import PerformanceTagEventObserver
from api.events.tags.tag_event_observer import TagEventObserver
from api.typings.tags import Tag
from exceptions.exceptions import InvalidArgumentException


class TagEventSubject:
    default_observers: List[TagEventObserver] = [
        PerformanceTagEventObserver,
    ]

    def __init__(self, config, observers: Optional[List[TagEventObserver]] = None) -> None:
        """
        :param observers: The observers to attach to the subject. We default to the default observers, but allow observers to be injected for testability.
        """
        self.observers = (
            observers
            if isinstance(observers, list)
            else [observer(config) for observer in self.default_observers]
        )

    def attach(self, observer: TagEventObserver) -> None:
        self.observers.append(observer)

    def publish_event(self, state: Tag, event_type: TagEventType) -> TagEvent:
        event = self._build_event_object(state, event_type)

        for observer in self.observers:
            observer.process_event(event)

        return event

    def _build_event_object(self, tag: Tag, event_type: TagEventType) -> TagEvent:

        if event_type == TagEventType.CREATED.value:
            return TagCreatedEvent(tag)
        
        elif event_type == TagEventType.DELETED.value:
            return TagDeletedEvent(tag)

        raise InvalidArgumentException(f"Invalid tag event type: {event_type}", "event_type")
