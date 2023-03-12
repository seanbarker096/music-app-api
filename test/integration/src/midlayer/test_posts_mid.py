import json
import time
from test.integration import IntegrationTestCase
from test.integration.src.fixtures.DTO.feature_fixture_dto import FeatureFixtureDTO
from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO
from test.integration.src.fixtures.DTO.tag_fixture_dto import TagFixtureDTO
from unittest.mock import patch

import pytest

from api.midlayer.posts_mid import PostAttachmentsMidlayerMixin, PostsMidlayerMixin
from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostOwnerType,
    PostsGetFilter,
    ProfilePostsGetFilter,
    ProfileType,
)
from api.typings.tags import TaggedEntityType, TaggedInEntityType


class PostsMidIntegrationTest(IntegrationTestCase):
    def setUp(self):
        super().setUp()

    @patch("time.time")
    def test_post_create(self, time):
        time.return_value = self.current_time

        post_mid = PostsMidlayerMixin(config=self.config)

        request = PostCreateRequest(
            owner_id=555,
            owner_type=PostOwnerType.USER.value,
            content="A test post",
            creator_id=555,
        )

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
            owner_id=555,
            owner_type=PostOwnerType.USER.value,
            content="My great post",
            create_time=self.current_time,
            creator_id=555,
        )

        post_id = self.fixture_factory.post_fixture_create(post_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = PostsGetFilter(ids=[post_id])

        result = post_mid.posts_get(filter=filter)
        post = result.posts[0]

        self.assertEqual(len(result.posts), 1, "Should only return one post")
        self.assertEqual(post.id, post_id, "Should return the correct post_id")
        self.assertEqual(post.owner_id, 555, "Should return the correct post owner id")
        self.assertEqual(
            post.owner_type, PostOwnerType.USER.value, "Should return the correct post owner type"
        )
        self.assertEqual(post.content, "My great post", "Should return the correct post content")

    def test_profile_posts_get(self):
        requesting_profile_id = 555

        owned_post = PostFixtureDTO(
            owner_id=requesting_profile_id,
            owner_type=PostOwnerType.ARTIST.value,
            content="User 555 created this post",
            create_time=self.current_time,
            creator_id=requesting_profile_id,
        )

        owned_post_id = self.fixture_factory.post_fixture_create(owned_post)

        tagged_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will not be tagged in this post",
            create_time=self.current_time + 1000,
            creator_id=32,
        )

        tagged_post_id = self.fixture_factory.post_fixture_create(tagged_post)

        featured_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 feature this post in their profile",
            create_time=self.current_time + 2000,
            creator_id=32,
        )

        featured_post_id = self.fixture_factory.post_fixture_create(featured_post)

        feature_dto = FeatureFixtureDTO(
            featured_entity_type=FeaturedEntityType.POST.value,
            featured_entity_id=featured_post_id,
            featurer_type=FeaturerType.ARTIST.value,
            featurer_id=requesting_profile_id,
            creator_id=requesting_profile_id,
        )

        self.fixture_factory.feature_fixture_create(feature_dto)

        tag_dto = TagFixtureDTO(
            tagged_entity_id=requesting_profile_id,
            tagged_entity_type=TaggedEntityType.ARTIST.value,
            tagged_in_entity_id=tagged_post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=1111,
        )

        self.fixture_factory.tag_fixture_create(tag_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = ProfilePostsGetFilter(
            profile_id=requesting_profile_id,
            profile_type=ProfileType.ARTIST.value,
            include_featured=True,
            include_tagged=True,
            include_owned=True,
        )

        result = post_mid.profile_posts_get(filter=filter)

        posts = result.posts
        owned_post_result = result.posts[2]
        tagged_post_result = result.posts[1]
        featured_post_result = result.posts[0]

        self.assertEqual(len(posts), 3, "Should return tagged, featured and owned posts")
        self.assertEqual(
            owned_post_result.id, owned_post_id, "Should return the correct owned post"
        )
        self.assertEqual(
            tagged_post_result.id, tagged_post_id, "Should return the correct tagged post"
        )
        self.assertEqual(
            featured_post_result.id, featured_post_id, "Should return the correct featured post"
        )

    def test_profile_owned_posts_only_get(self) -> None:
        requesting_profile_id = 555
        other_user_id = 200

        owned_post = PostFixtureDTO(
            owner_id=requesting_profile_id,
            owner_type=PostOwnerType.ARTIST.value,
            content="User 555 created this post",
            create_time=self.current_time,
            creator_id=323,  # mock the user id of the person who owns the artist profile
        )

        owned_post_id = self.fixture_factory.post_fixture_create(owned_post)

        tagged_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will not be tagged in this post",
            create_time=self.current_time + 1000,
            creator_id=other_user_id,
        )

        tagged_post_id = self.fixture_factory.post_fixture_create(tagged_post)

        featured_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will not feature this post in their profile",
            create_time=self.current_time + 2000,
            creator_id=other_user_id,
        )

        featured_post_id = self.fixture_factory.post_fixture_create(featured_post)

        feature_dto = FeatureFixtureDTO(
            featured_entity_type=FeaturedEntityType.POST.value,
            featured_entity_id=featured_post_id,
            featurer_type=FeaturerType.ARTIST.value,
            featurer_id=other_user_id,
            creator_id=other_user_id,
        )

        self.fixture_factory.feature_fixture_create(feature_dto)

        tag_dto = TagFixtureDTO(
            tagged_entity_id=other_user_id,
            tagged_entity_type=TaggedEntityType.ARTIST.value,
            tagged_in_entity_id=tagged_post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=1111,
        )

        self.fixture_factory.tag_fixture_create(tag_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = ProfilePostsGetFilter(
            profile_id=requesting_profile_id,
            profile_type=ProfileType.ARTIST.value,
            include_featured=False,
            include_tagged=False,
            include_owned=True,
        )

        result = post_mid.profile_posts_get(filter=filter)

        posts = result.posts
        returned_post = result.posts[0]

        self.assertEqual(len(posts), 1, "Should only return the owned posts")
        self.assertEqual(returned_post.id, owned_post_id, "Should return the correct owned post")

    def test_profile_tagged_posts_only_get(self) -> None:
        requesting_profile_id = 555
        other_user_id = 200

        owned_post = PostFixtureDTO(
            owner_id=other_user_id,
            owner_type=PostOwnerType.USER.value,
            content="Some other user created this post",
            create_time=self.current_time,
            creator_id=other_user_id,
        )

        owned_post_id = self.fixture_factory.post_fixture_create(owned_post)

        tagged_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will be tagged in this post",
            create_time=self.current_time + 1000,
            creator_id=32,
        )

        tagged_post_id = self.fixture_factory.post_fixture_create(tagged_post)

        featured_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will not feature this post in their profile",
            create_time=self.current_time + 2000,
            creator_id=32,
        )

        featured_post_id = self.fixture_factory.post_fixture_create(featured_post)

        feature_dto = FeatureFixtureDTO(
            featured_entity_type=FeaturedEntityType.POST.value,
            featured_entity_id=featured_post_id,
            featurer_type=FeaturerType.ARTIST.value,
            featurer_id=other_user_id,
            creator_id=other_user_id,
        )

        self.fixture_factory.feature_fixture_create(feature_dto)

        tag_dto = TagFixtureDTO(
            tagged_entity_id=requesting_profile_id,
            tagged_entity_type=TaggedEntityType.ARTIST.value,
            tagged_in_entity_id=tagged_post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=1111,
        )

        self.fixture_factory.tag_fixture_create(tag_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = ProfilePostsGetFilter(
            profile_id=requesting_profile_id,
            profile_type=ProfileType.ARTIST.value,
            include_featured=False,
            include_tagged=True,
            include_owned=False,
        )

        result = post_mid.profile_posts_get(filter=filter)

        posts = result.posts
        returned_post = result.posts[0]

        self.assertEqual(len(posts), 1, "Should only return the tagged post")
        self.assertEqual(returned_post.id, tagged_post_id, "Should return the correct tagged post")

    def test_profile_featured_posts_only_get(self) -> None:
        requesting_profile_id = 555
        other_user_id = 200

        owned_post = PostFixtureDTO(
            owner_id=other_user_id,
            owner_type=PostOwnerType.USER.value,
            content="Some other user created this post",
            create_time=self.current_time,
            creator_id=other_user_id,
        )

        self.fixture_factory.post_fixture_create(owned_post)

        tagged_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="Some other user will be tagged in this post",
            create_time=self.current_time + 1000,
            creator_id=32,
        )

        tagged_post_id = self.fixture_factory.post_fixture_create(tagged_post)

        featured_post = PostFixtureDTO(
            owner_id=32,
            owner_type=PostOwnerType.USER.value,
            content="User 555 will not feature this post in their profile",
            create_time=self.current_time + 2000,
            creator_id=32,
        )

        featured_post_id = self.fixture_factory.post_fixture_create(featured_post)

        feature_dto = FeatureFixtureDTO(
            featured_entity_type=FeaturedEntityType.POST.value,
            featured_entity_id=featured_post_id,
            featurer_type=FeaturerType.ARTIST.value,
            featurer_id=requesting_profile_id,
            creator_id=requesting_profile_id,
        )

        self.fixture_factory.feature_fixture_create(feature_dto)

        tag_dto = TagFixtureDTO(
            tagged_entity_id=other_user_id,
            tagged_entity_type=TaggedEntityType.ARTIST.value,
            tagged_in_entity_id=tagged_post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=1111,
        )

        self.fixture_factory.tag_fixture_create(tag_dto)

        post_mid = PostsMidlayerMixin(config=self.config)

        filter = ProfilePostsGetFilter(
            profile_id=requesting_profile_id,
            profile_type=ProfileType.ARTIST.value,
            include_featured=True,
            include_tagged=False,
            include_owned=False,
        )

        result = post_mid.profile_posts_get(filter=filter)

        posts = result.posts
        returned_post = result.posts[0]

        self.assertEqual(len(posts), 1, "Should only return the featured post")
        self.assertEqual(
            returned_post.id, featured_post_id, "Should return the correct featured post"
        )


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
