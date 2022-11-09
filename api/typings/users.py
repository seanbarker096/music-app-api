from typing import Optional


class User:
    id: int
    username: str
    first_name: str
    second_name: str
    create_time: int
    is_deleted: bool
    email: str
    last_login_date: Optional[str]
    language_id: Optional[str]
    timezone_id: Optional[int]

    def __init__(
        self,
        id: int,
        username: str,
        first_name: str,
        second_name: str,
        create_time: int,
        is_deleted: bool,
        email: str,
        last_login_date: Optional[str],
        language_id: Optional[str],
        timezone_id: Optional[str],
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.create_time = create_time
        self.is_deleted = is_deleted
        self.email = email
        self.last_login_date = last_login_date
        self.language_id = language_id
        self.timezone_id = timezone_id


class UserWithPassword:
    user: User
    password_hash: str
    salt: str

    def __init__(self, user: User, password_hash: str, salt: str):
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.second_name = user.second_name
        self.create_time = user.create_time
        self.is_deleted = user.is_deleted
        self.email = user.email
        self.last_login_date = user.last_login_date
        self.language_id = user.language_id
        self.timezone_id = user.timezone_id

        self.password_hash = password_hash
        self.salt = salt


class UsersGetFilter:
    username: Optional[str]
    password: Optional[str]

    def __init__(self, username: Optional[str], password: Optional[str]) -> None:
        self.username = username
        self.password = password


class UsersGetResult:
    users: list[User]

    def __init__(self, users: list[User]):
        self.users = users
