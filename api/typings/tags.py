from enum import Enum
from typing import List, Optional


class TaggedEntityType(Enum):
    USER = "user"
    PERFORMER = "performer"
    PERFORMANCE = "performance"


# I.e. 'A user has been tagged IN a post'
class TaggedInEntityType(Enum):
    POST = "post"


class Tag:
    id: int = ...
    tagged_entity_type: TaggedEntityType = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: TaggedInEntityType = ...
    tagged_in_entity_id: int = ...
    creator_id: int = ...  # The user who created the tag object

    def __init__(
        self,
        id: int,
        tagged_entity_type: TaggedEntityType,
        tagged_entity_id: int,
        tagged_in_entity_type: TaggedInEntityType,
        tagged_in_entity_id: int,
        creator_id: int,
    ) -> None:
        self.id = id
        self.tagged_entity_type = tagged_entity_type
        self.tagged_entity_id = tagged_entity_id
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.creator_id = creator_id


class TagCreateRequest:
    tagged_entity_type: TaggedEntityType = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: TaggedInEntityType = ...
    tagged_in_entity_id: int = ...
    creator_id: int = ...

    def __init__(
        self,
        tagged_entity_type: TaggedEntityType,
        tagged_entity_id: int,
        tagged_in_entity_type: TaggedInEntityType,
        tagged_in_entity_id: int,
        creator_id: int,
    ) -> None:
        self.tagged_entity_type = tagged_entity_type
        self.tagged_entity_id = tagged_entity_id
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.creator_id = creator_id


class TagCreateResult:
    tag: Tag = ...

    def __init__(self, tag: Tag) -> None:
        self.tag = tag


class TagsGetFilter:
    tagged_entity_id: Optional[int] = ...
    tagged_entity_type: Optional[TaggedEntityType] = ...
    tagged_in_entity_type: Optional[TaggedInEntityType] = ...
    tagged_in_entity_id: Optional[int] = ...

    def __init__(self, tagged_entity_id: Optional[int] = None, tagged_entity_type: Optional[TaggedEntityType] = None, tagged_in_entity_type: Optional[TaggedInEntityType] = None, tagged_in_entity_id: Optional[int] = None) -> None:
        self.tagged_entity_id = tagged_entity_id
        self.tagged_entity_type = tagged_entity_type
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id


class TagsGetResult:
    tags: List[Tag] = ...

    def __init__(self, tags: List[Tag]) -> None:
        self.tags = tags
