import time
from unittest.mock import Mock

from rest import PostAPITestCase

from api.typings.posts import Post, PostCreateRequest, PostCreateResult


class PostApiTest(PostAPITestCase):
    def test_post_create(self):
        now = time.time()

        json = {
            "content": "This is a test post!",
            "owner_id": 555,
        }

        post = Post(
            id=123,
            attachment_id=None,
            create_time=now,
            update_time=None,
            owner_id=555,
            content="This is a test post!",
        )

        expected_response = PostCreateResult(post=post)

        self.app.conns.midlayer = Mock()
        self.app.conns.midlayer.post_create = Mock(return_value=expected_response)

        response = self.test_client.post("/posts/", json=json)

        response_dict = {}
        response_dict["post"] = vars(expected_response.post)

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(response.json, response_dict, "Should return the correct post")

    def test_post_create_with_attachment(self):
        now = time.time()

        json = {"content": "This is a test post!", "owner_id": "555", "attachment_id": "1111"}

        post = Post(
            id=123,
            create_time=now,
            update_time=None,
            owner_id=555,
            content="This is a test post!",
            attachment_id=1111,
        )

        expected_response = PostCreateResult(post=post)

        self.app.conns.midlayer = Mock()
        self.app.conns.midlayer.post_create = Mock(return_value=expected_response)

        response = self.test_client.post("/posts/", json=json)

        response_dict = {}
        response_dict["post"] = vars(expected_response.post)

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(response.json, response_dict, "Should return the correct post")
