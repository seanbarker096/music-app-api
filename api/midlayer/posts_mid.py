from typing import Optional

from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostAttachmentsCreateResult,
    PostAttachmentsGetFilter,
    PostAttachmentsGetResult,
    PostCreateRequest,
    PostCreateResult,
    PostsGetFilter,
    PostsGetResult,
)
from exceptions.exceptions import InvalidArgumentException


class PostMidlayerConnections:
    def __init__(self, config, post_dao: Optional[PostsDAO] = None):
        self.post_dao = post_dao if post_dao else PostsDAO(config)


class PostsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):

        connections = (
            conns.post_mid_conns
            if conns and conns.post_mid_conns
            else PostMidlayerConnections(config)
        )
        self.posts_dao = connections.post_dao

        ## Call the next mixins constructor
        super().__init__(config, conns)

    def post_create(self, request: PostCreateRequest) -> PostCreateResult:
        if not isinstance(request.owner_id, int) or not str:
            raise InvalidArgumentException(
                f"Invalid value {request.owner_id} for argument owner_id", "owner_id"
            )

        if not isinstance(request.content, str) or not request.content:
            raise InvalidArgumentException(
                f"Invalid value {request.content} for argument content", "content"
            )

        try:
            post = self.posts_dao.post_create(request)
            return PostCreateResult(post=post)

        except Exception:
            raise Exception(
                f"Failed to create post with content {request.content} for user with id {request.owner_id}"
            )

    def posts_get(self, filter=PostsGetFilter) -> PostsGetResult:

        if filter.post_ids and len(filter.post_ids) == 0:
            raise InvalidArgumentException(
                "Invalid value provided for filter field post_ids. At least one post_id must be provided",
                "filter.post_ids",
            )

        if filter.is_deleted and not isinstance(filter.is_deleted, bool):
            raise InvalidArgumentException(
                "Invalid value provided for filter field is_deleted. A boolean argument must be provided",
                "filter.is_deleted",
            )

        posts = self.posts_dao.posts_get(filter)

        return PostsGetResult(posts=posts)


class PostAttachmentsMidlayerConnections:
    def __init__(self, config, post_attachments_dao: Optional[PostsDAO] = None):
        self.post_attachments_dao = (
            post_attachments_dao if post_attachments_dao else PostAttachmentsDAO(config)
        )


class PostAttachmentsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):
        connections = (
            conns.post_attachments_mid_conns
            if conns and conns.post_attachments_mid_conns
            else PostAttachmentsMidlayerConnections(config)
        )
        self.posts_attachments_dao = connections.post_attachments_dao

        ## Call the next mixins constructor
        super().__init__(config, conns)

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
        ...
