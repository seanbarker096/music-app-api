from typing import Dict, List, Optional

from api.db.db import FlaskDBConnectionManager
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.tags import (
    Tag,
    TagCreateRequest,
    TagDeleteRequest,
    TaggedEntityType,
    TaggedInEntityType,
    TagsGetFilter,
)


class TagsDBAlias:
    TAG_ID = "tag_id"
    TAG_TAGGED_ENTITY_TYPE = "tag_tagged_entity_type"
    TAG_TAGGED_ENTITY_ID = "tag_tagged_entity_id"
    TAG_TAGGED_IN_ENTITY_TYPE = "tag_tagged_in_entity_type"
    TAG_TAGGED_IN_ENTITY_ID = "tag_tagged_in_entity_id"
    TAG_CREATOR_ID = "tag_creator_id"


class TagsDAO:
    db: FlaskDBConnectionManager

    TAG_SELECTS = [
        "t.id as " + TagsDBAlias.TAG_ID,
        "t.tagged_entity_type as " + TagsDBAlias.TAG_TAGGED_ENTITY_TYPE,
        "t.tagged_entity_id as " + TagsDBAlias.TAG_TAGGED_ENTITY_ID,
        "t.tagged_in_entity_type as " + TagsDBAlias.TAG_TAGGED_IN_ENTITY_TYPE,
        "t.tagged_in_entity_id as " + TagsDBAlias.TAG_TAGGED_IN_ENTITY_ID,
        "t.creator_id as " + TagsDBAlias.TAG_CREATOR_ID,
    ]

    def __init__(self, config, db: Optional[FlaskDBConnectionManager] = None) -> None:
        # We will initialise the connection mananger for each database query
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def tag_create(self, request: TagCreateRequest) -> Tag:
        query = """
            INSERT INTO tag(tagged_entity_type, tagged_entity_id, tagged_in_entity_type, tagged_in_entity_id, creator_id)
            VALUES (%s, %s, %s, %s, %s)
        """

        binds = (
            request.tagged_entity_type,
            request.tagged_entity_id,
            request.tagged_in_entity_type,
            request.tagged_in_entity_id,
            request.creator_id,
        )

        with self.db(self.config) as cursor:
            cursor.execute(query, binds)
            tag_id = cursor.lastrowid

        return Tag(
            id=tag_id,
            tagged_entity_type=request.tagged_entity_type,
            tagged_entity_id=request.tagged_entity_id,
            tagged_in_entity_type=request.tagged_in_entity_type,
            tagged_in_entity_id=request.tagged_in_entity_id,
            creator_id=request.creator_id,
        )

    def tags_get(self, filter: TagsGetFilter) -> List[Tag]:
        selects = f"""
            SELECT {', '.join(self.TAG_SELECTS)} from tag as t
        """

        wheres = []
        binds = []
        joins = []

        if filter.only_single_tagged_entity_type is True and filter.tagged_entity_type in (
            TaggedEntityType.PERFORMANCE.value,
            TaggedEntityType.PERFORMER.value,
        ):
            joins.append(
                """
                LEFT JOIN tag t2
                ON t.tagged_in_entity_type = t2.tagged_in_entity_type
                AND t.tagged_in_entity_id = t2.tagged_in_entity_id
                AND t2.tagged_entity_type = %s
                """
            )
            other_tagged_entity_type = (
                TaggedEntityType.PERFORMER.value
                if filter.tagged_entity_type == TaggedEntityType.PERFORMANCE.value
                else TaggedEntityType.PERFORMANCE.value
            )

            binds.append(other_tagged_entity_type)
            wheres.append("t2.id is null")

        if filter.ids:
            wheres.append("t.id in %s")
            binds.append(filter.ids)

        if filter.tagged_entity_id:
            wheres.append("t.tagged_entity_id = %s")
            binds.append(filter.tagged_entity_id)

        if filter.tagged_entity_type:
            wheres.append("t.tagged_entity_type = %s")
            binds.append(filter.tagged_entity_type)

        if filter.tagged_in_entity_id:
            wheres.append("t.tagged_in_entity_id = %s")
            binds.append(filter.tagged_in_entity_id)

        if filter.tagged_in_entity_type:
            wheres.append("t.tagged_in_entity_type = %s")
            binds.append(filter.tagged_in_entity_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = f"""
            {selects}
            {''.join(joins)}
            {where_string}
            """
        
        with self.db(self.config) as cursor:

            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        return [self._build_tag_from_db_row(row) for row in rows]

    def tags_delete(self, request: TagDeleteRequest) -> None:
        query = """
            DELETE FROM tag t
            WHERE t.id = %s
        """

        binds = request.id  # PyMySQL requires a unique list of values for DELETE statements

        with self.db(self.config) as cursor:
            cursor.execute(query, binds)

    def delete_performance_post_tags_by_performer_id(self, post_id: int, performer_id: int) -> None:
        """
        For a given performer, delete all tags between a specific post and any of their performances.
        """
        query = """
            DELETE FROM tag
            WHERE tagged_entity_type = %s
            AND tagged_in_entity_type = %s
            AND tagged_in_entity_id = %s
            AND tagged_entity_id in (
                SELECT p.id from performance p
                INNER JOIN performers pf
                    ON p.performer_id = pf.id
                WHERE pf.id = %s
            )
        """

        binds = (
            TaggedEntityType.PERFORMANCE.value,
            TaggedInEntityType.POST.value,
            post_id,
            performer_id,
        )

        with self.db(self.config) as cursor:
            cursor.execute(query, binds)

    def _build_tag_from_db_row(self, db_row: Dict[str, any]) -> Tag:

        assert_row_key_exists(db_row, TagsDBAlias.TAG_ID)
        tag_id = int(db_row[TagsDBAlias.TAG_ID])

        assert_row_key_exists(db_row, TagsDBAlias.TAG_TAGGED_ENTITY_TYPE)
        tagged_entity_type = db_row[TagsDBAlias.TAG_TAGGED_ENTITY_TYPE]

        assert_row_key_exists(db_row, TagsDBAlias.TAG_TAGGED_ENTITY_ID)
        tagged_entity_id = int(db_row[TagsDBAlias.TAG_TAGGED_ENTITY_ID])

        assert_row_key_exists(db_row, TagsDBAlias.TAG_TAGGED_IN_ENTITY_TYPE)
        tagged_in_entity_type = db_row[TagsDBAlias.TAG_TAGGED_IN_ENTITY_TYPE]

        assert_row_key_exists(db_row, TagsDBAlias.TAG_TAGGED_IN_ENTITY_ID)
        tagged_in_entity_id = int(db_row[TagsDBAlias.TAG_TAGGED_IN_ENTITY_ID])

        assert_row_key_exists(db_row, TagsDBAlias.TAG_CREATOR_ID)
        creator_id = int(db_row[TagsDBAlias.TAG_CREATOR_ID])

        return Tag(
            id=tag_id,
            tagged_entity_type=tagged_entity_type,
            tagged_entity_id=tagged_entity_id,
            tagged_in_entity_type=tagged_in_entity_type,
            tagged_in_entity_id=tagged_in_entity_id,
            creator_id=creator_id,
        )
