import json
from typing import Optional

from api.dao.users_dao import UsersDAO
from api.db.db import DBConnectionManager, DBDuplicateKeyException
from api.file_service.api import FileService
from api.file_service.typings.typings import FilesGetFilter, FilesGetResult
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
from api.utils.rest_utils import process_string_request_param
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import (
    ResponseBaseException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class UserMidlayerConnections:
    def __init__(
        self,
        config,
        users_dao: Optional[UsersDAO] = None,
        file_service: Optional[FileService] = None,
    ):
        self.users_dao = users_dao if users_dao else UsersDAO(config=config)
        self.file_service = file_service if file_service else FileService(config=config)


class UsersMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[UserMidlayerConnections] = None, **kwargs):
        self.users_dao = conns.users_dao if conns and conns.users_dao else UsersDAO(config=config)
        self.file_service = (
            conns.file_service if conns and conns.file_service else FileService(config=config)
        )

        ## Call the next mixins constructor
        super().__init__(config)

    def users_get(
        self,
        filter: UsersGetFilter,
        projection: Optional[UsersGetProjection] = UsersGetProjection(),
    ) -> UsersGetResult:
        if filter.user_ids and (not isinstance(filter.user_ids, list) or len(filter.user_ids) == 0):
            raise InvalidArgumentException(
                "user_ids filter field must be a non empty list", filter.user_ids
            )

        search_query = process_string_request_param(
            "search_query", filter.search_query, optional=True, allow_empty_string=True
        )

        if not search_query and not filter.user_ids:
            raise InvalidArgumentException(
                f"Must provide at least one filter field. Request: {vars(filter)}", "filter"
            )

        users = []

        try:
            users = self.users_dao.users_get(filter)

            if projection.include_profile_image is True:

                profile_image_files_by_uuid = {}
                uuids = [
                    user.avatar_file_uuid for user in users if user.avatar_file_uuid is not None
                ]

                if len(uuids) > 0:
                    filter = FilesGetFilter(uuids=uuids)

                    profile_image_files = self.file_service.get_files(filter).files

                    profile_image_files_by_uuid = {file.uuid: file for file in profile_image_files}

                for user in users:
                    if user.avatar_file_uuid:
                        user.avatar_file = profile_image_files_by_uuid.get(
                            user.avatar_file_uuid, None
                        )

        except:
            raise Exception("Failed to get users")

        return UsersGetResult(users=users)

    def get_user_by_id(self, user_id: int) -> User:
        filter = UsersGetFilter(user_ids=[user_id])

        users = self.users_dao.users_get(filter)

        if len(users) == 0:
            raise UserNotFoundException(f"Could not find user with id {user_id}")

        return users[0]

    def get_user_by_username_or_email_and_password(
        self,
        password: str,
        username: Optional[str],
        email: Optional[str],
        projection: UsersGetProjection,
    ) -> User | UserWithPassword:

        process_string_request_param("username", username, optional=True)
        process_string_request_param("email", username, optional=True)
        process_string_request_param("password", password, optional=False)

        if not username and not email:
            raise InvalidArgumentException(
                "Must provide at least one of username or email", "username, email"
            )

        user_with_password = self.users_dao.get_user_by_username_or_email(
            username=username, email=email, include_password=True
        )

        if not self._is_correct_password(password, user_with_password.password_hash):
            raise UnauthorizedException(
                f"Cannot get user with username {username} or email {email}. Incorrect password provided"
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

        if request.first_name and (
            not isinstance(request.first_name, str) or len(request.first_name) == 0
        ):
            raise Exception(f"Invalid value {request.first_name} for request argument first_name")

        if request.second_name and (
            not isinstance(request.second_name, str) or len(request.second_name) == 0
        ):
            raise Exception(f"Invalid value {request.second_name} for request argument second_name")

        if not isinstance(request.email, str) or len(request.email) == 0:
            raise Exception(f"Invalid value {request.email} for request argument email")

        validate_password(password=request.password)

        password_hash = hash_password(request.password)

        existing_user = None

        try:
            # First check if user exists already
            existing_user = self.users_dao.get_user_by_username_or_email(
                username=request.username, email=request.email
            )

        except UserNotFoundException:
            pass

        if existing_user:
            raise UserAlreadyExistsException(
                f"Cannot create user. User with username {request.username} or email {request.email} already exists."
            )

        user = self.users_dao.user_create(request, password_hash=password_hash)
        return UserCreateResult(user=user)

    def user_update(self, request: UserUpdateRequest) -> UserUpdateResult:
        if not request.user_id:
            raise Exception("Must provide a valid user_id")

        process_string_request_param("avatar_file_uuid", request.avatar_file_uuid)
        process_string_request_param("bio", request.bio)
        process_string_request_param("first_name", request.first_name)
        process_string_request_param("second_name", request.second_name)

        if (
            not request.avatar_file_uuid
            and not request.bio
            and not request.first_name
            and not request.second_name
        ):
            raise InvalidArgumentException(
                f"Must provide at least one User field to update. Request: {json.dumps(vars(request))}",
                source="request",
            )

        try:
            updated_user = self.users_dao.user_update(request)

            return UserUpdateResult(user=updated_user)

        except UserNotFoundException as e:
            raise e
        except Exception:
            raise Exception(f"Failed to update user with id {request.user_id}.")
