import os
import random
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

config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../api/config/", f"{env}.cfg")

config.read(filename)

# If we are in aws we need to use the RDS environment variables
if 'RDS_HOSTNAME' in os.environ:
    config['db'] = {
        'user' : os.environ['RDS_USERNAME'], 
        'password' : os.environ['RDS_PASSWORD'],
        'database' : os.environ['RDS_DB_NAME'],
        'host' : os.environ['RDS_HOSTNAME'],
        'port' : os.environ['RDS_PORT'],
    }

config['aws'] = {
    'aws_access_key_id' : os.environ['aws_access_key_id'], 
    'aws_secret_access_key' : os.environ['aws_secret_access_key'],
    'region':  config.get("aws", "region")
}


config['performer-search-service'] = {
    'search-client': config.get("performer-search-service", "search-client"),
    'spotify-client-id' : os.environ['spotify_client_id'], 
    'spotity-client-secret' : os.environ['spotify_client_secret'],
}

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
    config=config_dict,
    conns=tags_mid_conns,
    tag_event_subject=tag_event_subject,
    performances_mid=performances_mid,
)

#### CREATE files ####

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show1.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show1",
        file_name="show1.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    show1_video = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show1-thumbnail.png"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show1thumbnail",
        file_name="show1-thumbnail.png",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="img/png",
        url=None,
    )
    show1_thumbnail = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show2.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show2",
        file_name="show2.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    show2_video = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show2-thumbnail.png"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show2thumbnail",
        file_name="show2-thumbnail.png",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="img/png",
        url=None,
    )
    show2_thumbnail = file_service.create_file(request).file


with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show3.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show3",
        file_name="show3.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    show3_video = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show3-thumbnail.png"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show3thumbnail",
        file_name="show3-thumbnail.png",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="img/png",
        url=None,
    )
    show3_thumbnail = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show4.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show4",
        file_name="show4.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    show4_video = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show4-thumbnail.png"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show4thumbnail",
        file_name="show4-thumbnail.png",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="img/png",
        url=None,
    )
    show4_thumbnail = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show5.mp4"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show5",
        file_name="show5.mp4",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="video/mp4",
        url=None,
    )
    show5_video = file_service.create_file(request).file

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "show5-thumbnail.png"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="show5thumbnail",
        file_name="show5-thumbnail.png",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="img/png",
        url=None,
    )
    show5_thumbnail = file_service.create_file(request).file


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

event_create_request = EventCreateRequest(
    venue_name="Primavera Sound",
    event_type=EventType.MUSIC_FESTIVAL.value,
    start_date=1681531032 + 200000,
    end_date=1681531032 + 300000,
)

prima = events_mid.event_create(event_create_request).event

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

update_request = UserUpdateRequest(
    user_id=user_one.id,
    bio="I love music and live in London",
)

users_dao.user_update(request=update_request)



# set it on the user
user_update_request = UserUpdateRequest(user_one.id, avatar_file_uuid=avatar_file_uuid)

users_dao.user_update(user_update_request)


request = UserCreateRequest(
    username="gregory",
    first_name="Greg",
    second_name="Baxter",
    email="gg_no_re@sky.com",
    password="password",
)

user_two = users_dao.user_create(request=request, password_hash=password_hash)


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

update_request = UserUpdateRequest(
    user_id=user_two.id,
    bio="Mi nem Geoff. Mi like watching people play music and venues and shit",
)

users_dao.user_update(request=update_request)


password_hash = hash_password("password")
request = UserCreateRequest(
    username="seanborker",
    first_name="Sean",
    second_name="Borker",
    email="seanborker@sky.com",
    password="password",
)

user_three = users_dao.user_create(request=request, password_hash=password_hash)

update_request = UserUpdateRequest(
    user_id=user_three.id,
    bio="Reeeeeeeeeeee. Im 28 years old and moved to London 2 years ago. I love music and live in London",
)

users_dao.user_update(request=update_request)

# set it on the user


