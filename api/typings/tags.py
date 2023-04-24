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
    is_deleted: bool = ...

    def __init__(
        self,
        id: int,
        tagged_entity_type: TaggedEntityType,
        tagged_entity_id: int,
        tagged_in_entity_type: TaggedInEntityType,
        tagged_in_entity_id: int,
        creator_id: int,
        is_deleted: bool,
    ) -> None:
        self.id = id
        self.tagged_entity_type = tagged_entity_type
        self.tagged_entity_id = tagged_entity_id
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.creator_id = creator_id
        self.is_deleted = is_deleted


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
    # Filter out tags where the tagged_in_entity is linked to other tagged_entity_types (e.g. if a performance and a performer are tagged in the same post, only_single_tagged_entity_type = True would filter these tags out of any request). NOTE: This is current only implemented for PERFORMER and PERFORMANCE tagged_in_entity_types
    only_single_tagged_entity_type: Optional[bool] = ... 

    def __init__(
            self, 
            tagged_entity_id: Optional[int] = None, 
            tagged_entity_type: Optional[TaggedEntityType] = None, 
            tagged_in_entity_type: Optional[TaggedInEntityType] = None, 
            tagged_in_entity_id: Optional[int] = None,
            only_single_tagged_entity_type: Optional[bool] = None
            ) -> None:
        self.tagged_entity_id = tagged_entity_id
        self.tagged_entity_type = tagged_entity_type
        self.tagged_in_entity_type = tagged_in_entity_type
        self.tagged_in_entity_id = tagged_in_entity_id
        self.only_single_tagged_entity_type = only_single_tagged_entity_type


class TagsGetResult:
    tags: List[Tag] = ...

    def __init__(self, tags: List[Tag]) -> None:
        self.tags = tags


class TagDeleteRequest:
    ids: List[int] = ...

    def __init__(self, ids: List[int]) -> None:
        self.ids = ids
