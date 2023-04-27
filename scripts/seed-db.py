import logging
import os
import time
from configparser import ConfigParser

from api.dao.events_dao import EventsDAO
from api.dao.features_dao import FeaturesDAO
from api.dao.performances_dao import PerformanceAttendancesDAO, PerformancesDAO
from api.dao.performers_dao import PerformersDAO
from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.dao.tags_dao import TagsDAO
from api.dao.users_dao import UsersDAO
from api.db.db import TestingDBConnectionManager
from api.events.tags.performance_tag_event_observer import PerformanceTagEventObserver
from api.events.tags.tag_event_subject import TagEventSubject
from api.file_service.api import FileService, FileServiceDAO
from api.file_service.typings.typings import FileCreateRequest
from api.midlayer.events_mid import EventsMidlayerConnections, EventsMidlayerMixin
from api.midlayer.features_mid import FeaturesMidlayerConnections, FeaturesMidlayerMixin
from api.midlayer.performances_mid import (
    PerformanceAttendancesMidlayerConnections,
    PerformanceAttendancesMidlayerMixin,
    PerformancesMidlayerConnections,
    PerformancesMidlayerMixin,
)
from api.midlayer.performers_mid import (
    PerformersMidlayerConnections,
    PerformersMidlayerMixin,
)
from api.midlayer.posts_mid import PostMidlayerConnections, PostsMidlayerMixin
from api.midlayer.tags_mid import TagsMidlayerConnections, TagsMidlayerMixin
from api.typings.events import EventCreateRequest, EventType
from api.typings.features import FeatureCreateRequest, FeaturedEntityType, FeaturerType
from api.typings.performances import (
    PerformanceAttendanceCreateRequest,
    PerformanceCreateRequest,
)
from api.typings.performers import PerformerCreateRequest
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostCreateRequest,
    PostOwnerType,
)
from api.typings.tags import TagCreateRequest, TaggedEntityType, TaggedInEntityType
from api.typings.users import UserCreateRequest, UserUpdateRequest
from api.utils import hash_password

log_file_path = f"{os.path.dirname(__file__)}/../api/db.log"
with open(log_file_path, "w") as file:
    file.write("")

logging.basicConfig(filename=log_file_path, level=logging.ERROR)

config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../api/config/", f"{env}.cfg")

config.read(filename)

config_dict = {"config_file": config}

users_dao = UsersDAO(config_dict, db=TestingDBConnectionManager)

features_dao = FeaturesDAO(config_dict, db=TestingDBConnectionManager)
feature_conns = FeaturesMidlayerConnections(config_dict, features_dao=features_dao)
features_mid = FeaturesMidlayerMixin(config_dict, feature_conns)

posts_dao = PostsDAO(config_dict, db=TestingDBConnectionManager)
post_attachments_dao = PostAttachmentsDAO(config_dict, db=TestingDBConnectionManager)

posts_midlayer_conns = PostMidlayerConnections(config, posts_dao=posts_dao)
posts_mid = PostsMidlayerMixin(config_dict, conns=posts_midlayer_conns)


events_dao = EventsDAO(config=config_dict, db=TestingDBConnectionManager)
events_midlayer_conns = EventsMidlayerConnections(config=config_dict, events_dao=events_dao)
events_mid = EventsMidlayerMixin(config=config_dict, conns=events_midlayer_conns)

performers_dao = PerformersDAO(config=config_dict, db=TestingDBConnectionManager)
performers_conns = PerformersMidlayerConnections(config=config_dict, performers_dao=performers_dao)
performers_mid = PerformersMidlayerMixin(config=config_dict, conns=performers_conns)

performances_dao = PerformancesDAO(config=config_dict, db=TestingDBConnectionManager)
performances_midlayer_conns = PerformancesMidlayerConnections(
    config=config_dict, performances_dao=performances_dao
)
performances_mid = PerformancesMidlayerMixin(config=config_dict, conns=performances_midlayer_conns)

performance_attendances_dao = PerformanceAttendancesDAO(
    config=config_dict, db=TestingDBConnectionManager
)
performance_attendance_conns = PerformanceAttendancesMidlayerConnections(
    config=config_dict, performance_attendances_dao=performance_attendances_dao
)
performance_attendances_mid = PerformanceAttendancesMidlayerMixin(
    config_dict, conns=performance_attendance_conns, performances_mid=performances_mid
)


