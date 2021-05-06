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
    # source = sqlite3.connect(definitions.DB_PATH)
    source_db = DBHelper(definitions.DB_PATH)
    print(f'### source DB connected')
    yield source_db.connection
    source_db.close()
    print(f'### source DB close')


@pytest.fixture(scope="session")
def use_randomized_db(use_source_db):
    print(f'### use_randomized_db connected')
    source_db = use_source_db

    # будем класть копию на диск, будет как доп. лог
    if os.path.exists(definitions.RANDOMIZED_DB_PATH):
        os.remove(definitions.RANDOMIZED_DB_PATH)

    randomized_db = DBHelper(definitions.RANDOMIZED_DB_PATH)
    source_db.backup(randomized_db.connection)

    # randomize_ship_part(randomized_db.connection)
    randomize_parts_value(randomized_db.connection)

    randomized_db.connection.commit()

    yield randomized_db.connection
    randomized_db.close()
    print(f'### use_randomized_db close')


def randomize_using_pandas(dest):
    df_ships = pd.read_sql_query('SELECT * FROM Ships', dest)
    df_weapons = pd.read_sql_query('SELECT * FROM weapons', dest)
    df_hulls = pd.read_sql_query('SELECT * FROM hulls', dest)
    df_engines = pd.read_sql_query('SELECT * FROM engines', dest)
    parts = [df_weapons, df_hulls, df_engines]

    columns = df_ships.columns
    # print(f'columns')
    # for i in range(0, len(columns)):
    #     print(f'{i} - {columns[i]}')
    print('===============================================')
    # для каждого корабля
    for i in range(0, df_ships.shape[0]):
        print(f'====== ship: {df_ships.iat[i, 0]} ======')
        # генерируем рандомный индекс
        rand_field_int = random.randint(1, len(columns) - 1)
        # print(f'rand_field_int: {rand_field_int}')

        # текущее значение поля корабля
        print(f'value: {df_ships.iat[i, rand_field_int]}')

        # берём по этому же рандомному индексу часть корабля и меняем
        part = parts[rand_field_int - 1]
        rand_row = random.randint(0, part.shape[0] - 1)
        ref = part.iat[rand_row, 0]
        print(f'ref: {ref}')
        df_ships.iat[i, rand_field_int] = ref

    df_ships.to_sql('Ships', dest, if_exists='replace')


def pytest_generate_tests(metafunc):
    print(f'### pytest_generate_tests')
    # ищем только нужную фикстуру
    if 'par_db' in metafunc.fixturenames:
        # читаем базы
        # source_db = sqlite3.connect(definitions.DB_PATH)
        print(f'## pytest_generate_tests source_db connected')
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
                ids.append(f'{ship_name[0]}_{ship_name[specific_row_index+1]}')

        source_db.close()
        print(f'argvalues: {argvalues}')
        print(f'## pytest_generate_tests source_db close')

        if not argvalues:
            raise ValueError("Test cases not loaded")
        # else:
            # print(f'argvalues: {argvalues}')

        return metafunc.parametrize("par_db", argvalues, ids=ids, scope='session')
