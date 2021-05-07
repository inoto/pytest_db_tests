import logging
import os
from sqlite3 import Error
import definitions
from helpers.db_helper import DBHelper


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


def show_db_tables(conn):
    try:
        c = conn.cursor()
        c.execute('SELECT name from sqlite_master where type= "table"')
        print(c.fetchall())
    except Error as e:
        logging.exception(e)


if __name__ == '__main__':
    if os.path.exists(definitions.DB_PATH):
        os.remove(definitions.DB_PATH)

    conn = DBHelper(definitions.DB_PATH).connection

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

    create_table(conn, sql_create_ships_table)
    create_table(conn, sql_create_weapons_table)
    create_table(conn, sql_create_hulls_table)
    create_table(conn, sql_create_engines_table)

    show_db_tables(conn)
    conn.close()
