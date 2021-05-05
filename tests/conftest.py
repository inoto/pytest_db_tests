import os
import random
import sqlite3
import pytest
import pandas as pd
import definitions


@pytest.fixture(scope="session")
def randomize_some_db_values():
    source = sqlite3.connect(definitions.DB_PATH)
    dest = sqlite3.connect(':memory:') # TODO: надо использовать на диске, потому что будет как доп лог
    source.backup(dest)
    df_ships = pd.read_sql_query('SELECT * FROM Ships', dest)
    df_weapons = pd.read_sql_query('SELECT * FROM weapons', dest)
    df_hulls = pd.read_sql_query('SELECT * FROM hulls', dest)
    df_engines = pd.read_sql_query('SELECT * FROM engines', dest)
    parts = [df_weapons, df_hulls, df_engines]

    columns = df_ships.columns
    print(f'columns')
    for i in range(0, len(columns)):
        print(f'{i} - {columns[i]}')
    print('===============================================')
    # для каждого корабля
    for i in range(0, df_ships.shape[0]):
        # генерируем рандомный индекс
        rand_field_int = random.randint(1, len(columns)-1)
        # print(f'rand_field_int: {rand_field_int}')

        # берём значение поля корабля
        value = df_ships.iat[i, rand_field_int]
        print(f'value: {value}')

        # берём по этому же рандомному индексу часть корабля и меняем
        part = parts[rand_field_int-1]
        rand_row = random.randint(0, part.shape[0]-1)
        ref = part.iat[rand_row, 0]
        print(f'ref: {ref}')
        value = ref



        # rand_field_int = random.randint(0, len(row)-1)
        # df_part = parts[rand_field_int]
        # print(f'df_part: {df_part}')

        # row.values[rand_field_int] =
        # print(f'row: {row["weapon"]}')
        # for field in row:
        #     print(f'field 1: {field}')
    # rand_df =

    yield df_ships
