from test.integration import IntegrationTestCase
from unittest.mock import patch

import jwt

from api.authentication_service.api import JWTTokenAuthService
from api.authentication_service.typings import (
    AuthStateCreateRequest,
    AuthStates,
    AuthUser,
    AuthUserRole,
    TokenType,
)


class TokenAuthenticationServiceIntegrationTestCase(IntegrationTestCase):
    @patch("time.time")
    def test_create_auth_state(self, time):
        time.return_value = 12345
        secret = self.config["config_file"]["auth"].get("signing-secret")

        expected_access_token_payload = {"user_id": 123456, "type": TokenType.ACCESS.value}
        expected_refresh_token_payload = {"user_id": 123456, "type": TokenType.REFRESH.value}

        auth_user = AuthUser(id=123456, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService()

        result = authentication_service.create_auth_state(request)

        access_token = result.access_token

        access_token_payload = jwt.decode(access_token, secret, algorithms=["HS256"])

        refresh_token_payload = jwt.decode(result.refresh_token, secret, algorithms=["HS256"])

        self.assertEqual(
            result.state, AuthStates.AUTHENTICATED, "Should return an authenticated state"
        )

        self.assertEqual(result.auth_user, auth_user, "Should return the auth user")

        self.assertEqual(
            access_token_payload["user_id"],
            expected_access_token_payload["user_id"],
            "Should return access token with payload containing user id",
        )

        self.assertEqual(
            access_token_payload["exp"],
            time.time + authentication_service.ACCESS_TOKEN_TTL,
            "Should return the correct access token expiration time",
        )

        self.assertEqual(
            access_token_payload["type"],
            TokenType.ACCESS.value,
            "Should return the correct token type",
        )

        self.assertEquals(
            refresh_token_payload["exp"],
            time.time + authentication_service.REFRESH_TOKEN_TTL,
            "Should return the correct refresh token expiration type",
        )

        self.assertEqual(
            refresh_token_payload["user_id"],
            expected_refresh_token_payload["user_id"],
            "Should return refresh token with payload containing user id",
        )

        self.assertEqual(
            access_token_payload["type"],
            TokenType.REFRESH.value,
            "Should return the correct token type",
        )

        ## check that refresh token added to db correctly
        db_refresh_token = authentication_service.dao.get_refresh_token()

        self.assertEqual(
            result.refresh_token,
            db_refresh_token,
            "Should store encoded refresh token in the database",
        )

    def get_auth_state_with_invalid_access_token(self):
        ...

    def test_validate_with_valid_token(self):
        ...

    def test_validate_with_expired_token(self):
        ...

    def test_validate_token_with_duplicate(self):
        ...

    def test_invalidate_token(self):
        ...

    def test_invalidate_and_create(self):
        """i.e. when resetting password"""
        ...

    def test_refresh_auth_state(self):
        """using refresh token to create new access token"""
