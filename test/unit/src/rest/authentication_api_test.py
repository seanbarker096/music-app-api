from test.test_utils import mock_decorator
from unittest.mock import MagicMock, Mock, patch

import jwt
from rest import AuthAPITestCase

from api.authentication_service.api import JWTTokenAuthService
from api.authentication_service.typings import (
    AuthState,
    AuthStateCreateResult,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenType,
)
from api.midlayer.api import Midlayer
from api.midlayer.users_mid import User
from api.utils.rest_utils import auth
from exceptions.response.exceptions import UserAlreadyExistsException


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

    def test_login_with_duplicate_user_agent(self):
        """Tests that you can only have 1 refresh token per user and user agent combo"""
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
        json = {
            "username": "Saka7",
            "password": "testPassword1",
            "first_name": "Bukayo",
            "second_name": "Saka",
            "email": "saka7@gmail.com",
        }

        expected_exception = UserAlreadyExistsException(
            "Cannot create user with username Saka7 because user already exists"
        )

        self.app.conns.midlayer = Mock()
        self.app.conns.midlayer.user_create = Mock(side_effect=expected_exception)

        response = self.test_client.post("/signup/", json=json)

        response_body = response.json

        self.assertEqual(400, response.status_code, "Should return 400 status code")
        self.assertEqual(
            expected_exception.get_code(),
            response_body["error_code"],
            "Should return the correct error code",
        )
        self.assertEqual(
            "Cannot create user with username Saka7 because user already exists",
            response_body["message"],
            "Should return the correct error message",
        )

    def test_signup_with_deleted_user(self):
        ...
        ## Probably just delete the user which has is_deleted=True and create another

    def test_signup_with_authed_user(self):
        ## Test signup with a user who was deleted but has auth token stored
        ...

    def test_signout(self):
        """Test that signing out invalidates all tokens for that users session"""
        ...

    def test_signout_with_token_that_does_not_exist(self):
        """Tests that error is thrown if we try to invalidate a token that does not exist"""
        ...

    @patch("api.utils.rest_utils.auth", auth)
    def test_auth_check_with_valid_auth_token(self):

        auth_token_payload = {
            "user_id": 1234,
            "type": TokenType.ACCESS.value,
            "role": AuthUserRole.USER.value,
            "session_id": "safdksdfasdf",
        }

        ## Ensure validate token does not throw to immitate a valid auth token
        self.app.conns.auth_service.validate_token = Mock(return_value=auth_token_payload)

        response = self.test_client.get("/validate/", headers={"Authorization": "an_auth_jwt"})

        self.assertEqual(
            response.headers.get("Authorization"),
            None,
            "Should not set auth header if request authenticated successfully",
        )

        self.assertEqual(response.status_code, 200, "Should authorize request for valid auth token")

    @patch("api.utils.rest_utils.auth", auth)
    def test_authorize_request_with_invalid_auth_token_but_valid_refresh_token(self):
        refresh_token_payload = {
            "user_id": 1234,
            "type": TokenType.REFRESH.value,
            "role": AuthUserRole.USER.value,
            "session_id": "safdksdfasdf",
        }

        ## Get validation to throw
        self.app.conns.auth_service.validate_token = Mock()
        self.app.conns.auth_service.validate_token.side_effect = [
            Exception(),
            refresh_token_payload,
        ]

        self.app.conns.auth_service.create_token = Mock(return_value="new_auth_jwt")

        response = self.test_client.get(
            "/validate/",
            headers={"Authorization": "invalid_auth_jwt", "Refresh-Token": "refresh_jwt"},
        )

        self.assertEqual(
            response.status_code,
            200,
            "Should authorize request for invalid auth token but valid refresh token",
        )

        self.assertEqual(
            response.headers.get("Authorization"),
            "Bearer new_auth_jwt",
            "Should update Authorization header with new auth token if refresh token was valid",
        )

    @patch("api.utils.rest_utils.auth", auth)
    def test_authorize_request_with_invalid_auth_and_refresh_tokens(self):
        ## Get validation to throw
        self.app.conns.auth_service.validate_token = Mock()
        self.app.conns.auth_service.validate_token.side_effect = [
            Exception(),
            Exception(),
        ]

        self.app.conns.auth_service.create_token = Mock(return_value="new_auth_jwt")

        with self.assertRaises(Exception) as e:
            response = self.test_client.get(
                "/validate/",
                headers={
                    "Authorization": "invalid_auth_jwt",
                    "Refresh Token": "invalid_refresh_jwt",
                },
            )

            self.assertEqual(
                e.exception.get_message(),
                "Authorization of the request failed. Please try logging out and in again to revalidate your session",
            )
