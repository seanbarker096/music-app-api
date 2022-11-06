from api.midlayer.posts_mid import PostsMidlayerMixin, UsersMidlayerMixin


class Midlayer(PostsMidlayerMixin, UsersMidlayerMixin):
    def __init__(self, config):
        super().__init__(config)
