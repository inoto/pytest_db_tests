import logging
import os
import sqlite3
from sqlite3 import Error

DB_PATH = os.path.join(os.path.dirname(__file__), "some.db")


def create_connection(db_path):
    """ create a database connection to the SQLite database specified by db_path
    :param db_path: a path to database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        logging.exception(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logging.exception(e)


def show_db(conn):
    try:
        c = conn.cursor()

        c.execute('SELECT name from sqlite_master where type= "table"')
        print(c.fetchall())

    except Error as e:
        logging.exception(e)


if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = create_connection(DB_PATH)

    sql_create_ships_table = """CREATE TABLE Ships (
                                    ship TEXT PRIMARY KEY,
                                    weapon TEXT,
                                    hull TEXT,
                                    engine TEXT
                                );"""
    sql_create_weapons_table = """CREATE TABLE weapons (
                                    weapon TEXT PRIMARY KEY,
                                    "reload speed" INTEGER,
                                    "rotational speed" INTEGER,
                                    diameter INTEGER,
                                    "power volley" INTEGER,
                                    count INTEGER,
                                    FOREIGN KEY (weapon) REFERENCES Ships (weapon)
                                )"""
    sql_create_hulls_table = """CREATE TABLE hulls (
                                    hull TEXT PRIMARY KEY,
                                    armor INTEGER,
                                    type INTEGER,
                                    capacity INTEGER,
                                    FOREIGN KEY (hull) REFERENCES Ships (hull)
                                )"""
    sql_create_engines_table = """CREATE TABLE engines (
                                    engine TEXT PRIMARY KEY,
                                    power INTEGER,
                                    type INTEGER,
                                    FOREIGN KEY (engine) REFERENCES Ships (engine)
                                )"""

    if conn is not None:
        create_table(conn, sql_create_ships_table)
        create_table(conn, sql_create_weapons_table)
        create_table(conn, sql_create_hulls_table)
        create_table(conn, sql_create_engines_table)
    else:
        print("Error! cannot create the database connection.")

    show_db(conn)
    conn.close()
