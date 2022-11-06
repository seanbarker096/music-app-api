import logging
import time
from abc import ABC
from typing import Dict

import jwt

from api.authentication_service.dao.api import AuthTokenServiceDAO
from api.authentication_service.typings import (
    AuthenticateRequest,
    AuthState,
    AuthStateCreateRequest,
    AuthStatus,
    AuthUser,
    AuthUserRole,
    TokenCreateRequest,
    TokenType,
)


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

    def create_auth_state(self, request: AuthStateCreateRequest) -> AuthState:
        user_id = request.auth_user.user_id
        role = request.auth_user.role
        # Check if we have a refresh token already for this user
        token_exists = False
        token = None
        try:
            token = self.auth_dao.get_token_by_user_id(user_id)
            if isinstance(token, str):
                token_exists = True
        except:
            ## get token by id will throw if no token found
            pass

        if token_exists:
            raise Exception(f"Token already exists for user with id {user_id}")

        if token is not None:
            raise Exception(
                f"Failed to create new auth state. A auth token already exists for user with id {user_id}"
            )

        access_token = self._generate_token(user_id, TokenType.ACCESS.value, role)
        refresh_token = self._generate_token(user_id, TokenType.REFRESH.value, role)

        try:
            create_request = TokenCreateRequest(token=refresh_token, owner_id=user_id)
            row_id = self.auth_dao.token_create(request=create_request)
            print(f"row id: {row_id}")
            if row_id is None:
                raise Exception("Failed to create token. Failed to store token in databse")
        except:
            ## This didn't seem to be
            raise Exception(f"Failed to save refresh token to database")

        return AuthState(
            auth_user=request.auth_user,
            access_token=access_token,
            refresh_token=refresh_token,
            status=AuthStatus.AUTHENTICATED.value,
        )

    def create_admin_auth_state(self, user_id: int) -> AuthState:
        ...

    def _generate_token(self, user_id: int, token_type: TokenType, role: AuthUserRole) -> str:
        token_ttl = (
            self._ACCESS_TOKEN_TTL
            if token_type is TokenType.ACCESS.value
            else self._REFRESH_TOKEN_TTL
        )

        payload = {
            "exp": int(time.time()) + token_ttl,
            "user_id": user_id,
            "type": token_type,
            "role": role,
        }
        new_token = jwt.encode(payload, self.signing_secret, algorithm=self.SIGNING_ALGORITHM)

        return new_token

    def get_auth_state(self):
        """Given various tokens etc. works out if user is authenticated"""
        ## Shouldn't deal with refresh tokens
        ...

    def update_auth_state(self):
        ...

    def delete_auth_state(self):
        "e.g. when logging out"
        ...

    def authenticate(self, request: AuthenticateRequest) -> AuthState:
        """Does not process any previous auth state. Just creates a new one e.g. when logging in"""
        if not isinstance(request.token, str) or len(request.token) == 0:
            raise Exception(f"Invalid token {request.token} provided")

        payload = None
        try:
            payload = self._validate_token(request.token)
            auth_status = AuthStatus.AUTHENTICATED.value

            if payload["type"] == TokenType.REFRESH:
                raise Exception(
                    f"Invalid token receieved of type {payload['type']}. Authenticate should only be used with access tokens"
                )

            auth_user = AuthUser(user_id=payload["user_id"], role=payload["role"], permissions=[])

        except Exception:
            # Log cause of failed validation
            logging.exception("message")
            auth_status = AuthStatus.UNAUTHENTICATED.value
            auth_user = None

        auth_state = AuthState(
            auth_user=auth_user,
            access_token=request.token,
            refresh_token=None,
            status=auth_status,
        )

        return auth_state

    def _validate_token(self, token: str) -> Dict[str, any]:
        """Validate token allowing for 10 second leway."""
        return jwt.decode(
            token, self.signing_secret, leeway=self._LEWAY, algorithms=self.SIGNING_ALGORITHM
        )

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
