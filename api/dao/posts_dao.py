import time
from typing import Optional

from api.db.db import DB
from api.typings.posts import Post, PostAttachment, PostCreateRequest


class PostsDAO(object):
    db: DB

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def post_create(self, request: PostCreateRequest) -> Post:
        sql = """
            INSERT INTO post(owner_id, content, create_time, updated_time, is_deleted)
            VALUES(%s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
        """
        now = time.time()

        binds = (
            request.owner_id,
            request.content,
            now,
            None,
            False,
        )

        db_result = self.db.run_query(sql, binds)

        post_id = db_result.get_last_row_id()

        return Post(
            id=post_id,
            owner_id=request.owner_id,
            content=request.content,
            create_time=now,
            update_time=None,
        )


class PostAttachmentsDAO(object):
    db: DB

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def post_attachment_create(self, post_id: int, file_id: int) -> PostAttachment:
        sql = """
            INSERT INTO post_attachment(post_id, file_id, create_time) VALUES(%s, %s, FROM_UNIXTIME(%s))
        """

        now = time.time()

        binds = (
            post_id,
            file_id,
            now,
        )

        db_result = self.db.run_query(sql, binds)

        post_attachment_id = db_result.get_last_row_id()

        return PostAttachment(
            id=post_attachment_id, post_id=post_id, file_id=file_id, create_time=now
        )
