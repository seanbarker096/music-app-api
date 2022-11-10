from unittest.mock import Mock

import jwt
from rest import AuthAPITestCase

from api.authentication_service.api import JWTTokenAuthService
from api.authentication_service.typings import AuthState, AuthStateCreateResult
from api.midlayer.api import Midlayer


class AuthApiTest(AuthAPITestCase):
    def test_login_with_username_and_password(self):

        user_id = 12345

        json = {"username": "testUser12345", "password": "testPassword1"}

        self.app.conns.auth_service = Mock()

        self.app.conns.midlayer = Midlayer(config=self.config, users_midlayer=Mock())

        self.app.conns.midlayer.users_midlayer.get_user_by_username_and_password = Mock()

        self.app.conns.auth_service.create_auth_state()

        response = self.test_client.post("/login/", json=json)

        [bearer_str, jwt] = response.headers["Authorization"].split(" ")

        self.assertEquals(response.status, 200, "Should return 200 status code")

        self.assertEqual(bearer_str, "Bearer", "Should correctly format the Authorization header")

        self.assertIsInstance(jwt, str, "Should return an access token")

        self.assertRegex(jwt, r"^(?:[\w-]*\.){2}[\w-]*$", "Should set the bearer token to be a jwt")

        self.assertEqual(jwt, response["token"], "Should also return the jwt in the response")

        self.assertRegex(
            response["r_token"],
            r"^(?:[\w-]*\.){2}[\w-]*$",
            "Should set the refresh token to be a jwt and return in the response",
        )

        self.assertEqual(response["user_id"], user_id, "Should return the correct user id")

    def test_login_with_non_registered_user(self):
        ...

    def test_login_with_email_and_password(self):
        ...
