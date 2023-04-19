import json
from typing import Optional

from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.posts import (
    FeaturedPostsGetFilter,
    PostAttachmentsCreateRequest,
    PostAttachmentsCreateResult,
    PostAttachmentsGetFilter,
    PostAttachmentsGetResult,
    PostCreateRequest,
    PostCreateResult,
    PostOwnerType,
    PostsGetFilter,
    PostsGetResult,
    ProfilePostsGetFilter,
    ProfileType,
)
from api.utils.rest_utils import (
    process_bool_request_param,
    process_enum_request_param,
    process_enum_set_param,
    process_int_request_param,
)
from exceptions.exceptions import InvalidArgumentException


class PostMidlayerConnections:
    def __init__(self, config, posts_dao: Optional[PostsDAO] = None):
        self.posts_dao = posts_dao if posts_dao else PostsDAO(config)


class PostsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[PostMidlayerConnections] = None, **kwargs):
        self.posts_dao = conns.posts_dao if conns and conns.posts_dao else PostsDAO(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def post_create(self, request: PostCreateRequest) -> PostCreateResult:
        if not request.creator_id or not isinstance(request.creator_id, int):
            raise InvalidArgumentException(
                f"Invalid value {request.creator_id} for argument creator_id", "creator_id"
            )

        if not request.owner_id or not isinstance(request.owner_id, int):
            raise InvalidArgumentException(
                f"Invalid value {request.owner_id} for argument owner_id", "owner_id"
            )

        if request.owner_type not in set(item.value for item in PostOwnerType):
            raise InvalidArgumentException(
                f"Invalid value {request.owner_type} for argument owner_type. Must provide a valid member of the PostOwnerType enum",
                "owner_type",
            )

        if not isinstance(request.content, str) or not request.content:
            raise InvalidArgumentException(
                f"Invalid value {request.content} for argument content", "content"
            )

        try:
            post = self.posts_dao.post_create(request)
            return PostCreateResult(post=post)

        except Exception as err:
            raise Exception(
                f"Failed to create post with content {request.content} for user with id {request.owner_id} because {str(err)}. Request: {vars(request)}"
            )

    def posts_get(self, filter=PostsGetFilter) -> PostsGetResult:

        if filter.ids and len(filter.ids) == 0:
            raise InvalidArgumentException(
                "Invalid value provided for filter field ids. At least one post_id must be provided",
                "filter.ids",
            )

        if filter.is_deleted and not isinstance(filter.is_deleted, bool):
            raise InvalidArgumentException(
                "Invalid value provided for filter field is_deleted. A boolean argument must be provided",
                "filter.is_deleted",
            )

        if filter.owner_ids and not isinstance(filter.owner_ids, list):
            raise InvalidArgumentException(
                "Invalid value provided for filter field owner_ids. At least one owner_id must be provided",
                "filter.owner_ids",
            )

        if filter.owner_types:
            print(filter.owner_types)
            process_enum_set_param("owner_types", filter.owner_types, PostOwnerType)

        if (filter.owner_ids and not filter.owner_types) or (
            filter.owner_types and not filter.owner_ids
        ):
            raise InvalidArgumentException(
                "Must provide both owner_types and owner_ids when filtering by owner_types or owner_ids",
                "filter.owner_types or filter.owner_ids",
            )

        if not filter.ids and not filter.is_deleted and not filter.owner_ids and not filter.owner_types:
            raise InvalidArgumentException(
                f"Ubounded request made to posts_get. Must provide at least one filter field. Filter: {vars(filter)}",
                "PostsGetFilter"
            )

        posts = self.posts_dao.posts_get(filter)

        return PostsGetResult(posts=posts)

    def profile_posts_get(self, filter=ProfilePostsGetFilter) -> PostsGetResult:
        if not filter.profile_id or not isinstance(filter.profile_id, int):
            raise InvalidArgumentException(
                f"Invalid value {filter.profile_id} for argument profile_id. Must be a valid integer.",
                "filter.profile_id",
            )

        if not filter.profile_type or filter.profile_type not in set(
            item.value for item in ProfileType
        ):
            raise InvalidArgumentException(
                f"Invalid value {filter.profile_type} for argument profile_type. Must be a valid member of ProfileType.",
                "filter.profile_type",
            )

        if not isinstance(filter.include_featured, bool):
            raise InvalidArgumentException(
                f"Invalid value {filter.include_featured} for argument include_featured. Must be a valid boolean.",
                "filter.include_featured",
            )

        if not isinstance(filter.include_owned, bool):
            raise InvalidArgumentException(
                f"Invalid value {filter.include_owned} for argument include_owned. Must be a valid boolean.",
                "filter.include_owned",
            )

        if not isinstance(filter.include_tagged, bool):
            raise InvalidArgumentException(
                f"Invalid value {filter.include_tagged} for argument include_tagged. Must be a valid boolean.",
                "filter.include_tagged",
            )

        if not filter.include_featured and not filter.include_owned and not filter.include_tagged:
            raise InvalidArgumentException(
                f"Must include at least one of include_featured, include_owned, or include_tagged.",
                "filter.include_featured, filter.include_owned, filter.include_tagged",
            )

        try:
            posts = self.posts_dao.profile_posts_get(filter)

        except Exception as err:
            raise Exception(
                f"Failed to get posts for profile with id {filter.profile_id} and type {filter.profile_type} because {json.dumps(str(err))}. Request: {vars(filter)}"
            )

        return PostsGetResult(posts=posts)
    
    ## TODO: COuld update this to include posts when counts=0 if filtes are set to false rather than throwing if at least one is not true
    def featured_posts_get(self, filter: FeaturedPostsGetFilter) -> PostsGetResult:
        process_int_request_param("owner_id", filter.owner_id, optional=False)
        process_enum_request_param("owner_type", filter.owner_type, PostOwnerType, optional=False)
        process_bool_request_param("is_featured_by_users", filter.is_featured_by_users)
        process_bool_request_param("is_featured_by_performers", filter.is_featured_by_performers)

        if not filter.is_featured_by_users and not filter.is_featured_by_performers:
            raise InvalidArgumentException(
                f"Must include at least one of is_featured_by_users or is_featured_by_performers.",
                "filter.is_featured_by_users, filter.is_featured_by_performers",
            )
        
        try:
            posts = self.posts_dao.featured_posts_get(filter)

            return PostsGetResult(posts=posts)

        except Exception as err:
            raise Exception(
                f"Failed to get featured posts for user with id {filter.owner_id} because {json.dumps(str(err))}. Request: {vars(filter)}"
            )




class PostAttachmentsMidlayerConnections:
    def __init__(self, config, post_attachments_dao: Optional[PostsDAO] = None):
        self.post_attachments_dao = (
            post_attachments_dao if post_attachments_dao else PostAttachmentsDAO(config)
        )


class PostAttachmentsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[PostAttachmentsMidlayerConnections] = None, **kwargs):
        self.posts_attachments_dao = conns.post_attachments_dao if conns and conns.post_attachments_dao else PostAttachmentsDAO(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def post_attachments_create(
        self, request: PostAttachmentsCreateRequest
    ) -> PostAttachmentsCreateResult:

        if not isinstance(request.post_id, int):
            raise InvalidArgumentException(
                f"Invalid value {request.post_id} for field post_id. Must provide a valid integer to create post attachments.",
                "post_id",
            )

        file_ids = request.file_ids

        print("file_ids", type(file_ids))
        if not isinstance(file_ids, list):
            raise InvalidArgumentException(
                f"Invalid value {file_ids} for field file_ids. Field must be iterable",
                "file_ids",
            )

        try:
            ## TODO: Check if files exist by injecting file serving and calling files_get with array of file_ids
            attachments = []
            for file_id in file_ids:
                attachment = self.posts_attachments_dao.post_attachment_create(
                    post_id=request.post_id, file_id=file_id
                )
                attachments.append(attachment)

            return PostAttachmentsCreateResult(post_attachments=attachments)

        except Exception:
            raise Exception(
                f"Failed to create attachment for post with id {request.post_id} and file with id {file_id}  "
            )

    def post_attachments_get(self, filter=PostAttachmentsGetFilter) -> PostAttachmentsGetResult:

        if not filter.post_attachment_ids and not filter.post_ids:
            raise InvalidArgumentException(
                "Must provide one of post_attachment_ids or post_ids in the filter", "filter"
            )

        if filter.post_attachment_ids and len(filter.post_attachment_ids) == 0:
            raise InvalidArgumentException(
                "Invalid argument provided for post_attachment_ids filter field. Value must be an of type list with at least one id provided",
                "filter.post_attachment_ids",
            )

        if filter.post_ids and len(filter.post_ids) == 0:
            raise InvalidArgumentException(
                "Invalid argument provided for post_ids filter field. Value must be an of type list with at least one id provided",
                "filter.post_ids",
            )

        try:
            post_attachments = self.posts_attachments_dao.post_attachments_get(filter=filter)
            return PostAttachmentsGetResult(post_attachments=post_attachments)

        except Exception as err:
            raise Exception(
                f"Failed to get post attachments because {str(err)}. Request: {vars(filter)}"
            )
