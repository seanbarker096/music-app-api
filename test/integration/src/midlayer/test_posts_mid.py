import time
from test.integration import IntegrationTestCase
from unittest.mock import patch

from api.midlayer.posts_mid import (
    PostAttachmentsCreateRequest,
    PostAttachmentsMidlayerMixin,
    PostCreateRequest,
    PostsMidlayerMixin,
)


class PostsMidIntegrationTest(IntegrationTestCase):
    def setUp(self):
        super().setUp()

    @patch("time.time")
    def test_post_create(self, time):
        time.return_value = self.current_time

        post_mid = PostsMidlayerMixin(config=self.config)

        request = PostCreateRequest(owner_id=555, content="A test post")

        post = post_mid.post_create(request).post

        self.assertEqual(post.id, 1, "Should return the correct post id")
        self.assertEqual(
            post.create_time, self.current_time, "Should return the correct post create time"
        )
        self.assertEqual(post.update_time, None, "Should not set the post update time on creation")

    def test_post_get(self):
        ...


class PostAttachmentsMidIntegrationTest(IntegrationTestCase):
    def setUp(self):
        super().setUp()

    @patch("time.time")
    def test_post_attachments_create(self, time):
        time.return_value = self.current_time

        post_attachments_mid = PostAttachmentsMidlayerMixin(config=self.config)

        request = PostAttachmentsCreateRequest(post_id=123, file_ids=[567, 8910])

        result = post_attachments_mid.post_attachments_create(request=request)

        attachments = result.post_attachments
        first_attachment = attachments[0]
        second_attachment = attachments[1]

        self.assertEqual(len(attachments), 2, "Should return 2 attachments")

        self.assertEqual(first_attachment.file_id, 567, "Should return correct file_id (1)")
        self.assertEqual(
            first_attachment.create_time,
            self.current_time,
            "Should return the correct create time (1)",
        )
        self.assertEqual(first_attachment.post_id, 123, "Should return the correct post id (1)")
        self.assertEqual(first_attachment.id, 1, "Should return the correct attachment id (1)")

        self.assertEqual(second_attachment.file_id, 8910, "Should return correct file_id (2)")
        self.assertEqual(
            second_attachment.create_time,
            self.current_time,
            "Should return the correct create time (2)",
        )
        self.assertEqual(second_attachment.post_id, 123, "Should return the correct post id (2)")
        self.assertEqual(second_attachment.id, 2, "Should return the correct attachment id (2)")

    def test_post_attachments_get(self):
        ...
