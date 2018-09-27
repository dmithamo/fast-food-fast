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
    if not db_url:
        db_url = CONFIGS["db_url"]
    try:
        conn = psycopg2.connect(db_url)
        print("\n\n\nConnection Successful\n\n\n")
        cursor = conn.cursor()

        # Reset db on restart : drop all tables
        cursor.execute(select_all_tables_to_reset())
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute(
                "DROP TABLE {} CASCADE".format(row[0]))

        # Create the tables afresh
        for query in set_up_tables():
            cursor.execute(query)

        # Commit changes and close the connection to db
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # Print error for ease of debugging
        print(error)

    finally:
        # Close connection after commiting
        if conn:
            conn.close()

def set_up_tables():
    """
        List of queries run at set up to create tables in db
    """
    users_table_query = """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR (24) NOT NULL UNIQUE,
        user_email VARCHAR (30) NOT NULL UNIQUE,
        user_password VARCHAR (128) NOT NULL,
        registered_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP NOT NULL,
        user_orders INT[]
    )"""

    menu_table_query = """
    CREATE TABLE menu (
        food_item_id SERIAL PRIMARY KEY,
        food_item_name VARCHAR (24) NOT NULL,
        food_item_price numeric NOT NULL,
        food_item_quantity integer NOT NULL
    )"""

    orders_table_query = """
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        food_item_id INTEGER REFERENCES menu (food_item_id)
           ON DELETE NO ACTION ON UPDATE NO ACTION,
        ordered_on TIMESTAMP NOT NULL,
        quantity INTEGER NOT NULL,
        total_order_cost NUMERIC NOT NULL
    )"""


    return [users_table_query, menu_table_query, orders_table_query]

def select_all_tables_to_reset():
    """
        Removes all tables if app needs restarting
    """
    # drop_table_query = """
    # DROP TABLE IF EXISTS {} CASCADE
    # """.format(table_name)

    select_all_tables_query = """
    SELECT table_name FROM information_schema.tables WHERE
        table_schema = 'public'"""

    return select_all_tables_query


if __name__ == '__main__':
    init_db()
