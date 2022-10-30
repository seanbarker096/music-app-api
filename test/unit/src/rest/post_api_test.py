import time
from unittest.mock import Mock

from api.rest import PostAPITestCase
from api.typings.posts import Post, PostCreateResult


class PostApiTest(PostAPITestCase):
    def test_post_create(self):

        now = time.time()

        data = {
            "content": "This is a test post!",
        }

        post = Post(id=123, attachment_id=None, create_time=now, update_time=None, owner_id=555)

        post_create_result = PostCreateResult(post=post)

        self.conns.posts_midlayer = Mock()
        self.conns.posts_midlayer.post_create = Mock(return_value=post_create_result)

        post_response = self.test_client.post("/posts/", data=data).post

        self.assertEqual(post_response.id, 123, "Should return the correct post id")
        self.assertEqual(post_response.owner_id, 555, "Should return the correct owner id")
        self.assertEqual(post_response.create_time, now, "Should return the correct create time")
        self.assertEqual(post_response.update_time, now, "Should return the correct update time")
        self.assertEqual(post_response.attachment_id, None, "Should not contain an attachment")
        self.assertEqual(
            post_response.content, "This is a test post!", "Should return the correct post content"
        )

    def test_post_create_with_attachment(self):
        ...
