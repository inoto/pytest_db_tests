import pytest


def test_ships(use_source_db, use_randomized_db, par_db):
    source_db = use_source_db
    randomized_db = use_randomized_db

    # print(f'par_db: {par_db}')

    cs = source_db.cursor()
    cs.execute(f'SELECT "{par_db[1]}" FROM Ships WHERE ship = "{par_db[0]}"')
    data = cs.fetchone()
    # print(f'data: {data}')

    cr = randomized_db.cursor()
    cr.execute(f'SELECT "{par_db[1]}" FROM Ships WHERE ship = "{par_db[0]}"')
    data_rand = cr.fetchone()
    # print(f'data rand: {data_rand}')

    part_source = data[0]
    part_randomized = data_rand[0]
    # print(f'{part_source} -> {part_randomized}')
    assert part_source == part_randomized, f'{part_source} -> {part_randomized}'

    c_read_columns = source_db.cursor()
    c_read_columns.execute(f'SELECT name FROM PRAGMA_TABLE_INFO("Ships")')
    ships_table_columns = c_read_columns.fetchall()
    ships_table_columns = [x for t in ships_table_columns for x in t]
    del ships_table_columns[0]

    print(f'argvalue: {par_db[0]}, {par_db[1]}, {par_db[2]}')

    part = par_db[1]

    cs = source_db.cursor()
    cs.execute(f'SELECT * FROM "{part}s" WHERE "{part}" = "{par_db[2]}"')
    value_source = cs.fetchall()

    cr = randomized_db.cursor()
    cr.execute(f'SELECT * FROM "{part}s" WHERE "{part}" = "{par_db[2]}"')
    value_randomized = cr.fetchall()

    assert value_source == value_randomized, f'{value_source} -> {value_randomized}'
