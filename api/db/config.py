class DBConfig:
    host: str = None
    user: str = None
    password: str = None
    database: str = None

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user =  user
        self.password = password
        self.database = database


class DBConfigIntegrationTest(DBConfig):

    def __init__(self, host: str, user: str, password: str, database: str):
        super().__init__(host, user, password, database)

