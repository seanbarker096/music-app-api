from api.midlayer.posts_mid import PostsMidlayerMixin
from api.midlayer.users_mid import UsersMidlayer


class Midlayer:
    users_midlayer: UsersMidlayer

    def __init__(self, config, users_midlayer=None):
        self.users_midlayer = users_midlayer if users_midlayer else UsersMidlayer(config)