with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "avatar2.jpg"), "rb"
) as file_bytes_buffer_reader:
    request = FileCreateRequest(
        uuid="aaaaaaaaaaaaaaa",
        file_name="profile-pic2.jpg",
        bytes=file_bytes_buffer_reader.read(),
        mime_type="image/jpeg",
        url=None,
    )
    avatar_file = file_service.create_file(request).file


user_update_request = UserUpdateRequest(user_three.id, avatar_file_uuid=avatar_file_uuid)

users_dao.user_update(user_update_request)


################### CREATE POSTS with no tags or features ####################

# 1 - Post uploaded by the user we created
post_create_request = PostCreateRequest(
    owner_id=user_one.id,
    owner_type=PostOwnerType.USER.value,
    content="What a great day at Glastonbury!",
    creator_id=user_one.id,
)

post_one = posts_dao.post_create(post_create_request)


post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post_one.id, attachment_file_id=show1_video.id, attachment_thumbnail_file_id=show1_thumbnail.id
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
    post_id=post_two.id, attachment_file_id=show2_video.id, attachment_thumbnail_file_id=show2_thumbnail.id
)

###################### PERFORMER ONE ######################

performer_create_request = PerformerCreateRequest(
    name="Taylor Swift",
    uuid="06HL4z0CvFAxyc27GXpf02",
    owner_id=user_two.id,
    image_url="https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0",
    biography='Taylor Alison Swift is an American singer-songwriter. Her narrative songwriting, which often centers around her personal life, has received widespread critical plaudits and media coverage.',
)

taylor_swift = performers_mid.performer_create(performer_create_request).performer


# Create a performance created by them

performance_create_request = PerformanceCreateRequest(
    performer_id=taylor_swift.id,
    event_id=event_one.id,
    performance_date=time.time(),
)

taylor_performance = performances_mid.performance_create(
    request=performance_create_request
).performance


# 1 - Post uploaded by the user we created
post_create_request = PostCreateRequest(
    owner_id=user_one.id,
    owner_type=PostOwnerType.USER.value,
    content="Taylor swifts show was good!",
    creator_id=user_one.id,
)

taylor_post = posts_dao.post_create(post_create_request)


post_attachment = post_attachments_dao.post_attachment_create(
    post_id=taylor_post.id, attachment_file_id=show3_video.id, attachment_thumbnail_file_id=show3_thumbnail.id
)


