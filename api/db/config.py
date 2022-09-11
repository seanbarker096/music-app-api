class DBConfig:
    host: str = None
    user: str = None
    password: str = None
    database: str = None

    def __init__(self, host: str, user: str, password: str, database: str):
        ...


class DBConfigIntegrationTest(DBConfig):

    def __init__(self, host: str, user: str, password: str, database: str):
        super().__init__(host, user, password, database)

