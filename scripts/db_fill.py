import random
import definitions
from helpers import random_helper
from helpers.db_helper import DBHelper


def create_ship(conn, ship):
    """
    Create a new ship into the Ships table
    :param conn:
    :param ship:
    :return: ship id
    """
    query = """ INSERT INTO Ships(ship,weapon,hull,engine)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(query, ship)
    return cur.lastrowid


def create_weapon(conn, weapon):
    """
    Create a new weapon into the weapons table
    :param conn:
    :param weapon:
    :return: weapon id
    """
    query = """ INSERT INTO weapons(weapon,"reload speed","rotational speed",diameter,"power volley",count)
              VALUES(?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(query, weapon)
    return cur.lastrowid


def create_hull(conn, hull):
    """
    Create a new hull into the hulls table
    :param conn:
    :param hull:
    :return: hull id
    """
    query = """ INSERT INTO hulls(hull,armor,type,capacity)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(query, hull)
    return cur.lastrowid


def create_engine(conn, engine):
    """
    Create a new engine into the engines table
    :param conn:
    :param engine:
    :return: engine id
    """
    query = """ INSERT INTO engines(engine,power,type)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(query, engine)
    return cur.lastrowid


if __name__ == '__main__':
    conn = DBHelper(definitions.DB_PATH).connection
    with conn:
        weapons = []
        for i in range(0, 20):
            weapon = (f'Weapon-{i+1}', random_helper.randint_component(), random_helper.randint_component(),
                      random_helper.randint_component(), random_helper.randint_component(),
                      random_helper.randint_component())
            weapons.append(weapon)
            create_weapon(conn, weapon)

        hulls = []
        for i in range(0, 5):
            hull = (f'Hull-{i+1}', random_helper.randint_component(), random_helper.randint_component(),
                    random_helper.randint_component())
            hulls.append(hull)
            create_hull(conn, hull)

        engines = []
        for i in range(0, 6):
            engine = (f'Engine-{i+1}', random_helper.randint_component(), random_helper.randint_component())
            engines.append(engine)
            create_engine(conn, engine)

        for i in range(0, 200):
            ship = (f'Ship-{i+1}', random.choice(weapons)[0], random.choice(hulls)[0], random.choice(engines)[0])
            create_ship(conn, ship)

        conn.commit()
