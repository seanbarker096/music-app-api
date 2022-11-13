import time
from typing import Dict, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists
from api.typings.users import User, UserCreateRequest, UsersGetFilter, UserWithPassword
from api.utils import date_time_to_unix_time, hash_password


class UserDBAlias:
    USER_ID = "user_id"
    USER_USERNAME = "user_username"
    USER_FIRST_NAME = "user_first_name"
    USER_SECOND_NAME = "user_second_name"
    USER_CREATE_TIME = "user_create_time"
    USER_IS_DELETED = "user_is_deleted"
    USER_EMAIL = "user_email"
    USER_LAST_LOGIN_DATE = "user_last_login_date"
    USER_LANGUAGE_ID = "user_language_id"
    USER_TIMEZONE_ID = "USER_TIMEZONE_ID"
    USER_PASSWORD_HASH = "user_password_hash"
    USER_SALT = "user_salt"


class UsersDAO(object):
    db: DB

    USER_SELECTS = [
        "id as " + UserDBAlias.USER_ID,
        "username as " + UserDBAlias.USER_USERNAME,
        "first_name as " + UserDBAlias.USER_FIRST_NAME,
        "second_name as " + UserDBAlias.USER_SECOND_NAME,
        "create_time as " + UserDBAlias.USER_CREATE_TIME,
        "is_deleted as " + UserDBAlias.USER_IS_DELETED,
        "email as " + UserDBAlias.USER_EMAIL,
        "last_login_date as " + UserDBAlias.USER_LAST_LOGIN_DATE,
        "language_id as " + UserDBAlias.USER_LANGUAGE_ID,
        "timezone_id as " + UserDBAlias.USER_TIMEZONE_ID,
    ]

    USER_SELECTS_WITH_PASSWORD = [
        *USER_SELECTS,
        "password_hash as " + UserDBAlias.USER_PASSWORD_HASH,
        "salt as " + UserDBAlias.USER_SALT,
    ]

    def __init__(self, config, db: Optional[DB] = None) -> None:
        self.db = db if db else DB(config)

    def users_get(self, filter: UsersGetFilter):
        ...

    def get_user_by_username(
        self, username: str, include_password=False
    ) -> User | UserWithPassword:

        selects = self.USER_SELECTS_WITH_PASSWORD if include_password else self.USER_SELECTS
        sql = f"""
            SELECT {', '.join(selects)}
            FROM users
            WHERE username = %s
        """

        binds = (username,)

        try:
            result = self.db.run_query(sql, binds)
        except Exception:
            raise Exception(f"Failed to get user with username {username} from the database")

        rows = result.get_rows()

        if len(rows) == 0:
            raise Exception(
                f"Failed to find user with username {username} because they do not exist"
            )

        if len(rows) > 1:
            raise Exception(f"Found more than one user with username {username}")

        user = (
            self._build_user_with_password_from_db_row(db_row=rows[0])
            if include_password
            else self._build_user_from_db_row(db_row=rows[0])
        )

        return user

    def user_create(self, request: UserCreateRequest, password_hash: str) -> User:

        sql = """
            INSERT INTO users(username, first_name, second_name, create_time, is_deleted, email, last_login_date, language_id, timezone_id, password_hash, salt)
            VALUES(%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s)
        """

        now = time.time()

        hash_password(request.password)

        binds = (
            request.username,
            request.first_name,
            request.second_name,
            now,
            False,
            request.email,
            now,
            1,
            1,
            password_hash,
            None,  ## Current implementation for passwords doesn't require us to store a salt
        )

        try:
            db_result = self.db.run_query(sql, binds)

            user_id = db_result.get_last_row_id()

            return User(
                id=user_id,
                username=request.username,
                first_name=request.first_name,
                second_name=request.second_name,
                create_time=now,
                is_deleted=False,
                email=request.email,
                last_login_date=now,
                language_id=1,
                timezone_id=1,
            )
        except:
            raise Exception(f"Failed to create user with username {request.username}")

    def _build_user_from_db_row(self, db_row: Dict[str, any]) -> User:

        assert_row_key_exists(db_row, UserDBAlias.USER_ID)
        user_id = int(db_row[UserDBAlias.USER_ID])

        assert_row_key_exists(db_row, UserDBAlias.USER_USERNAME)
        username = db_row[UserDBAlias.USER_USERNAME]

        assert_row_key_exists(db_row, UserDBAlias.USER_FIRST_NAME)
        first_name = db_row[UserDBAlias.USER_FIRST_NAME]

        assert_row_key_exists(db_row, UserDBAlias.USER_SECOND_NAME)
        second_name = db_row[UserDBAlias.USER_SECOND_NAME]

        assert_row_key_exists(db_row, UserDBAlias.USER_CREATE_TIME)
        create_unix_time = float(date_time_to_unix_time(db_row[UserDBAlias.USER_CREATE_TIME]))

        assert_row_key_exists(db_row, UserDBAlias.USER_IS_DELETED)
        is_deleted = db_row[UserDBAlias.USER_IS_DELETED]

        assert_row_key_exists(db_row, UserDBAlias.USER_EMAIL)
        email = db_row[UserDBAlias.USER_EMAIL]

        assert_row_key_exists(db_row, UserDBAlias.USER_LAST_LOGIN_DATE)
        last_login_unix_time = float(
            date_time_to_unix_time(db_row[UserDBAlias.USER_LAST_LOGIN_DATE])
        )

        assert_row_key_exists(db_row, UserDBAlias.USER_LANGUAGE_ID)
        language_id = db_row[UserDBAlias.USER_LANGUAGE_ID]

        assert_row_key_exists(db_row, UserDBAlias.USER_TIMEZONE_ID)
        timezone_id = db_row[UserDBAlias.USER_TIMEZONE_ID]

        return User(
            id=user_id,
            username=username,
            first_name=first_name,
            second_name=second_name,
            create_time=create_unix_time,
            is_deleted=is_deleted,
            email=email,
            last_login_date=last_login_unix_time,
            language_id=language_id,
            timezone_id=timezone_id,
        )

    def _build_user_with_password_from_db_row(self, db_row: Dict[str, any]) -> UserWithPassword:

        user = self._build_user_from_db_row(
            db_row=db_row,
        )

        assert_row_key_exists(db_row, UserDBAlias.USER_PASSWORD_HASH)
        password_hash = db_row[UserDBAlias.USER_PASSWORD_HASH]

        assert_row_key_exists(db_row, UserDBAlias.USER_SALT)
        salt = db_row[UserDBAlias.USER_SALT]

        return UserWithPassword(
            user=user,
            password_hash=password_hash,
            salt=salt,
        )

    def strip_users_password(self, user_with_password: UserWithPassword) -> User:
        if not isinstance(user_with_password, UserWithPassword):
            raise Exception(
                "Invalid argument user_with_password provided. Must provide user of type UserWithPassword"
            )

        return User(
            id=user_with_password.id,
            username=user_with_password.username,
            first_name=user_with_password.first_name,
            second_name=user_with_password.second_name,
            create_time=user_with_password.create_time,
            is_deleted=user_with_password.is_deleted,
            email=user_with_password.email,
            last_login_date=user_with_password.last_login_date,
            language_id=user_with_password.language_id,
            timezone_id=user_with_password.timezone_id,
        )
