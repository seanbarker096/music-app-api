from enum import Enum
from typing import Iterable, Optional


class AuthUserRole(Enum):
    USER = 1
    ADMIN = 2


class AuthUser:
    """User class specifically for the AuthenticationService. This does not map directly to the main User data model"""

    id: int = ...
    role: AuthUserRole = ...
    permissions: Optional[Iterable] = ...

    def __init__(self, id: int, role: AuthUserRole, permissions: Optional[Iterable] = None):
        self.id = id
        self.role = role
        self.permissions = permissions


class AuthState:
    auth_user: AuthUser = ...
    verifier: JWT = ...


class AuthStateCreateRequest:
    auth_user: AuthUser = ...

    def __init__(self, auth_user: AuthUser):
        self.auth_user = auth_user


class AuthStateCreateResult:
    auth_state: AuthState = ...

    def __init__(self, auth_state: AuthState):
        self.auth_state = auth_state
