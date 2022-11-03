from typings import TokenCreateRequest

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
            INSERT INTO tokens(encoded_token, owner_id) VALUES (%s, %s)
        """

        binds = (request.token, request.owner_id)

        result = self.db.run_query(sql, binds)

        return result.get_last_row_id()

    def get_token_by_user_id(self, user_id: int) -> str:
        ...
