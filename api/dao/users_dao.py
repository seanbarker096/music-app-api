from typing import Dict, Optional

import bcrypt

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists
from api.midlayer.users_mid import User, UsersGetFilter


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
    USER_TIMEZONE = "user_timezone"


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
        "timezone as " + UserDBAlias.USER_TIMEZONE,
    ]

    def __init__(self, config, db: Optional[DB] = None) -> None:
        self.db = db if db else DB(config)

    def users_get(self, filter: UsersGetFilter):
        ...

    def get_user_by_username(self, username: str) -> User:
        sql = f"""
            SELECT {', '.join(self.USER_SELECTS)}
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

        user = self._build_user_from_db_row(rows[0])

        return user

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
        create_time = int(db_row[UserDBAlias.USER_CREATE_TIME])

        assert_row_key_exists(db_row, UserDBAlias.USER_IS_DELETED)
        is_deleted = db_row[UserDBAlias.USER_IS_DELETED]

        assert_row_key_exists(db_row, UserDBAlias.USER_EMAIL)
        email = db_row[UserDBAlias.USER_EMAIL]

        assert_row_key_exists(db_row, UserDBAlias.USER_LAST_LOGIN_DATE)
        last_login_date = (
            int(db_row[UserDBAlias.USER_LAST_LOGIN_DATE])
            if db_row[UserDBAlias.USER_LAST_LOGIN_DATE]
            else None
        )

        assert_row_key_exists(db_row, UserDBAlias.USER_LANGUAGE_ID)
        language_id = db_row[UserDBAlias.USER_LANGUAGE_ID]

        assert_row_key_exists(db_row, UserDBAlias.USER_TIMEZONE)
        timezone = db_row[UserDBAlias.USER_TIMEZONE]

        return User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            second_name=second_name,
            create_time=create_time,
            is_deleted=is_deleted,
            email=email,
            last_login_date=last_login_date,
            language_id=language_id,
            timezone=timezone,
        )
