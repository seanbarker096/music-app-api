import time
from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.posts import (
    Post,
    PostAttachment,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostsGetFilter,
)
from api.utils import date_time_to_unix_time


class PostDBAlias:
    POST_ID = "post_id"
    POST_OWNER_ID = "post_owner_id"
    POST_CONTENT = "post_content"
    POST_CREATE_TIME = "post_create_time"
    POST_UPDATE_TIME = "post_update_time"
    POST_IS_DELETED = "post_is_deleted"


class PostsDAO(object):
    db: DB

    POST_SELECTS = [
        "id as " + PostDBAlias.POST_ID,
        "owner_id as " + PostDBAlias.POST_OWNER_ID,
        "content as " + PostDBAlias.POST_CONTENT,
        "create_time as " + PostDBAlias.POST_CREATE_TIME,
        "update_time as " + PostDBAlias.POST_UPDATE_TIME,
        "is_deleted as " + PostDBAlias.POST_IS_DELETED,
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

        if filter.ids:
            wheres.append("id in %s")
            binds.append(filter.ids)

        if filter.is_deleted:
            wheres.append("is_deleted = %s")
            binds.append(int(filter.is_deleted))

        if filter.owner_ids:
            wheres.append("owner_id in %s")
            binds.append(filter.owner_ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        posts = []
        for row in rows:
            post = self._build_post_from_db_row(row)
            posts.append(post)

        return posts

    def _build_post_from_db_row(self, db_row: Dict[str, any]) -> Post:

        assert_row_key_exists(db_row, PostDBAlias.POST_ID)
        post_id = int(db_row[PostDBAlias.POST_ID])

        assert_row_key_exists(db_row, PostDBAlias.POST_OWNER_ID)
        owner_id = int(db_row[PostDBAlias.POST_OWNER_ID])

        assert_row_key_exists(db_row, PostDBAlias.POST_CONTENT)
        content = db_row[PostDBAlias.POST_CONTENT]

        assert_row_key_exists(db_row, PostDBAlias.POST_CREATE_TIME)
        create_time = float(date_time_to_unix_time(db_row[PostDBAlias.POST_CREATE_TIME]))

        assert_row_key_exists(db_row, PostDBAlias.POST_UPDATE_TIME)
        update_time = (
            float(date_time_to_unix_time(db_row[PostDBAlias.POST_UPDATE_TIME]))
            if db_row[PostDBAlias.POST_UPDATE_TIME]
            else None
        )

        assert_row_key_exists(db_row, PostDBAlias.POST_IS_DELETED)
        is_deleted = db_row[PostDBAlias.POST_IS_DELETED]

        return Post(
            id=post_id,
            owner_id=owner_id,
            content=content,
            create_time=create_time,
            update_time=update_time,
            is_deleted=is_deleted,
        )


class PostAttachmentDBAlias:
    POST_ATTACHMENT_ID = "post_attachment_id"
    POST_ATTACHMENT_POST_ID = "post_attachment_post_id"
    POST_ATTACHMENT_FILE_ID = "post_attachment_file_id"
    POST_ATTACHMENT_CREATE_TIME = "post_attachment_create_time"


class PostAttachmentsDAO(object):
    db: DB

    POST_ATTACHMENT_SELECTS = [
        "id as " + PostAttachmentDBAlias.POST_ATTACHMENT_ID,
        "post_id as " + PostAttachmentDBAlias.POST_ATTACHMENT_POST_ID,
        "file_id as " + PostAttachmentDBAlias.POST_ATTACHMENT_FILE_ID,
        "create_time as " + PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME,
    ]

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

    def post_attachments_get(self, filter: PostAttachmentsGetFilter) -> List[PostAttachment]:
        selects = f"""
            SELECT {', '.join(self.POST_ATTACHMENT_SELECTS)} 
            FROM post_attachment
        """

        wheres = []
        binds = []

        if filter.post_ids:
            wheres.append("id in %s")
            binds.append(filter.post_ids)

        if filter.post_attachment_ids:
            wheres.append("post_attachment_ids in %s")
            binds.append(filter.post_attachment_ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        posts_attachments = []
        for row in rows:
            post = self._build_post_attachment_from_db_row(row)
            posts_attachments.append(post)

        return posts_attachments

    def _build_post_attachment_from_db_row(self, db_row: Dict[str, any]) -> PostAttachment:

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_ID)
        post_attachment_id = int(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_ID])

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_POST_ID)
        post_id = int(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_POST_ID])

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_FILE_ID)
        file_id = int(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_FILE_ID])

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME)
        create_time = float(
            date_time_to_unix_time(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME])
        )

        return PostAttachment(
            id=post_attachment_id, post_id=post_id, file_id=file_id, create_time=create_time
        )
