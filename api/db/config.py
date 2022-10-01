class DBConfig:
    host: str = None
    user: str = None
    password: str = None
    database: str = None
    port: int = None

    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        self.host = host
        self.user =  user
        self.password = password
        self.database = database
        self.port = port


class DBConfigIntegrationTest(DBConfig):

    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        super().__init__(host, user, password, database, port)

