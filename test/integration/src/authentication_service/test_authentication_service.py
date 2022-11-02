from test.integration import IntegrationTestCase

from api.authentication_service.api import TokenAuthService

from typings import AuthStateCreateRequest, AuthUser, AuthUserRole


class TokenAuthenticationServiceIntegrationTestCase(IntegrationTestCase):
    def test_create_auth_state():

        auth_user = AuthUser(id=123456, role=AuthUserRole.USER.value, permissions=None)

        request = AuthStateCreateRequest(auth_user=auth_user)

        authentication_service = JWTTokenAuthService()

        result = authentication_service.create_auth_state(request)
