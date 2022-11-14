import json
import traceback
from typing import Any, Dict

import pymysql.cursors
import pymysql.err

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
            autocommit=True,
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
