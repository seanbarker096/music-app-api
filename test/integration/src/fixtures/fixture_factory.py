from test.integration.src.fixtures.DTO.feature_fixture_dto import FeatureFixtureDTO
from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO
from test.integration.src.fixtures.DTO.tag_fixture_dto import TagFixtureDTO

from api.db.db import DB


class FixtureFactory:
    def __init__(self, db: DB) -> None:
        self.db = db

    def post_fixture_create(self, dto: PostFixtureDTO) -> int:

        binds = (
            dto.get_owner_id(),
            dto.get_owner_type(),
            dto.get_content(),
            dto.get_create_time(),
            dto.get_update_time(),
            dto.get_is_deleted(),
        )

        sql = """
                INSERT INTO post(owner_id, owner_type, content, create_time, update_time, is_deleted)
                VALUES(%s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
            """

        db_result = self.db.run_query(sql, binds)

        return db_result.get_last_row_id()

    def post_attachment_fixture_create(self, dto: PostAttachmentFixtureDTO) -> int:
        sql = """
            INSERT INTO post_attachment(post_id, file_id, create_time) VALUES(%s, %s, FROM_UNIXTIME(%s))
        """

        binds = (
            dto.get_post_id(),
            dto.get_file_id(),
            dto.get_create_time(),
        )

        db_result = self.db.run_query(sql, binds)

        return db_result.get_last_row_id()

    def tag_fixture_create(self, dto: TagFixtureDTO) -> int:
        sql = """
            INSERT INTO tag(tagged_in_entity_type, tagged_in_entity_id, tagged_entity_type, tagged_entity_id, creator_type, creator_id) VALUES(%s, %s, %s, %s, %s, %s)
        """

        binds = (
            dto.get_tagged_in_entity_type(),
            dto.get_tagged_in_entity_id(),
            dto.get_tagged_entity_type(),
            dto.get_tagged_entity_id(),
            dto.get_creator_type(),
            dto.get_creator_id(),
        )

        db_result = self.db.run_query(sql, binds)

        return db_result.get_last_row_id()

    def feature_fixture_create(self, dto: FeatureFixtureDTO) -> int:
        sql = """
            INSERT INTO feature(featured_entity_type, featured_entity_id, featurer_type, featurer_id, creator_id)
            VALUES(%s, %s, %s, %s, %s)
        """

        binds = (
            dto.get_featured_entity_type(),
            dto.get_featured_entity_id(),
            dto.get_featurer_type(),
            dto.get_featurer_id(),
            dto.get_creator_id(),
        )

        db_result = self.db.run_query(sql, binds)

        return db_result.get_last_row_id()
