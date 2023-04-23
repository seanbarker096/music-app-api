import logging
from random import randint
from typing import Any, Dict

import flask
import pymysql
from mysql.connector import errorcode
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
        print(f"created cinnection with id {self.connection_id}")

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

                self.opened = True

            except Exception as err:
                raise Exception(f"Failed to connect to database because {str(err)}") from err

    @staticmethod
    def close(instance_key: str):
        """
        Close the connection to the database and remove the singleton instance
        """

        conn_exists = DBConnection.has_instance(instance_key=instance_key)

        if conn_exists is False:
            raise Exception(
                f"Failed to close database connection for connection uuid {instance_key} because it could not be found"
            )

        connection = DBConnection.instance(DBConnection, instance_key=instance_key)

        try:
            print(f"Closing connection with id {connection.connection_id}")
            connection._cursor.close()
            connection.connection.close()
            DBConnection.remove_instance(instance_key=instance_key)

        except Exception as err:
            logging.exception(
                f"Failed to close connection with id {connection.connection_id} because {str(err)}"
            )

    def get_cursor(self):
        return self._cursor


# To enable multiple queries to be run in a single transcation, we can add an instance property which modifies the __exit__ behabiour, and that can be configred in certain places to not immediately rollback or commit on __exit__. We can then run multiple queries and multiple with statements in a single transaction.
class DBConnectionManager:
    """
    This class should not be used directly, but should be extended by a parent class which provides the connection uuids.

    @see FlaskDBConnectionManager, TestingDBConnectionManager
    """

    def __init__(self, config, connection_uuid: str):
        self.config = config
        self.connection_uuid = connection_uuid

    def __enter__(self):
        self.db_connection = DBConnection.instance(
            DBConnection, instance_key=self.connection_uuid, config=self.config
        )

        cursor = self.db_connection.get_cursor()

        if cursor is None:
            raise Exception(
                f"Failed to get cursor from DBConnection with connection id {self.db_connection.connection_id}"
            )

        return cursor

    def __exit__(self, exception_type, exception_value, trace):
        if exception_type is not None:
            if self.db_connection.connection.get_autocommit() is False:
                self.db_connection.connection.rollback()

            if (
                isinstance(exception_value, pymysql.err.IntegrityError)
                and exception_value.args[0] == errorcode.ER_DUP_ENTRY
            ):
                raise DBDuplicateKeyException(exception_value.args[1]) from exception_value

            raise exception_value

        elif self.db_connection.connection.get_autocommit() is False:
            self.db_connection.connection.commit()

    @staticmethod
    def close(connection_uuid: str):
        DBConnection.close(instance_key=connection_uuid)


class FlaskDBConnectionManager(DBConnectionManager):
    """
    A simple wrapper around DBConnection manager which uses flask request to create the connection uuid.
    """

    def __init__(self, config):
        connection_uuid = flask.request.request_id
        super().__init__(config, connection_uuid)

    @staticmethod
    def close():
        connection_uuid = flask.request.request_id
        super().close(connection_uuid)


class TestingDBConnectionManager(DBConnectionManager):
    """
    A simple wrapper around DBConnection. This is similar to FlaskDBConnectionManager but uses a static uuid for testing, rather than flask globals.
    """

    def __init__(self, config):
        connection_uuid = "id-for-testing"
        super().__init__(config, connection_uuid)

    @staticmethod
    def close():
        super().close("id-for-testing")
