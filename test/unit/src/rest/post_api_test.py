import time
from test.test_utils import mock_decorator
from unittest.mock import MagicMock, Mock, patch

from rest import PostAPITestCase, set_up_patches

from api.typings.posts import (
    Post,
    PostAttachment,
    PostAttachmentsCreateResult,
    PostAttachmentsGetResult,
    PostCreateResult,
    PostsGetResult,
)

## Setup patches before the test case is initialised, which results in the blueprint file being called and defines functions before they can be patched
set_up_patches()


class PostApiTest(PostAPITestCase):
    def test_post_create(self):
        now = time.time()

        json = {
            "content": "This is a test post!",
            "owner_id": 555,
        }

        post = Post(
            id=123,
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
        response_dict["attachments"] = []

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(response.json, response_dict, "Should return the correct post")

    def test_post_create_with_attachment(self):
        now = time.time()

        json = {
            "content": "This is a test post!",
            "owner_id": "555",
            "attachment_file_ids": '["1111"]',
        }

        post = Post(
            id=123,
            create_time=now,
            update_time=None,
            owner_id=555,
            content="This is a test post!",
        )

        post_attachments = [
            PostAttachment(id=456, post_id=123, file_id=888, create_time=now),
        ]

        expected_post_create_response = PostCreateResult(post=post)
        expected_post_attachments_create_response = PostAttachmentsCreateResult(
            post_attachments=post_attachments
        )

        self.app.conns.midlayer = Mock()
        self.app.conns.midlayer.post_create = Mock(return_value=expected_post_create_response)

        self.app.conns.midlayer.post_attachments_create = Mock(
            return_value=expected_post_attachments_create_response
        )

        response = self.test_client.post("/posts/", json=json)

        response_dict = {}
        response_dict["post"] = vars(expected_post_create_response.post)

        attachment_dicts = []
        for attachment in expected_post_attachments_create_response.post_attachments:
            attachment_dicts.append(vars(attachment))

        response_dict["attachments"] = attachment_dicts

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(response.json, response_dict, "Should return the correct post")

    def test_post_get_by_id_without_attachments(self):

        self.app.conns.midlayer = Mock()

        expected_post = Post()

        expected_posts_get_result = PostsGetResult(posts=[expected_post])

        self.app.conns.midlayer.posts_get = Mock(return_value=expected_posts_get_result)

        response = self.test_client.get(
            "/posts/123",
        )

        response_dict = {}
        response_dict["posts"] = [vars(expected_post)]
        response_dict["attachments"] = []

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(response.json, response_dict, "Should return the correct post")

    def test_post_get_post_not_found(self):
        ...

    def test_posts_get_multiple_posts_found(self):
        ...

    def test_post_get_with_attachments(self):

        self.app.conns.midlayer = Mock()

        now = time.time()
        expected_post = Post(id=123, owner_id=555, content="My great test post", create_time=now)
        expected_post_attachment = PostAttachment(post_id=123, file_id=888, create_time=now)

        expected_posts_get_result = PostsGetResult(posts=[expected_post])
        expected_post_attachments_get_result = PostAttachmentsGetResult(
            post_attachments=[expected_post_attachment]
        )

        self.app.conns.midlayer.posts_get = Mock(return_value=expected_posts_get_result)
        self.app.conns.midlayer.post_attachments_get = Mock(
            return_value=expected_post_attachments_get_result
        )

        response = self.test_client.get(
            "/posts/123",
        )

        response_dict = {}
        response_dict["posts"] = [vars(expected_post)]
        response_dict["attachments"] = [vars(expected_post_attachment)]

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertEqual(
            response.json, response_dict, "Should return the correct post and post attachments"
        )
