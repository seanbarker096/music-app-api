
from api.midlayer.events_mid import EventsMidlayerMixin
from api.midlayer.features_mid import FeaturesMidlayerMixin
from api.midlayer.performances_mid import (
    PerformanceAttendancesMidlayerMixin,
    PerformancesMidlayerMixin,
)
from api.midlayer.performers_mid import PerformersMidlayerMixin
from api.midlayer.posts_mid import PostAttachmentsMidlayerMixin, PostsMidlayerMixin
from api.midlayer.tags_mid import TagsMidlayerMixin
from api.midlayer.users_mid import UsersMidlayerMixin


class Midlayer(
    PostsMidlayerMixin,
    PostAttachmentsMidlayerMixin,
    UsersMidlayerMixin,
    PerformersMidlayerMixin,
    FeaturesMidlayerMixin,
    TagsMidlayerMixin,
    PerformancesMidlayerMixin,
    PerformanceAttendancesMidlayerMixin,
    EventsMidlayerMixin,
):
    def __init__(self, config):
        super().__init__(config)
