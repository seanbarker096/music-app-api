import json
import logging
import secrets
import time
from abc import ABC
from typing import Dict, Optional

import flask
import jwt

from api.authentication_service.dao.api import AuthTokenServiceDAO
from api.authentication_service.typings import (
    AuthenticateRequest,
    AuthState,
    AuthStateCreateRequest,
    AuthStateCreateResult,
    AuthStateDeleteRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenCreateRequest,
    TokenType,
)
from api.utils.rest_utils import (
    process_int_request_param,
    process_string_request_param,
    remove_bearer_from_token,
)
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import InvalidTokenException


class TokenAuthService(ABC):
    def create_auth_state(self, user_id: int):
        ...

        # def authenticate():
        #     """Does not process any previous auth state. Just creates a new one e.g. when logging in"""
        #     ...

        # # def process_header():
        # #     ...

        # # def process_cookie():
        # #     ...

        # # def validate():
        # #     ...

        # # def invalidate():
        # #     """Removes or invalidates the auth state"""
        # #     ...

        # # def refresh():
        # #     ...

        # # """these probably should be in auth state handler"""

        # # def update_auth_state():
        # #     ...

        # # def delete_auth_state():
        ...


## TODO: Create getters and setters for these TTL, leways etc.
class JWTTokenAuthService(TokenAuthService):
    _ACCESS_TOKEN_TTL = 60 * 60 * 1  # Valid for 1 hours
    _REFRESH_TOKEN_TTL = 60 * 60 * 14  # Valid for 14 days
    _LEWAY = 10
    SIGNING_ALGORITHM = "HS256"

    def __init__(self, config, auth_dao=None):
        # self.auth_state_handler = AuthStateHandler()
        # self.admin_auth_state_handler = AdminAuthStateHandler()
        self.auth_dao = auth_dao if auth_dao else AuthTokenServiceDAO(config)
        self.signing_secret = config["config_file"]["auth"].get("signing-secret")

    def create_auth_state(self, request: AuthStateCreateRequest) -> AuthStateCreateResult:
        try:
            refresh_token = self.create_token(request.auth_user, token_type=TokenType.REFRESH.value)
            access_token = self.create_token(
                request.auth_user, TokenType.ACCESS.value, refresh_token=refresh_token
            )

            auth_state = AuthState(
                auth_user=request.auth_user,
                access_token=access_token,
                refresh_token=refresh_token,
                status=AuthStatus.AUTHENTICATED.value,
            )

            return AuthStateCreateResult(auth_state=auth_state)

        except Exception:
            raise Exception(
                f"Failed to create auth state for user with id {request.auth_user.user_id}"
            )

    def create_admin_auth_state(self, user_id: int) -> AuthState:
        ...

    def create_token(
        self, auth_user: AuthUser, token_type=TokenType, refresh_token: Optional[str] = None
    ) -> str:
        user_id = auth_user.user_id

        if token_type == TokenType.ACCESS.value and not refresh_token:
            raise Exception("Must provide a refresh token to create an access token")

        session_id = secrets.token_urlsafe(16)

        payload = {
            "user_id": user_id,
            "type": token_type,
            "role": auth_user.role,
            "session_id": session_id,
        }

        if token_type == TokenType.ACCESS.value:
            ## Validate refresh token
            self.validate_token(refresh_token)
            ## TODO: Check the token payload matches that of the auth_user in request
            return self._generate_token(payload, TokenType.ACCESS.value, auth_user.role)

        if token_type == TokenType.REFRESH.value:
            try:
                # Delete any existing refresh tokens for this user
                # TODO: Fine tune api to only delete tokens for this user + device combo, to ensure we don't log them
                # out of other devices
                self.delete_auth_state(request=AuthStateDeleteRequest(owner_id=user_id))
            except:
                pass

            token = self._generate_token(payload, TokenType.REFRESH.value, auth_user.role)
            self._persist_token(token, owner_id=user_id, session_id=session_id)

            return token

        raise Exception(f"Cannot create token of invalid type {TokenType(token_type).name}")

    def validate_token(self, token: str, token_type: Optional[TokenType] = None) -> Dict[str, any]:
        """Validate token allowing for 10 second leway."""
        try:
            decoded_token = jwt.decode(
                token, self.signing_secret, leeway=self._LEWAY, algorithms=self.SIGNING_ALGORITHM
            )
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException(f"Failed to validate token {token} because it has expired")

        ## We also need to check the REFRESH token is saved in the db for refresh tokens
        if token_type == TokenType.REFRESH.value:
            try:
                self.auth_dao.get_token_by_user_id_and_session_id(
                    user_id=decoded_token["user_id"], session_id=decoded_token["session_id"]
                )
            except:
                raise InvalidTokenException(
                    f"Failed to validate token {token} of type {TokenType.REFRESH.value} as it could not be found. It may have been deleted and is therefore no longer valid"
                )
        return decoded_token

    def _generate_token(
        self, payload: Dict[str, int | str], token_type: TokenType, role: AuthUserRole
    ) -> str:
        token_ttl = (
            self._ACCESS_TOKEN_TTL
            if token_type is TokenType.ACCESS.value
            else self._REFRESH_TOKEN_TTL
        )

        ## Todo: make a type for this
        payload["exp"] = time.time() + token_ttl

        new_token = jwt.encode(payload, self.signing_secret, algorithm=self.SIGNING_ALGORITHM)

        return new_token

    def _persist_token(self, token: str, owner_id: int, session_id: str) -> int:
        create_request = TokenCreateRequest(token=token, owner_id=owner_id, session_id=session_id)
        row_id = self.auth_dao.token_create(request=create_request)
        if row_id is None:
            raise Exception(f"Failed to persist token for user with id {owner_id}")

        return row_id

    def get_auth_state(self):
        """Given various tokens etc. works out if user is authenticated"""
        ## Shouldn't deal with refresh tokens
        ...

    def update_auth_state(self):
        ...

    def delete_auth_state(self, request: AuthStateDeleteRequest) -> None:
        process_string_request_param("refresh_token", request.refresh_token, optional=True)
        process_string_request_param("session_id", request.session_id, optional=True)
        process_int_request_param("owner_id", request.owner_id, optional=True)

        if not request.refresh_token and not request.session_id and not request.owner_id:
            raise InvalidArgumentException(
                f"Must provide at least one of refresh_token, session_id or owner_id when deleting auth state. Request: {json.dumps(vars(request))}",
                "request",
            )

        self.auth_dao.token_delete(request)
