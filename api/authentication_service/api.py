import logging
import secrets
import time
from abc import ABC
from typing import Dict, Optional

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
from exceptions.exceptions import InvalidArgumentException


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
            token = self._generate_token(payload, TokenType.REFRESH.value, auth_user.role)
            self._persist_token(token, owner_id=user_id)

            return token

        raise Exception(f"Cannot create token of invalid type {TokenType(token_type).name}")

    def validate_token(self, token: str, token_type: Optional[TokenType] = None) -> Dict[str, any]:
        """Validate token allowing for 10 second leway."""

        ## We also need to check the REFRESH token is saved in the db for this session
        if token_type == TokenType.REFRESH.value:
            self.auth_dao.get_token_by_user_and_session_id()

        ## Handle tokens in Authorization header format ("Bearer the_actual_token")
        strings = token.split("Bearer ")

        if len(strings) == 2 and strings[0] == "":
            token = strings[1]

        try:
            return jwt.decode(
                token, self.signing_secret, leeway=self._LEWAY, algorithms=self.SIGNING_ALGORITHM
            )
        except jwt.ExpiredSignatureError:
            raise Exception(f"Failed to validate token {token} because it has expired")

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

    def _persist_token(self, token: str, owner_id: int) -> int:
        create_request = TokenCreateRequest(token=token, owner_id=owner_id)
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
        if not request.refresh_token or len(request.refresh_token) == 0:
            raise InvalidArgumentException(
                message=f"Invalid argument {request.refresh_token}", source="refresh_token"
            )

        self.auth_dao.token_delete(request.refresh_token)

    # def authenticate(self, request: AuthenticateRequest) -> AuthState:
    #     """Does not process any previous auth state. Just creates a new one e.g. when logging in"""
    #     if not isinstance(request.token, str) or len(request.token) == 0:
    #         raise Exception(f"Invalid token {request.token} provided")

    #     payload = None
    #     try:
    #         payload = self.validate_token(request.token)
    #         auth_status = AuthStatus.AUTHENTICATED.value

    #         if payload["type"] == TokenType.REFRESH:
    #             raise Exception(
    #                 f"Invalid token receieved of type {payload['type']}. Authenticate should only be used with access tokens"
    #             )

    #         auth_user = AuthUser(user_id=payload["user_id"], role=payload["role"], permissions=[])

    #     except Exception:
    #         # Log cause of failed validation
    #         logging.exception("message")
    #         auth_status = AuthStatus.UNAUTHENTICATED.value
    #         auth_user = None

    #     auth_state = AuthState(
    #         auth_user=auth_user,
    #         access_token=request.token,
    #         refresh_token=None,
    #         status=auth_status,
    #     )

    #     return auth_state

    # def process_header():
    #     ...

    # def process_cookie():
    #     ...

    # def _validate():
    #     ...

    # def _invalidate():
    #     """Removes or invalidates the auth state"""
    #     ...

    # def refresh():
    #     ...

    # """these probably should be in auth state handler"""

    # def update_auth_state():
    #     ...

    # def delete_auth_state():
    #     ...

    # What we want the service to do:

    # Log user in
    # Log user out
    # Invalidate sessions
    # Validate sessions by:
    #   - checking they are logged in
    #   - checking information trying to proove the session is valid is valid itself e.g. token     hasn't epxired
    # Maintaing session validity/ lifetime
    # Creating, updating and deleting any information related to user authentication
    # Should not handle authorization beyond simple logged in authorization
    # Managing sessions more generally e.g. removing invalid tokens etc.
    # Probably shouldn't handle sign ups to be honest. Nor closing accounts. This should be a UserService if it were to be, as it manges the User resource.
    # This should ideally not be interacting with our data models e.g. posts, users etc.
    # Handle different types of auth e.g. admin auth vs normal user - it can handle auth roles but shouldn't handle too many permissions with that role. That would be authorization

    # This should be done regardless of implementation details and therefore should be agnostic of the implementation as far as possible

    # Maybe encapsulate authState into a class
