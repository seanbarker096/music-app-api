import json
from typing import Dict

import pymysql.cursors
from api.db.config import DBConfig


## TODO: Make agnostic of the platform hosting our DB
## TODO: Make this a singleton class as don't want multiple connections all over the place
class DB:

    def __init__(self, config: Dict[str, str]):
        self.connection = None

        db_config = config['config_file']['db']
        print(json.dumps(db_config['host']))
        if db_config and db_config['host'] and db_config['user'] and db_config['password'] and db_config['database']:
            self.config = DBConfig(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        else:
            raise Exception('Failed to instantiate DB class. Invalid configuration supplied')
    
        self.connection = pymysql.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def run_query(self, sql, binds) -> Dict:
        ## TODO: validate sql and binds
        ## TODO: Check connection exists

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, binds)
                result = cursor.fetchone()
            self.connection.commit()
        
        return result
