from typing import Optional

from api.midlayer.posts_mid import (
    PostAttachmentsMidlayerConnections,
    PostAttachmentsMidlayerMixin,
    PostMidlayerConnections,
    PostsMidlayerMixin,
)
from api.midlayer.users_mid import UserMidlayerConnections, UsersMidlayerMixin


class MidlayerConnections:
    def __init__(
        self,
        config,
        post_mid_conns: Optional[PostMidlayerConnections] = None,
        post_attachments_mid_conns: Optional[PostAttachmentsMidlayerConnections] = None,
        user_mid_conns: Optional[UserMidlayerConnections] = None,
    ):
        self.post_mid_conns = post_mid_conns if post_mid_conns else PostMidlayerConnections(config)
        self.post_attachments_mid_conns = (
            post_attachments_mid_conns
            if post_attachments_mid_conns
            else PostAttachmentsMidlayerConnections(config)
        )
        self.user_mid_conns = user_mid_conns if user_mid_conns else UserMidlayerConnections(config)


class Midlayer(PostsMidlayerMixin, PostAttachmentsMidlayerMixin, UsersMidlayerMixin):
    def __init__(self, config, conns: Optional[MidlayerConnections] = None):
        connections = conns if conns else MidlayerConnections(config)
        super().__init__(config, connections)
