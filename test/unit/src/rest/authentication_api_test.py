from unittest.mock import Mock

import jwt
from rest import AuthAPITestCase

from api.authentication_service.api import JWTTokenAuthService
from api.authentication_service.typings import (
    AuthState,
    AuthStateCreateResult,
    AuthStatus,
    AuthUser,
    AuthUserRole,
)
from api.midlayer.api import Midlayer
from api.midlayer.users_mid import User


class AuthApiTest(AuthAPITestCase):
    def setUp(self):
        self.test_user = User(
            id=4444,
            first_name="Bukayo",
            second_name="Saka",
            username="Saka7",
            create_time=5555,
            is_deleted=False,
            email="saka7@gmail.com",
            last_login_date=None,
            language_id=None,
            timezone_id=None,
        )
        super().setUp()

    def test_login_with_username_and_password(self):

        user_id = 12345

        json = {"username": "testUser12345", "password": "testPassword1"}

        self.app.conns.auth_service = Mock()

        auth_user = AuthUser(user_id=12345, role=AuthUserRole.USER.value)
        expected_auth_state = AuthState(
            auth_user=auth_user,
            access_token="a-mock-access-token",
            refresh_token="a-mock-refresh-token",
            status=AuthStatus.AUTHENTICATED.value,
        )

        create_auth_state_result = AuthStateCreateResult(auth_state=expected_auth_state)
        self.app.conns.auth_service.create_auth_state = Mock(return_value=create_auth_state_result)

        self.app.conns.midlayer = Mock()

        self.app.conns.midlayer.get_user_by_username_and_password = Mock(
            return_value=self.test_user
        )

        response = self.test_client.post("/login/", json=json)

        response_body = response.json

        [bearer_str, token] = response.headers["Authorization"].split(" ")

        self.assertEqual(response.status_code, 200, "Should return 200 status code")

        self.assertEqual(bearer_str, "Bearer", "Should correctly format the Authorization header")

        self.assertIsInstance(token, str, "Should return an access token")

        self.assertEqual(
            token, response_body["token"], "Should also return the access token in the response"
        )

        self.assertIsInstance(
            response_body["r_token"],
            str,
            "Should return a refresh token in the response",
        )

        self.assertEqual(response_body["user_id"], user_id, "Should return the correct user id")

    def test_login_with_non_registered_user(self):
        ...

    def test_login_with_email_and_password(self):
        ...

    def test_signup(self):
        expected_user = self.test_user

        json = {
            "username": "Saka7",
            "password": "testPassword1",
            "first_name": "Bukayo",
            "second_name": "Saka",
            "email": "saka7@gmail.com",
        }

        self.app.conns.auth_service = Mock()
        self.app.conns.midlayer = Mock()
        self.app.conns.midlayer.user_create(return_value=expected_user)
        self.app.conns.midlayer.get_user_by_username_and_password = Mock(return_value=expected_user)

        auth_user = AuthUser(user_id=expected_user.id, role=AuthUserRole.USER.value)

        expected_auth_state = AuthState(
            auth_user=auth_user,
            access_token="a-mock-access-token",
            refresh_token="a-mock-refresh-token",
            status=AuthStatus.AUTHENTICATED.value,
        )

        create_auth_state_result = AuthStateCreateResult(auth_state=expected_auth_state)
        self.app.conns.auth_service.create_auth_state = Mock(return_value=create_auth_state_result)

        response = self.test_client.post("/signup/", json=json)

        response_body = response.json

        [bearer_str, token] = response.headers["Authorization"].split(" ")

        self.assertEqual(response.status_code, 200, "Should return 200 status code")

        self.assertEqual(bearer_str, "Bearer", "Should correctly format the Authorization header")

        self.assertIsInstance(token, str, "Should return an access token")

        self.assertEqual(
            token, response_body["token"], "Should also return the access token in the response"
        )

        self.assertIsInstance(
            response_body["r_token"],
            str,
            "Should return a refresh token in the response",
        )

        self.assertEqual(
            response_body["user_id"], expected_user.id, "Should return the correct user id"
        )

    def test_signup_with_invalid_username(self):
        ...

    def test_signup_with_invalid_password(self):
        ...

    def test_signup_with_duplicate_username(self):
        ...

    def test_signup_with_deleted_user(self):
        ...
        ## Probably just delete the user which has is_deleted=True and create another

    def test_signup_with_authed_user(self):
        ## Test signup with a user who was deleted but has auth token stored
        ...
