import json
import logging
from typing import Optional

from api.authentication_service.typings import (
    AuthStateDeleteRequest,
    TokenCreateRequest,
)
from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import build_where_query_string


class AuthTokenServiceDAO:
    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def token_create(self, request: TokenCreateRequest) -> int:
        if not isinstance(request.owner_id, int):
            raise Exception("Failed to create token. Owner id must be of type int")

        if not isinstance(request.token, str) or len(request.token) == 0:
            raise Exception("Failed to create token. Token must be a valid string")

        sql = """
            INSERT INTO auth_tokens(token, owner_id, session_id) VALUES (%s, %s, %s)
        """

        binds = (request.token, request.owner_id, request.session_id)

        with self.db(self.config) as cursor:
            result = cursor.execute(sql, binds)

            return cursor.lastrowid

    def get_token_by_user_id_and_session_id(self, user_id: int, session_id: str) -> str:

        if not isinstance(user_id, int):
            raise Exception(f"Failed to get auth token. Invalid value {user_id} for field user_id.")

        if not isinstance(session_id, str) or len(session_id) == 0:
            raise Exception(
                f"Failed to get auth token. Invalid value {session_id} for field session_id."
            )

        sql = """
            SELECT id, token, owner_id, session_id FROM auth_tokens 
                WHERE owner_id = %s and session_id = %s
        """

        binds = (user_id, session_id)
        rows = None

        with self.db(self.config) as cursor:
            result = cursor.execute(sql, binds)

            rows = cursor.fetchall()

        if not rows or len(rows) == 0:
            raise Exception(
                f"Failed to find token for user with id {user_id} and session_id {session_id}"
            )

        if len(rows) > 1:
            raise Exception(
                f"More than one token found for user with id {user_id} and session_id {session_id}"
            )

        encoded_token = rows[0]["token"]

        if not isinstance(encoded_token, str) or len(encoded_token) == 0:
            raise Exception(
                f"Invalid token returned for user with id {user_id} and session_id {session_id}"
            )

        return encoded_token

    def token_delete(self, request: AuthStateDeleteRequest) -> int:
        delete = f"""
            DELETE FROM auth_tokens
        """

        wheres = []
        binds = []

        if request.refresh_token:
            wheres.append("token = %s")
            binds.append(request.refresh_token)
        
        if request.session_id:
            wheres.append("session_id = %s")
            binds.append(request.session_id)

        if request.owner_id:
            wheres.append("owner_id = %s")
            binds.append(request.owner_id)

        where_string = build_where_query_string(wheres, 'AND') 

        sql = f"{delete} {where_string}"

        row_count = None

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)

            row_count = cursor.rowcount

        if row_count == 0:
            logging.info(f"Failed to remove token from the database. Request: {json.dumps(vars(request))}")

        if row_count > 1 and (request.refresh_token or (request.session_id and request.owner_id)):
            logging.info(f"More than one token removed from the database. Request: {json.dumps(vars(request))}")

        return row_count
