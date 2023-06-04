from enum import Enum
from typing import List, Optional


class PostOwnerType(Enum):
    PERFORMER = "performer"
    USER = "user"


class Post(object):
    id: int = ...
    owner_id: int = ...
    owner_type = PostOwnerType = ...
    content: str = ...
    create_time: int = ...
    creator_id: int = ...
    update_time: Optional[int] = ...
    is_deleted: Optional[bool] = ...

    def __init__(
        self,
        id: int,
        owner_id: int,
        owner_type: PostOwnerType,
        content: str,
        creator_id: int,
        create_time: int,
        update_time: Optional[int] = None,
        is_deleted: Optional[bool] = False,
    ):
        self.id = id
        self.owner_id = owner_id
        self.owner_type = owner_type
        self.creator_id = creator_id
        self.content = content
        self.create_time = create_time
        self.is_deleted = is_deleted
        self.update_time = update_time


class PostCreateRequest(object):
    creator_id: int = ...
    owner_id: int = ...
    owner_type: PostOwnerType = ...
    content: Optional[str] = ...

    def __init__(
        self,
        creator_id: int,
        owner_id: int,
        owner_type: PostOwnerType,
        content: Optional[str] = None,
    ):
        self.creator_id = creator_id
        self.owner_id = owner_id
        self.owner_type = owner_type
        self.content = content


class PostCreateResult(object):
    post: Post = ...

    def __init__(self, post: Post):
        self.post = post


class PostsGetFilter(object):
    ids: Optional[List[int]] = ...
    is_deleted: Optional[bool] = ...
    owner_ids: Optional[List[int]] = ...
    owner_types: Optional[List[PostOwnerType]] = ...
    limit: Optional[int] = ...

    def __init__(
        self,
        ids: Optional[List[int]] = None,
        is_deleted: Optional[bool] = None,
        owner_ids: Optional[List[int]] = None,
        owner_types: Optional[List[PostOwnerType]] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.ids = ids
        self.is_deleted = is_deleted
        self.owner_ids = owner_ids
        self.owner_types = owner_types
        self.limit = limit


class PostsGetResult(object):
    posts: List[Post] = ...

    def __init__(self, posts: List[Post]) -> None:
        self.posts = posts


class ProfileType(Enum):
    PERFORMER = "performer"
    USER = "user"


class ProfilePostsGetFilter(object):
    profile_id: int = ...
    profile_type: ProfileType = ...
    include_tagged: Optional[bool] = ...
    include_featured: Optional[bool] = ...
    include_owned: Optional[bool] = ...
    limit: Optional[int] = ...
    offset: Optional[int] = ...

    def __init__(
        self,
        profile_id: int,
        profile_type: ProfileType,
        include_tagged: Optional[bool] = None,
        include_featured: Optional[bool] = None,
        include_owned: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> None:
        self.profile_id = profile_id
        self.profile_type = profile_type
        self.include_tagged = True if include_tagged is None else include_tagged
        self.include_featured = True if include_featured is None else include_featured
        self.include_owned = True if include_owned is None else include_owned
        self.limit = limit
        self.offset = offset



class FeaturedPostsGetFilter:
    owner_id: int
    owner_type: PostOwnerType
    is_featured_by_users: bool
    is_featured_by_performers: bool
    limit: Optional[int]

    def __init__(
        self,
        owner_id: int,
        owner_type: PostOwnerType,
        is_featured_by_users: bool,
        is_featured_by_performers: bool,
        limit: Optional[int] = None,
    ) -> None:
        self.owner_id = owner_id
        self.owner_type = owner_type
        self.is_featured_by_users = is_featured_by_users
        self.is_featured_by_performers = is_featured_by_performers
        self.limit = limit


# ********* POST ATTACHMENTS ************* #
class PostAttachment(object):
    id: int = ...
    post_id: int = ...
    file_id: int = ...
    create_time: int = ...

    def __init__(self, id: int, post_id: int, file_id: int, create_time: int):
        self.id = id
        self.post_id = post_id
        self.file_id = file_id
        self.create_time = create_time


class PostAttachmentsCreateRequest(object):
    post_id: int = ...
    file_ids: list[int] = ...

    def __init__(self, post_id: int, file_ids: list[int]):
        self.post_id = post_id
        self.file_ids = file_ids


class PostAttachmentsCreateResult(object):
    post_attachments: list[PostAttachment]

    def __init__(self, post_attachments: list[PostAttachment]) -> None:
        self.post_attachments = post_attachments


class PostAttachmentsGetFilter(object):
    post_attachment_ids: Optional[List[int]] = ...
    post_ids: Optional[List[int]]

    def __init__(
        self, post_attachment_ids: Optional[List[int]] = None, post_ids: Optional[List[int]] = None
    ):
        self.post_attachment_ids = post_attachment_ids
        self.post_ids = post_ids


class PostAttachmentsGetResult(object):
    post_attachments: List[PostAttachment] = ...

    def __init__(self, post_attachments: List[PostAttachment]) -> None:
        self.post_attachments = post_attachments
