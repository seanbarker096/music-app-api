from enum import Enum
from typing import List


class TaggedEntityType(Enum):
    USER = "user"
    ARTIST = "artist"


class TaggedInEntityType(Enum):
    POST = "post"


class TagCreatorType(Enum):
    USER = "user"


class Tag:
    id: int = ...
    tagged_entity_type: TaggedEntityType = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: TaggedInEntityType = ...
    tagged_in_entity_id: int = ...
    creator_type: TagCreatorType = ...
    creator_id: int = ...

    def __init__(
        self,
        id: int,
        tagged_entity_type: TaggedEntityType,
        tagged_entity_id: int,
        tagged_in_entity_type: TaggedInEntityType,
        tagged_in_entity_id: int,
        creator_type: TagCreatorType,
        creator_id: int,
    ) -> None:
        self.id = id
        self.tagged_entity_type = tagged_entity_type
        self.tagged_entity_id = tagged_entity_id
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.creator_type = creator_type
        self.creator_id = creator_id


class TagCreateRequest:
    tagged_entity_type: TaggedEntityType = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: TaggedInEntityType = ...
    tagged_in_entity_id: int = ...
    creator_type: TagCreatorType = ...
    creator_id: int = ...

    def __init__(
        self,
        tagged_entity_type: TaggedEntityType,
        tagged_entity_id: int,
        tagged_in_entity_type: TaggedInEntityType,
        tagged_in_entity_id: int,
        creator_type: TagCreatorType,
        creator_id: int,
    ) -> None:
        self.tagged_entity_type = tagged_entity_type
        self.tagged_entity_id = tagged_entity_id
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.creator_type = creator_type
        self.creator_id = creator_id


class TagCreateResult:
    tag: Tag = ...

    def __init__(self, tag: Tag) -> None:
        self.tag = tag


class TagsGetFilter:
    tagged_entity_id: int = ...
    tagged_entity_type: TaggedEntityType = ...

    def __init__(self, tagged_entity_id: int, tagged_entity_type: TaggedEntityType) -> None:
        self.tagged_entity_id = tagged_entity_id
        self.tagged_entity_type = tagged_entity_type


class TagsGetResult:
    tags: List[Tag] = ...

    def __init__(self, tags: List[Tag]) -> None:
        self.tags = tags
