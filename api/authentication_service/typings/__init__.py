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


class AuthStatus(Enum):
    AUTHENTICATED = 1
    UNAUTHENTICATED = 2


class AuthState:
    # Information about the authenticated user. This is None if the user is unauthenticated
    auth_user: Optional[AuthUser] = ...
    access_token: PyJWT = ...
    refresh_token: Optional[PyJWT] = ...
    status: AuthStatus

    def __init__(
        self,
        auth_user: Optional[AuthUser],
        access_token: PyJWT,
        refresh_token: PyJWT,
        status: AuthStatus,
    ):
        self.auth_user = auth_user
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.status = status


class AuthStateCreateRequest:
    auth_user: AuthUser = ...

    def __init__(self, auth_user: AuthUser):
        self.auth_user = auth_user


class AuthStateCreateResult:
    auth_state: AuthState = ...

    def __init__(self, auth_state: AuthState):
        self.auth_state = auth_state


class AuthStateDeleteRequest:
    refresh_token: Optional[str] = ...
    owner_id: Optional[int] = ...
    session_id: Optional[str] = ...

    def __init__(self, refresh_token: Optional[str] = None, owner_id: Optional[int] = None, session_id: Optional[str] = None):
        self.refresh_token = refresh_token
        self.owner_id = owner_id
        self.session_id = session_id



class TokenCreateRequest:
    token: str = ...
    owner_id: int = ...
    session_id: str = ...

    def __init__(self, token: str, owner_id: int, session_id: str):
        self.token = token
        self.owner_id = owner_id
        self.session_id = session_id


class AuthenticateRequest:
    token: str

    def __init__(self, token: str):
        self.token = token
