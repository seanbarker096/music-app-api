import os
import unittest
from configparser import ConfigParser

import flask
from api.application import FlaskApp


##
class IntegrationTestAPI(unittest.TestCase):
    def setUp(self):
        config = ConfigParser(allow_no_value=True, interpolation=None)
        config.optionxform = str

        filename = os.path.join(flask.helpers.get_root_path(__name__), 'dev.cfg')
        ## Get IPs from environment variables
        db_host = os.environ.get("CONTAINER_IP")

        config.read(filename)
        config['db']['host'] = db_host

        self.app = FlaskApp(config)
