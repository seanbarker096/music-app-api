from test.integration.src.fixtures.DTO.feature_fixture_dto import FeatureFixtureDTO
from test.integration.src.fixtures.DTO.performance_attendance_fixture_dto import (
    PerformanceAttendanceFixtureDTO,
)
from test.integration.src.fixtures.DTO.performance_fixture_dto import (
    PerformanceFixtureDTO,
)
from test.integration.src.fixtures.DTO.performer_fixture_dto import PerformerFixtureDTO
from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO
from test.integration.src.fixtures.DTO.tag_fixture_dto import TagFixtureDTO

from api.db.db import DBConnection


class FixtureFactory:
    def __init__(self, db: DBConnection) -> None:
        self.db = db

    def post_fixture_create(self, dto: PostFixtureDTO) -> int:

        binds = (
            dto.get_owner_id(),
            dto.get_owner_type(),
            dto.get_content(),
            dto.get_creator_id(),
            dto.get_create_time(),
            dto.get_update_time(),
            dto.get_is_deleted(),
        )

        sql = """
                INSERT INTO post(owner_id, owner_type, content, creator_id, create_time, update_time, is_deleted)
                VALUES(%s, %s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
            """

        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid

    def post_attachment_fixture_create(self, dto: PostAttachmentFixtureDTO) -> int:
        sql = """
            INSERT INTO post_attachment(post_id, file_id, create_time) VALUES(%s, %s, FROM_UNIXTIME(%s))
        """

        binds = (
            dto.get_post_id(),
            dto.get_file_id(),
            dto.get_create_time(),
        )

        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid

    def tag_fixture_create(self, dto: TagFixtureDTO) -> int:
        sql = """
            INSERT INTO tag(tagged_in_entity_type, tagged_in_entity_id, tagged_entity_type, tagged_entity_id, creator_id) VALUES(%s, %s, %s, %s, %s)
        """

        binds = (
            dto.get_tagged_in_entity_type(),
            dto.get_tagged_in_entity_id(),
            dto.get_tagged_entity_type(),
            dto.get_tagged_entity_id(),
            dto.get_creator_id(),
        )

        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid

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

        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid

    def performer_fixture_create(self, dto: PerformerFixtureDTO) -> int:
        sql = """
            INSERT INTO performers(uuid, performer_name, create_time, biography, update_time, owner_id, image_url) VALUES(%s, %s, FROM_UNIXTIME(%s), %s, FROM_UNIXTIME(%s), %s, %s)
        """

        binds = (
            dto.get_uuid(),
            dto.get_name(),
            dto.get_create_time(),
            dto.get_biography(),
            dto.get_update_time(),
            dto.get_owner_id(),
            dto.get_image_url(),
        )
        
        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid
    

    def performance_attendance_fixture_create(self, dto: PerformanceAttendanceFixtureDTO) -> int:
        sql = """
            INSERT INTO performance_attendance(performance_id, attendee_id, create_time) VALUES(%s, %s, FROM_UNIXTIME(%s))
        """

        binds = (
            dto.get_performance_id(),
            dto.get_attendee_id(),
            dto.get_create_time(),
        )
        
        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid
    
    def performance_fixture_create(self, dto: PerformanceFixtureDTO) -> int:
        sql = """
            INSERT INTO performance(performer_id, performance_date, create_time, update_time, venue_id) VALUES(%s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
        """

        binds = (
            dto.get_performer_id(),
            dto.get_performance_date(),
            dto.get_create_time(),
            dto.get_update_time(),
            dto.get_venue_id(),
        )

        with self.db as cursor:
            cursor.execute(sql, binds)

            return cursor.lastrowid
    