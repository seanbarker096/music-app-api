from enum import Enum
from typing import Iterable, Optional

from jwt import PyJWT


class AuthUserRole(Enum):
    USER = 1
    ADMIN = 2


class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2


class AuthUser:
    """User class specifically for the AuthenticationService. This does not map directly to the main User data model"""

    user_id: int = ...
    role: AuthUserRole = ...
    permissions: Optional[Iterable] = ...

    def __init__(self, user_id: int, role: AuthUserRole, permissions: Optional[Iterable] = None):
        self.user_id = user_id
        self.role = role
        self.permissions = permissions


class AuthStates(Enum):
    AUTHENTICATED = 1
    UNAUTHENTICATED = 2


class AuthState:
    auth_user: AuthUser = ...
    access_token: PyJWT = ...
    refresh_token: Optional[PyJWT] = ...
    state: AuthStates

    def __init__(
        self, auth_user: AuthUser, access_token: PyJWT, refresh_token: PyJWT, state: AuthStates
    ):
        self.auth_user = auth_user
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.state = state


class AuthStateCreateRequest:
    auth_user: AuthUser = ...

    def __init__(self, auth_user: AuthUser):
        self.auth_user = auth_user


class AuthStateCreateResult:
    auth_state: AuthState = ...

    def __init__(self, auth_state: AuthState):
        self.auth_state = auth_state


class TokenCreateRequest:
    token: str
    owner_id: int

    def __init__(self, token: str, owner_id: int):
        self.token = token
        self.owner_id = owner_id
