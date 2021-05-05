import os
import random
import sqlite3
import pytest
import pandas as pd
import definitions


@pytest.fixture(scope="session")
def use_db():
    source = sqlite3.connect(definitions.DB_PATH)
    yield source
    source.close()


@pytest.fixture(scope="session")
def randomize_some_db_values():
    # TODO: добавить try except finally
    source = sqlite3.connect(definitions.DB_PATH)
    # будем класть копию на диск, будет как доп. лог
    if os.path.exists(definitions.RANDOMIZED_DB_PATH):
        os.remove(definitions.RANDOMIZED_DB_PATH)
    dest = sqlite3.connect(definitions.RANDOMIZED_DB_PATH)
    source.backup(dest)
    source.close()

    randomize_using_sql(dest)

    dest.commit()
    # dest.close()

    # c = dest.cursor()
    # c.execute('SELECT * FROM Ships')
    # for row in c:
    #     c.execute('UPDATE Ships SET ')
    # dest.commit()
    #
    # pass
    # df_ships = pd.read_sql_query('SELECT * FROM Ships', dest)
    # df_weapons = pd.read_sql_query('SELECT * FROM weapons', dest)
    # df_hulls = pd.read_sql_query('SELECT * FROM hulls', dest)
    # df_engines = pd.read_sql_query('SELECT * FROM engines', dest)
    # parts = [df_weapons, df_hulls, df_engines]

    # dest.commit()
    # dest.close()

    yield dest
    dest.close()


def randomize_using_sql(dest):
    c = dest.cursor()
    part_names = ['weapon', 'hull', 'engine']

    # получается все названия кораблей
    c_ships_read = dest.cursor()
    c_ships_read.execute(f'SELECT ship FROM Ships')
    ships = c_ships_read.fetchall()
    # print(f'ships: {ships}')

    # получаем новое значение
    parts = fetch_parts(dest, part_names)
    # print(f'parts: {parts}')
    # part_value = get_random_part_value(dest, part_name)

    # применяем новое значение
    for i in range(0, len(ships)):
        part_name = random.choice(part_names)

        new_value = random.choice(parts[part_name])[0] #'LOLKA'
        query = f'UPDATE Ships SET {part_name} = "{new_value}" WHERE ship = "{ships[i][0]}"'
        # print(f'query: {query}')
        c.execute(query)


def fetch_parts(dest, part_names):
    parts = {}
    for part_name in part_names:
        c = dest.cursor()
        query = f'SELECT {part_name} FROM {part_name}s'
        c.execute(query)
        parts[part_name] = c.fetchall()
    return parts


def get_random_part_value(dest, part_name):
    c = dest.cursor()
    query = f'SELECT {part_name} FROM {part_name}s'
    c.execute(query)
    data = c.fetchall()
    # print(f'data: {data}')


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
