"""
    Module initializes a connection to the db
    Given a db_url previously exported to thevirtualenv
"""
import sys
import psycopg2

# local imports
from api.v2.config import CONFIGS


def init_db(db_url=None):
    """
        Initialize db connection
        Run queries that set up tables
    """
    try:
        conn, cursor = connect_to_and_query_db()
        all_init_queries = drop_table_if_exists() + set_up_tables()
        i = 0
        while i != len(all_init_queries):
            query = all_init_queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        print("--"*50)
        conn.close()

    except Exception as error:
        print("\nQuery not executed : {} \n".format(error))


def set_up_tables():
    """
        List of queries run at set up to create tables in db
    """
    users_table_query = """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR (24) NOT NULL UNIQUE,
        email VARCHAR (30) NOT NULL UNIQUE,
        password VARCHAR (128) NOT NULL
    )"""

    menu_table_query = """
    CREATE TABLE menu (
        food_item_id SERIAL PRIMARY KEY,
        food_item_name VARCHAR (24) NOT NULL,
        food_item_price INTEGER NOT NULL
    )"""

    orders_table_query = """
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        ordered_by VARCHAR (24) NOT NULL,
        food_item_name VARCHAR (24) NOT NULL,
        food_item_price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_order_cost INTEGER NOT NULL
    )"""

    return [users_table_query, menu_table_query, orders_table_query]


def drop_table_if_exists():
    """
        Removes all tables on app restart
    """
    drop_orders_table = """
    DROP TABLE IF EXISTS orders"""

    drop_users_table = """
    DROP TABLE IF EXISTS users"""

    drop_menu_table = """
    DROP TABLE IF EXISTS menu"""

    return [drop_menu_table, drop_orders_table, drop_users_table]


def connect_to_and_query_db(query=None, db_url=None):
    """
        Initiates a connection to the db
        Executes a query
    """
    conn = None
    if db_url is None:
        db_url = CONFIGS['db_url']

    try:
        # connect to db
        conn = psycopg2.connect(db_url)
        print("\n\nConnected {}\n".format(conn.get_dsn_parameters()))
        cursor = conn.cursor()

        if query:
            # Execute query
            cursor.execute(query)
            # Commit changes
            conn.commit()

    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print("DB ERROR: {}".format(error))

    return conn, cursor


def insert_into_db(query):
    """
        Handles INSERT queries
    """
    try:
        conn = connect_to_and_query_db(query)[0]
        # After successful INSERT query
        conn.close()
    except psycopg2.Error as error:
        sys.exit(1)


def select_from_db(query):
    """
        Handles SELECT queries
    """
    rows = None
    conn, cursor = connect_to_and_query_db(query)
    if conn:
        # Retrieve SELECT query results from db
        rows = cursor.fetchall()
        conn.close()

    return rows


if __name__ == '__main__':
    init_db()
    connect_to_and_query_db()
