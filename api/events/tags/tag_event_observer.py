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

    def handle_exception(self, exception) -> bool:
        # TODO: Add logging for the exception in here
        return False
