from typing import Optional

from api.typings.tags import TagCreatorType, TaggedEntityType, TaggedInEntityType


class TagFixtureDTO:
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

    def get_tagged_entity_type(self) -> TaggedEntityType:
        return self.tagged_entity_type

    def get_tagged_entity_id(self) -> int:
        return self.tagged_entity_id

    def get_tagged_in_entity_type(self) -> TaggedInEntityType:
        return self.tagged_in_entity_type

    def get_tagged_in_entity_id(self) -> int:
        return self.tagged_in_entity_id

    def get_creator_id(self) -> int:
        return self.creator_id
