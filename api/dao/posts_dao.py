import time
from typing import Dict, List, Optional

from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import (
    assert_row_key_exists,
    build_having_query_string,
    build_where_query_string,
)
from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.posts import (
    FeaturedPostsGetFilter,
    Post,
    PostAttachment,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostOwnerType,
    PostsGetFilter,
    ProfilePostsGetFilter,
    ProfileType,
)
from api.typings.tags import TaggedEntityType, TaggedInEntityType


class PostDBAlias:
    POST_ID = "post_id"
    POST_OWNER_ID = "post_owner_id"
    POST_OWNER_TYPE = "post_owner_type"
    POST_CONTENT = "post_content"
    POST_CREATOR_ID = "post_creator_id"
    POST_CREATE_TIME = "post_create_time"
    POST_UPDATE_TIME = "post_update_time"
    POST_IS_DELETED = "post_is_deleted"


class PostsDAO(object):
    db: DBConnectionManager

    POST_COLUMNS = [
        "p.id",
        "p.owner_id",
        "p.owner_type",
        "p.content",
        "p.creator_id",
        "p.create_time",
        "p.update_time",
        "p.is_deleted",
    ]

    POST_SELECTS = [
        "p.id as " + PostDBAlias.POST_ID,
        "p.owner_id as " + PostDBAlias.POST_OWNER_ID,
        "p.owner_type as " + PostDBAlias.POST_OWNER_TYPE,
        "p.content as " + PostDBAlias.POST_CONTENT,
        "p.creator_id as " + PostDBAlias.POST_CREATOR_ID,
        "UNIX_TIMESTAMP(p.create_time) as " + PostDBAlias.POST_CREATE_TIME,
        "UNIX_TIMESTAMP(p.update_time) as " + PostDBAlias.POST_UPDATE_TIME,
        "p.is_deleted as " + PostDBAlias.POST_IS_DELETED,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def post_create(self, request: PostCreateRequest) -> Post:
        sql = """
            INSERT INTO post(owner_id, owner_type, content, creator_id, create_time, update_time, is_deleted)
            VALUES(%s, %s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s), %s)
        """
        now = time.time()

        request.content = None if request.content == "" else request.content
        
        binds = (
            request.owner_id,
            request.owner_type,
            request.content,
            request.creator_id,
            now,
            None,
            0,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            post_id = cursor.lastrowid

        return Post(
                id=post_id,
                owner_id=request.owner_id,
                owner_type=request.owner_type,
                content=request.content,
                creator_id=request.creator_id,
                create_time=now,
                update_time=None,
        )

    def posts_get(self, filter: PostsGetFilter) -> List[Post]:
        selects = f"""
            SELECT {', '.join(self.POST_SELECTS)} 
            FROM post as p
        """

        wheres = []
        binds = []

        if filter.ids:
            wheres.append("p.id in %s")
            binds.append(filter.ids)

        if filter.is_deleted:
            wheres.append("p.is_deleted = %s")
            binds.append(int(filter.is_deleted))

        if filter.owner_ids:
            wheres.append("p.owner_id in %s")
            binds.append(filter.owner_ids)

        if filter.owner_types:
            wheres.append("p.owner_type = %s")
            binds.append(filter.owner_types)

        where_string = build_where_query_string(wheres, "AND")

        binds.append(filter.limit if filter.limit else 10)

        sql = f"""
            {selects}
            {where_string}
            LIMIT %s
        """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        posts = []
        for row in rows:
            post = self._build_post_from_db_row(row)
            posts.append(post)

        return posts

    def profile_posts_get(self, filter: ProfilePostsGetFilter) -> List[Post]:
        # IF THIS QUERY IS SLOW CONSIDER USING A UNION ALL

        selects = f"""SELECT DISTINCT {', '.join(self.POST_SELECTS)} 
            FROM post as p"""

        wheres = []
        binds = []
        joins = []
        join_wheres = []

        if not filter.include_featured and not filter.include_owned and not filter.include_tagged:
            raise Exception(f"Unbounded request made to profile_posts_get. Request: {vars(filter)}")

        ## Before converting the ProfileType enum value to corresponding values for features and tags, ensure its valid
        if filter.profile_type not in set(item.value for item in ProfileType):
            raise Exception(f"Invalid profile_type: {filter.profile_type}")

        # If include_owned set, we want to grab all posts the user owns, along with ones they have featured on their profile, or hav ebeen tagged in (if those filters are set). If we use where here, we will filter out tagged and featured posts this query finds, because the user will not own any of these. We therefore LEFT JOIN the posts table on itself.
        if filter.include_owned is True and filter.profile_id and filter.profile_type:
            if filter.profile_type == ProfileType.PERFORMER.value:
                owner_type = PostOwnerType.PERFORMER.value
            if filter.profile_type == ProfileType.USER.value:
                owner_type = PostOwnerType.USER.value
            joins.append(
                """
                LEFT JOIN post owned_post
                ON owned_post.id = p.id
                AND owned_post.owner_id = %s
                AND owned_post.owner_type = %s
                """
            )

            binds.append(filter.profile_id)
            binds.append(owner_type)

            join_wheres.append("owned_post.id IS NOT NULL")

        # Join to get all posts this profile has featured on their profile. I.e. get all posts
        # that this profile owns/created.
        if filter.include_featured is True:
            if filter.profile_type == ProfileType.USER.value:
                featurer_type = FeaturerType.USER.value
            if filter.profile_type == ProfileType.PERFORMER.value:
                featurer_type = FeaturerType.PERFORMER.value

            joins.append(
                """
                LEFT JOIN feature
                ON  feature.featured_entity_id = p.id
                AND feature.featured_entity_type = %s
                AND feature.featurer_type = %s
                AND feature.featurer_id = %s
                """
            )

            binds.append(FeaturedEntityType.POST.value)
            binds.append(featurer_type)
            binds.append(filter.profile_id)

            join_wheres.append("feature.id IS NOT NULL")

        # Join to get all posts this profile has been tagged in.
        if filter.include_tagged is True:
            if filter.profile_type == ProfileType.USER.value:
                tagged_entity_type = TaggedEntityType.USER.value
            if filter.profile_type == ProfileType.PERFORMER.value:
                tagged_entity_type = TaggedEntityType.PERFORMER.value

            joins.append(
                """
                LEFT JOIN tag
                ON tag.tagged_in_entity_id = p.id
                AND tag.tagged_in_entity_type = %s
                AND tag.tagged_entity_id = %s
                AND tag.tagged_entity_type = %s
                """
            )

            binds.append(TaggedInEntityType.POST.value)
            binds.append(filter.profile_id)
            binds.append(tagged_entity_type)

            join_wheres.append("tag.id IS NOT NULL")

        join_wheres_string = build_where_query_string(join_wheres, "OR", prepend_where_string=False)

        wheres.append(f"p.is_deleted = %s")
        binds.append(0)

        wheres.append(f"({join_wheres_string})")
        wheres_string = build_where_query_string(wheres, "AND")

        final_wheres_string = wheres_string

        binds.append(filter.limit if filter.limit else 10)
        binds.append(filter.offset if filter.offset else 0)
        # Now filter out any rows where there is a null in all 3 columns. We dont need to add any new line escape characters here because of our use of triple strings above.
        sql = f"""
            {selects}
            {"".join(joins)}
            {final_wheres_string}
            ORDER BY {PostDBAlias.POST_CREATE_TIME} DESC
            LIMIT %s OFFSET %s
        """
        
        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        posts = []
        for row in rows:
            post = self._build_post_from_db_row(row)
            posts.append(post)

        return posts
    

    ## TODO: COuld update this to include posts when counts=0 if filtes are set to false
    def featured_posts_get(self, filter: FeaturedPostsGetFilter) -> List[Post]:
        """
        Get all posts that have been featured by at least one user or performer, depending on the filter.
        """
        selects = [*self.POST_SELECTS]

        joins = []
        wheres = []
        havings = []
        binds = []

        # Handle select binds first as they need to be injected into query first
        if filter.is_featured_by_performers:
            selects.append(
                'COUNT(CASE WHEN f.featurer_type = %s THEN f.id END) AS featured_by_performers_count'
            )
            binds.append(FeaturerType.PERFORMER.value)
            havings.append('featured_by_performers_count > 0')

        if filter.is_featured_by_users:
            selects.append(
                'COUNT(CASE WHEN f.featurer_type = %s THEN f.id END) AS featured_by_users_count'
            )
            binds.append(FeaturerType.USER.value)
            havings.append('featured_by_users_count > 0')

        
        joins.append(
                f"""
                INNER JOIN feature f
                    ON f.featured_entity_id = p.id
                    AND f.featured_entity_type = %s
                """
            )  
        binds.append(FeaturedEntityType.POST.value)

        # Post owner filters should be defined here
        wheres.append("p.owner_id = %s")
        binds.append(filter.owner_id)
        
        wheres.append("p.owner_type = %s")
        binds.append(filter.owner_type)

        wheres_string = build_where_query_string(wheres, "AND")
        havings_string = build_having_query_string(havings, "AND")

        binds.append(filter.limit if filter.limit else 10)
    

        sql = f"""
            SELECT {', '.join(selects)} from post as p
            {"".join(joins)}
            {wheres_string}
            GROUP BY {", ".join(self.POST_COLUMNS)}
            {havings_string}
            ORDER BY {PostDBAlias.POST_CREATE_TIME} DESC
            LIMIT %s
            """
        
        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

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

        assert_row_key_exists(db_row, PostDBAlias.POST_OWNER_TYPE)
        owner_type = db_row[PostDBAlias.POST_OWNER_TYPE]

        assert_row_key_exists(db_row, PostDBAlias.POST_CONTENT)
        content = db_row[PostDBAlias.POST_CONTENT]

        assert_row_key_exists(db_row, PostDBAlias.POST_CREATOR_ID)
        creator_id = int(db_row[PostDBAlias.POST_CREATOR_ID])

        assert_row_key_exists(db_row, PostDBAlias.POST_CREATE_TIME)
        create_time = int(db_row[PostDBAlias.POST_CREATE_TIME])

        assert_row_key_exists(db_row, PostDBAlias.POST_UPDATE_TIME)
        update_time = (
            int(db_row[PostDBAlias.POST_UPDATE_TIME])
            if db_row[PostDBAlias.POST_UPDATE_TIME]
            else None
        )

        assert_row_key_exists(db_row, PostDBAlias.POST_IS_DELETED)
        is_deleted = bool(db_row[PostDBAlias.POST_IS_DELETED])

        return Post(
            id=post_id,
            owner_id=owner_id,
            owner_type=owner_type,
            content=content,
            creator_id=creator_id,
            create_time=create_time,
            update_time=update_time,
            is_deleted=is_deleted,
        )


class PostAttachmentDBAlias:
    POST_ATTACHMENT_ID = "post_attachment_id"
    POST_ATTACHMENT_POST_ID = "post_attachment_post_id"
    POST_ATTACHMENT_FILE_ID = "post_attachment_file_id"
    POST_ATTACHMENT_ATTACHMENT_THUMBNAIL_FILE_ID = "post_attachment_attachment_thumbnail_file_id"
    POST_ATTACHMENT_CREATE_TIME = "post_attachment_create_time"


class PostAttachmentsDAO(object):
    db: DBConnectionManager

    POST_ATTACHMENT_SELECTS = [
        "id as " + PostAttachmentDBAlias.POST_ATTACHMENT_ID,
        "post_id as " + PostAttachmentDBAlias.POST_ATTACHMENT_POST_ID,
        "file_id as " + PostAttachmentDBAlias.POST_ATTACHMENT_FILE_ID,
        "attachment_thumbnail_file_id as " + PostAttachmentDBAlias.POST_ATTACHMENT_ATTACHMENT_THUMBNAIL_FILE_ID,
        "UNIX_TIMESTAMP(create_time) as " + PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.config = config
        self.db = db if db else FlaskDBConnectionManager

    def post_attachment_create(self, post_id: int, attachment_file_id: int, attachment_thumbnail_file_id: Optional[int] = None) -> PostAttachment:
        sql = """
            INSERT INTO post_attachment(post_id, file_id, attachment_thumbnail_file_id, create_time) VALUES(%s, %s, %s, FROM_UNIXTIME(%s))
        """

        now = time.time()

        binds = (
            post_id,
            attachment_file_id,
            attachment_thumbnail_file_id,
            now,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            post_attachment_id = cursor.lastrowid

        return PostAttachment(
            id=post_attachment_id, 
            post_id=post_id, file_id=attachment_file_id, 
            thumbnail_file_id=attachment_thumbnail_file_id, 
            create_time=now
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
        
        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

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

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_ATTACHMENT_THUMBNAIL_FILE_ID)
        thumbnail_file_id = int(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_ATTACHMENT_THUMBNAIL_FILE_ID]) if db_row[PostAttachmentDBAlias.POST_ATTACHMENT_ATTACHMENT_THUMBNAIL_FILE_ID] else None

        assert_row_key_exists(db_row, PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME)
        create_time = int(db_row[PostAttachmentDBAlias.POST_ATTACHMENT_CREATE_TIME])

        return PostAttachment(
            id=post_attachment_id, 
            post_id=post_id, 
            file_id=file_id, 
            thumbnail_file_id=thumbnail_file_id,
            create_time=create_time
        )
