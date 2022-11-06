from typing import Optional


class User:
    username: str
    first_name: str
    second_name: str
    create_time: int
    is_deleted: bool
    email: str
    password_hash: str
    last_login_date: Optional[str]
    language_id: Optional[str]
    timezone: Optional[int]

    def __init__(
        self,
        username: str,
        first_name: str,
        second_name: str,
        create_time: int,
        is_deleted: bool,
        email: str,
        password_hash: str,
        last_login_date: Optional[str],
        language_id: Optional[str],
        timezone: Optional[str],
    ):
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.create_time = create_time
        self.is_deleted = is_deleted
        self.email = email
        self.password_hash = password_hash
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
    user: User

    def __init__(self, user: User):
        self.user = user
