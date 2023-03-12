import os
from configparser import ConfigParser

from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.dao.users_dao import UsersDAO
from api.file_service.api import FileService
from api.file_service.typings.typings import FileCreateRequest
from api.midlayer.artists_mid import ArtistsMidlayerMixin
from api.midlayer.features_mid import FeaturesMidlayerMixin
from api.midlayer.tags_mid import TagsMidlayerMixin
from api.typings.artists import ArtistCreateRequest
from api.typings.features import FeatureCreateRequest, FeaturedEntityType, FeaturerType
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostCreateRequest,
    PostOwnerType,
)
from api.typings.tags import (
    TagCreateRequest,
    TagCreatorType,
    TaggedEntityType,
    TaggedInEntityType,
)
from api.typings.users import UserCreateRequest, UserUpdateRequest
from api.utils import hash_password

config = ConfigParser(allow_no_value=True, interpolation=None)
config.optionxform = str

env = os.environ.get("ENVIRONMENT", "dev")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../api/config/", f"{env}.cfg")
print(filename)

config.read(filename)

config_dict = {"config_file": config}

users_dao = UsersDAO(config_dict)

features_mid = FeaturesMidlayerMixin(config_dict)

posts_dao = PostsDAO(config_dict)
post_attachments_dao = PostAttachmentsDAO(config_dict)

aritsts_mid = ArtistsMidlayerMixin(config_dict)

file_service = FileService(config_dict)

tags_mid = TagsMidlayerMixin(config_dict)


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
    owner_id=user_one.id, owner_type=PostOwnerType.USER.value, content="This is a new post"
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=dog_video_file.id
)

# 2 Post uploaded by second user, and tags the first user
post_create_request = PostCreateRequest(
    owner_id=user_two.id,
    owner_type=PostOwnerType.USER.value,
    content="This is a post which user one will be tagged in",
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=dog_video_file.id
)

tag_create_request = TagCreateRequest(
    tagged_in_entity_id=post.id,
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
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=avatar_file.id
)

feature_create_request = FeatureCreateRequest(
    owner_id=user_one.id,
    owner_type=FeaturerType.USER.value,
    context_type=FeaturedEntityType.POST.value,
    context_id=post.id,
)

feature = features_mid.feature_create(feature_create_request).feature

# # 4
# post_create_request = PostCreateRequest(owner_id=user_one.id, content="This is a fourth post")

# post = posts_dao.post_create(post_create_request)

# post_attachment = post_attachments_dao.post_attachment_create(
#     post_id=post.id, file_id=avatar_file.id
# )


###################### CREATE ARTISTS ######################

artist_create_request = ArtistCreateRequest(
    name="Eminem",
    biography="I'm a rapper",
    uuid="7dGJo4pcD2V6oG8kP0tJRR",
    owner_id=user_two.id,
    image_url="https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b",
)

artist = aritsts_mid.artist_create(artist_create_request).artist


# Create a post for him

post_create_request = PostCreateRequest(
    owner_id=artist.id,
    owner_type=PostOwnerType.ARTIST.value,
    content="Eminems first post",
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=dog_video_file.id
)


################### CREATE FEATURES ####################
