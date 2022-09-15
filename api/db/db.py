from typing import Dict

import pymysql.cursors

from config import DBConfig

## TODO: Make agnostic of the platform hosting our DB

class DB:

    def __init__(self):
        self.connection = None
    
    def connect(self, config: DBConfig):

        self.connection = pymysql.connect(host=config.host,
                        user=config.user,
                        password=config.password,
                        database=config.database,
                        cursorclass=pymysql.cursors.DictCursor)

    def run_query(self, sql, binds) -> Dict:
        ## TODO: validate sql and binds
        ## TODO: Check connection exists

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, binds)
                result = cursor.fetchone()
            self.connection.commit()
        
        return result
