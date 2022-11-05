import time
from abc import ABC

import jwt

from api.authentication_service.dao.api import AuthTokenServiceDAO
from api.authentication_service.typings import (
    AuthState,
    AuthStateCreateRequest,
    AuthStates,
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


class JWTTokenAuthService(TokenAuthService):
    ACCESS_TOKEN_TTL = 60 * 60 * 1  # Valid for 1 hours
    REFRESH_TOKEN_TTL = 60 * 60 * 14  # Valid for 14 days

    def __init__(self, config, auth_dao=None):
        # self.auth_state_handler = AuthStateHandler()
        # self.admin_auth_state_handler = AdminAuthStateHandler()
        self.auth_dao = auth_dao if auth_dao else AuthTokenServiceDAO(config)
        self.signing_secret = config["config_file"]["auth"].get("signing-secret")

    def create_auth_state(self, request: AuthStateCreateRequest) -> AuthState:
        user_id = request.auth_user.user_id
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

        access_token = self.generate_token(user_id, TokenType.ACCESS.value)
        refresh_token = self.generate_token(user_id, TokenType.REFRESH.value)

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
            state=AuthStates.AUTHENTICATED,
        )

    def create_admin_auth_state(self, user_id: int) -> AuthState:
        ...

    def generate_token(self, user_id: int, token_type: TokenType) -> str:
        token_ttl = (
            self.ACCESS_TOKEN_TTL
            if token_type is TokenType.ACCESS.value
            else self.REFRESH_TOKEN_TTL
        )

        payload = {"exp": int(time.time()) + token_ttl, "user_id": user_id, "type": token_type}
        new_token = jwt.encode(payload, self.signing_secret, algorithm="HS256")

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

    # def authenticate():
    #     """Does not process any previous auth state. Just creates a new one e.g. when logging in"""
    #     ...

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
