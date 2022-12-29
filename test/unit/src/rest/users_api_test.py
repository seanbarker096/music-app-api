## Setup patches before the test case is initialised, which results in the blueprint file being called and defines functions before they can be patched
from test.test_utils import set_up_patches
from test.unit.src.rest.base import APITestCase
from unittest.mock import Mock

from api.typings.users import User, UserUpdateRequest, UserUpdateResult

set_up_patches()

from api.rest import users_api


## Ideally we'd put these in base.py, however it results in early imports of certain files which prevent patching certain functions such as @auth
class UsersAPITestCase(APITestCase):
    BLUEPRINT = users_api.blueprint

    def setUp(self):
        self.test_user = User(
            id=4444,
            first_name="Bukayo",
            second_name="Saka",
            username="Saka7",
            create_time=5555,
            is_deleted=False,
            email="saka7@gmail.com",
            avatar_file_uuid=None,
            last_login_date=None,
            language_id=None,
            timezone_id=None,
        )
        super().setUp()


class UsersApiTest(UsersAPITestCase):
    def user_update(self):
        ...
        # request = UserUpdateRequest(user_id=self.test_user.id, avatar_file_uuid=1234)

        # expected_response = UserUpdateResult(user=self.test_user)

        # self.app.conns.midlayer = Mock()
        # self.app.conns.midlayer.user_update = Mock(return_value=expected_response)
