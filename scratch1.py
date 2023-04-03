
import configparser
import os
import random

from scratch2 import Singleton


class DBConnection(Singleton):

    def __init__(self, *args, **kwargs):
        # Call parent to ensure MyClass only being instantiated from inside Singleton
        create_key = kwargs.pop('create_key', None)
        super().__init__(create_key)

        config = {}
        new_conn_per_request = kwargs.pop('new_conn_per_request', True)

        # Do other stuff
        app_db_config = kwargs.pop('config')
        self.rand = random.randint(0, 1000)
      
        if (
            app_db_config
            and app_db_config["host"]
            and app_db_config["user"]
            and app_db_config["password"]
            and app_db_config["database"]
            and app_db_config["port"]
        ):
            self.x = 'yay'
        else:
            raise Exception("Failed to instantiate DB class. Invalid configuration supplied")

        self._new_conn_per_request = new_conn_per_request
        self.opened = False
        self.connection = None





x = DBConnection.instance(DBConnection,config={'host': 1, 'user': 2, 'password': 3, 'database': 4, 'port': 5})

print(x.rand)

y = DBConnection.instance(DBConnection)
print(y.rand)