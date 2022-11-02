from abc import ABC


class TokenAuthService(ABC):
    def __init__(self):
        self.auth_state_handler = AuthStateHandler()
        self.admin_auth_state_handler = AdminAuthStateHandler()


    def create_auth_state():
        ...

    def authenticate():
        """Does not process any previous auth state. Just creates a new one e.g. when logging in"""
        ...


    def process_header():
        ...

    def process_cookie():
        ...
        
    def validate():
        ...

    def invalidate():
        """Removes or invalidates the auth state"""
        ...

    def refresh():
        ...

    """these probably should be in auth state handler"""

    def update_auth_state():
        ...

    def delete_auth_state():
        ...


class JWTTokenAuthService(TokenAuthService):
    def __init__(self):
        self.auth_state_handler = AuthStateHandler()
        self.admin_auth_state_handler = AdminAuthStateHandler()


    def create_auth_state():
        

    def authenticate():
        """Does not process any previous auth state. Just creates a new one e.g. when logging in"""


    def process_header():

    def process_cookie():


    def validate():
        ...

    def invalidate():
        """Removes or invalidates the auth state"""
        ...

    def refresh():
        ...

    """these probably should be in auth state handler"""

    def update_auth_state():
        ...

    def delete_auth_state():
        ...

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
