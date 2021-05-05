import logging
import os
import random
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


def create_ship(conn, ship):
    """
    Create a new project into the projects table
    :param conn:
    :param ship:
    :return: ship id
    """
    sql = """ INSERT INTO Ships(ship,weapon,hull,engine)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, ship)
    # conn.commit()
    return cur.lastrowid


def create_weapon(conn, weapon):
    """
    Create a new project into the projects table
    :param conn:
    :param weapon:
    :return: weapon id
    """
    sql = """ INSERT INTO weapons(weapon,"reload speed","rotational speed",diameter,"power volley",count)
              VALUES(?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, weapon)
    # conn.commit()
    return cur.lastrowid


def create_hull(conn, hull):
    """
    Create a new project into the projects table
    :param conn:
    :param hull:
    :return: hull id
    """
    sql = """ INSERT INTO hulls(hull,armor,type,capacity)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, hull)
    # conn.commit()
    return cur.lastrowid


def create_engine(conn, engine):
    """
    Create a new project into the projects table
    :param conn:
    :param engine:
    :return: engine id
    """
    sql = """ INSERT INTO engines(engine,power,type)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, engine)
    # conn.commit()
    return cur.lastrowid


def get_random_int(upto=20):
    return random.randint(1, upto)


if __name__ == '__main__':
    conn = create_connection(DB_PATH)
    with conn:
        weapons = []
        for i in range(0, 20):
            weapon = (f'Weapon-{i+1}', get_random_int(), get_random_int(), get_random_int(), get_random_int(), get_random_int())
            weapons.append(weapon)
            # print(f'weapon: {weapon}')
            create_weapon(conn, weapon)

        hulls = []
        for i in range(0, 5):
            hull = (f'Hull-{i+1}', get_random_int(), get_random_int(), get_random_int())
            hulls.append(hull)
            create_hull(conn, hull)

        engines = []
        for i in range(0, 6):
            engine = (f'Engine-{i+1}', get_random_int(), get_random_int())
            engines.append(engine)
            create_engine(conn, engine)

        for i in range(0, 200):
            ship = (f'Ship-{i+1}', random.choice(weapons)[0], random.choice(hulls)[0], random.choice(engines)[0])
            print(f'{ship}')
            create_ship(conn, ship)

        conn.commit()
