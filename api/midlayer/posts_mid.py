from typing import Optional

from api.dao.posts_dao import PostsDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.posts import PostCreateRequest, PostCreateResult
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
