from test.integration import IntegrationTestCase
from unittest.mock import patch

import jwt

from api.authentication_service.api import AuthTokenServiceDAO, JWTTokenAuthService
from api.authentication_service.typings import (
    AuthenticateRequest,
    AuthStateCreateRequest,
    AuthStateDeleteRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenType,
)
from api.db.db import TestingDBConnectionManager


class TokenAuthenticationServiceIntegrationTestCase(IntegrationTestCase):

    def setUp(self):
        super().setUp()

        dao = AuthTokenServiceDAO(config=self.config, db=TestingDBConnectionManager)
        self.authentication_service = JWTTokenAuthService(config=self.config, auth_dao=dao)

    @patch("time.time")
    def test_create_auth_state(self, time):
        ## This just ensures the time remains fixed so we can assert on it
        time.return_value = self.current_time

        user_id = 12345
        secret = self.config["config_file"]["auth"].get("signing-secret")

        expected_access_token_payload = {"user_id": user_id, "type": TokenType.ACCESS.value}
        expected_refresh_token_payload = {"user_id": user_id, "type": TokenType.REFRESH.value}

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        result = self.authentication_service.create_auth_state(request).auth_state

        access_token = result.access_token

        access_token_payload = jwt.decode(access_token, secret, algorithms=["HS256"])

        refresh_token_payload = jwt.decode(result.refresh_token, secret, algorithms=["HS256"])

        self.assertEqual(
            result.status, AuthStatus.AUTHENTICATED.value, "Should return an authenticated state"
        )

        self.assertEqual(result.auth_user, auth_user, "Should return the auth user")

        self.assertEqual(
            access_token_payload["user_id"],
            expected_access_token_payload["user_id"],
            "Should return access token with payload containing user id",
        )

        self.assertEqual(
            access_token_payload["exp"],
            time.return_value + self.authentication_service._ACCESS_TOKEN_TTL,
            "Should return the correct access token expiration time",
        )

        self.assertEqual(
            access_token_payload["type"],
            TokenType.ACCESS.value,
            "Should return the correct token type for the access token",
        )

        self.assertIsInstance(access_token_payload["session_id"], str)

        self.assertEqual(
            refresh_token_payload["exp"],
            time.return_value + self.authentication_service._REFRESH_TOKEN_TTL,
            "Should return the correct refresh token expiration type",
        )

        self.assertEqual(
            refresh_token_payload["user_id"],
            expected_refresh_token_payload["user_id"],
            "Should return refresh token with payload containing user id",
        )

        self.assertEqual(
            refresh_token_payload["type"],
            TokenType.REFRESH.value,
            "Should return the correct token type for the refresh token",
        )

        self.assertIsInstance(refresh_token_payload["session_id"], str)

        ## check that refresh token added to db correctly
        db_refresh_token = self.authentication_service.auth_dao.get_token_by_user_id_and_session_id(
            user_id, refresh_token_payload["session_id"]
        )

        self.assertEqual(
            result.refresh_token,
            db_refresh_token,
            "Should store encoded refresh token in the database",
        )

    def get_auth_state_with_invalid_access_token(self):
        ...

    # def test_authenticate_with_valid_token(self):
    #     # time.return_value = self.current_time

    #     user_id = 12345

    #     auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

    #     request = AuthStateCreateRequest(auth_user=auth_user)

    #     self.authentication_service = JWTTokenAuthService(config=self.config)

    #     result = self.authentication_service.create_auth_state(request).auth_state

    #     access_token = result.access_token

    #     authenticate_request = AuthenticateRequest(token=access_token)

    #     result = self.authentication_service.authenticate(request=authenticate_request)

    #     self.assertEqual(
    #         result.status,
    #         AuthStatus.AUTHENTICATED.value,
    #         "Should authenticate user if token is valid",
    #     )

    #     self.assertEqual(
    #         result.access_token,
    #         access_token,
    #         "Should return the access token used to authenticate the user",
    #     )

    #     self.assertEqual(
    #         result.auth_user.user_id, user_id, "Should store the correct user id in the auth state"
    #     )

    #     self.assertEqual(
    #         result.auth_user.role,
    #         AuthUserRole.USER.value,
    #         "Should store the correct users role in the auth state",
    #     )

    #     self.assertListEqual(
    #         result.auth_user.permissions, [], "Should return empty permissions array for auth user"
    #     )

    #     self.assertIsNone(
    #         result.refresh_token,
    #         "Should not return refresh token if one wasn/'t provided in request",
    #     )

    def test_authenticate_with_refresh_token(self):
        ...

    @patch("time.time")
    def test_validate_with_expired_token(self, time):
        user_id = 12345
        time.return_value = self.current_time

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        # Use this to simulate a recently expired token
        self.authentication_service._ACCESS_TOKEN_TTL = -100

        result = self.authentication_service.create_auth_state(request).auth_state

        access_token = result.access_token

        with self.assertRaisesRegex(
            Exception,
            expected_regex=f"Failed to validate token {access_token} because it has expired",
            msg="Should throw error with correct exception message",
        ):
            self.authentication_service.validate_token(token=access_token)

    def test_validate_with_valid_token(self):
        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        result = self.authentication_service.create_auth_state(request).auth_state

        access_token = result.access_token

        result = self.authentication_service.validate_token(token=access_token)

        self.assertEqual(
            result["user_id"], 12345, "Should return the user_id in the decoded token payload"
        )

        self.assertIsInstance(
            result["session_id"],
            str,
        )

        self.assertTrue(
            len(result["session_id"]) > 0,
        )

    # @patch("time.time")
    # def test_authenticate_with_recently_expired_token(self, time):
    #     ## Tests that there is a bit of leway
    #     time.return_value = self.current_time

    #     user_id = 12345

    #     auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

    #     request = AuthStateCreateRequest(auth_user=auth_user)

    #     self.authentication_service = JWTTokenAuthService(config=self.config)

    #     ## TODO: Use getters and setters to configure these fields
    #     # This simulates the token being expired, but its expiry time falling within the leway window
    #     self.authentication_service._ACCESS_TOKEN_TTL = -self.authentication_service._LEWAY * 0.5

    #     result = self.authentication_service.create_auth_state(request).auth_state

    #     access_token = result.access_token

    #     authenticate_request = AuthenticateRequest(token=access_token)

    #     result = self.authentication_service.authenticate(request=authenticate_request)

    #     self.assertEqual(
    #         result.status,
    #         AuthStatus.AUTHENTICATED.value,
    #         "Should authenticate user if token is expired but inside the leway window",
    #     )

    #     self.assertEqual(
    #         result.access_token,
    #         access_token,
    #         "Should return the access token used to authenticate the user",
    #     )

    #     self.assertEqual(
    #         result.auth_user.user_id, user_id, "Should store the correct user id in the auth state"
    #     )

    #     self.assertEqual(
    #         result.auth_user.role,
    #         AuthUserRole.USER.value,
    #         "Should store the correct users role in the auth state",
    #     )

    #     self.assertListEqual(
    #         result.auth_user.permissions, [], "Should return empty permissions array for auth user"
    #     )

    #     self.assertIsNone(
    #         result.refresh_token,
    #         "Should not return refresh token if one wasn/'t provided in request",
    #     )

    # @patch("time.time")
    # def test_authenticate_with_almost_expired_token(self, time):
    #     ## Tests that there is a bit of leway
    #     time.return_value = self.current_time

    #     user_id = 12345

    #     auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

    #     request = AuthStateCreateRequest(auth_user=auth_user)

    #     self.authentication_service = JWTTokenAuthService(config=self.config)

    #     ## TODO: Use getters and setters to configure these fields
    #     # This simulates the token being expired, but only just falling outside the leway window
    #     self.authentication_service._ACCESS_TOKEN_TTL = -self.authentication_service._LEWAY * 1.1

    #     result = self.authentication_service.create_auth_state(request).auth_state

    #     access_token = result.access_token

    #     authenticate_request = AuthenticateRequest(token=access_token)

    #     result = self.authentication_service.authenticate(request=authenticate_request)

    #     self.assertEqual(
    #         result.status,
    #         AuthStatus.UNAUTHENTICATED.value,
    #         "Should authenticate user if token is expired but inside the leway window",
    #     )

    #     self.assertIsNone(
    #         result.auth_user, "Should not return an auth user if the user is unauthenticated"
    #     )

    #     self.assertEqual(
    #         result.access_token,
    #         access_token,
    #         "Should return the access token used to authenticate the user",
    #     )

    #     self.assertIsNone(
    #         result.refresh_token,
    #         "Should not return refresh token if one wasn/'t provided in request",
    #     )

    @patch("time.time")
    def test_create_access_token(self, time):
        """using refresh token to create new access token"""
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        create_auth_state_request = AuthStateCreateRequest(auth_user=auth_user)

        ## First generate a refresh token
        refresh_token = self.authentication_service.create_auth_state(
            request=create_auth_state_request
        ).auth_state.refresh_token

        new_acess_token = self.authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=refresh_token
        )

        ## Check new token is valid
        token_payload = self.authentication_service.validate_token(token=new_acess_token)

        self.assertEqual(
            token_payload["user_id"],
            12345,
            "Should return the decoded token payload with the correct fields",
        )

    def test_create_access_token_without_refresh_token(self):
        user_id = 12345
        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        with self.assertRaisesRegex(
            Exception,
            expected_regex="Must provide a refresh token to create an access token",
            msg="Should throw error with correct exception message",
        ):
            self.authentication_service.create_token(
                auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=None
            )

    @patch("time.time")
    def test_create_refresh_token(self, time):
        """using refresh token to create new access token"""
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        new_refresh_token = self.authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.REFRESH.value, refresh_token=None
        )

        ## Should be able to use the refresh token to create a new access token and authenticate with it
        new_acess_token = self.authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=new_refresh_token
        )

        ## Check new token is valid
        token_payload = self.authentication_service.validate_token(token=new_acess_token)

        self.assertEqual(
            token_payload["user_id"],
            12345,
            "Should return the decoded token payload with the correct fields",
        )

        ## Inspect refresh token
        payload = self.authentication_service.validate_token(
            token=new_refresh_token, token_type=TokenType.REFRESH.value
        )

        self.assertEqual(
            payload["user_id"],
            user_id,
            "Should return the correct user id in the refresh token payload",
        )

        self.assertEqual(
            payload["exp"],
            time() + self.authentication_service._REFRESH_TOKEN_TTL,
            "Should return the correct expiry time in the refresh token payload",
        )

        self.assertEqual(
            payload["type"], TokenType.REFRESH.value, "Should return a token of the correct type"
        )

        self.assertEqual(
            payload["role"],
            AuthUserRole.USER.value,
            "Should return a token with the correct user role",
        )

    def test_validate_token_with_duplicate(self):
        ...

    def test_invalidate_and_create(self):
        """i.e. when resetting password"""
        ...

    def test_delete_auth_state(self):
        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        create_auth_state_request = AuthStateCreateRequest(auth_user=auth_user)

        ## First generate a refresh token
        refresh_token = self.authentication_service.create_auth_state(
            request=create_auth_state_request
        ).auth_state.refresh_token

        self.authentication_service.delete_auth_state(
            request=AuthStateDeleteRequest(refresh_token=refresh_token)
        )

        ## Validation of invalidated token should fail
        with self.assertRaisesRegex(
            Exception,
            expected_regex=f"Failed to validate token {refresh_token} of type {TokenType.REFRESH.value} as it could not be found. It may have been deleted and is therefore no longer valid",
            msg="Should throw error with correct exception message",
        ):
            self.authentication_service.validate_token(
                token=refresh_token, token_type=TokenType.REFRESH.value
            )
