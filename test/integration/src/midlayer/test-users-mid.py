import time
from unittest.mock import Mock

import bcrypt
from integration import IntegrationTestCase

from api.midlayer.users_mid import UsersMidlayer
from api.typings.users import User, UsersGetFilter, UserWithPassword


class UsersMidIntegrationTestCase(IntegrationTestCase):
    def setUp(self):
        now = time.time()
        self.test_user = User(
            id=123,
            username="testUser123",
            first_name="Mikel",
            second_name="Arteta",
            create_time=now,
            is_deleted=False,
            email="mikel@gmail.com",
            last_login_date=None,
            language_id=None,
            timezone=None,
        )
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw("password1", salt)

        self.test_user_with_password = UserWithPassword(
            self.user, password_hash=password_hash, salt=salt
        )

    def _seed_user(self):

        sql = """
            INSERT INTO user(username, first_name, second_name, create_time, is_deleted, email, last_login_date, language_id, timezone, password_hash, salt)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        binds = list(vars(self.test_user_with_password).values())

        binds = binds[1:]  ## Ignore the id
        self.db.run_query(sql, binds)

    def get_user_by_username_and_password(self):
        self._seed_user()

        users_mid = UsersMidlayer()

        filter = UsersGetFilter(username="testUser123", password="password1")
        user_result = users_mid.get_user_by_username_and_password(filter=filter)

        user_result_dict = vars(user_result)

        test_user_dict = vars(self.test_user)
        self.assertEqual(user_result_dict, test_user_dict, "Should return the correct user")

        self.assertNotIsInstance(
            user_result, UserWithPassword, "Should not return a user with password information"
        )

        self.assertNone(
            user_result_dict.get("password_hash", None), "Should not return the users password"
        )

        self.assertNone(
            user_result_dict.get("salt", None), "Should not return the users password salt"
        )

    def get_user_by_username_and_incorrect_password(self):
        self._seed_user()

        users_mid = UsersMidlayer()

        filter = UsersGetFilter(username="testUser123", password="thisPasswordIsWrong")

        with self.assertRaises(
            Exception,
            f"Cannot get user with username {filter.username}. Incorrect password provided",
        ):

            user_result = users_mid.get_user_by_username_and_password(filter=filter)
