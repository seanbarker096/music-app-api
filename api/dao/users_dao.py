import logging
import time
from typing import Dict, List, Optional

from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import (
    assert_row_key_exists,
    build_update_set_string,
    build_where_query_string,
)
from api.typings.users import (
    User,
    UserCreateRequest,
    UsersGetFilter,
    UserUpdateRequest,
    UserWithPassword,
)
from api.utils import hash_password
from exceptions.db.exceptions import DBDuplicateKeyException
from exceptions.response.exceptions import UserNotFoundException


class UserDBAlias:
    USER_ID = "user_id"
    USER_USERNAME = "user_username"
    USER_FIRST_NAME = "user_first_name"
    USER_SECOND_NAME = "user_second_name"
    USER_FULL_NAME = "user_full_name"
    USER_BIO = "user_bio"
    USER_CREATE_TIME = "user_create_time"
    USER_IS_DELETED = "user_is_deleted"
    USER_EMAIL = "user_email"
    USER_AVATAR_FILE_UUID = "user_avatar_file_uuid"
    USER_LAST_LOGIN_DATE = "user_last_login_date"
    USER_LANGUAGE_ID = "user_language_id"
    USER_TIMEZONE_ID = "USER_TIMEZONE_ID"
    USER_PASSWORD_HASH = "user_password_hash"
    USER_SALT = "user_salt"


