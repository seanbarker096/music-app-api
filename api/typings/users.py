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
    timezone: Optional[int]

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
        timezone: Optional[str],
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
        self.timezone = timezone


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
