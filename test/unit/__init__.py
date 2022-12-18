import os
import unittest
from configparser import ConfigParser
from unittest.mock import Mock, patch

import flask

from api.application import FlaskApp
from api.rest import file_service_api


class TestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser(allow_no_value=True, interpolation=None)
        config.optionxform = str

        # We load the config here so its available to all test case classes
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../../api/config/dev.cfg"
        )

        config.read(filename)

        self.config = {}
        self.config["config_file"] = config

    @classmethod
    def tearDownAfterClass(cls):
        ## Remove any patches which might be specific to a given test case/file
        patch.stopall()
