import os
import random
import sqlite3
import pytest
import pandas as pd
import definitions
from scripts.db_helper import DBHelper
from scripts.randomizer_helper import randomize_ship_part, randomize_parts_value


def db_helper(db_path):
    source = DBHelper(db_path)
    yield source.connection
    source.close()


@pytest.fixture(scope="session")
def use_source_db():
    source_db = DBHelper(definitions.DB_PATH)
    yield source_db.connection
    source_db.close()


@pytest.fixture(scope="session")
def use_randomized_db(use_source_db):
    source_db = use_source_db

    # будем класть копию на диск, будет как доп. лог
    if os.path.exists(definitions.RANDOMIZED_DB_PATH):
        os.remove(definitions.RANDOMIZED_DB_PATH)

    randomized_db = DBHelper(definitions.RANDOMIZED_DB_PATH)
    source_db.backup(randomized_db.connection)

    randomize_ship_part(randomized_db.connection)
    randomize_parts_value(randomized_db.connection)

    randomized_db.connection.commit()

    yield randomized_db.connection
    randomized_db.close()


def pytest_generate_tests(metafunc):
    # ищем только нужную фикстуру
    if 'parametrize_ships' in metafunc.fixturenames:
        # читаем базы
        source_db = DBHelper(definitions.DB_PATH)
        c = source_db.connection.cursor()
        c.execute(f'SELECT * FROM Ships') # TODO: вынести Ships в константу
        ship_names = c.fetchall()
        print(f'ship_names: {ship_names}')

        # c_read_ships = source_db.connection.cursor()
        # c.execute(f'SELECT * FROM Ships')

        c_read_columns = source_db.connection.cursor()
        c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("Ships")')
        part_names = c_read_columns.fetchall()
        part_names = [x for t in part_names for x in t]
        del part_names[0]
        print(f'part_names: {part_names}')

        # заполняем значения параметризации с названием корабля и его частей
        argvalues = []
        ids = []
        # part_names = ['weapon', 'hull', 'engine']

        for ship_name in ship_names:
            # print(f'ship_name: {ship_name}')
            for part_name in part_names:
                # print(f'part_name: {part_name}')
                specific_row_index = part_names.index(part_name)
                argvalues.append((ship_name[0], part_name, ship_name[specific_row_index+1]))
                ids.append(f'{ship_name[0]}, {ship_name[specific_row_index+1]}')

        source_db.close()
        print(f'argvalues: {argvalues}')

        if not argvalues:
            raise ValueError("Test cases not loaded")
        # else:
            # print(f'argvalues: {argvalues}')

        return metafunc.parametrize("parametrize_ships", argvalues, ids=ids, scope='session')
