import os
from configparser import ConfigParser
from test.unit import TestCase
from unittest.mock import Mock

import flask
from api.application import FlaskApp
from api.rest import file_service_api


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
        self.app = FlaskApp(config=config, conns=mock_conns)

        ## Dont bother with full url for testing
        self.app.register_blueprint(self.BLUEPRINT)
        self.test_client = self.app.test_client()

        super().setUp()


class FileServiceAPITestCase(APITestCase):
    BLUEPRINT = file_service_api.blueprint

    def setUp(self):
        super().setUp()
