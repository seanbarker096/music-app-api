import time
from typing import Optional

from api.db import DB
from api.db.utils.db_util import add_wheres_to_query
from api.typings.posts import Post, PostAttachment, PostCreateRequest, PostsGetFilter


class PostDBAlias:
    OWNER_ID = "post_owner_id"
    CONTENT = "post_content"
    CREATE_TIME = "post_create_time"
    UPDATE_TIME = "post_update_time"
    IS_DELETED = "post_is_deleted"


class PostsDAO(object):
    db: DB

    POST_SELECTS = [
        "owner_id as " + PostDBAlias.USER_ID,
        "content as " + PostDBAlias.USER_USERNAME,
        "create_time as " + PostDBAlias.CREATE_TIME,
        "update_time as " + PostDBAlias.UPDATE_TIME,
        "is_deleted as " + PostDBAlias.IS_DELETED,
    ]

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def post_create(self, request: PostCreateRequest) -> Post:
        sql = """
            INSERT INTO post(owner_id, content, create_time, update_time, is_deleted)
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

    def posts_get(self, filter: PostsGetFilter) -> List[Post]:
        selects = f"""
            SELECT {', '.join(self.POST_SELECTS)} 
            FROM post
        """

        wheres = []
        binds = []

        if filter.post_ids:
            wheres.append("id in %s")
            binds.append(filter.post_ids)

        if filter.is_deleted:
            wheres.append("is_deleted = %s")
            binds.append(int(filter.is_deleted))

        where_string = add_wheres_to_query(wheres, "AND")

        sql = selects + where_string

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        posts = []
        for row in rows:
            post = build_post_from_db_row(row)
            posts.append(post)


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
