from enum import Enum


class Tag:
    id: int = ...
    tagged_entity_type: str = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: str = ...
    tagged_in_entity_id: int = ...
    creator_type: str = ...
    creator_id: int = ...

    def __init__(
        self,
        id: int,
        tagged_entity_type: str,
        tagged_entity_id: int,
        tagged_in_entity_type: str,
        tagged_in_entity_id: int,
        creator_type: str,
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
    tagged_entity_type: str = ...
    tagged_entity_id: int = ...
    tagged_in_entity_type: str = ...
    tagged_in_entity_id: int = ...
    creator_type: str = ...
    creator_id: int = ...

    def __init__(
        self,
        tagged_entity_type: str,
        tagged_entity_id: int,
        tagged_in_entity_type: str,
        tagged_in_entity_id: int,
        creator_type: str,
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


class TaggedEntityType(Enum):
    USER = "user"
    ARTIST = "artist"


class TaggedInEntityType(Enum):
    POST = "post"


class TagCreatorType(Enum):
    USER = "user"
