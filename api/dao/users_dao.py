from typing import Dict, Optional

import bcrypt

from api.db.db import DB
from api.midlayer.users_mid import User, UsersGetFilter


class UsersDAO(object):
    db: DB

    def __init__(self, config, db: Optional[DB] = None) -> None:
        self.db = db if db else DB(config)

    def users_get(self, filter: UsersGetFilter):
        ...

    def get_user_by_username(self, username: str) -> User:
        sql = """
            SELECT username, first_name, second_name, create_time, is_deleted, email, last_login_date, language_id, timezone 
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

        user = self._build_user(rows[0])

        return user

    def _build_user_from_db_row(self, db_row: Dict[str, any]) -> User:
        ...
