import os
from configparser import ConfigParser
from test.unit import TestCase
from unittest.mock import Mock

import flask

from api.application import FlaskApp
from api.utils.rest_utils import after_request_setup


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
        app.testing = True

        ## Dont bother with full url for testing
        app.register_blueprint(self.BLUEPRINT)

        @app.after_request
        def after_request(response):
            after_request_setup(response)
            return response

        self.app = app

        self.test_client = self.app.test_client()

        self.app_context = self.app.app_context()

        super().setUp()
