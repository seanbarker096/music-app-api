import os
import unittest
from configparser import ConfigParser

from api.db.db import DB


class IntegrationTestAPI(unittest.TestCase):
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
        self.db = DB(self.config)

    def tearDown(self):
        self.truncate_db()

    def truncate_db(self):
        with self.db.connection:
            with self.db.connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                tables_list = [table for table_dict in tables for table in table_dict.values()]
                for table in tables_list:
                    cursor.execute(f"TRUNCATE {table}")
