import time
from test.integration import IntegrationTestCase
from unittest.mock import patch

from api.midlayer.posts_mid import PostCreateRequest, PostsMidlayerMixin


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
