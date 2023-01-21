import os
from configparser import ConfigParser

from api.dao.users_dao import UsersDAO
from api.file_service.api import FileService
from api.file_service.typings.typings import FileCreateRequest
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


# set it on the user
user_update_request = UserUpdateRequest(user.id, avatar_file_uuid=avatar_file_uuid)

users_dao.user_update(user_update_request)
