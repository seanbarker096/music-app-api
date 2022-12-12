import time
from typing import Optional

from api.db.db import DB
from api.typings.posts import Post, PostCreateRequest
from exceptions.db.exceptions import DBDuplicateKeyException


class PostsDAO(object):
    db: DB

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def post_create(self, request: PostCreateRequest) -> Post:
        sql = """
            INSERT INTO post(attachment_uuid, owner_id, content, create_time, updated_time, is_deleted)
            VALUES(%s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
        """
        now = time.time()

        binds = (
            request.attachment_id,
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
            attachment_id=request.attachment_id,
        )
