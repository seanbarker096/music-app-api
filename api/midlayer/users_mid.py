import bcrypt

from api.dao.users_dao import UsersDAO
from api.typings.users import User, UsersGetFilter


class UsersMidlayerMixin(object):
    def __init__(self, config, users_dao: UsersDAO = None):
        self.users_dao = users_dao if users_dao else UsersDAO(config)

    def users_get(self):
        ...

    def get_user_by_username_and_password(self, filter: UsersGetFilter) -> User:

        if not filter.password or not isinstance(filter.password, str):
            raise Exception(f"Invalid value {filter.password} for filter argument password")

        if not filter.username or not isinstance(filter.username, str):
            raise Exception(f"Invalid value {filter.username} for filter argument username")

        try:
            users = self.users_dao.get_user_by_username(username=filter.username)

        ## TODO: Keep code checking length here and place DBException as Exception type
        except:
            raise Exception(f"Failed to get user with username {filter.username}")

        if len(users) == 0:
            raise Exception(
                f"Failed to find user with username {filter.username} because they do not exist"
            )

        return users[0]

    def _check_password(self, user: User, password: str):
        bytes_password = password.encode("utf8")

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(bytes_password, salt)
