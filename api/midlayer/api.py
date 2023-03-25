from typing import Optional

from api.midlayer.features_mid import FeaturesMidlayerConnections, FeaturesMidlayerMixin
from api.midlayer.performances_mid import (
    PerformanceAttendancesMidlayerConnections,
    PerformanceAttendancesMidlayerMixin,
    PerformancesMidlayerConnections,
    PerformancesMidlayerMixin,
)
from api.midlayer.performers_mid import (
    PerformersMidlayerConnections,
    PerformersMidlayerMixin,
)
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
        performer_mid_conns: Optional[PerformersMidlayerConnections] = None,
        feature_mid_conns: Optional[PerformersMidlayerConnections] = None,
        tag_mid_conns: Optional[TagsMidlayerConnections] = None,
        performance_mid_conns: Optional[PerformancesMidlayerConnections] = None,
        performance_attendance_mid_conns: Optional[
            PerformanceAttendancesMidlayerConnections
        ] = None,
    ):
        self.post_mid_conns = post_mid_conns if post_mid_conns else PostMidlayerConnections(config)
        self.post_attachments_mid_conns = (
            post_attachments_mid_conns
            if post_attachments_mid_conns
            else PostAttachmentsMidlayerConnections(config)
        )
        self.user_mid_conns = user_mid_conns if user_mid_conns else UserMidlayerConnections(config)
        self.performer_mid_conns = (
            performer_mid_conns if performer_mid_conns else PerformersMidlayerConnections(config)
        )
        self.feature_mid_conns = (
            feature_mid_conns if feature_mid_conns else FeaturesMidlayerConnections(config)
        )
        self.tag_mid_conns = tag_mid_conns if tag_mid_conns else TagsMidlayerConnections(config)
        self.performance_mid_conns = (
            performance_mid_conns
            if performance_mid_conns
            else PerformancesMidlayerConnections(config)
        )
        self.performance_attendance_mid_conns = (
            performance_attendance_mid_conns
            if performance_attendance_mid_conns
            else PerformanceAttendancesMidlayerConnections(config)
        )


class Midlayer(
    PostsMidlayerMixin,
    PostAttachmentsMidlayerMixin,
    UsersMidlayerMixin,
    PerformersMidlayerMixin,
    FeaturesMidlayerMixin,
    TagsMidlayerMixin,
    PerformancesMidlayerMixin,
    PerformanceAttendancesMidlayerMixin,
):
    def __init__(self, config, conns: Optional[MidlayerConnections] = None):
        connections = conns if conns else MidlayerConnections(config)
        super().__init__(config, connections)
