import copy
import time
from test.integration import IntegrationTestCase
from unittest.mock import Mock, patch

from api.midlayer.users_mid import UsersMidlayerMixin
from api.typings.users import (
    User,
    UserCreateRequest,
    UsersGetFilter,
    UsersGetProjection,
    UserUpdateRequest,
    UserWithPassword,
)
from api.utils import generate_salt, hash_password
from exceptions.response.exceptions import UserAlreadyExistsException


class UsersMidIntegrationTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        now = int(time.time())
        self.test_user = User(
            id=1,
            username="testUser123",
            first_name="Mikel",
            second_name="Arteta",
            create_time=now,
            is_deleted=False,
            email="mikel@gmail.com",
            avatar_file_uuid=None,
            last_login_date=now,
            language_id=1,
            timezone_id=1,
        )

        password_hash = hash_password("password1")

        self.test_user_with_password = UserWithPassword(
            self.test_user, password_hash=password_hash, salt="salt"
        )

    def _seed_user(self):

        sql = """
            INSERT INTO users(username, first_name, second_name, create_time, is_deleted, email, avatar_file_uuid, last_login_date, language_id, timezone_id, password_hash, salt)
            VALUES(%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s)
        """

        binds = list(vars(self.test_user_with_password).values())

        binds = binds[1:]  ## Ignore the id
        self.db.run_query(sql, binds)

    @patch("time.time")
    def test_user_create(self, time):
        time.return_value = self.current_time

        users_mid = UsersMidlayerMixin(config=self.config)

        request = UserCreateRequest(
            username="testUser123",
            first_name="Gabriel",
            second_name="Martinelli",
            email="gMartinelli@gmail.com",
            password="testPassword",
        )

        result = users_mid.user_create(request)

        user = result.user

        self.assertIsInstance(user.id, int, "Should return valid user id")
        self.assertEqual(request.email, user.email, "Should return the new users email address")
        self.assertEqual(request.first_name, user.first_name, "Should return the users firstname")
        self.assertFalse(user.is_deleted, "Should not mark the user as deleted")
        self.assertEqual(
            request.second_name, user.second_name, "Should return the users second name"
        )
        self.assertEqual(
            self.current_time, user.create_time, "Should return the correct created time"
        )
        self.assertEqual(
            self.current_time,
            user.last_login_date,
            "Should set the last login date to be the datetime at when the user was created",
        )
        self.assertEqual(None, user.avatar_file_uuid, "Should not have created a user avatar")
        self.assertEqual(1, user.language_id, "Should return the correct language id")
        self.assertEqual(1, user.timezone_id, "Should return the correct timezone id")

        ## Assert password stored correctly
        filter = UsersGetFilter(username="testUser123", password="testPassword")
        user_with_password = users_mid.get_user_by_username_and_password(
            filter=filter, projection=UsersGetProjection(password=True)
        )
        self.assertIsInstance(user_with_password.password_hash, str)
        self.assertTrue(len(user_with_password.password_hash))

    def test_user_create_with_duplicate_username(self):

        request = UserCreateRequest(
            username="testUser123",
            first_name="Gabriel",
            second_name="Martinelli",
            email="gMartinelli@gmail.com",
            password="testPassword",
        )

        users_mid = UsersMidlayerMixin(config=self.config)

        users_mid.user_create(request)

        with self.assertRaisesRegex(
            UserAlreadyExistsException,
            expected_regex=f"Cannot create user. User with username testUser123 already exists.",
            msg="Should raise correct exception if username is a duplicate",
        ):
            new_request = copy.copy(request)
            new_request.email = "gMartinelli2@gmail.com"
            users_mid.user_create(new_request)

    def test_user_create_with_duplicate_email(self):

        request = UserCreateRequest(
            username="testUser123",
            first_name="Gabriel",
            second_name="Martinelli",
            email="gMartinelli@gmail.com",
            password="testPassword",
        )

        users_mid = UsersMidlayerMixin(config=self.config)

        users_mid.user_create(request)

        with self.assertRaisesRegex(
            UserAlreadyExistsException,
            expected_regex=f"Cannot create user. User with email gMartinelli@gmail.com already exists.",
            msg="Should raise correct exception if email is a duplicate",
        ):
            new_request = copy.copy(request)
            new_request.username = "testUser888"
            users_mid.user_create(new_request)

    def test_get_user_by_username_and_password(self):
        self._seed_user()

        users_mid = UsersMidlayerMixin(self.config)

        filter = UsersGetFilter(username="testUser123", password="password1")
        user_result = users_mid.get_user_by_username_and_password(
            filter=filter, projection=UsersGetProjection()
        )

        user_result_dict = vars(user_result)

        test_user_dict = vars(self.test_user)
        self.assertEqual(user_result_dict, test_user_dict, "Should return the correct user")

        self.assertNotIsInstance(
            user_result, UserWithPassword, "Should not return a user with password information"
        )

        self.assertIsNone(
            user_result_dict.get("password_hash", None), "Should not return the users password"
        )

        self.assertIsNone(
            user_result_dict.get("salt", None), "Should not return the users password salt"
        )

    def test_get_user_by_username_and_incorrect_password(self):
        self._seed_user()

        users_mid = UsersMidlayerMixin(self.config)

        filter = UsersGetFilter(username="testUser123", password="thisPasswordIsWrong")

        with self.assertRaisesRegex(
            Exception,
            expected_regex=f"Cannot get user with username {filter.username}. Incorrect password provided",
            msg="Should raise exception with correct error message",
        ):
            users_mid.get_user_by_username_and_password(
                filter=filter, projection=UsersGetProjection()
            )

    def test_user_update(self):
        self._seed_user()

        users_mid = UsersMidlayerMixin(self.config)

        request = UserUpdateRequest(user_id=1, avatar_file_uuid="abcdefg")

        result = users_mid.user_update(request)
        updated_user = result.user

        self.assertEqual(1, updated_user.id, "Should return the user_id of the updated user")
        self.assertEqual(
            "abcdefg", updated_user.avatar_file_uuid, "Should return the updated avatar file uuid"
        )
        self.assertEqual(
            "testUser123", updated_user.username, "Should return the user's original username"
        )

    def test_user_update_when_user_does_not_exist(self):
        self._seed_user()

        users_mid = UsersMidlayerMixin(self.config)

        request = UserUpdateRequest(user_id=2, avatar_file_uuid="abcdefg")

        with self.assertRaisesRegex(
            expected_exception=Exception,
            expected_regex="Failed to update user with id 2 because user could not be found.",
            msg="Should throw exception if user is not found",
        ):
            users_mid.user_update(request)

    def test_user_update_with_no_property_values_provided(self):
        self._seed_user()

        users_mid = UsersMidlayerMixin(self.config)

        request = UserUpdateRequest(user_id=1, avatar_file_uuid=None)

        with self.assertRaisesRegex(
            expected_exception=Exception,
            expected_regex="Failed to update user with id 1.",
        ):
            users_mid.user_update(request)
