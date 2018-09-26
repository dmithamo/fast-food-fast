"""
    Module initializes a connection to the db
    Given a db_url previously exported to thevirtualenv
"""

import os
import psycopg2


def init_db():
    """
        Initialize db connection
        Run queries that set up tables
    """

    try:
        db_url = os.getenv('DB_URL')
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        for query in set_up_tables():
            # Drop all tables on app restart
            table_name = query.split()[2]
            cursor.execute(drop_table_at_set_up(table_name))

            # Create the tables afresh
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

def drop_table_at_set_up(table_name):
    """
        Removes a given table if app needs restarting
    """
    drop_table_query = """
    DROP TABLE IF EXISTS {} CASCADE
    """.format(table_name)

    return drop_table_query

if __name__ == '__main__':
    init_db()
