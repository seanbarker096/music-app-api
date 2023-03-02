import time
from test.integration import IntegrationTestCase
from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO
from unittest.mock import patch

from api.midlayer.posts_mid import PostAttachmentsMidlayerMixin, PostsMidlayerMixin
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostsGetFilter,
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
        self.assertEqual(post.content, "A test post", "Should return the correct post content")
        self.assertEqual(
            post.create_time, self.current_time, "Should return the correct post create time"
        )
        self.assertEqual(post.update_time, None, "Should not set the post update time on creation")
        self.assertFalse(post.is_deleted)

    def test_post_get(self):

        post_dto = PostFixtureDTO(
            owner_id=555, content="My great post", create_time=self.current_time
        )

        post_id = self.fixture_factory.post_fixture_create(post_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = PostsGetFilter(ids=[post_id])

        result = post_mid.posts_get(filter=filter)
        post = result.posts[0]

        self.assertEqual(len(result.posts), 1, "Should only return one post")
        self.assertEqual(post.id, post_id, "Should return the correct post_id")
        self.assertEqual(post.owner_id, 555, "Should return the correct post owner id")
        self.assertEqual(post.content, "My great post", "Should return the correct post content")


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
        post_attachment_dto = PostAttachmentFixtureDTO(
            post_id=444, file_id=333, create_time=self.current_time
        )

        post_attachment_id = self.fixture_factory.post_attachment_fixture_create(
            post_attachment_dto
        )

        post_attachments_mid = PostAttachmentsMidlayerMixin(config=self.config)

        filter = PostAttachmentsGetFilter(post_ids=[post_attachment_id])

        result = post_attachments_mid.post_attachments_get(filter=filter)
        post_attachment = result.post_attachments[0]

        self.assertEqual(
            post_attachment.id, post_attachment_id, "Should return the correct post_id"
        )
        self.assertEqual(post_attachment.file_id, 333, "Should return the correct file id")
        self.assertEqual(post_attachment.post_id, 444, "Should return the correct post id")
