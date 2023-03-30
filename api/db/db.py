import json
import traceback
from typing import Any, Dict

import pymysql.cursors
import pymysql.err
from mysql.connector import MySQLConnection

from api.db.config import DBConfig
from exceptions.db.exceptions import DBDuplicateKeyException

## TODO: Make agnostic of the platform hosting our DB
## TODO: Make this a singleton class as don't want multiple connections all over the place


class DBResult(object):
    _cursor: pymysql.cursors.DictCursor = ...

    def __init__(self, cursor: pymysql.cursors.DictCursor):
        self._cursor = cursor

    def get_last_row_id(self):
        return self._cursor.lastrowid

    def get_rows(self) -> tuple[dict[str, Any], ...]:
        return self._cursor.fetchall()

    def affected_rows(self) -> int:
        """Number of affected rows (or selected rows for SELECT statements)"""
        return self._cursor.rowcount


class DB:
    def __init__(self, config: Dict[str, str]):
        self.connection = None

        db_config = config["config_file"]["db"]

        if (
            db_config
            and db_config["host"]
            and db_config["user"]
            and db_config["password"]
            and db_config["database"]
            and db_config["port"]
        ):
            self.config = DBConfig(
                db_config["host"],
                db_config["user"],
                db_config["password"],
                db_config["database"],
                db_config["port"],
            )
        else:
            raise Exception("Failed to instantiate DB class. Invalid configuration supplied")

        self.connection = pymysql.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            port=int(self.config.port),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True, # TODO: Can disable this for readonly transactions
        )

    def run_query(self, sql, binds) -> DBResult:
        ## TODO: validate sql and binds
        ## TODO: Check connection exists

        ## TODO: What if connection fails? Shoulld i return None, throw error??

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, binds)
            return DBResult(cursor=cursor)
        except pymysql.err.IntegrityError as e:
            print(e)
            raise DBDuplicateKeyException(e.args[1])
        



class DBConnection(MySQLConnection):
    _cursor: pymysql.cursors.DictCursor = ...
    _new_conn_per_request: bool = ...
    config: Dict[str, Any] = ...
    opened: bool = ...

    def __init__(self, config: Dict[str, str], new_conn_per_request: bool = True):
        self.config = config
        self._new_conn_per_request = new_conn_per_request
        self.opened = False

        if not self.new_conn_per_request:
            self._open()
        else:
            self._connection = None
            self._cursor = None

    def __enter__(self):
        # Open the connection. We don't handle on transient connections here as they shouldn't use the context manager
        if self.new_conn_per_request and not self.opened:
            self._open()
        
        self._cursor = self.cursor()
        return self._cursor


    def __exit__(self, exception, exception_message, trace):
        if exception and self.autocommit is False:
            self.rollback()

        else:
            self.commit()

        # we always close the cursor on exit because we always initialise a new one on enter
        self._cursor.close()
        self._cursor = None

        if self.new_conn_per_request and self.opened:
            self._close()


    def _open(self):
        if not self.opened:
            MySQLConnection.__init__(self, host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            port=int(self.config.port),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            )
            self.opened = True

    def _close(self):
        super().close()
        self.opened = False
        