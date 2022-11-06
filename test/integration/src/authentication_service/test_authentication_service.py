from test.integration import IntegrationTestCase
from unittest.mock import patch

import jwt

from api.authentication_service.api import JWTTokenAuthService
from api.authentication_service.typings import (
    AuthenticateRequest,
    AuthStateCreateRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenType,
)


class TokenAuthenticationServiceIntegrationTestCase(IntegrationTestCase):
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

        authentication_service = JWTTokenAuthService(config=self.config)

        result = authentication_service.create_auth_state(request)

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
            time.return_value + authentication_service._ACCESS_TOKEN_TTL,
            "Should return the correct access token expiration time",
        )

        self.assertEqual(
            access_token_payload["type"],
            TokenType.ACCESS.value,
            "Should return the correct token type for the access token",
        )

        self.assertEqual(
            refresh_token_payload["exp"],
            time.return_value + authentication_service._REFRESH_TOKEN_TTL,
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

        ## check that refresh token added to db correctly
        db_refresh_token = authentication_service.auth_dao.get_token_by_user_id(user_id)

        self.assertEqual(
            result.refresh_token,
            db_refresh_token,
            "Should store encoded refresh token in the database",
        )

    def get_auth_state_with_invalid_access_token(self):
        ...

    def test_authenticate_with_valid_token(self):
        # time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService(config=self.config)

        result = authentication_service.create_auth_state(request)

        access_token = result.access_token

        authenticate_request = AuthenticateRequest(token=access_token)

        result = authentication_service.authenticate(request=authenticate_request)

        self.assertEqual(
            result.status,
            AuthStatus.AUTHENTICATED.value,
            "Should authenticate user if token is valid",
        )

        self.assertEqual(
            result.access_token,
            access_token,
            "Should return the access token used to authenticate the user",
        )

        self.assertEqual(
            result.auth_user.user_id, user_id, "Should store the correct user id in the auth state"
        )

        self.assertEqual(
            result.auth_user.role,
            AuthUserRole.USER.value,
            "Should store the correct users role in the auth state",
        )

        self.assertListEqual(
            result.auth_user.permissions, [], "Should return empty permissions array for auth user"
        )

        self.assertIsNone(
            result.refresh_token,
            "Should not return refresh token if one wasn/'t provided in request",
        )

    def test_authenticate_with_refresh_token(self):
        ...

    @patch("time.time")
    def test_validate_with_expired_token(self, time):
        user_id = 12345
        time.return_value = self.current_time

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService(config=self.config)

        # Use this to simulate a recently expired token
        authentication_service._ACCESS_TOKEN_TTL = -100

        result = authentication_service.create_auth_state(request)

        access_token = result.access_token

        authenticate_request = AuthenticateRequest(token=access_token)

        result = authentication_service.authenticate(request=authenticate_request)

        self.assertEqual(
            result.status,
            AuthStatus.UNAUTHENTICATED.value,
            "Should not authenticate user if token is expired",
        )

        self.assertIsNone(
            result.auth_user, "Should not return an auth user if the user is unauthenticated"
        )

        self.assertEqual(
            result.access_token,
            access_token,
            "Should return the access token used to authenticate the user",
        )

        self.assertIsNone(
            result.refresh_token,
            "Should not return refresh token if one wasn/'t provided in request",
        )

    @patch("time.time")
    def test_authenticate_with_recently_expired_token(self, time):
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService(config=self.config)

        ## TODO: Use getters and setters to configure these fields
        # This simulates the token being expired, but its expiry time falling within the leway window
        authentication_service._ACCESS_TOKEN_TTL = -authentication_service._LEWAY * 0.5

        result = authentication_service.create_auth_state(request)

        access_token = result.access_token

        authenticate_request = AuthenticateRequest(token=access_token)

        result = authentication_service.authenticate(request=authenticate_request)

        self.assertEqual(
            result.status,
            AuthStatus.AUTHENTICATED.value,
            "Should authenticate user if token is expired but inside the leway window",
        )

        self.assertEqual(
            result.access_token,
            access_token,
            "Should return the access token used to authenticate the user",
        )

        self.assertEqual(
            result.auth_user.user_id, user_id, "Should store the correct user id in the auth state"
        )

        self.assertEqual(
            result.auth_user.role,
            AuthUserRole.USER.value,
            "Should store the correct users role in the auth state",
        )

        self.assertListEqual(
            result.auth_user.permissions, [], "Should return empty permissions array for auth user"
        )

        self.assertIsNone(
            result.refresh_token,
            "Should not return refresh token if one wasn/'t provided in request",
        )

    @patch("time.time")
    def test_authenticate_with_almost_expired_token(self, time):
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService(config=self.config)

        ## TODO: Use getters and setters to configure these fields
        # This simulates the token being expired, but only just falling outside the leway window
        authentication_service._ACCESS_TOKEN_TTL = -authentication_service._LEWAY * 1.1

        result = authentication_service.create_auth_state(request)

        access_token = result.access_token

        authenticate_request = AuthenticateRequest(token=access_token)

        result = authentication_service.authenticate(request=authenticate_request)

        self.assertEqual(
            result.status,
            AuthStatus.UNAUTHENTICATED.value,
            "Should authenticate user if token is expired but inside the leway window",
        )

        self.assertIsNone(
            result.auth_user, "Should not return an auth user if the user is unauthenticated"
        )

        self.assertEqual(
            result.access_token,
            access_token,
            "Should return the access token used to authenticate the user",
        )

        self.assertIsNone(
            result.refresh_token,
            "Should not return refresh token if one wasn/'t provided in request",
        )

    @patch("time.time")
    def test_create_access_token(self, time):
        """using refresh token to create new access token"""
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        create_auth_state_request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService(config=self.config)

        ## First generate a refresh token
        refresh_token = authentication_service.create_auth_state(
            request=create_auth_state_request
        ).refresh_token

        new_acess_token = authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=refresh_token
        )

        ## Check new token is valid
        authenticate_result = authentication_service.authenticate(
            request=AuthenticateRequest(token=new_acess_token)
        )

        self.assertEqual(
            authenticate_result.status,
            AuthStatus.AUTHENTICATED.value,
            "Should return a valid access token which can be used to authenticate the user",
        )

    def test_create_access_token_without_refresh_token(self):
        user_id = 12345
        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        authentication_service = JWTTokenAuthService(config=self.config)

        with self.assertRaises(
            Exception, msg="Must provide a refresh token to create an access token"
        ):
            authentication_service.create_token(
                auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=None
            )

    @patch("time.time")
    def test_create_refresh_token(self, time):
        """using refresh token to create new access token"""
        ## Tests that there is a bit of leway
        time.return_value = self.current_time

        user_id = 12345

        auth_user = AuthUser(user_id=user_id, role=AuthUserRole.USER.value, permissions=None)

        authentication_service = JWTTokenAuthService(config=self.config)

        new_refresh_token = authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.REFRESH.value, refresh_token=None
        )

        ## Should be able to use the refresh token to create a new access token and authenticate with it
        new_acess_token = authentication_service.create_token(
            auth_user=auth_user, token_type=TokenType.ACCESS.value, refresh_token=new_refresh_token
        )

        ## Check new token is valid
        authenticate_result = authentication_service.authenticate(
            request=AuthenticateRequest(token=new_acess_token)
        )

        self.assertEqual(
            authenticate_result.status,
            AuthStatus.AUTHENTICATED.value,
            "Should return a refresh token which can be used to return a valid access token, which can be used to authenticate the user",
        )

        ## Inspect token itself
        secret = self.config["config_file"]["auth"].get("signing-secret")
        payload = jwt.decode(
            jwt=new_refresh_token, key=secret, algorithms=authentication_service.SIGNING_ALGORITHM
        )

        self.assertEqual(
            payload["user_id"],
            user_id,
            "Should return the correct user id in the refresh token payload",
        )

        self.assertEqual(
            payload["exp"],
            time() + authentication_service._REFRESH_TOKEN_TTL,
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

    def test_invalidate_token(self):
        ...

    def test_invalidate_and_create(self):
        """i.e. when resetting password"""
        ...
