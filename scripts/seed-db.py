import os
from configparser import ConfigParser

from api.dao.posts_dao import PostAttachmentsDAO, PostsDAO
from api.dao.users_dao import UsersDAO
from api.file_service.api import FileService
from api.file_service.typings.typings import FileCreateRequest
from api.midlayer.artists_mid import ArtistsMidlayerMixin
from api.midlayer.features_mid import FeaturesMidlayerMixin
from api.typings.artists import ArtistCreateRequest
from api.typings.features import FeatureCreateRequest
from api.typings.posts import (
    PostAttachmentsCreateRequest,
    PostCreateRequest,
    PostOwnerType,
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


## Create user
password_hash = hash_password("password")
request = UserCreateRequest(
    username="sean",
    first_name="Sean",
    second_name="Barker",
    email="seanbarker6@sky.com",
    password="password",
)

user = users_dao.user_create(request=request, password_hash=password_hash)


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
user_update_request = UserUpdateRequest(user.id, avatar_file_uuid=avatar_file_uuid)

users_dao.user_update(user_update_request)


################### CREATE POSTS ####################

# 1
post_create_request = PostCreateRequest(
    owner_id=user.id, owner_type=PostOwnerType.USER, content="This is a new post"
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=dog_video_file.id
)

# 2
post_create_request = PostCreateRequest(
    owner_id=user.id, owner_type=PostOwnerType.ARTIST, content="This is a second post"
)

post = posts_dao.post_create(post_create_request)

post_attachment = post_attachments_dao.post_attachment_create(
    post_id=post.id, file_id=dog_video_file.id
)

# # 3
# post_create_request = PostCreateRequest(owner_id=user.id, content="This is a thrid post")

# post = posts_dao.post_create(post_create_request)

# post_attachment = post_attachments_dao.post_attachment_create(
#     post_id=post.id, file_id=avatar_file.id
# )

# # 4
# post_create_request = PostCreateRequest(owner_id=user.id, content="This is a fourth post")

# post = posts_dao.post_create(post_create_request)

# post_attachment = post_attachments_dao.post_attachment_create(
#     post_id=post.id, file_id=avatar_file.id
# )


###################### CREATE ARTISTS ######################

artist_create_request = ArtistCreateRequest(
    name="Sean Barker",
    biography="I am a software developer",
    uuid="asdaskjflkhw",
    owner_id=user.id,
)

artist = aritsts_mid.artist_create(artist_create_request).artist


################### CREATE FEATURES ####################

feature_create_request = FeatureCreateRequest(
    owner_id=2, owner_type="artist", context_type="post", context_id=post.id
)

print("artist.id", artist.id)

feature = features_mid.feature_create(feature_create_request).feature
