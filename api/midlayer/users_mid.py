import bcrypt

from api.dao.users_dao import UsersDAO
from api.typings.users import User, UsersGetFilter


class UsersMidlayer(object):
    def __init__(self, config, users_dao: UsersDAO = None):
        self.users_dao = users_dao if users_dao else UsersDAO(config)

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

        if not self._is_correct_password(
            filter.password, user_with_password.password_hash, user_with_password.salt
        ):
            raise Exception(
                f"Cannot get user with username {filter.username}. Incorrect password provided"
            )

        return self.users_dao.strip_users_password(user_with_password)

    def _is_correct_password(self, password: str, hashed_password: str, salt: str) -> bool:
        bytes_password = password.encode("utf8")

        hash = bcrypt.hashpw(bytes_password, salt)

        return hashed_password == hash
