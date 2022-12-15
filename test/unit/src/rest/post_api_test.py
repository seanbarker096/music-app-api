import time
from unittest.mock import Mock

from rest import PostAPITestCase

from api.typings.posts import (
    Post,
    PostAttachment,
    PostAttachmentsCreateResult,
    PostCreateRequest,
    PostCreateResult,
)


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

    def test_post_get_without_attachments(self):
        ...

    def test_post_get_with_attachments(self):
        ...