# Also tag their performance in a post. This will mark them as having attended too
tag_create_request = TagCreateRequest(
    tagged_entity_id=taylor_performance.id,
    tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
    tagged_in_entity_id=taylor_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

talyor_performance_post_tag = tags_mid.tag_create(tag_create_request)

tag_create_request = TagCreateRequest(
    tagged_entity_id=taylor_swift.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=taylor_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

taylor_post_tag = tags_mid.tag_create(tag_create_request)


# Create a feature for a post they are tagged in

feature_create_request = FeatureCreateRequest(
    featured_entity_id=taylor_post.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=taylor_swift.id,
    featurer_type=FeaturerType.PERFORMER.value,
    creator_id=user_two.id,
)

feature = features_mid.feature_create(feature_create_request).feature


# Create another post, performance tag and performanc attendance

performance_create_request = PerformanceCreateRequest(
    performer_id=taylor_swift.id,
    event_id=prima.id,
    performance_date=time.time(),
)

prima_performance = performances_mid.performance_create(
    request=performance_create_request
).performance

print("prima_performance id", prima_performance.id)

post_create_request = PostCreateRequest(
    owner_id=user_three.id,
    owner_type=PostOwnerType.USER.value,
    content="Taylor swifts show at prima was sick!",
    creator_id=user_one.id,
)

taylor_prima_post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=taylor_prima_post.id, attachment_file_id=show5_video.id, attachment_thumbnail_file_id=show5_thumbnail.id
)


# Also tag their performance in a post
tag_create_request = TagCreateRequest(
    tagged_entity_id=prima_performance.id,
    tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
    tagged_in_entity_id=taylor_prima_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

talyor_prima_performance_post_tag = tags_mid.tag_create(tag_create_request)

tag_create_request = TagCreateRequest(
    tagged_entity_id=taylor_swift.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=taylor_prima_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

taylor_prima_post_tag = tags_mid.tag_create(tag_create_request)

# Create one final post not linked to a performance

post_create_request = PostCreateRequest(
    owner_id=user_three.id,
    owner_type=PostOwnerType.USER.value,
    content="Cool show mite",
    creator_id=user_one.id,
)

taylor_not_linked_to_performance_post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=taylor_not_linked_to_performance_post.id, attachment_file_id=show1_video.id, attachment_thumbnail_file_id=show1_thumbnail.id
)

tag_create_request = TagCreateRequest(
    tagged_entity_id=taylor_swift.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=taylor_not_linked_to_performance_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

taylor_prima_post_tag = tags_mid.tag_create(tag_create_request)


###################### PERFORMER TWO ######################

# Eminem can have no performances, and only posts

performer_create_request = PerformerCreateRequest(
    name="Eminem",
    uuid="7dGJo4pcD2V6oG8kP0tJRR",
    owner_id=user_one.id,
    image_url="https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b",
    biography="Eminem is an American rapper, songwriter, record producer, record executive, and actor. He is consistently cited as one of the greatest and most influential rappers of all time and was labeled the King of Hip Hop by Rolling Stone magazine.",
)

eminem = performers_mid.performer_create(performer_create_request).performer

# 1 - Post uploaded by the user we created
post_create_request = PostCreateRequest(
    owner_id=user_three.id,
    owner_type=PostOwnerType.USER.value,
    content="Eminems show was good!",
    creator_id=user_three.id,
)

em_post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=em_post.id, attachment_file_id=show1_video.id, attachment_thumbnail_file_id=show1_thumbnail.id
)


# Also tag their performance in a post
tag_create_request = TagCreateRequest(
    tagged_entity_id=eminem.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=em_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_three.id,
)

performance_post_tag = tags_mid.tag_create(tag_create_request)




################### CREATE MORE PERFORMANCES for taylor that wont have any posts ####################


performance_two_create_request = PerformanceCreateRequest(
    performer_id=taylor_swift.id,
    event_id=event_two.id,
    performance_date=time.time() + 200000,
)

performance_two = performances_mid.performance_create(
    request=performance_two_create_request
).performance

performance_three_create_request = PerformanceCreateRequest(
    performer_id=taylor_swift.id,
    event_id=event_one.id,
    performance_date=time.time() + 400000,
)

performance_three = performances_mid.performance_create(
    request=performance_three_create_request
).performance

performance_four_create_request = PerformanceCreateRequest(
    performer_id=taylor_swift.id,
    event_id=event_two.id,
    performance_date=time.time() + 400000,
)

performance_four = performances_mid.performance_create(
    request=performance_four_create_request
).performance


###################### PERFORMER FOUR ####################

performer_create_request = PerformerCreateRequest(
    name="Kendrick Lamar",
    uuid="2YZyLoL8N0Wb9xBt1NhZWg",
    owner_id=5677,
    image_url="https://i.scdn.co/image/ab6761610000f178437b9e2a82505b3d93ff1022",
    biography="Kendrick Lamar Duckworth is an American rapper, songwriter, and record producer. Since his debut into the mainstream with Good Kid, M.A.A.D City, Lamar has been regarded as one of the most influential artists of his generation, as well as one of the greatest rappers and lyricists of all time.",
)

kendrick = performers_mid.performer_create(performer_create_request).performer

kendrick_perf_create_request = PerformanceCreateRequest(
    performer_id=kendrick.id,
    event_id=event_two.id,
    performance_date=time.time() + 700000,
)

kendrick_per = performances_mid.performance_create(request=kendrick_perf_create_request).performance

post_create_request = PostCreateRequest(
    owner_id=user_one.id,
    owner_type=PostOwnerType.USER.value,
    content="Kendrick at o2",
    creator_id=user_one.id,
)

kendrick_post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=kendrick_post.id, attachment_file_id=dog_video_file.id, attachment_thumbnail_file_id=avatar_file.id
)

tag_create_request = TagCreateRequest(
    tagged_entity_id=kendrick.id,
    tagged_entity_type=TaggedEntityType.PERFORMER.value,
    tagged_in_entity_id=kendrick_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

kendrick_post_tag = tags_mid.tag_create(tag_create_request)

tag_create_request = TagCreateRequest(
    tagged_entity_id=kendrick_per.id,
    tagged_entity_type=TaggedEntityType.PERFORMANCE.value,
    tagged_in_entity_id=kendrick_post.id,
    tagged_in_entity_type=TaggedInEntityType.POST.value,
    creator_id=user_one.id,
)

kendrick_performance_post_tag = tags_mid.tag_create(tag_create_request)


# Create some extra posts for view more testing
i = 0

while i < 27:
    post_create_request = PostCreateRequest(
        creator_id=user_one.id,
        content=f"Post {i}",
        owner_id=user_one.id,
        owner_type=PostOwnerType.USER.value,
    )
    post = posts_mid.post_create(post_create_request).post

    x = random.randint(1, 5)

    if x == 1:
        video_id = show1_video.id
        thumbnail_id = show1_thumbnail.id
    elif x == 2:
        video_id = show2_video.id
        thumbnail_id = show2_thumbnail.id
    elif x == 3:
        video_id = show3_video.id
        thumbnail_id = show3_thumbnail.id
    elif x == 4:
        video_id = show4_video.id
        thumbnail_id = show4_thumbnail.id
    elif x == 5:
        video_id = show5_video.id
        thumbnail_id = show5_thumbnail.id

    post_attachment = post_attachments_dao.post_attachment_create(post_id=post.id, attachment_file_id=video_id, attachment_thumbnail_file_id=thumbnail_id)

    i += 1

# Create user who has done nothing

password_hash = hash_password("password")
request = UserCreateRequest(
    username="newuser",
    first_name="Geoff",
    second_name="Mi Name",
    email="newuser@sky.com",
    password="password",
)

users_dao.user_create(request=request, password_hash=password_hash)


# Create a feature for a post they are tagged in

feature_create_request = FeatureCreateRequest(
    featured_entity_id=taylor_prima_post.id,
    featured_entity_type=FeaturedEntityType.POST.value,
    featurer_id=taylor_swift.id,
    featurer_type=FeaturerType.PERFORMER.value,
    creator_id=user_two.id,
)

feature = features_mid.feature_create(feature_create_request).feature


i = 0

while i < 40:
    password_hash = hash_password("password")
    request = UserCreateRequest(
        username=f"user{i}",
        first_name=f"User {i}",
        second_name=f"Second name is {i}",
        email=f"user{i}@gmail.com",
        password="password",
    )

    users_dao.user_create(request=request, password_hash=password_hash)

    i += 1


    # Create user and performer for testing empty states

password_hash = hash_password("password")

request = UserCreateRequest(
        username=f"emptystateuser",
        first_name=f"Empty",
        second_name=f"State",
        email=f"emptystateuser@gmail.com",
        password="password",
    )

empty_state_user = users_dao.user_create(request=request, password_hash=password_hash)


performer_create_request = PerformerCreateRequest(
    name="J cole",
    uuid="6l3HvQ5sa6mXTsMTB19rO5",
    owner_id=empty_state_user.id,
    image_url="https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0",
    biography="Jermaine Lamarr Cole, known professionally as J. Cole, is an American rapper, singer, songwriter, record producer, and record executive. Born on a military base in Germany and raised in Fayetteville, North Carolina, Cole initially gained recognition as a rapper following the release of his debut mixtape, The Come Up, in early 2007.",
)

jcole = performers_mid.performer_create(performer_create_request).performer

