import json
import time
from test.integration import IntegrationTestCase
from test.integration.src.fixtures.DTO.feature_fixture_dto import FeatureFixtureDTO
from test.integration.src.fixtures.DTO.performance_fixture_dto import (
    PerformanceFixtureDTO,
)
from test.integration.src.fixtures.DTO.performer_fixture_dto import PerformerFixtureDTO
from test.integration.src.fixtures.DTO.post_attachment_fixture_dto import (
    PostAttachmentFixtureDTO,
)
from test.integration.src.fixtures.DTO.post_fixture_dto import PostFixtureDTO
from test.integration.src.fixtures.DTO.tag_fixture_dto import TagFixtureDTO
from unittest.mock import Mock, patch

import pytest

from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.dao.tags_dao import TagsDAO
from api.db.db import TestingDBConnectionManager
from api.midlayer.posts_mid import (
    PostAttachmentsMidlayerConnections,
    PostAttachmentsMidlayerMixin,
    PostMidlayerConnections,
    PostsMidlayerMixin,
)
from api.midlayer.tags_mid import TagsMidlayerConnections, TagsMidlayerMixin
from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.performances import Performance, PerformancesGetResult
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostOwnerType,
    PostsGetFilter,
    ProfilePostsGetFilter,
    ProfileType,
)
from api.typings.tags import (
    TagCreateRequest,
    TaggedEntityType,
    TaggedInEntityType,
    TagsGetFilter,
)


class TagsMidIntegrationTest(IntegrationTestCase):
    def setUp(self):
        super().setUp()

        tags_dao = TagsDAO(config=self.config, db=TestingDBConnectionManager)
        tags_mid_conns = TagsMidlayerConnections(config=self.config, tags_dao=tags_dao)

        tag_event_subject_mock = Mock()
        tag_event_subject_mock.publish_event = Mock()

        self.performances_mid_mock = Mock()
        
        self.tags_mid = TagsMidlayerMixin(
            config=self.config,
            conns=tags_mid_conns,
            tag_event_subject=tag_event_subject_mock,
            performances_mid=self.performances_mid_mock,
            )

    def test_post_tag_create_when_tag_already_exists(self):
        """
        Tests that for a given performer trying to tag a performance in a post, other tags between a post and that performance are deleted if they exist
        """

        post_dto = PostFixtureDTO(
            owner_id=555,
            owner_type=PostOwnerType.USER.value,
            content="My great post",
            create_time=self.current_time,
            creator_id=555,
        )

        post_id = self.fixture_factory.post_fixture_create(post_dto)

        # Create artist
        performer_one_dto = PerformerFixtureDTO(
            name="Performer One",
            uuid="performer-one",
            biography="Performer One Biography",
            create_time=self.current_time,
        )

        performer_one_id = self.fixture_factory.performer_fixture_create(performer_one_dto)
        
        # Create performances
        performance_one_dto = PerformanceFixtureDTO(
            performer_id=performer_one_id,
            performance_date=self.current_time,
            create_time=self.current_time,
            update_time=None,
            event_id=111,
        )

        performance_one_id = self.fixture_factory.performance_fixture_create(
            performance_one_dto
        )

        performance_one = Performance(
            id=performance_one_id,
            performer_id=performer_one_id,
            performance_date=self.current_time,
            create_time=self.current_time,
            update_time=None,
            event_id=111,
        )

        performance_two_dto = PerformanceFixtureDTO(
            performer_id=performer_one_id,
            performance_date=self.current_time,
            create_time=self.current_time,
            update_time=None,
            event_id=222,
        )

        performance_two_id = self.fixture_factory.performance_fixture_create(performance_two_dto)


        # Create tag
        tag_one_dto = TagFixtureDTO(
            tagged_entity_id=performance_one_id,
            tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
            tagged_in_entity_id=post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=555
        )

        tag_one_id = self.fixture_factory.tag_fixture_create(tag_one_dto)

        # Create another tag between the same post, but a different performance
        tag_create_request = TagCreateRequest(
            tagged_entity_id=performance_two_id,
            tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
            tagged_in_entity_id=post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value,
            creator_id=555
        )
      
        self.performances_mid_mock.performances_get = Mock(
            return_value=PerformancesGetResult(performances=[performance_one])
        )
        
        created_tag = self.tags_mid.tag_create(tag_create_request).tag


        # Assert that only one tag exists between that performers performances, and that post. We only seeded one performer, so we dont need to try and filter for this specific performer
        tags_get_filter = TagsGetFilter(
            tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
            tagged_in_entity_id=post_id,
            tagged_in_entity_type=TaggedInEntityType.POST.value
        )

        tags = self.tags_mid.tags_get(tags_get_filter).tags

        self.assertEqual(len(tags), 1, 'Only one tag should exist between the post and the performers performances')
        self.assertEqual(tags[0].id, created_tag.id, 'Should return the newest tag')