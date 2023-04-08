import os
import time
import unittest
import uuid
from configparser import ConfigParser
from test.integration.src.fixtures.fixture_factory import FixtureFactory

from api.db.db import DBConnectionManager, TestingDBConnectionManager


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        config = ConfigParser(allow_no_value=True, interpolation=None)
        config.optionxform = str

        ## TODO:: Just updated the config object here locally like we do in IntegrationTestCase file

        # We load the config here so its available to all test case classes
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../../api/config/dev.cfg"
        )

        config.read(filename)

        self.config = {}
        self.config["config_file"] = config


        self.db =TestingDBConnectionManager
       
        ## Allows us to access the actual time in tests when we mock time.time()
        self.current_time = int(time.time())

        self.fixture_factory = FixtureFactory(config=self.config, db=self.db)

        ## We use addCleanup instead of tearDown because teardown does not get called if a test or setup fails
        self.addCleanup(self.truncate_db)

        # Once test case complete, close the db connection
        IntegrationTestCase.addClassCleanup(lambda : self.db.close(connection_uuid='id-for-testing'))
        

    def truncate_db(self):
        with self.db(self.config) as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                tables_list = [table for table_dict in tables for table in table_dict.values()]
                for table in tables_list:
                    cursor.execute(f"TRUNCATE {table}")


