import psycopg

from python.api_basics.config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD


class DBClient:
    def __init__(self):
        self.db_name = DB_NAME
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None

    def connect_db(self):
        try:
            self.conn = psycopg.connect(
                dbname = self.db_name,
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password
            )
            print("Connected to database")
        except psycopg.OperationalError as e:
            print(e)
        return self.conn

    def close_db(self):
        if self.conn is not None:
            self.conn.close()

# Функция SELECT
    def select_db(self, sql_request):
        cursor = self.conn.cursor()
        cursor.execute(sql_request)
        result = cursor.fetchall()
        cursor.close()
        return result


# Функция INSERT
    def insert_db(self, sql_request, value):
        cursor = self.conn.cursor()
        cursor.execute(sql_request, value)
        self.conn.commit()
        cursor.close()



