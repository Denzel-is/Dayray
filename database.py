import psycopg2

def connectionbd():
    connection = psycopg2.connect(
        user="postgres",
        password="food",
        port="5432",
        database="Dayray"
    )
    return connection
