from typing import Optional

from api.api_utils import hash_password, validate_password, verify_hash
from api.dao.users_dao import UsersDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.users import (
    User,
    UserCreateRequest,
    UserCreateResult,
    UsersGetFilter,
    UsersGetProjection,
    UserWithPassword,
)


class UserMidlayerConnections:
    def __init__(self, config, users_dao: Optional[UsersDAO] = None):
        self.users_dao = users_dao if users_dao else UsersDAO(config=config)


class UsersMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):
        connections = (
            conns.user_mid_conns
            if conns and conns.user_mid_conns
            else UserMidlayerConnections(config)
        )
        self.users_dao = connections.users_dao

    def get_user_by_username_and_password(
        self, filter: UsersGetFilter, projection: UsersGetProjection
    ) -> User | UserWithPassword:

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

        if projection.password:
            return user_with_password

        return self.users_dao.strip_users_password(user_with_password)

    def _is_correct_password(self, password: str, hashed_password: str) -> bool:
        return verify_hash(hashed_password, password)

    def user_create(self, request: UserCreateRequest) -> UserCreateResult:
        ## TODO: Add validation for username length or maybe do this on front-end
        if not isinstance(request.username, str) or len(request.username) == 0:
            raise Exception(f"Invalid value {request.username} for request argument username")

        if not isinstance(request.first_name, str) or len(request.first_name) == 0:
            raise Exception(f"Invalid value {request.first_name} for request argument first_name")

        if not isinstance(request.second_name, str) or len(request.second_name) == 0:
            raise Exception(f"Invalid value {request.second_name} for request argument second_name")

        if not isinstance(request.email, str) or len(request.email) == 0:
            raise Exception(f"Invalid value {request.email} for request argument email")

        validate_password(password=request.password)

        password_hash = hash_password(request.password)

        user = self.users_dao.user_create(request, password_hash=password_hash)

        return UserCreateResult(user=user)
