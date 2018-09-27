"""
    Module initializes a connection to the db
    Given a db_url previously exported to thevirtualenv
"""

import psycopg2

# local imports
from api.v2.config import CONFIGS


def init_db(db_url=None):
    """
        Initialize db connection
        Run queries that set up tables
    """
    # Connect to db on start up/restart : drop all tables
    if db_url is None:
        db_url = CONFIGS['db_url']
    try:
        conn = psycopg2.connect(db_url)

        print("\nConnected: {} \n\n".format(conn.get_dsn_parameters()))

        cursor = conn.cursor()
        cursor.execute(select_all_tables_to_reset())
        rows = cursor.fetchall()

        for row in rows:
            print("Droping {} ......".format(row[0]))
            cursor.execute(
                "DROP TABLE {}".format(row[0]))
            print("Dropped {} ......\n".format(row[0]))

        # Create the tables afresh
        for query in set_up_tables():
            cursor.execute(query)
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("\n\nError: {}".format(error))

    # Close the connection to db
    finally:
        conn.close()

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
        food_item_price numeric NOT NULL
    )"""

    orders_table_query = """
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        ordered_on TIMESTAMP NOT NULL,
        quantity INTEGER NOT NULL,
        total_order_cost NUMERIC NOT NULL
    )"""

    return [users_table_query, menu_table_query, orders_table_query]

def select_all_tables_to_reset():
    """
        Removes all tables if app needs restarting
    """
    select_all_tables_query = """
    SELECT table_name FROM information_schema.tables WHERE
        table_schema = 'public'"""

    return select_all_tables_query

def insert_into_db(query):
    """
        Handles INSERT queries
    """
    db_url = CONFIGS['db_url']
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Connection failed: {}".format(error))

    # Commit changes and close the connection to db
    finally:
        conn.close()

def select_from_db(query):
    """
        Handles SELECT queries
    """
    db_url = CONFIGS['db_url']
    result = None
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        result = {}
        if rows:
            return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print("Connection failed: {}".format(error))

    # Commit changes and close the connection to db
    finally:
        conn.close()

    return result
