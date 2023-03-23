import json
from abc import ABC, abstractmethod

from api.events.tags.event_objects.tag_event import TagEvent


class TagEventObserver(ABC):
    def __init__(
        self,
        config,
    ):
        self.config = config

    @abstractmethod
    def process_event(self, event: TagEvent):
        ...

    def handle_exception(self, exception, event: TagEvent) -> bool:
        # TODO: Add logging for the exception in here instead of throwing for a side effect
        raise Exception(
            f"Failed to process TagEvent of type {event.type} for tag with id {event.tag.id} because {json.dumps(str(exception))}"
            )
        