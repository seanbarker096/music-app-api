from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO

from api.db.db import DB


class FixtureFactory:
    def __init__(self, db: DB) -> None:
        self.db = db

    def post_fixture_create(self, dto: PostFixtureDTO) -> int:

        binds = (
            dto.get_owner_id(),
            dto.get_content(),
            dto.get_create_time(),
            dto.get_update_time(),
            dto.get_is_deleted(),
        )

        sql = """
                INSERT INTO post(owner_id, content, create_time, update_time, is_deleted)
                VALUES(%s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
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
