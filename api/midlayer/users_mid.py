from typing import Optional

from api.api_utils import hash_password, verify_hash
from api.dao.users_dao import UsersDAO
from api.typings.users import User, UsersGetFilter


class UserMidlayerConnections:
    def __init__(self, config, users_dao: Optional[UsersDAO] = None):
        self.users_dao = users_dao if users_dao else UsersDAO(config=config)


class UsersMidlayerMixin(object):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None):
        connections = (
            conns.user_mid_conns
            if conns and conns.user_mid_conns
            else UserMidlayerConnections(config)
        )
        self.users_dao = connections.users_dao

        ## Call the next mixins constructor
        self.super().__init__(config, conns)

    def users_get(self):
        ...

    def get_user_by_username_and_password(self, filter: UsersGetFilter) -> User:

        if not filter.password or not isinstance(filter.password, str):
            raise Exception(f"Invalid value {filter.password} for filter argument password")

        if not filter.username or not isinstance(filter.username, str):
            raise Exception(f"Invalid value {filter.username} for filter argument username")

        user_with_password = self.users_dao.get_user_by_username(
            username=filter.username, include_password=True
        )

        if not self._is_correct_password(filter.password, user_with_password.password_hash):
            raise Exception(
                f"Cannot get user with username {filter.username}. Incorrect password provided"
            )

        return self.users_dao.strip_users_password(user_with_password)

    def _is_correct_password(self, password: str, hashed_password: str) -> bool:
        return verify_hash(hashed_password, password)