file_service_dao = FileServiceDAO(config=config_dict, db=TestingDBConnectionManager)
file_service = FileService(config_dict, file_service_dao=file_service_dao)


tags_dao = TagsDAO(config_dict, db=TestingDBConnectionManager)
tags_mid_conns = TagsMidlayerConnections(config, tags_dao=tags_dao)
tag_event_subject = TagEventSubject(
    config=config_dict,
    observers=[
        PerformanceTagEventObserver(
            config=config_dict,
            performance_attendances_midlayer=performance_attendances_mid,
            posts_midlayer=posts_mid,
        )
    ],
)
tags_mid = TagsMidlayerMixin(
    config=config_dict, conns=tags_mid_conns, tag_event_subject=tag_event_subject, performances_mid=performances_mid
)


## Create user 1 and their avatar image
password_hash = hash_password("password")
request = UserCreateRequest(
    username="sean",
    first_name="Sean",
    second_name="Barker",
    email="seanbarker6@sky.com",
    password="password",
)

user_one = users_dao.user_create(request=request, password_hash=password_hash)

request = UserCreateRequest(
    username="gregory",
    first_name="Greg",
    second_name="Baxter",
    email="gg_no_re@sky.com",
    password="password",
)

user_one = users_dao.user_create(request=request, password_hash=password_hash)



# Create avatar file
avatar_file_uuid = "123456"
avatar_file = None

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "male-profile-pic.jpg"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid=avatar_file_uuid,
        file_name="profile-pic.jpg",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="image/jpeg",
        url=None,
    )
    avatar_file = file_service.create_file(request).file

dog_video_uuid = "202"
dog_video_file = None

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "dog.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid=dog_video_uuid,
        file_name="dog.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    dog_video_file = file_service.create_file(request).file


# set it on the user
user_update_request = UserUpdateRequest(user_one.id, avatar_file_uuid=avatar_file_uuid)

users_dao.user_update(user_update_request)


## Create user 2

password_hash = hash_password("password")
request = UserCreateRequest(
    username="tim14",
    first_name="Tim",
    second_name="Smith",
    email="timsmith@sky.com",
    password="password",
)

user_two = users_dao.user_create(request=request, password_hash=password_hash)


################### CREATE POSTS ####################

# 1 - Post uploaded by the user we created
post_create_request = PostCreateRequest(
    owner_id=user_one.id,
    owner_type=PostOwnerType.USER.value,
    content="This is a new post",
    creator_id=user_one.id,
)

post_one = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post_one.id, file_id=dog_video_file.id
)

# 2 Post uploaded by second user, and tags the first user
post_create_request = PostCreateRequest(
    owner_id=user_two.id,
    owner_type=PostOwnerType.USER.value,
    content="This is a post which user one will be tagged in",
    creator_id=user_two.id,
)

post_two = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post_two.id, file_id=dog_video_file.id
)

tag_create_request = TagCreateRequest(
    tagged_in_entity_id=post_two.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    tagged_entity_type=TaggedEntityType.USER.value,
    tagged_entity_id=user_one.id,
    creator_id=user_two.id,
)
tag = tags_mid.tag_create(tag_create_request)

# # 3 Post uploaded be second user, featured by first user
post_create_request = PostCreateRequest(
    owner_id=user_two.id,
    owner_type=PostOwnerType.USER.value,
    content="This is a thrid post which user one will feature on their profile",
    creator_id=user_two.id,
)

post_three = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post_three.id, file_id=avatar_file.id
)

feature_create_request = FeatureCreateRequest(
    featured_entity_type=FeaturedEntityType.POST.value,
    featured_entity_id=post_three.id,
    featurer_type=FeaturerType.USER.value,
    featurer_id=user_one.id,
    creator_id=user_one.id,
)

feature = features_mid.feature_create(feature_create_request).feature

# # 4
# post_create_request = PostCreateRequest(owner_id=user_one.id, content="This is a fourth post")

# post = posts_dao.post_create(post_create_request)

# post_attachment = post_attachments_dao.post_attachment_create(
#     post_id=post.id, file_id=avatar_file.id
# )


###################### CREATE PERFORMERS ######################

