import json
import logging
import traceback
from random import randint
from typing import Any, Dict

import pymysql
from mysql.connector import IntegrityError, MySQLConnection
from mysql.connector.cursor import MySQLCursor

from api.db.config import DBConfig
from api.utils.util_classes import Singleton
from exceptions.db.exceptions import DBDuplicateKeyException


class DBConnection(Singleton):
    _cursor: MySQLCursor | None = None
    _new_conn_per_request: bool = True
    _app_config: Dict[str, Any] = None
    opened: bool = False
    connection: pymysql.connections.Connection = None
    connection_id: int = None

    def __init__(self, *args, **kwargs):
        # Call parent to ensure MyClass only being instantiated from inside Singleton
        create_key = kwargs.pop("create_key", None)
        super().__init__(create_key)

        # Handle instantiation of this class
        config = kwargs.pop("config")
        app_db_config = config["config_file"]["db"]

        if (
            app_db_config
            and app_db_config["host"]
            and app_db_config["user"]
            and app_db_config["password"]
            and app_db_config["database"]
            and app_db_config["port"]
        ):
            self._app_config = DBConfig(
                app_db_config["host"],
                app_db_config["user"],
                app_db_config["password"],
                app_db_config["database"],
                app_db_config["port"],
            )
        else:
            raise Exception("Failed to instantiate DB class. Invalid configuration supplied")

        self._new_conn_per_request = kwargs.pop("new_conn_per_request", True)
        # if not self._new_conn_per_request:
        self._open()
        self._cursor = self.connection.cursor()
        self.connection_id = randint(0, 1000000)

    # def __enter__(self):
    #     # Open the connection. We don't handle on transient connections here as they shouldn't use the context manager

    #     try:
    #         if self._new_conn_per_request and not self.opened:
    #             self._open()

    #         self._cursor = self.connection.cursor()

    #     except Exception as err:
    #         raise Exception(f"Failed to open DB connection because {str(err)}") from err

          
    #     print(f"{self.connection_id} open")

    #     return self._cursor

    # def __exit__(self, exception_type, exception_value, trace):
    #     # if exception_type is not None:
    #     #     if self.connection.autocommit is False:
    #     #         self.connection.rollback()
    #     # else:
    #     #     self.connection.commit()

    #     # # we always close the cursor on exit because we always initialise a new one on enter
    #     # res = self._cursor.close()

    #     # if res is False:
    #     #     raise Exception(f"Failed to close cursor.")

    #     # self._cursor = None

    #     # if self._new_conn_per_request and self.opened:
    #     #     self._close()
    #     #     print(f"{self.connection_id} closed \n\n")

    #     if exception_type is not None:
    #         if isinstance(exception_value, pymysql.err.IntegrityError):
    #             raise DBDuplicateKeyException(exception_value.args[1]) from exception_value

    #         raise exception_value

    def _open(self):
        if not self.opened:
            try:
                self.connection = pymysql.connect(
                    host=self._app_config.host,
                    user=self._app_config.user,
                    password=self._app_config.password,
                    database=self._app_config.database,
                    port=int(self._app_config.port),
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,  # TODO: Can disable this for readonly transactions
                )
            except Exception as err:
                raise Exception(f"Failed to connect to database because {str(err)}") from err
            
            self.opened = True

    def close(self):
        try:
            self._cursor.close()
            self.connection.close()
            self.opened = False
            self.connection_id = None

        except Exception as err:
            logging.exception(f"Failed to close connection with id {self.connection_id} because {str(err)}")

    def get_cursor(self):
        return self._cursor


class DBConnectionManager:
    def __init__(self, config):
        self.config = config
        self.db_connection = None

    def __enter__(self):
        self.db_connection = DBConnection.instance(DBConnection, config=self.config)

        print("connection_id", self.db_connection.connection_id)

        cursor = self.db_connection.get_cursor()

        if cursor is None:
            raise Exception(f"Failed to get cursor from DBConnection with connection id {self.db_connection.connection_id}")
        
        return cursor

    def __exit__(self, exception_type, exception_value, trace):
        if exception_type is not None:
            if self.db_connection.connection.autocommit is False:
                self.db_connection.connection.rollback()

            if isinstance(exception_value, pymysql.err.IntegrityError):
                raise DBDuplicateKeyException(exception_value.args[1]) from exception_value

            raise exception_value
        elif self.db_connection.connection.autocommit is False:
            self.db_connection.connection.commit()
            
    def close(self):
        self.db_connection.close()
        self.db_connection = None
