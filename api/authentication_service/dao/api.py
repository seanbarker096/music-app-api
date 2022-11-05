import json

from api.authentication_service.typings import TokenCreateRequest
from api.db.db import DB


class AuthTokenServiceDAO:
    def __init__(self, config):
        self.db = DB(config)

    def token_create(self, request: TokenCreateRequest) -> int:
        if not isinstance(request.owner_id, int):
            raise Exception("Failed to create token. Owner id must be of type int")

        if not isinstance(request.token, str) or len(request.token) == 0:
            raise Exception("Failed to create token. Token must be a valid string")

        sql = """
            INSERT INTO auth_tokens(token, owner_id) VALUES (%s, %s)
        """

        binds = (request.token, request.owner_id)

        result = self.db.run_query(sql, binds)

        return result.get_last_row_id()

    def get_token_by_user_id(self, user_id: int) -> str:

        if not isinstance(user_id, int):
            raise Exception(f"Failed to get auth token. Invalid value {user_id} for field user_id.")

        sql = """
            SELECT id, token, owner_id FROM auth_tokens 
                WHERE owner_id = %s
        """

        binds = (user_id,)

        result = self.db.run_query(sql, binds)

        rows = result.get_rows()

        print(json.dumps(rows))

        if not rows or len(rows) == 0:
            raise Exception(f"Failed to find token for user with id {user_id}")

        if len(rows) > 1:
            raise Exception(f"More than one token found for user with id {user_id}")

        encoded_token = rows[0]["token"]

        if not isinstance(encoded_token, str) or len(encoded_token) == 0:
            raise Exception(f"Invalid token returned for user with id {user_id}")

        return encoded_token
