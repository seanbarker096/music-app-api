from typing import Dict

import pymysql.cursors

from config import DBConfig

## TODO: Make agnostic of the platform hosting our DB

class DB:

    def __init__(self, config: Dict[str, str]):
        self.connection = None

        config = config.get('db')

        if config and config.host and config.user and config.password and config.database:
            self.config = DBConfig(config.host, config.user, config.password, config.database)
        else:
            raise Exception('Failed to instantiate DB class. Invalid configuration supplied')
    
    def _connect(self):

        self.connection = pymysql.connect(host=self.config.host,
                        user=self.config.user,
                        password=self.config.password,
                        database=self.config.database,
                        cursorclass=pymysql.cursors.DictCursor)

    def run_query(self, sql, binds) -> Dict:
        ## TODO: validate sql and binds
        ## TODO: Check connection exists

        ## TODO: Is there a better way to do this? Or is it better to connect each time before running query
        self._connect()

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, binds)
                result = cursor.fetchone()
            self.connection.commit()
        
        return result
