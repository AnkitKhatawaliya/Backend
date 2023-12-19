import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user='postgres',
    password='Ankit123@post',
    database='School',
    host='localhost',
    port='8003',
    cursor_factory=RealDictCursor
)


def Check_DB_Connection():
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT 1""")
    except Exception as e:
        print(f"Error in Executing SQL Query: {e}")
        return False
    finally:
        cursor.close()
        db_pool.putconn(connection)
        return True


def Execute_on_DB(Query):
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(Query)
        connection.commit()
    except Exception as e:
        print(f"Error in Executing SQL Query: {e}")
        return False
    finally:
        cursor.close()
        db_pool.putconn(connection)
        return True


def Insert_on_DB(Query, values):
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(Query, values)
        connection.commit()
    except Exception as e:
        print(f"Error in Inserting the Values: {e}")
        return False
    finally:
        cursor.close()
        db_pool.putconn(connection)
        return True


def fetch_from_database(Query, values):
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(Query, values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error in Fetching from Database: {e}")
        return False
    finally:
        connection.commit()
        cursor.close()
        db_pool.putconn(connection)
        print("Connection Closed")


def Fetch_par_from_database(Query, values):
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(Query, values)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error in Fetching from DataBase: {e}")
        return False
    finally:
        connection.commit()
        cursor.close()
        db_pool.putconn(connection)


def Fetch_all_from_database(Query):
    connection = db_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(Query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error in Fetching from DataBase: {e}")
        return False
    finally:
        connection.commit()
        cursor.close()
        db_pool.putconn(connection)
