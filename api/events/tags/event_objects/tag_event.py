from enum import Enum

from api.typings.tags import Tag


class TagEventType(Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"


class TagEvent:
    tag: Tag = ...

    def __init__(self, tag: Tag):
        self.tag = tag


class TagCreatedEvent(TagEvent):
    type: TagEventType = ...

    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.type = TagEventType.CREATED.value


class TagDeletedEvent(TagEvent):

    def __init__(self, tag: Tag):
        super().__init__(tag)
        self.type = TagEventType.DELETED.value
