import json
import traceback
from typing import Any, Dict

import pymysql
from mysql.connector import IntegrityError, MySQLConnection
from mysql.connector.cursor import MySQLCursor

from api.db.config import DBConfig
from exceptions.db.exceptions import DBDuplicateKeyException


class DBConnection:
    _cursor: MySQLCursor | None = ...
    _new_conn_per_request: bool = ...
    app_config: Dict[str, Any] = ...
    opened: bool = ...
    connection: pymysql.connections.Connection = ...

    def __init__(self, config: Dict[str, str], new_conn_per_request: bool = True):
        app_db_config = config["config_file"]["db"]

        if (
            app_db_config
            and app_db_config["host"]
            and app_db_config["user"]
            and app_db_config["password"]
            and app_db_config["database"]
            and app_db_config["port"]
        ):
            self.app_config = DBConfig(
                app_db_config["host"],
                app_db_config["user"],
                app_db_config["password"],
                app_db_config["database"],
                app_db_config["port"],
            )
        else:
            raise Exception("Failed to instantiate DB class. Invalid configuration supplied")

        self._new_conn_per_request = new_conn_per_request
        self.opened = False
        self.connection = None

        if not self._new_conn_per_request:
            self._open()
            self._cursor = self.connection.cursor()

    def __enter__(self):
        # Open the connection. We don't handle on transient connections here as they shouldn't use the context manager
        if self._new_conn_per_request and not self.opened:
            self._open()

        self._cursor = self.connection.cursor()
        return self._cursor

    def __exit__(self, exception_type, exception_value, trace):
        if exception_type is not None:
            if self.connection.autocommit is False:
                self.connection.rollback()
        else:
            self.connection.commit()

        # we always close the cursor on exit because we always initialise a new one on enter
        self._cursor.close()
        self._cursor = None

        if self._new_conn_per_request and self.opened:
            self._close()

        if exception_type is not None:
            if isinstance(exception_value, pymysql.err.IntegrityError):
                raise DBDuplicateKeyException(exception_value.args[1]) from exception_value

            raise exception_value

    def _open(self):
        if not self.opened:
            self.connection = pymysql.connect(
                host=self.app_config.host,
                user=self.app_config.user,
                password=self.app_config.password,
                database=self.app_config.database,
                port=int(self.app_config.port),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,  # TODO: Can disable this for readonly transactions
            )
            self.opened = True

    def _close(self):
        self.connection.close()
        self.opened = False
