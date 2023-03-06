from typing import Optional

from api.midlayer.artists_mid import ArtistsMidlayerConnections, ArtistsMidlayerMixin
from api.midlayer.features_mid import FeaturesMidlayerConnections, FeaturesMidlayerMixin
from api.midlayer.posts_mid import (
    PostAttachmentsMidlayerConnections,
    PostAttachmentsMidlayerMixin,
    PostMidlayerConnections,
    PostsMidlayerMixin,
)
from api.midlayer.tags_mid import TagsMidlayerConnections, TagsMidlayerMixin
from api.midlayer.users_mid import UserMidlayerConnections, UsersMidlayerMixin


class MidlayerConnections:
    def __init__(
        self,
        config,
        post_mid_conns: Optional[PostMidlayerConnections] = None,
        post_attachments_mid_conns: Optional[PostAttachmentsMidlayerConnections] = None,
        user_mid_conns: Optional[UserMidlayerConnections] = None,
        artist_mid_conns: Optional[ArtistsMidlayerConnections] = None,
        feature_mid_conns: Optional[ArtistsMidlayerConnections] = None,
        tag_mid_conns: Optional[TagsMidlayerConnections] = None,
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
        self.feature_mid_conns = (
            feature_mid_conns if feature_mid_conns else FeaturesMidlayerConnections(config)
        )
        self.tag_mid_conns = tag_mid_conns if tag_mid_conns else TagsMidlayerConnections(config)


class Midlayer(
    PostsMidlayerMixin,
    PostAttachmentsMidlayerMixin,
    UsersMidlayerMixin,
    ArtistsMidlayerMixin,
    FeaturesMidlayerMixin,
    TagsMidlayerMixin,
):
    def __init__(self, config, conns: Optional[MidlayerConnections] = None):
        connections = conns if conns else MidlayerConnections(config)
        super().__init__(config, connections)
