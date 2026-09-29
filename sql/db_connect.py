import psycopg
conn = None
cursor = None
user = ('Ivan Petrov', 'test2@test.test', 24)
try:
    conn = psycopg.connect(
        dbname = "qa_db",
        host = "localhost",
        port = "5432",
        user = "qa_user",
        password = "qa_password"
    )
    print("Connected to database")
    cursor = conn.cursor()
    cursor.execute("select * from users")
    print(cursor.fetchall())
    cursor.execute("INSERT INTO users(username, email, age) VALUES (%s, %s, %s)", user)
    conn.commit()
    cursor.execute("select * from users")
    print(cursor.fetchall())
    cursor.close()
except psycopg.OperationalError as e:
    print(e)
finally:
    if conn:
        conn.close()



