from typing import Optional

from api.dao.users_dao import UsersDAO
from api.db.db import DBConnectionManager, DBDuplicateKeyException
from api.midlayer import BaseMidlayerMixin
from api.typings.users import (
    User,
    UserCreateRequest,
    UserCreateResult,
    UsersGetFilter,
    UsersGetProjection,
    UsersGetResult,
    UserUpdateRequest,
    UserUpdateResult,
    UserWithPassword,
)
from api.utils import hash_password, validate_password, verify_hash
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import (
    ResponseBaseException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class UserMidlayerConnections:
    def __init__(self, config, users_dao: Optional[UsersDAO] = None):
        self.users_dao = users_dao if users_dao else UsersDAO(config=config)


class UsersMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[UserMidlayerConnections] = None, **kwargs):
        self.users_dao = conns.users_dao if conns and conns.users_dao else UsersDAO(config=config)

        ## Call the next mixins constructor
        super().__init__(config)

    def users_get(self, filter: UsersGetFilter) -> UsersGetResult:
        if not isinstance(filter.user_ids, list) or len(filter.user_ids) == 0:
            raise InvalidArgumentException(
                "user_ids filter field must be a non empty list", filter.user_ids
            )

        users = []

        try:
            users = self.users_dao.users_get(filter)
        except:
            raise Exception("Failed to get users")

        return UsersGetResult(users=users)

    def get_user_by_id(self, user_id: int) -> User:
        filter = UsersGetFilter(user_id=user_id)

        users = self.users_dao.users_get(filter)

        if filter.password or filter.username:
            raise Exception(
                "get_user_by_id called with username or password filter set. Please use UsersMidlayerMixin:get_user_by_username_and_password instead"
            )

        if len(users) == 0:
            raise UserNotFoundException(f"Could not find user with id {user_id}")

        return users[0]

    def get_user_by_username_and_password(
        self, password: str, username: str, projection: UsersGetProjection
    ) -> User | UserWithPassword:

        if not password or not isinstance(password, str):
            raise Exception(f"Invalid value {password} for filter argument password")

        if not username or not isinstance(username, str):
            raise Exception(f"Invalid value {username} for filter argument username")

        user_with_password = self.users_dao.get_user_by_username(
            username=username, include_password=True
        )

        if not self._is_correct_password(password, user_with_password.password_hash):
            raise Exception(
                f"Cannot get user with username {username}. Incorrect password provided"
            )

        if projection.password:
            return user_with_password

        return self.users_dao.strip_users_password(user_with_password)

    def _is_correct_password(self, password: str, hashed_password: str) -> bool:
        try:
            return verify_hash(hashed_password, password)
        except:
            return False

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

        try:
            user = self.users_dao.user_create(request, password_hash=password_hash)
        ## TODO: Update to use our own duplicate key error and move to dao as mmidlayer shoiuyldnt know about db duplicate key exceptions
        except DBDuplicateKeyException as e:
            duplicate_key = e.get_column()
            duplicate_value = request.username if duplicate_key == "username" else request.email
            raise UserAlreadyExistsException(
                f"Cannot create user. User with {duplicate_key} {duplicate_value} already exists."
            )

        return UserCreateResult(user=user)

    def user_update(self, request: UserUpdateRequest) -> UserUpdateResult:
        if not request.user_id:
            raise Exception("Must provide a valid user_id")

        try:
            updated_user = self.users_dao.user_update(request)

            return UserUpdateResult(user=updated_user)

        except UserNotFoundException as e:
            raise e
        except Exception:
            raise Exception(f"Failed to update user with id {request.user_id}.")
