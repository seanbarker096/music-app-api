from typing import List, Optional

from api.file_service.typings.typings import FileServiceFile


class User:
    id: int
    username: str
    first_name: str
    second_name: str
    full_name: str
    create_time: float
    is_deleted: bool
    email: str
    last_login_date: float
    bio: Optional[str]
    avatar_file_uuid: Optional[str]
    avatar_file: Optional[FileServiceFile]
    language_id: Optional[str]
    timezone_id: Optional[int]

    def __init__(
        self,
        id: int,
        username: str,
        first_name: str,
        second_name: str,
        full_name: str,
        create_time: int,
        is_deleted: bool,
        email: str,
        last_login_date: float,
        bio: Optional[str],
        language_id: Optional[str],
        timezone_id: Optional[str],
        avatar_file_uuid: Optional[str] = None,
        avatar_file: Optional[FileServiceFile] = None,
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.full_name = full_name
        self.bio = bio
        self.create_time = create_time
        self.is_deleted = is_deleted
        self.email = email
        self.avatar_file_uuid = avatar_file_uuid
        self.last_login_date = last_login_date
        self.language_id = language_id
        self.timezone_id = timezone_id
        self.avatar_file = avatar_file


class UserWithPassword:
    user: User
    password_hash: str
    salt: str

    def __init__(self, user: User, password_hash: str, salt: str):
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.second_name = user.second_name
        self.full_name = user.full_name
        self.bio = user.bio
        self.create_time = user.create_time
        self.is_deleted = user.is_deleted
        self.email = user.email
        self.avatar_file_uuid = user.avatar_file_uuid
        self.last_login_date = user.last_login_date
        self.language_id = user.language_id
        self.timezone_id = user.timezone_id

        self.password_hash = password_hash
        self.salt = salt


class UsersGetFilter:
    user_ids: Optional[List[str]] = None
    search_query: Optional[str] = None
    limit: Optional[int] = None

    def __init__(
        self,
        user_ids: Optional[List[str]] = None,
        search_query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.user_ids = user_ids
        self.search_query = search_query
        self.limit = limit


class UsersGetProjection:
    password: bool = ...
    include_profile_image: bool = ...

    def __init__(self, password: bool = False, include_profile_image: bool = False):
        self.password = password
        self.include_profile_image = True if include_profile_image is True else False


class UsersGetResult:
    users: list[User]

    def __init__(self, users: list[User]):
        self.users = users


class UserCreateRequest:
    username: str
    first_name: Optional[str]
    second_name: Optional[str]
    email: str
    password: str

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        second_name: Optional[str] = None,
    ):
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = password


class UserCreateResult:
    user: User

    def __init__(self, user: User):
        self.user = user


class UserUpdateRequest:
    user_id: int = ...
    avatar_file_uuid: Optional[str] = ...
    bio: Optional[str] = ...
    first_name: Optional[str] = ...
    second_name: Optional[str] = ...

    def __init__(self, user_id: int, avatar_file_uuid: Optional[str] = None, bio: Optional[str] = None, first_name: Optional[str] = None, second_name: Optional[str] = None):
        self.user_id = user_id
        self.avatar_file_uuid = avatar_file_uuid
        self.bio = bio
        self.first_name = first_name
        self.second_name = second_name


class UserUpdateResult:
    user: User

    def __init__(self, user: User):
        self.user = user