performer_create_request = PerformerCreateRequest(
    name="Eminem",
    biography="I'm a rapper",
    uuid="7dGJo4pcD2V6oG8kP0tJRR",
    owner_id=user_one.id,
    image_url="https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b",
)

performer = performers_mid.performer_create(performer_create_request).performer


# Create a post for him

post_create_request = PostCreateRequest(
    owner_id=performer.id,
    owner_type=PostOwnerType.PERFORMER.value,
    content="Eminems first post",
    creator_id=user_two.id,
)

post_four = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post_four.id, file_id=dog_video_file.id
)


#### CREATE EVENTS ####
event_create_request = EventCreateRequest(
    venue_name="Glastonbury",
    event_type=EventType.MUSIC_FESTIVAL.value,
    start_date=1681551032,
    end_date=1681551032 + 100000,
)

event_one = events_mid.event_create(event_create_request).event


event_create_request = EventCreateRequest(
    venue_name="O2 Academy Brixton",
    event_type=EventType.MUSIC_CONCERT.value,
    start_date=1681551032 + 200000,
    end_date=1681551032 + 300000,
)

event_two = events_mid.event_create(event_create_request).event


################### CREATE PERFORMANCES ####################

performance_create_request = PerformanceCreateRequest(
    performer_id=performer.id,
    event_id=event_one.id,
    performance_date=time.time(),
)

performance_one = performances_mid.performance_create(
    request=performance_create_request
).performance

performance_two_create_request = PerformanceCreateRequest(
    performer_id=performer.id,
    event_id=event_two.id,
    performance_date=time.time() + 200000,
)

performance_two = performances_mid.performance_create(
    request=performance_two_create_request
).performance

performance_three_create_request = PerformanceCreateRequest(
    performer_id=performer.id,
    event_id=event_one.id,
    performance_date=time.time() + 400000,
)

performance_three = performances_mid.performance_create(
    request=performance_three_create_request
).performance


################### CREATE PERFORMANCE ATTENDANCES ####################

performance_attendance_two_create_request = PerformanceAttendanceCreateRequest(
    performance_id=performance_two.id,
    attendee_id=user_one.id,
)

performance_attendance_two = performance_attendances_mid.performance_attendance_create(
    request=performance_attendance_two_create_request
).performance_attendance


################### CREATE TAGS for the performances ####################

tag_create_request = TagCreateRequest(
    tagged_entity_id=performance_one.id,
    tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
    tagged_in_entity_id=post_one.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_two.id,
)

tag = tags_mid.tag_create(tag_create_request)

tag_two_create_request = TagCreateRequest(
    tagged_entity_id=performance_one.id,
    tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
    tagged_in_entity_id=post_two.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_two.id,
)

tag = tags_mid.tag_create(tag_two_create_request)

################### CREATE FEATURES for the performances ####################
feature_create_request = FeatureCreateRequest(
    featured_entity_id=post_one.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=performer.id,
    featurer_type=FeaturerType.PERFORMER.value,
    creator_id=user_two.id,
)

feature = features_mid.feature_create(feature_create_request).feature

feature_two_create_request = FeatureCreateRequest(
    featured_entity_id=post_two.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=performer.id,
    featurer_type=FeaturerType.PERFORMER.value,
    creator_id=user_two.id,
)

feature_two = features_mid.feature_create(feature_two_create_request).feature

feature_three_create_request = FeatureCreateRequest(
    featured_entity_id=post_three.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=performer.id,
    featurer_type=FeaturerType.PERFORMER.value,
    creator_id=user_two.id,
)


feature_three = features_mid.feature_create(feature_three_create_request).feature

feature_create_request = FeatureCreateRequest(
    featured_entity_id=post_one.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=user_two.id,
    featurer_type=FeaturerType.USER.value,
    creator_id=user_two.id,
)

feature = features_mid.feature_create(feature_create_request).feature


################### create some user TAGS for posts so we cna view them from the Manage pages ####################

tag_create_request = TagCreateRequest(
    tagged_entity_id=performer.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=post_one.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id
)

tag = tags_mid.tag_create(tag_create_request)

tag_create_request = TagCreateRequest(
    tagged_entity_id=performer.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=post_two.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id
)

tag = tags_mid.tag_create(tag_create_request)

