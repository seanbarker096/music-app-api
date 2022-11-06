import jwt
from rest import AuthAPITestCase


class AuthApiTest(AuthAPITestCase):
    def test_login_with_username_and_password(self):

        user_id = 12345

        json = {"username": "testUser123", "password": "testPassword1"}

        response = self.test_client.post("/login/", json=json)

        [bearer_str, jwt] = response.headers["Authorization"].split(" ")

        self.assertEquals(response.status, 200, "Should return 200 status code")

        self.assertEqual(bearer_str, "Bearer", "Should correctly format the Authorization header")

        self.assertIsInstance(jwt, str, "Should return an access token")

        self.assertRegex(jwt, r"^(?:[\w-]*\.){2}[\w-]*$", "Should set the bearer token to be a jwt")

        self.assertEqual(jwt, response["token"], "Should return the jwt in the response")

        self.assertRegex(
            response["r_token"],
            r"^(?:[\w-]*\.){2}[\w-]*$",
            "Should set the refresh token to be a jwt",
        )

        self.assertEqual(response["user_id"], user_id, "Should return the correct user id")

    def test_login_with_non_registered_user(self):
        ...

    def test_login_with_email_and_password(self):
        ...
