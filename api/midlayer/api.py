from typing import Optional

from api.midlayer.artists_mid import ArtistsMidlayerConnections, ArtistsMidlayerMixin
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
        artist_mid_conns: Optional[ArtistsMidlayerConnections] = None,
    ):
        self.post_mid_conns = post_mid_conns if post_mid_conns else PostMidlayerConnections(config)
        self.post_attachments_mid_conns = (
            post_attachments_mid_conns
            if post_attachments_mid_conns
            else PostAttachmentsMidlayerConnections(config)
        )
        self.user_mid_conns = user_mid_conns if user_mid_conns else UserMidlayerConnections(config)
        self.artist_mid_conns = (
            artist_mid_conns if artist_mid_conns else ArtistsMidlayerConnections(config)
        )


class Midlayer(
    PostsMidlayerMixin, PostAttachmentsMidlayerMixin, UsersMidlayerMixin, ArtistsMidlayerMixin
):
    def __init__(self, config, conns: Optional[MidlayerConnections] = None):
        connections = conns if conns else MidlayerConnections(config)
        super().__init__(config, connections)