class UsersDAO(object):
    db: DBConnectionManager

    # TODO: Add full_name if we decide we want it returned for GET requests
    USER_SELECTS = [
        "id as " + UserDBAlias.USER_ID,
        "username as " + UserDBAlias.USER_USERNAME,
        "first_name as " + UserDBAlias.USER_FIRST_NAME,
        "second_name as " + UserDBAlias.USER_SECOND_NAME,
        "full_name as " + UserDBAlias.USER_FULL_NAME,
        "bio as " + UserDBAlias.USER_BIO,
        "UNIX_TIMESTAMP(create_time) as " + UserDBAlias.USER_CREATE_TIME,
        "is_deleted as " + UserDBAlias.USER_IS_DELETED,
        "email as " + UserDBAlias.USER_EMAIL,
        "avatar_file_uuid as " + UserDBAlias.USER_AVATAR_FILE_UUID,
        "UNIX_TIMESTAMP(last_login_date) as " + UserDBAlias.USER_LAST_LOGIN_DATE,
        "language_id as " + UserDBAlias.USER_LANGUAGE_ID,
        "timezone_id as " + UserDBAlias.USER_TIMEZONE_ID,
    ]

    USER_SELECTS_WITH_PASSWORD = [
        *USER_SELECTS,
        "password_hash as " + UserDBAlias.USER_PASSWORD_HASH,
        "salt as " + UserDBAlias.USER_SALT,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None) -> None:
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def users_get(self, filter: UsersGetFilter) -> List[User]:
        selects = f"""
            SELECT {', '.join(self.USER_SELECTS)} 
            FROM users
        """

        wheres = []
        binds = []

        if filter.user_ids and isinstance(filter.user_ids, list):
            wheres.append("id in %s")
            binds.append(filter.user_ids)

        if filter.search_query:
            search_wheres = []
            search_wheres.append("username LIKE %s")
            binds.append("%" + filter.search_query + "%")
            search_wheres.append("full_name LIKE %s")
            binds.append("%" + filter.search_query + "%")

            search_where_string = "(" + " OR ".join(search_wheres) + ")"
            wheres.append(search_where_string)

        where_string = build_where_query_string(wheres, "AND")

        binds.append(filter.limit if filter.limit else 20)

        sql = f"""
            {selects}
            {where_string}
            LIMIT %s
            """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)

            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = self._build_user_from_db_row(row)
                users.append(user)

            return users

    def get_user_by_username_or_email(
        self, username: Optional[str], email: Optional[str], include_password=False
    ) -> User | UserWithPassword:

        selects = [*self.USER_SELECTS_WITH_PASSWORD] if include_password else [*self.USER_SELECTS]

        wheres = []
        binds = []

        if username:
            wheres.append("username = %s")
            binds.append(username)

        if email:
            wheres.append("email = %s")
            binds.append(email)

        where_string = build_where_query_string(wheres, "OR")

        sql = f"""
            SELECT {', '.join(selects)}
            FROM users
            {where_string}
        """

        try:
            with self.db(self.config) as cursor:
                cursor.execute(sql, binds)
                rows = cursor.fetchall()

        except Exception as err:
            raise Exception(
                f"Failed to get user from the database because {str(err)}. Email: {email}. Username: {username}"
            )

        if len(rows) == 0:
            raise UserNotFoundException(
                f"Failed to find user. Username provided: {username}. Email provided: {email}"
            )

        if len(rows) > 1:
            raise Exception(
                f"Found more than one user. Email provided: {email}. Username provided: {username}"
            )

        user = (
            self._build_user_with_password_from_db_row(db_row=rows[0])
            if include_password
            else self._build_user_from_db_row(db_row=rows[0])
        )

        return user

    def user_create(self, request: UserCreateRequest, password_hash: str) -> User:

        sql = """
            INSERT INTO users(username, first_name, second_name, full_name, bio, create_time, is_deleted, email, avatar_file_uuid, last_login_date, language_id, timezone_id, password_hash, salt)
            VALUES(%s, %s, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s)
        """

        now = time.time()

        hash_password(request.password)

        fullname = (
            request.first_name + request.second_name
            if request.second_name and request.first_name
            else None
        )
        binds = (
            request.username,
            request.first_name,
            request.second_name,
            fullname,
            None,
            now,
            0,
            request.email,
            None,
            now,
            1,
            1,
            password_hash,
            None,  ## Current implementation for passwords doesn't require us to store a salt
        )

        try:
            with self.db(self.config) as cursor:
                cursor.execute(sql, binds)

                user_id = cursor.lastrowid

            return User(
                id=user_id,
                username=request.username,
                first_name=request.first_name,
                second_name=request.second_name,
                full_name=fullname,
                bio=None,
                create_time=now,
                is_deleted=False,
                avatar_file_uuid=None,
                email=request.email,
                last_login_date=now,
                language_id=1,
                timezone_id=1,
            )

        except DBDuplicateKeyException as e:
            raise e

        except Exception:
            raise Exception(
                f"Failed to create user with username {request.username} and email {request.email}"
            )

    def user_update(self, request: UserUpdateRequest) -> User:
        if not request.user_id:
            raise Exception(
                "Cannot update user as not user_id. Must provide user_id to update a user"
            )

        ## Get user to update
        filter = UsersGetFilter(user_ids=[request.user_id])
        users = self.users_get(filter)

        if len(users) == 0:
            raise UserNotFoundException(
                f"Failed to update user with id {request.user_id} because user could not be found."
            )

        user = users[0]

        updates = []
        binds = []

        if request.avatar_file_uuid is not None:
            updates.append("avatar_file_uuid = %s")
            binds.append(request.avatar_file_uuid)
            user.avatar_file_uuid = request.avatar_file_uuid

        if request.bio is not None:
            updates.append("bio = %s")
            binds.append(request.bio)
            user.bio = request.bio

        if request.first_name is not None:
            updates.append("first_name = %s")
            binds.append(request.first_name)
            user.first_name = request.first_name

        if request.second_name is not None:
            updates.append("second_name = %s")
            binds.append(request.second_name)
            user.second_name = request.second_name

        if len(updates) == 0:
            raise Exception(
                "Failed to update user because no fields provided to update in the user update request, or no fields in request have changed from original users fields"
            )

        set_string = build_update_set_string(updates)

        sql = f"""
            UPDATE users {set_string} WHERE id = {request.user_id}
        """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)

            if cursor.rowcount == 0:
                # This can happen if no fields were actually updated on the user, because the request did not provide any different values
                logging.warning("Failed to update any users for the provided request parameters")

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

        assert_row_key_exists(db_row, UserDBAlias.USER_FULL_NAME)
        full_name = db_row[UserDBAlias.USER_FULL_NAME]

        assert_row_key_exists(db_row, UserDBAlias.USER_BIO)
        bio = db_row[UserDBAlias.USER_BIO]

        assert_row_key_exists(db_row, UserDBAlias.USER_CREATE_TIME)
        create_unix_time = int(db_row[UserDBAlias.USER_CREATE_TIME])

        assert_row_key_exists(db_row, UserDBAlias.USER_IS_DELETED)
        is_deleted = db_row[UserDBAlias.USER_IS_DELETED]

        assert_row_key_exists(db_row, UserDBAlias.USER_EMAIL)
        email = db_row[UserDBAlias.USER_EMAIL]

        assert_row_key_exists(db_row, UserDBAlias.USER_LAST_LOGIN_DATE)
        last_login_unix_time = int(db_row[UserDBAlias.USER_LAST_LOGIN_DATE])

        assert_row_key_exists(db_row, UserDBAlias.USER_AVATAR_FILE_UUID)
        avatar_file_uuid = db_row[UserDBAlias.USER_AVATAR_FILE_UUID]

        assert_row_key_exists(db_row, UserDBAlias.USER_LANGUAGE_ID)
        language_id = db_row[UserDBAlias.USER_LANGUAGE_ID]

        assert_row_key_exists(db_row, UserDBAlias.USER_TIMEZONE_ID)
        timezone_id = db_row[UserDBAlias.USER_TIMEZONE_ID]

        return User(
            id=user_id,
            username=username,
            first_name=first_name,
            second_name=second_name,
            full_name=full_name,
            bio=bio,
            create_time=create_unix_time,
            is_deleted=is_deleted,
            email=email,
            last_login_date=last_login_unix_time,
            avatar_file_uuid=avatar_file_uuid,
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
            full_name=user_with_password.full_name,
            bio=user_with_password.bio,
            create_time=user_with_password.create_time,
            is_deleted=user_with_password.is_deleted,
            email=user_with_password.email,
            avatar_file_uuid=user_with_password.avatar_file_uuid,
            last_login_date=user_with_password.last_login_date,
            language_id=user_with_password.language_id,
            timezone_id=user_with_password.timezone_id,
        )
