from typing import Optional

from api.db.db import DB
from api.typings.tags import Tag, TagCreateRequest


class TagsDBAlias:
    TAG_ID = "tag_id"
    TAG_TAGGED_ENTITY_TYPE = "tag_tagged_entity_type"
    TAG_TAGGED_ENTITY_ID = "tag_tagged_entity_id"
    TAG_TAGGED_IN_ENTITY_TYPE = "tag_tagged_in_entity_type"
    TAG_TAGGED_IN_ENTITY_ID = "tag_tagged_in_entity_id"
    TAG_CREATOR_TYPE = "tag_creator_type"
    TAG_CREATOR_ID = "tag_creator_id"


class TagsDAO:
    db: DB

    TAG_SELECTS = [
        "id as " + TagsDBAlias.TAG_ID,
        "tagged_entity_type as " + TagsDBAlias.TAG_TAGGED_ENTITY_TYPE,
        "tagged_entity_id as " + TagsDBAlias.TAG_TAGGED_ENTITY_ID,
        "tagged_in_entity_type as " + TagsDBAlias.TAG_TAGGED_IN_ENTITY_TYPE,
        "tagged_in_entity_id as " + TagsDBAlias.TAG_TAGGED_IN_ENTITY_ID,
        "creator_type as " + TagsDBAlias.TAG_CREATOR_TYPE,
        "creator_id as " + TagsDBAlias.TAG_CREATOR_ID,
    ]

    def __init__(self, config, db: Optional[DB] = None) -> None:
        self.db = db if db else DB(config)

    def tag_create(self, request: TagCreateRequest) -> Tag:
        query = """
            INSERT INTO tag(tagged_entity_type, tagged_entity_id, tagged_in_entity_type, tagged_in_entity_id, creator_type, creator_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        binds = (
            request.tagged_entity_type,
            request.tagged_entity_id,
            request.tagged_in_entity_type,
            request.tagged_in_entity_id,
            request.creator_type,
            request.creator_id,
        )

        db_result = self.db.run_query(query, binds)

        tag_id = db_result.get_last_row_id()

        return Tag(
            id=tag_id,
            tagged_entity_type=request.tagged_entity_type,
            tagged_entity_id=request.tagged_entity_id,
            tagged_in_entity_type=request.tagged_in_entity_type,
            tagged_in_entity_id=request.tagged_in_entity_id,
            creator_type=request.creator_type,
            creator_id=request.creator_id,
        )
