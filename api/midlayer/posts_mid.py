from typing import Optional

from api.dao.posts_dao import PostsDAO


class PostMidlayerConnections:
    def __init__(self, config, post_dao: Optional[PostsDAO] = None):
        self.post_dao = post_dao if post_dao else PostsDAO(config)


class PostsMidlayerMixin(object):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None):
        connections = (
            conns.post_mid_conns
            if conns and conns.post_mid_conns
            else PostMidlayerConnections(config)
        )
        self.posts_dao = connections.post_dao

        ## Call the next mixins constructor
        self.super().__init__(config, conns)

    def post_create(self):
        ...
