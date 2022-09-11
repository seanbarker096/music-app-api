import pymysql.cursors


class DB:

    def get_password_from_db():
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='mysqlroot',
                             database='gigs',
                             cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `post` (`owner_id`, `body_text`) VALUES (%s, %s)"
                cursor.execute(sql, (10, 'My great post'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `owner_id`, `body_text` FROM `post` WHERE `body_text`=%s"
                cursor.execute(sql, ('My great post',))
                result = cursor.fetchone()
                return result['body_text']
