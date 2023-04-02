import json

from api.authentication_service.typings import TokenCreateRequest
from api.db.db import DBConnection


class AuthTokenServiceDAO:
    def __init__(self, config):
        self.db = DBConnection(config)

    def token_create(self, request: TokenCreateRequest) -> int:
        if not isinstance(request.owner_id, int):
            raise Exception("Failed to create token. Owner id must be of type int")

        if not isinstance(request.token, str) or len(request.token) == 0:
            raise Exception("Failed to create token. Token must be a valid string")

        sql = """
            INSERT INTO auth_tokens(token, owner_id, session_id) VALUES (%s, %s, %s)
        """

        binds = (request.token, request.owner_id, request.session_id)

        with self.db as cursor:
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

        with self.db as cursor:
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

    def token_delete(self, token: str) -> int:
        sql = f"""
            DELETE FROM auth_tokens WHERE token = %s
        """
        binds = (token,)
        row_count = None

        with self.db as cursor:
            cursor.execute(sql, binds)

            row_count = cursor.rowcount

        if row_count == 0:
            raise Exception(f"Failed to remove token {token} from the database")

        if row_count > 1:
            ## TODO: Log warning here as token should be unique
            ...

        return row_count
