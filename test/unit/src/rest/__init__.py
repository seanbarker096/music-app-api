import os
from configparser import ConfigParser
from test.unit import TestCase
from unittest.mock import Mock

import flask

from api.application import FlaskApp
from api.rest import auth_api, file_service_api, posts_api
from api.server import after_request_setup


class APITestCase(TestCase):
    def setUp(self):
        ## TODO: This is used in server.py too so move to a create_app func or something
        config = ConfigParser(allow_no_value=True, interpolation=None)
        config.optionxform = str

        env = os.environ.get("ENVIRONMENT", "dev")
        filename = os.path.join(
            flask.helpers.get_root_path(__name__), "../../api/config", f"{env}.cfg"
        )

        config.read(filename)

        mock_conns = Mock()
        app = FlaskApp(config=config, conns=mock_conns)

        ## Dont bother with full url for testing
        app.register_blueprint(self.BLUEPRINT)

        @app.after_request
        def after_request(response):
            after_request_setup(response)
            return response

        self.app = app

        self.test_client = self.app.test_client()

        super().setUp()


class FileServiceAPITestCase(APITestCase):
    BLUEPRINT = file_service_api.blueprint

    def setUp(self):
        super().setUp()


class PostAPITestCase(APITestCase):
    BLUEPRINT = posts_api.blueprint

    def setUp(self):
        super().setUp()


class AuthAPITestCase(APITestCase):
    BLUEPRINT = auth_api.blueprint

    def setUp(self):
        super().setUp()
